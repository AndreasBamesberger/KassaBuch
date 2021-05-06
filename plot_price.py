"""
Open product file, extract final_price_per_unit and date_time of all entries in
the history and plot it
"""
from matplotlib import pyplot
from matplotlib import dates
import json
import datetime

import backend

backend.CONFIG_DICT = backend.read_config("config.json")
path = backend.CONFIG_DICT["product_folder"] + "product_00005.json"

with open(path, 'r', encoding="utf-16") as in_file:
    data = json.load(in_file)

prices = []
date_list = []
for item in data["history"]:
    prices.append(item["price_final_per_unit"])
    date_list.append(item["date_time"])

# Strip time from date_list
date_list = [item.split('T')[0] for item in date_list]

# x = [datetime.datetime.strptime(d, '%Y-%m-%d').date() for d in date_list]
# pyplot.gca().xaxis.set_major_formatter(dates.DateFormatter('%Y-%m-%d'))
# pyplot.gca().xaxis.set_major_locator(dates.DayLocator())

pyplot.plot(date_list, prices)
# pyplot.gcf().autofmt_xdate()
pyplot.show()
