import asyncio
import argparse
import socket
from aiosmtpd.handlers import Message
from aiosmtpd.controller import Controller

import constants

from actions import action

def bind(family, type, proto):
  """Create (or recreate) the actual socket object."""
  sock = socket.socket(family, type, proto)
  sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)

  # If listening on IPv6, activate dual-stack.
  if family == socket.AF_INET6:
    sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, False)

  return sock

class EAController(Controller):
  def make_socket(self):
    host = self.hostname
    port = self.port
    try:
      # First try to determine the socket type.
        info = socket.getaddrinfo(
          host, port,
          socket.AF_UNSPEC,
          socket.SOCK_STREAM,
          0,
          socket.AI_PASSIVE,
        )
    except socket.gaierror:
      # Infer the type from the host.
        addr = host, port
        if ':' in host:
          addr += 0, 0
          type_ = socket.AF_INET6
        else:
          type_ = socket.AF_INET
          info_0 = type_, socket.SOCK_STREAM, 0, '', addr
          info = info_0,

    family, type, proto, canonname, addr = next(iter(info))
    sock = bind(family, type, proto)
    return sock

class MessageHandler(Message):
  def handle_message(self, message):
    print(message)
    action(message['From'], message['To'], message['Subject'],
            message.get_payload())

class EASMPTServer():

  host = 'localhost'
  port = 8025

  def __init__(self, host, port):
    self.host = host
    self.port = port

  @asyncio.coroutine
  def serve(self, loop):
    controller = EAController(MessageHandler(), hostname=self.host,
                            port=self.port)
    controller.start()

  @asyncio.coroutine
  def stop(self):
    Controller.stop()

def main():
  parser = argparse.ArgumentParser(prog='email-actions')
  parser.add_argument('-v', '--version', action='version',
                      version='%(prog)s version ' + constants.VERSION)
  parser.add_argument('-H', '--hostname', action='store',
                      help='Host IP or name to bind the server to',
                      default='localhost')
  parser.add_argument('-p', '--port', type=int, action='store',
                      help='Port number to bind the server to',
                      default=8025)
  req_args = parser.add_argument_group('required arguments')
  req_args.add_argument('-c', '--config', required=True,
                        type=argparse.FileType('r', encoding='UTF-8'),
                        help='Specify config file')
  args = parser.parse_args()

  server = EASMPTServer(args.hostname, args.port)
  loop = asyncio.get_event_loop()
  loop.create_task(server.serve(loop))
  try:
    loop.run_forever()
  except KeyboardInterrupt:
    server.stop()
    loop.stop()

if __name__ == "__main__":
  main()
