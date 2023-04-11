#!/usr/bin/python3
"""
Este programa recebe linhas do stdin e imprime-as em stderr conforme é recebido.
Imprimimos em stderr porque é para lá que vão as informações de depuração do Maelstrom.
stdout é reservado para mensagens de rede.

To test:
../maelstrom/maelstrom test -w echo --bin echo_minimal.py --nodes n1 --time-limit 10 --log-stderr

Este programa não está completo, por isso gera um erro quando chamamos Maelstrom.

"""
from base import BaseServer


class EchoServer(BaseServer):

    def main(self):
        """ cria o loop basico de entrada/saida do servidor
        """
        while True:
            try:
                if (line := self.get_line()) is not None:
                    self.send_msg(f"Received: {line}")
            except KeyboardInterrupt:
                self.log("Program interrupted. Leaving..")
                break


if __name__ == "__main__":
    echo = EchoServer()
    echo.main()
