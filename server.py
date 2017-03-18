import asyncio
from aiosmtpd.handlers import Message
from aiosmtpd.controller import Controller

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
    controller = Controller(MessageHandler())
    controller.start()

  @asyncio.coroutine
  def stop(self):
    Controller.stop()

if __name__ == "__main__":
  server = FakeSMPTServer('localhost', 8025)
  loop = asyncio.get_event_loop()
  loop.create_task(server.serve(loop))
  try:
    loop.run_forever()
  except KeyboardInterrupt:
    server.stop()
    loop.stop()
