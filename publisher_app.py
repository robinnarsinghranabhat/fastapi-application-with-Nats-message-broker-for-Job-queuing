
# Nats server
NATS_HOST = '127.0.0.1'
NATS_PORT = '4222'

import nats
from common import SUBJECT
from fastapi import FastAPI

# web-application
app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/process_file/{file_path}")
async def process_task_endpoint(file_path: str):
    print("Got message ", file_path)
    message = b'test'
    nc = await nats.connect(servers=f"nats://{NATS_HOST}:{NATS_PORT}")
    await nc.publish(
        subject=SUBJECT, 
        payload=message,
        )
