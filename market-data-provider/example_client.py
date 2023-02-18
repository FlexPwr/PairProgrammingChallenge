import requests

response = requests.get("http://0.0.0.0:5060/reference-price",
                        params={"delivery_day": "2023-05-12", "delivery_hour": "08-09"})
response.raise_for_status()
print(response.json())
