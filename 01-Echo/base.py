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

    def log(self, *args):
        """Helper function for logging stuff to stderr"""
        sys.stderr.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f "))
        for i in range(len(args)):
            sys.stderr.write(str(args[i]))
            if i < (len(args) - 1):
                sys.stderr.write(" ")
        sys.stderr.write('\n')

    def get_line(self):
        """Handles a message from stdin, if one is currently available."""

        # select.select(rlist, wlist, xlist): first 3 arguments are iterables of file descriptors to be waited for to be ready for reading/writing/"exceptional condition":
        # thus, wait until sys.stdin is ready for reading
        if sys.stdin not in select.select([sys.stdin], [], [], 0)[0]:
            return None

        line = sys.stdin.readline()
        return line if line else None

    def send_msg(self, msg):
        """Sends a raw message object"""
        json.dump(msg, sys.stdout)
        sys.stdout.write('\n')
        sys.stdout.flush()
        self.log(f"Sent: {msg}")
