"""
Maelstrom funciona com qualquer tipo de binário.
As mensagens são enviadas via stdin,
recebidas em stdout e
as informações são registradas em stderr.

Este modulo contem as funções básicas de comunicação.
"""

import sys
import datetime
import select
import json


class BaseServer(object):
    """ Implementa as funcoes basicas de comunicacao do servidor Echo """

    def __init__(self):
        self.node_id = None  # nome do servidor (fornecido por Maelstrom na mensagem de "init")
        self._next_msg_id = 0  # controla o numero da mensagem retornada pelo servidor
        self.handlers = dict()  # dictionary com os handlers das mensagens (mapea um tipo de mensagem para um handler)

    def on(self, msg_type: str, handler):
        """ mapeia o handler para a mensagem """
        self.handlers[msg_type] = handler

    def log(self, *args):
        """ Função auxiliar para registrar coisas no stderr """
        sys.stderr.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f "))
        for i in range(len(args)):
            sys.stderr.write(str(args[i]))
            if i < (len(args) - 1):
                sys.stderr.write(" ")
        sys.stderr.write('\n')

    def get_line(self):
        """ Lida com uma mensagem do stdin, se houver uma disponível no momento """

        # select.select(rlist, wlist, xlist): os 3 primeiros argumentos são
        # iterators de descritores de arquivo que select() ira verificar se estao prontos para leitura/gravação/"condição excepcional":
        # portanto, o comando abaixo aguarde até que sys.stdin esteja pronto para leitura
        if sys.stdin not in select.select([sys.stdin], [], [], 0)[0]:
            return None

        line = sys.stdin.readline()
        return line if line else None

    def send_msg(self, msg):
        """ Envia um objeto de mensagem (em json) """
        json.dump(msg, sys.stdout)
        sys.stdout.write('\n')
        sys.stdout.flush()
        self.log(f"Sent: {msg}")
