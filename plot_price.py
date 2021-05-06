"""
Open product file, extract final_price_per_unit and date_time of all entries in
the history and plot it
"""
import matplotlib
import json

import backend

backend.CONFIG_DICT = backend.read_config("config.json")
path = backend.CONFIG_DICT["product_folder"] + "product_00005.json"

with open(path, 'r', encoding="utf-16") as in_file:
    data = json.load(in_file)

prices = []
dates = []
for item in data["history"]:
    print(item)
    print("price: ", item["price_final_per_unit"])
    prices.append(item["price_final_per_unit"])
    dates.append(item["date_time"])

print("prices: ", prices)
print("dates: ", dates)
