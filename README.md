# PairProgrammingChallenge

This is a playground for the pair-programming task within our recruitment process.
It contains an implementation of the external services described in the
[design challenge](https://github.com/FlexPwr/SystemDesignChallenge).

Start the stack by running the following command

```shell
./build.sh
```

## Exchange:
A websocket server running on `ws://0.0.0.0:5050`. You can use
the [websockets python library](https://websockets.readthedocs.io/).
The following is an example client to connect to the exchange:

```python
import websockets
import asyncio


async def handle(websocket):
    async for message in websocket:
        print(message)


async def main():
    async with websockets.connect("ws://0.0.0.0:5050") as websocket:
        await handle(websocket)


if __name__ == '__main__':
    asyncio.run(main())
```

The incoming messages are in the json format, with the following structure:

```json
{
  "deal_confirmation": {
    "id": "3624e95119f04b7bb054b2f91a980a83",
    "price": 20.64,
    "quantity": 1.2,
    "direction": "sell",
    "delivery_day": "2023-02-21",
    "delivery_hour": "15-16",
    "trader_id": "flex_trader_4",
    "execution_time": "2023-02-21T06:13:43+00:00"
  }
}
```

## Market data provider:

A web server running on `http://0.0.0.0:5060`. The api is as follows:

```yaml
swagger: "2.0"
info:
  title: Market Data API
  version: 1.0.0
host: market-data-provider.energy
basePath: /v1
schemes:
  - https
paths:
  /reference-price:
    get:
      summary: Reference price.
      parameters:
        - in: query
          name: delivery_day
          required: true
          type: string
          example: "2023-02-06"
        - in: query
          name: delivery_hour
          required: true
          type: string
          example: "12-13"
      produces:
        - application/json
      responses:
        200:
          description: A data object.
          schema:
            type: object
            properties:
              delivery_day:
                type: string
                example: "2023-02-06"
              delivery_hour:
                type: string
                example: "12-13"
              value:
                type: float
                example: 100.0
              unit:
                type: string
                example: euro
              last_update:
                type: string
                example: "2023-02-06T09:15:45Z"
```

An example request would be

```python
import requests

response = requests.get("http://0.0.0.0:5060/reference-price",
                        params={"delivery_day": "2023-05-12", "delivery_hour": "08-09"})
```

and an example response:
```json
{
  "delivery_day": "2023-05-12",
  "delivery_hour": "08-09",
  "last_update": "2023-02-21T07:10:20+00:00",
  "unit": "euro/mwh",
  "value": 27.74
}
```

## The challenge
Basically start implementing any part of your design from the design challenge. For example you can start writing a 
trade listener that write trades into the database, an ETL pipeline for the reference-price or you can work on the dashboard.
Obviously we don't have to finish any of those. 

This is more about seeing how you work and how we can collaborate on a coding task. We don't expect you to have all the 
right answers or to start typing right away. 