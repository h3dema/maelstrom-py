#!/usr/bin/python3
"""

To test:
../maelstrom/maelstrom test -w g-counter --bin counters.py --time-limit 20 --rate 10


"""
import threading
from node import Node


class GCounter(object):

    """ classe que mantem os contadores (por nó da rede) """

    def __init__(self, counts: dict) -> None:
        super().__init__()
        # mapea o nó da rede ao contador daquele nó
        self.counts = counts  # dict

    def value(self):
        """ retorna o valor efetivo do contador (soma dos valores armazenados) """
        total = sum([self.counts[node] for node in self.counts])
        return total

    def merge(self, other):
        """ Merge outro contador GCounter ao contador atual.
            Tem que associar por nó de rede

            other (GCouter):
                contador que queremos acrescentar
        """
        counts = self.counts.copy()
        for node in other.counts:
            if counts[node] is None:
                counts[node] = other.counts[node]
            else:
                counts[node] = max(self.counts[node], other.counts[node])
        return GCounter(counts)

    def increment(self, node, delta):
        """ Incrementa os contadores por delta """
        count = self.counts.get(node, 0)  # se o nó não existe, inicia com zero
        counts = self.counts.copy()
        counts[node] = count + delta
        return GCounter(counts)


class PNCounter(object):

    """ classe que mantem dois conjuntos de contadores (plus e minus) por nó da rede """

    def __init__(self, plus, minus) -> None:
        super().__init__()
        # Takes an increment GCounter and a decrement GCounter
        self.plus = plus
        self.minus = minus

    def value(self):
        """ retorna o valor efetivo dos contadores: (plus - minus) """
        return self.plus.value() - self.minus.value()

    def merge(self, other):
        """
            Merge outro PNCounter aos valores atuais

            other (PNCounter):
                o contador que queremos acrescentar

        """
        return PNCounter(
            self.plus.merge(other.plus),
            self.minus.merge(other.minus)
        )

    def increment(self, node, delta):
        """  Incrementa por delta.
             Mantem dois valores: um para adição e outro para subtração
        """
        if delta > 0:
            # atualiza `plus`
            return PNCounter(self.plus.increment(node, delta), self.minus)
        else:
            # atualiza `minus`
            return PNCounter(self.plus, self.minus.increment(node, delta * -1))

    def to_dict(self):
        return {"plus": self.plus.counts, "minus": self.plus.counts}

    @classmethod
    def from_json(self, json: dict):
        """ cria um novo PNCounter com os dados da mensagem. """
        return PNCounter(GCounter(json["plus"]), GCounter(json["minus"]))


class Counter(Node):

    def __init__(self) -> None:
        super().__init__()

        # CRDT state
        self.crdt = PNCounter(GCounter({}), GCounter({}))

        # intervalo das mensagens
        self.replicate_interval = 5

        # handlers
        self.on("add", self.handle_add)
        self.on("read", self.handle_read)
        self.on("replicate", self.handle_replicate)

    # -----------------------------------------------------
    #
    #                        HANDLERS
    #
    # -----------------------------------------------------
    def handle_add(self, req):
        # Add new elements to our local state
        self.crdt = self.crdt.increment(self.nodeId, req["body"]["delta"])
        self.log(f"state after add: {self.crdt.to_dict()}")
        self.reply(req, {"type": 'add_ok'})

    def handle_read(self, req):
        # When we get a read request, return our messages
        self.reply(req, {"type": 'read_ok', "value": self.crdt.value()})

    def handle_replicate(self, req):
        # When we receive a replication message, merge it into our CRDT
        self.crdt = self.crdt.merge(self.crdt.from_json(req["body"]["value"]))
        self.log(f"state after replicate: {self.crdt.to_dict()}")

    def handle_init(self, req):
        super().handle_init(req)  # call superclass to perform initialization of the node
        # When we initialize, start a replication loop
        self.periodic_replicate()

    def periodic_replicate(self):
        self.log('Replicate!')
        for peer in self.nodeIds():
            if peer == self.nodeId:
                # não precisa mandar para ele mesmo
                continue
            self.send(peer, {"type": 'replicate', "value": self.crdt.to_dict()})
        # chama o mesmo metodo com o intervalo definido em __init__()
        threading.Timer(self.replicate_interval, self.periodic_replicate).start()


if __name__ == "__main__":
    gcounter = Counter()
    gcounter.main()
