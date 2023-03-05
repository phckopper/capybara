#!/usr/bin/python

import asyncio
from http import HTTPStatus
import json
from websockets.http import Headers
import websockets
from lib.MotorDriver import MotorDriver

motor = MotorDriver()

def vector_to_commands(vec):
    commands = [100 * vec[0], 100 * vec[0]]
    commands[0] += 100 * vec[1]
    commands[1] -= 100 * vec[1]
    if commands[0] > 100 or commands[1] > 100 :
        commands[0] *= 100/max(commands)
        commands[1] *= 100/max(commands)
    if commands[0] < -100 or commands[1] < -100 :
        commands[0] *= 100/max(commands)
        commands[1] *= 100/max(commands)
    return commands

async def http_handler(path, headers):
    """Route HTTP requests to their handlers"""

    if path == '/':
        with open("index.html") as f:
            headers = Headers(**{'Content-Type': 'text/html'})
            body = bytes(f.read(), 'utf-8')

            return HTTPStatus.OK, headers, body

    else:
        return None

async def handler(websocket, path):
    while True:
        message = await websocket.recv()
        packet = json.loads(message)
        (command_left, command_right) = vector_to_commands((packet["throttle"], packet["direction"]))
        motor.run(0, 'forward' if command_left > 0 else 'backward', abs(int(command_left)))
        motor.run(1, 'forward' if command_right > 0 else 'backward', abs(int(command_right)))


async def main():
    async with websockets.serve(handler, "", 8001, process_request=http_handler):
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())