import asyncio
import websockets


async def handle(websocket):
    async for message in websocket:
        print(message)


async def main():
    async with websockets.connect("ws://0.0.0.0:5050") as websocket:
        await handle(websocket)
        await asyncio.Future()


if __name__ == '__main__':
    asyncio.run(main())
