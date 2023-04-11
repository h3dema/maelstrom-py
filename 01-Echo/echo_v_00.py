import sys
import json
import select
import datetime


class EchoServer(object):

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
        if sys.stdin not in select.select([sys.stdin], [], [], 0)[0]:
            return None

        line = sys.stdin.readline()
        return line if line else None

    def send_msg(self, msg):
        """Sends a raw message object"""
        self.log(f"Sent: {msg}")
        json.dump(msg, sys.stdout)
        sys.stdout.write('\n')
        sys.stdout.flush()

    def main(self):
        while True:
            try:
                line = self.get_line()
                self.send_msg(f"Received #{line}")
            except KeyboardInterrupt:
                self.log("Program interrupted. Leaving..")
                break


if __name__ == "__main__":
    echo = EchoServer()
    echo.main()
