from node import Node


class Gossip(Node):

    def __init__(self):
        super().__init__()
        self.on("topology", self.topology)
        self.on("read", self.read)
        self.on("broadcast", self.broadcast)

        # Our local peers: an array of nodes.
        self.peers = []

        # Our set of messages received.
        self.messages = set()


    def topology(self, msg):
        self.peers = msg["body"]["topology"][self.nodeId]
        self.log(f"My peers are {self.peers}")
        self.reply(msg, {type: 'topology_ok'})

    def read(self, msg):
        self.reply(
            msg,
            {"type": 'read_ok',
             "messages": self.messages
             }
        )

    def broadcast(self, msg):
        """ Quando recebermos uma mensagem de broadcast,
            adicionamos a mensagem ao conjunto de mensagens recebidas e
            transmitimos esta mensagem a todos os peers configurados (exceto aquele que enviou a mensagem)
        """
        msg_rec = msg["body"]["message"]
        if msg_rec not in self.messages:
            # esta mensagem ainda não foi recebida, portanto salva em self.messages
            self.messages.add(msg_rec);
            # Broadcast to peers except the one who sent it to us
            for peer in self.peers:
                if peer == msg.src:
                    # skip the source of the message
                    continue
                self.retryRPC(peer, {type: 'broadcast', "message": msg_rec})

        self.reply(msg, {type: 'broadcast_ok'})
