import logging
import asyncio
import argparse
import socket
from aiosmtpd.handlers import Message
from aiosmtpd.controller import Controller
from functools import partial

from email_actions.constants import VERSION
from email_actions.filters import Filter
from email_actions.config import check_config


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
  filter_obj = None

  def __init__(self, message_class=None):
    super().__init__(message_class)
    self.filter_obj = Filter()

  def handle_message(self, message):
    logging.debug(message)
    loop = asyncio.get_event_loop()
    filter_action = partial(
      self.filter_obj.filter, message['From'], message['To'],
      message['Subject'], message.get_payload()
    )
    loop.run_in_executor(None, filter_action)


class EASMPTServer():

  host = 'localhost'
  port = 8025

  def __init__(self, host, port):
    self.host = host
    self.port = port
    logging.debug("Using host: %s and port %d for smtp server"
                  % (host, port))

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
                      version='%(prog)s version ' + VERSION)
  parser.add_argument('-H', '--hostname', action='store',
                      help='Host IP or name to bind the server to',
                      default='localhost')
  parser.add_argument('-p', '--port', type=int, action='store',
                      help='Port number to bind the server to',
                      default=8025)
  parser.add_argument('-l', '--log', type=int, action='store',
                      help='Set log level. 0=> Warning, 1=>Info, 2=>Debug',
                      default=0)
  req_args = parser.add_argument_group('required arguments')
  req_args.add_argument('-c', '--config', required=True,
                        help='Specify config file (yaml format) to be used. '
                        'If it doesn\'t exist, we\'ll try to create it')
  try:
    args = parser.parse_args()
  except:
    exit(1)

  if args.log >= 2:
    log_level = logging.DEBUG
  elif args.log == 1:
    log_level = logging.INFO
  else:
    log_level = logging.WARNING
  logging.basicConfig(level=log_level,
                      format='%(asctime)s: [EA] %(filename)s '
                      '- %(message)s')

  cfg_status = check_config(args.config)

  if not cfg_status:
    exit(1)

  server = EASMPTServer(args.hostname, args.port)
  loop = asyncio.get_event_loop()
  loop.create_task(server.serve(loop))
  try:
    logging.info("Starting server")
    loop.run_forever()
  except KeyboardInterrupt:
    logging.info("Stopping server")
    server.stop()
    loop.stop()


if __name__ == "__main__":
  main()
