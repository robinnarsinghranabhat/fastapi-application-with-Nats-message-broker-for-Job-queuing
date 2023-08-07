## References 
# - https://stackoverflow.com/questions/63846385/how-do-i-subscribe-to-a-nats-subject-in-python-and-keep-receiving-messages

import asyncio
import signal
import sys
import time

from nats.aio.client import Client as NATS
# Nats server
# NATS_HOST = '127.0.0.1'
NATS_HOST = "localhost"
NATS_PORT = '4222'

from common import SUBJECT, FILE_PROCESS_QUEUE

async def run(loop):
    nc = NATS()

    async def error_cb(e):
        print("Error:", e)


    async def disconnected_cb():
        """
            Handle connection break
        """
        print("Got disconnected...")
        sys.exit()

    async def reconnected_cb():
        """
            What to do when reconnected. Just log ?
        """
        print("Got reconnected...")


    await nc.connect( 
                servers=f"nats://{NATS_HOST}:{NATS_PORT}",
                error_cb=error_cb,
                reconnected_cb=reconnected_cb,
                disconnected_cb=disconnected_cb,
                max_reconnect_attempts=-1,
                loop=loop,
        )

    async def task_handler(msg):
        """
            Worker on service side to handle event.
        """
        print("Processing the task")
        time.sleep(3)
        subject = msg.subject
        reply = msg.reply
        data = msg.data.decode()
        print("Received a message on '{subject} {reply}': {data}".format(
            subject=subject, reply=reply, data=data))


    def signal_handler():
        if nc.is_closed:
            return
        print("Disconnecting...")
        loop.create_task(nc.close())

    for sig in ('SIGINT', 'SIGTERM'):
        loop.add_signal_handler(getattr(signal, sig), signal_handler)

    await nc.subscribe(SUBJECT, FILE_PROCESS_QUEUE, task_handler)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(loop))
    try:
        loop.run_forever()
    finally:
        loop.close()