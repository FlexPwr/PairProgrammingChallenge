import asyncio
import datetime
import json
import os
import random
import sys
from logging import Handler

import websockets
import uuid
import pytz
import logging

HOST = os.environ.get("HOST")

PORT = os.environ.get("PORT")

DealConfirmation = dict[str, str | float]

def _create_stdout_log_handler() -> Handler:
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    return handler

LOGGER = logging.getLogger("exchange")
LOGGER.setLevel(logging.INFO)
LOGGER.addHandler(_create_stdout_log_handler())


def _get_direction() -> str:
    return random.choice(seq=["buy", "sell"])


def _get_quantity() -> float:
    return round(random.uniform(1.0, 5.0), 1)


def _get_price() -> float:
    return round(random.uniform(10.0, 30.0), 2)


def _get_id() -> str:
    return uuid.uuid4().hex


def _get_trader_id() -> str:
    return f"flex_trader_{random.randint(1, 5)}"


def _get_execution_time(now: datetime.datetime) -> str:
    return now.astimezone(pytz.utc).isoformat()


def _cet_now() -> datetime:
    return pytz.timezone("Europe/Berlin").localize(datetime.datetime.utcnow()).replace(microsecond=0)


def _get_delivery_day(now: datetime.datetime) -> str:
    return now.date().isoformat()


def _get_delivery_hour(now: datetime.datetime) -> str:
    def _format(h: int) -> str:
        if h <= 9:
            return f"0{h}"
        else:
            return str(h)

    next_hour = now.hour + 1
    delivery_hour = random.randint(next_hour, 23)

    return f"{_format(delivery_hour)}-{_format(delivery_hour + 1)}"


def _generate_deal_confirmation() -> DealConfirmation:
    now = _cet_now()
    return {
        "id": _get_id(),
        "price": _get_price(),
        "quantity": _get_quantity(),
        "direction": _get_direction(),
        "delivery_day": _get_delivery_day(now=now),
        "delivery_hour": _get_delivery_hour(now=now),
        "trader_id": _get_trader_id(),
        "execution_time": _get_execution_time(now=now)
    }


def _prepare_message(confirmation: DealConfirmation) -> str:
    message = {"deal_confirmation": confirmation}
    return json.dumps(message)


async def _wait_before_sending_next_message():
    delay = 5 + random.randint(0, 5)
    await asyncio.sleep(delay=delay)


async def publish_deal_confirmation(websocket):
    LOGGER.info("Start sending deals confirmations...")
    while True:
        await _wait_before_sending_next_message()
        confirmation = _generate_deal_confirmation()
        message = _prepare_message(confirmation)
        await websocket.send(message)
        LOGGER.info(f"Sent out deal confirmation with id={confirmation['id']}...")


async def main():
    LOGGER.info("Started exchange application...")
    async with websockets.serve(publish_deal_confirmation, HOST, PORT):
        LOGGER.info(f"Created websocket server on {HOST}:{PORT}")
        await asyncio.Future()


if __name__ == '__main__':
    asyncio.run(main())
