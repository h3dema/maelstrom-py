"""

O objeto Node fornece suporte para ler mensagens de STDIN,
gravá-las em STDOUT, acompanhar o estado básico,
escrever manipuladores conectáveis para solicitações de RPC do cliente e
enviar nossos próprios RPCs.

Este modulo contem as funções básicas de comunicação.
"""
import sys
import datetime
import select
import json
import threading


class Node(object):
    """ Implementa as funcoes basicas de comunicacao do servidor Echo """

    def __init__(self):
        self.node_id = None  # nome do servidor (fornecido por Maelstrom na mensagem de "init")
        self.next_msg_id = 0  # controla o numero da mensagem retornada pelo servidor
        self.node_ids = []
        self.rpcTimeout = 1000  # Nosso tempo limite de solicitação de RPC, em milisegundos
        self.handlers = dict()  # dictionary com os handlers das mensagens (mapea um tipo de mensagem para um handler)

        self.lock = threading.Lock()
        self.lock_log = threading.Lock()
        self.lock_send = threading.Lock()

        self.on("init", self.handle_init)

    @property
    def nodeId(self):
        """ node ID do servidor """
        return self.node_id

    def nodeIds(self) -> list:
        """ todos os IDs """
        return self.node_ids

    @property
    def new_msg_id(self) -> int:
        """ retorna o id da mensagem, controla o acesso com LOCK """
        self.lock.acquire()
        _id = self.next_msg_id
        self.next_msg_id += 1
        self.lock.release()
        return _id

    def on(self, msg_type: str, handler):
        """ mapeia o handler para a mensagem """
        self.handlers[msg_type] = handler

    def log(self, *args):
        """ Função auxiliar para registrar coisas no stderr """
        self.lock_log.acquire()  # usa lock, para garantir que as mensagens não fiquem interlaçadas
        sys.stderr.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f "))
        for i in range(len(args)):
            sys.stderr.write(str(args[i]))
            if i < (len(args) - 1):
                sys.stderr.write(" ")
        sys.stderr.write('\n')
        self.lock_log.release()

    def get_line(self):
        """ Lida com uma mensagem do stdin, se houver uma disponível no momento """

        # select.select(rlist, wlist, xlist): os 3 primeiros argumentos são
        # iterators de descritores de arquivo que select() ira verificar se estao prontos para leitura/gravação/"condição excepcional":
        # portanto, o comando abaixo aguarde até que sys.stdin esteja pronto para leitura
        if sys.stdin not in select.select([sys.stdin], [], [], 0)[0]:
            return None

        line = sys.stdin.readline()
        return line if line else None

    def msg_nope(self, msg, *args, **kwargs):
        self.log(f"Error: Handler not created for message: {msg}")

    def send(self, dest: str, body: dict):
        """ Envia um objeto de mensagem (em json) """
        msg = {"src": self.node_id, "dest": dest, "body": body}
        self.log(f"Sent: {msg}")
        self.lock_send.acquire()  # usa lock, para garantir que as mensagens enviadas estejam coerentes (não interlaçadas)
        json.dump(msg, sys.stdout)
        sys.stdout.write('\n')
        sys.stdout.flush()
        self.lock_send.release()

    def reply(self, msg, body):
        """ Responda a uma solicitação com um determinado corpo de resposta """
        if msg["body"]["msg_id"] is None:
            # error
            self.send(
                msg["src"],
                {"code": 13, "text": f"Can't reply to request without message id: {json.dumps(msg)}"}
            )
        else:
            body2 = body.copy()
            body2["msg_id"] = self.new_msg_id
            body2["in_reply_to"] = msg["body"]["msg_id"]
            self.send(msg["src"], body2)

    def rpc(self, dest, body):
        """
            TODO:
            - execute function in a thread
            - if timeout, return error
        """
        msg_id = self.new_msg_id
        msg_type = body["type"]
        if msg_type not in self.handlers:
            # envia mensagem de erro
            self.log(f"Error: {body['type']} -> {body}")

            body_err = {
                "type": 'error',
                "in_reply_to": msg_id,
                "code": 0,
                "text": 'RPC request timed out'
            }
            self.send(dest, body_err)
            return False

        body2 = body.copy()
        body2["msg_id"] = msg_id

        # manda mensagem
        self.send(dest, body2)
        return True

    def retryRPC(self, dest, body):
        """ Send an RPC request, and if it fails, retry it forever. """
        while True:
            if self.rpc(dest, body):
                # funcionou, então sai!
                break
            # loga que não funcionou
            self.log(f"Retrying RPC request to {dest} w/ {body}")

    # -------------------------------------
    #
    #             Handlers
    #
    # -------------------------------------
    def handle_init(self, req):
        body = req["body"]
        self.node_id = body["node_id"]
        self.node_ids = body["node_ids"]
        self.log(f"Node {self.node_id} initialized")

        body = {
            "in_reply_to": body["msg_id"],
            "type": "init_ok",
        }
        self.send(req["src"], body)

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

