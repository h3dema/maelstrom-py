#!/usr/bin/python3
"""

To test:
../maelstrom/maelstrom test -w broadcast --bin broadcast.py --time-limit 5 --rate 10

"""

from node import Node


class Gossip(Node):

    def __init__(self):
        super().__init__()
        self.on("topology", self.handle_topology)
        self.on("read", self.handle_read)
        self.on("broadcast", self.handle_broadcast)

        # Our local peers: an array of nodes.
        self.peers = []

        # Our set of messages received.
        self.messages = set()

    def handle_topology(self, msg):
        self.peers = msg["body"]["topology"][self.nodeId]
        self.log(f"My peers are {self.peers}")
        self.reply(msg, {"type": 'topology_ok'})

    def handle_read(self, msg):
        self.reply(
            msg,
            {"type": 'read_ok',
             "messages": list(self.messages),
             }
        )

    def handle_broadcast(self, msg):
        """ Quando recebermos uma mensagem de broadcast,
            adicionamos a mensagem ao conjunto de mensagens recebidas e
            transmitimos esta mensagem a todos os peers configurados (exceto aquele que enviou a mensagem)
        """
        msg_rec = msg["body"]["message"]
        if msg_rec not in self.messages:
            # esta mensagem ainda não foi recebida, portanto salva em self.messages
            self.messages.add(msg_rec)
            # Broadcast to peers except the one who sent it to us
            for peer in self.peers:
                if peer == msg["src"]:
                    # skip the source of the message
                    continue
                self.retryRPC(peer, {"type": 'broadcast', "message": msg_rec})

        self.reply(msg, {"type": 'broadcast_ok'})


if __name__ == "__main__":
    broadcast = Gossip()
    broadcast.main()
