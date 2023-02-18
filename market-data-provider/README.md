# Reference Price
We have a third party data provider for all types of market data.

For the purposes of this task, we are interested only in the so called reference price, which is the average price 
for a megawatthour sold on the exchange for a given hour.

If no deals happened yet for a given hour, the value is undefined.

To access the data, the provider offers an API, with the following entrypoint:
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
The reference prices are updated every 10 minutes until the beginning of the delivery hour.