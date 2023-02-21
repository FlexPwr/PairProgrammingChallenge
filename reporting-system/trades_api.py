import json
from abc import abstractmethod
import asyncio

import requests
import websockets


class TradesPersistency:
    def __init__(self, fpath):
        self.storage = list()
        self.fpath = fpath

    def append(self, message):
        self.storage.append(message)
        with open(self.fpath, "w") as fhandler:
            json.dump(self.storage, fhandler, indent=2)

    def read_trades(self, trader_id):
        pass


class TradesAPIClient():
    def __init__(self, server, *args, **kwargs):
        self.server = server
        pass

    def write_trade(self, message):
        self.server.write_trade(message)

    def get_trades(self):
        pass


class TradesAPIServer():
    def __init__(self, persistency):
        self.persistency = persistency

    def write_trade(self, message: dict):
        self.persistency.append(message)

    def get_trades(self, trader_id):
        self.persistency.read_trades(trader_id)


class WebsocketListner:
    async def connect(self):
        async with websockets.connect("ws://0.0.0.0:5050") as websocket:
            async for message in websocket:
                self.handle_message(message)

    @abstractmethod
    def handle_message(self, message: str):
        pass


class TradesListener(WebsocketListner):
    def __init__(self, api_client):
        self.api_client = api_client

    def _serialize_msg(self, message):
        return json.loads(message)

    def handle_message(self, message: str):
        self.api_client.write_trade(self._serialize_msg(message))


if __name__ == "__main__":
    persistency = TradesPersistency(fpath="trades.json")
    api_server = TradesAPIServer(persistency)
    api_client = TradesAPIClient(api_server)
    listener = TradesListener(api_client)
    asyncio.run(listener.connect())



