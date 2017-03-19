import asyncio
import argparse
from aiosmtpd.handlers import Message
from aiosmtpd.controller import Controller

import constants

from actions import action

class MessageHandler(Message):
  def handle_message(self, message):
    print(message)
    action(message['From'], message['To'], message['Subject'],
            message.get_payload())

class FakeSMPTServer():

  host = 'localhost'
  port = 8025

  def __init__(self, host, port):
    self.host = host
    self.port = port

  @asyncio.coroutine
  def serve(self, loop):
    controller = Controller(MessageHandler(), hostname=self.host,
                            port=self.port)
    controller.start()

  @asyncio.coroutine
  def stop(self):
    Controller.stop()

def main():
  parser = argparse.ArgumentParser(prog='fake-email-actions')
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

  server = FakeSMPTServer(args.hostname, args.port)
  loop = asyncio.get_event_loop()
  loop.create_task(server.serve(loop))
  try:
    loop.run_forever()
  except KeyboardInterrupt:
    server.stop()
    loop.stop()

if __name__ == "__main__":
  main()
