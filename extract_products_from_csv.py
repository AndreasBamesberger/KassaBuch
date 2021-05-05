"""
Reads data from csv file, formats it into a backend.Bill. From this it creates a
json file per product and stores the bills in the product history.
"""
import backend

# import json
# import os
import csv
# from collections import OrderedDict


backend.CONFIG_DICT = backend.read_config("config.json")

csv_content = []
in_csv = backend.CONFIG_DICT["output"] + "KassenBon 2020.csv"
with open(in_csv, 'r', newline='') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=';', quotechar='|')
    bill_headers = []
    for index, row in enumerate(csv_reader):
        # Ignore the first 2 rows
        if index in [0, 1]:
            continue
        csv_content.append(row)

for index, row in enumerate(csv_content):
    # print(index, ": ", row)
    # Find the start of a bill. First column has date
    # Save row numbers where a bill starts into a list
    if row[0] != '':
        bill_headers.append(index)
# print(bill_headers)

for index, row in enumerate(csv_content):
    if index in bill_headers:
        bill = backend.Bill()
        bill.date = row[0]
        bill.time = row[1]
        bill.store = row[2]
        bill.payment = row[3]
        bill.price_quantity_sum = row[9]
        bill.discount_sum = row[10]
        bill.quantity_discount_sum = row[11]
        bill.sale_sum = row[12]
        bill.total = row[13]
        bill.products = []
    else:
        product = backend.Product()
        product.name = row[3]
        product.price_single = row[4]
        product.quantity = row[5]
        product.discount_class = row[6]
        product.product_class = row[7]
        product.unknown = row[8]
        product.price_quantity = row[9]
        product.discount = row[10]
        product.quantity_discount = row[11]
        product.sale = row[12]
        product.price_final = row[13]

        bill.products.append(product)
        if (index + 1) in bill_headers:
            bill.products.pop(-1)
            backend.BILLS.append(bill)

print(backend.BILLS[5])

