Deals are pushed to us from the exchange through a websocket connection.

As soon as one of our traders, for example trader_1, performs a deal, we get a confirmation from the exchange formatted 
in json. 

Assume she buys 12.3 megawatt within the hour 8 to 9 for 20.5 euros/megawatt-hour, then we get the following message:
````json
{
  "deal_confirmation": 
    {
      "id": "123",
      "price": 20.5,
      "quantity": 12.3,
      "direction": "buy",
      "delivery_day": "2023-02-06",
      "delivery_hour": "08-09",
      "trader_id": "trader_1",
      "execution_time": "2023-02-06T06:13:45Z"
    }
}
````

It is essential that we maintain an open connection to the exchange at all times so that we don't miss any deals).