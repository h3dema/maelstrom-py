#!/usr/bin/python3

from node import Node
from gset import timely

class GCounter(object):

    """ classe que mantem os contadores (por nó da rede) """

    def __init__(self, counts: dict) -> None:
        super().__init__()
        # Takes a map of node names to the count on that node.
        self.counts = counts  # dict

    def value(self):
        # Returns the effective value of the counter.
        total = sum([self.counts[node] for node in self.counts])
        return total

    def merge(self, other):
        # Merges another GCounter into this one
        counts = self.counts.copy()
        for node in other.counts:
            if counts[node] is None:
                counts[node] = other.counts[node]
            else:
                counts[node] = max(self.counts[node], other.counts[node])
        return GCounter(counts)

    def increment(self, node, delta):
        # Increment by delta
        count = self.counts.get(node, 0)
        counts = self.counts.copy()
        counts[node] = count + delta
        return GCounter(counts)


class PNCounter(object):

    def __init__(self, plus, minus) -> None:
        super().__init__()
        # Takes an increment GCounter and a decrement GCounter
        self.plus = plus
        self.minus = minus

    def value(self):
        # The effective value is all increments minus decrements
        return self.plus.value() - self.minus.value()

    def merge(self, other):
        # Merges another PNCounter into this one
        return PNCounter(
            self.plus.merge(other.plus),
            self.minus.merge(other.minus)
        )

    def increment(self, node, delta):
        #  Increment by delta
        if delta > 0:
            return PNCounter(self.plus.increment(node, delta), self.minus)
        else:
            return PNCounter(self.plus, self.minus.increment(node, delta * -1))

    def to_dict(self):
        return {"plus": self.plus.counts, "minus": self.plus.counts}

    def from_json(self, json):
        """ create a PNCounter com os dados da mensagem. """
        return PNCounter(json["plus"], json["minus"])


class Counter(Node):

    def __init__(self, counts: dict) -> None:
        super().__init__()

        # CRDT state
        self.crdt = PNCounter(GCounter({}), GCounter({}))

        # handlers
        self.on("add", self.handle_add)
        self.on("read", self.handle_read)
        self.on("replicate", self.handle_replicate)

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

    @timely
    def periodic_replicate(self):
        self.log('Replicate!')
        for peer in self.nodeIds():
            if peer == self.nodeId:
                # não precisa mandar para ele mesmo
                continue
            self.send(peer, {"type": 'replicate', "value": self.crdt.to_dict()})

    def handle_init(self, req):
        super().handle_init(req)  # call superclass to perform initialization of the node
        # When we initialize, start a replication loop
        self.periodic_replicate()

