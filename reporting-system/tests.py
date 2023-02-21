import pytest
import json


def test_serialize_msg():
    msg = '{"deal_confirmation": {"id": "7c5bdbde6ca74a69b92c3891755f83dc", "price": 27.37, "quantity": 2.4, ' \
          '"direction": "buy", "delivery_day": "2023-02-21", "delivery_hour": "15-16", "trader_id": "flex_trader_3", ' \
          '"execution_time": "2023-02-21T12:36:57+00:00"}}'

    msg_dict = json.loads(msg)

    assert msg_dict == {"deal_confirmation": {"id": "7c5bdbde6ca74a69b92c3891755f83dc", "price": 27.37, "quantity": 2.4, "direction": "buy", "delivery_day": "2023-02-21", "delivery_hour": "15-16", "trader_id": "flex_trader_3", "execution_time": "2023-02-21T12:36:57+00:00"}}
