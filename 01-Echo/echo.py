#!/usr/bin/python3
"""
Este programa é uma evolução da versão em `echo_v_00.py`.
Quando Maelstrom inicia nosso nó (EchoServer) n1.
EchoServer recebe uma mensagem de inicialização do Maelstrom: {"dest":"n1", ...} e este
deve responder ao Maelstrom.


To test:
../maelstrom/maelstrom test -w echo --bin echo_v_01.py --nodes n1 --time-limit 10 --log-stderr

"""
import json
from base import BaseServer


class EchoServer(BaseServer):

    def __init__(self):
        self.node_id = None
        self._next_msg_id = 0
        self.handlers = dict()
        self.on("init", self.msg_init)
        self.on("echo", self.msg_echo)

    @property
    def next_msg_id(self) -> int:
        _id = self._next_msg_id
        self._next_msg_id += 1
        return _id

    def on(self, msg_type: str, handler):
        self.handlers[msg_type] = handler

    def msg_nope(self, msg, *args, **kwargs):
        self.log(f"Error: Handler not create for message: {msg}")

    def msg_init(self, msg):
        """
            recebe uma mensagem:
                {'id': 0, 'src': 'c0', 'dest': 'n1', 'body': {'type': 'init', 'node_id': 'n1', 'node_ids': ['n1'], 'msg_id': 1}}
            deve responder com outra mensagem:
                {src: "n1", dest: "c0", body: {msg_id: 0, in_reply_to: 1, type: "init_ok"}}

        """
        body = msg["body"]
        # set node id
        self.node_id = body["node_id"]
        self.log(f"Initialized node #{self.node_id}")

        # create reply
        reply = {
            "src": self.node_id,
            "dest": msg["src"],
            "body": {
                "msg_id": self.next_msg_id,
                "type": "init_ok",
                "in_reply_to": body["msg_id"],
            }
        }
        self.send_msg(reply)

    def msg_echo(self, msg):
        self.log(f"Echo: {msg}")
        # create reply
        reply = {
            "src": self.node_id,
            "dest": msg["src"],
            "body": {
                "msg_id": self.next_msg_id,
                "type": 'echo_ok',
                "in_reply_to": msg["body"]["msg_id"],
                "echo": msg["body"]["echo"],
            }
        }
        self.send_msg(reply)

    def main(self):
        while True:
            try:
                if (line := self.get_line()) is not None:
                    self.log(f"Received: {line}")
                    # parse the message
                    msg = json.loads(line)
                    body = msg["body"]
                    msg_type = body["type"]
                    self.handlers.get(msg_type, self.msg_nope)(msg)

            except KeyboardInterrupt:
                self.log("Program interrupted. Leaving..")
                break


if __name__ == "__main__":
    echo = EchoServer()
    echo.main()
