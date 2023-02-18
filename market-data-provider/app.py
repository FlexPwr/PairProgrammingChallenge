import datetime
import os
import random
from datetime import timedelta

import pytz
from flask import Flask, request

app = Flask(__name__)

DataPoint = tuple[float, datetime.datetime]


def _now() -> datetime.datetime:
    return pytz.UTC.localize(datetime.datetime.utcnow())


class Store:
    def __init__(self):
        self._data: dict[tuple[str, str], DataPoint] = {}

    def add_or_update(self, day: str, hour: str, update_time: datetime.datetime, value: float):
        self._data[(day, hour)] = (value, update_time)

    def get(self, day: str, hour: str) -> DataPoint:
        return self._data[(day, hour)]

    def data_empty_or_older_than_10_minutes(self, hour: str, day: str) -> bool:
        try:
            _, update_time = self.get(hour=hour, day=day)
            return update_time < _now() - timedelta(minutes=10)
        except KeyError:
            return True


class DataService:
    def __init__(self):
        self._store = Store()

    @staticmethod
    def _generate_new_value() -> float:
        return round(random.uniform(10.0, 40.0), 2)

    def get(self, day: str, hour: str) -> DataPoint:
        need_new_value = self._store.data_empty_or_older_than_10_minutes(hour=hour, day=day)
        # TODO check that delivery start in the past
        if need_new_value:
            new_value = self._generate_new_value()
            now = _now()
            self._store.add_or_update(day=day, hour=hour, value=new_value, update_time=now)

        return self._store.get(day=day, hour=hour)


data_service = DataService()


@app.route("/reference-price", methods=["GET"])
def reference_price():
    delivery_day = request.args.get("delivery_day")
    delivery_hour = request.args.get("delivery_hour")
    if delivery_day is None or delivery_hour is None:
        return {"error_message": "Cannot process request, make sure delivery_day and delivery_hour are set."}, 400

    value, update_time = data_service.get(day=delivery_day, hour=delivery_hour)
    data = {
        "delivery_day": delivery_day,
        "delivery_hour": delivery_hour,
        "value": value,
        "unit": "euro/mwh",
        "last_update": update_time.isoformat(sep="T", timespec="seconds")
    }
    return data, 200


PORT = os.environ.get("PORT")
HOST = os.environ.get("HOST")
app.run(host=HOST, port=PORT)
