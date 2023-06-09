#!/usr/bin/python3
"""


To test:
../maelstrom/maelstrom test -w g-set --bin gset.py

"""
import threading
from node import Node


class GSet(Node):

    def __init__(self) -> None:
        super().__init__()
        self.crdt = set()
        self.replicate_interval = 5  # seconds

        self.on("add", self.handle_add)
        self.on("read", self.handle_read)
        self.on("replicate", self.handle_replicate)

    def handle_add(self, req):
        # Add new elements to our local state
        self.crdt.add(req["body"]["element"])
        self.log(f"state after add: {self.crdt}")
        self.reply(req, {"type": 'add_ok'})

    def handle_read(self, req):
        # When we get a read request, return our messages
        self.reply(req, {"type": 'read_ok', "value": list(self.crdt)})

    def handle_replicate(self, req):
        # When we receive a replication message, merge it into our CRDT
        self.crdt.update(set(req["body"]["value"]))
        self.log(f"state after replicate: {self.crdt}")

    def periodic_replicate(self):
        self.log('Replicate!')
        for peer in self.nodeIds():
            if peer == self.nodeId:
                # não precisa mandar para ele mesmo
                continue
            self.send(peer, {"type": 'replicate', "value": list(self.crdt)})
        # chama o mesmo metodo com o intervalo definido em __init__()
        threading.Timer(self.replicate_interval, self.periodic_replicate).start()

    def handle_init(self, req):
        super().handle_init(req)  # call superclass to perform initialization of the node
        # When we initialize, start a replication loop
        self.periodic_replicate()


if __name__ == "__main__":
    gset = GSet()
    gset.main()
