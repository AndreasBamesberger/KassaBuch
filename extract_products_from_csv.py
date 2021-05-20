"""
Reads data from csv file, formats it into a backend.Bill. From this it creates a
json file per product and stores the bills in the product history.
"""
import backend

# import json
# import os
import csv
# from collections import OrderedDict


def str2float(in_str, default_empty=0):
    if in_str == '':
        return default_empty
    in_str = in_str.replace(',', '.')
    out_float = float(in_str)
    return out_float


backend.CONFIG_DICT = backend.read_config("config.json")

encoding = backend.CONFIG_DICT["encoding"]

csv_content = []
in_csv = backend.CONFIG_DICT["output"] + "KassenBon 2021 03 (ohne m).csv"
with open(in_csv, 'r', newline='', encoding=encoding) as csv_file:
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
        bill.price_quantity_sum = str2float(row[9])
        bill.discount_sum = str2float(row[10])
        bill.quantity_discount_sum = str2float(row[11])
        bill.sale_sum = str2float(row[12])
        bill.total = str2float(row[13])
        bill.products = []
    else:
        product = backend.Product()
        product.name = row[3]
        product.price_single = str2float(row[4])

        quantity = str2float(row[5], 1)
        if quantity == 0:
            product.quantity = 1
        else:
            product.quantity = quantity

        product.discount_class = row[6]
        product.product_class = row[7]
        product.unknown = row[8]
        product.price_quantity = str2float(row[9])
        product.discount = str2float(row[10])
        product.quantity_discount = str2float(row[11])
        product.sale = str2float(row[12])
        product.price_final = str2float(row[13])

        display = str2float(row[15])
        if display == 0:
            product.display = False
        elif display == 1:
            product.display = True

        product.notes = ''

        product.history = []

        bill.products.append(product)
        if (index + 1) in bill_headers:
            bill.products.pop(-1)
            backend.BILLS.append(bill)

# Go through all Bill objects and create the product history
for bill in backend.BILLS:
    day, month, year = bill.date.split('.')
    date = year + '-' + month + '-' + day
    date_time = date + 'T' + bill.time
    for product in bill.products:
        pfpu = round(product.price_final / product.quantity, 2)
        product.history.append({"date_time": date_time,
                                "store": bill.store,
                                "payment": bill.payment,
                                "price_single": product.price_single,
                                "quantity": product.quantity,
                                "price_quantity": product.price_quantity,
                                "discount_class": product.discount_class,
                                "quantity_discount": product.quantity_discount,
                                "sale": product.sale,
                                "discount": product.discount,
                                "price_final": product.price_final,
                                "price_final_per_unit": pfpu})


# Go through all Bill objects and give each product an identifier
# Make a mock entry so backend.TEMPLATES is not empty
test_entry = backend.Product()
test_entry.name = "TestEntry"
test_entry.identifier = -1
backend.TEMPLATES.update({"TestEntry": test_entry})
print("TEMPLATES: ", backend.TEMPLATES)
for bill in backend.BILLS:
    for product in bill.products:
        # Search backend.TEMPLATES for this product and give it the correct
        # identifier. If it is a new product, give it an identifier that has not
        # yet been used
        new_product = True
        for key, field in backend.TEMPLATES.items():
            if product.name == key:
                identifier = field.identifier
                new_product = False
                break
        if new_product:
            # Get all used identifier numbers, sort them, create a new one that
            # is one higher
            used_identifiers = [field.identifier
                                for _, field in backend.TEMPLATES.items()]
            used_identifiers = sorted(used_identifiers)
            new_identifier = used_identifiers[-1] + 1
            # To be safe, check if the new identifier hasn't been used so far
            for _, field in backend.TEMPLATES.items():
                if new_identifier == field.identifier:
                    raise SystemError
            identifier = new_identifier
        product.identifier = identifier
        # Update backend.TEMPLATES with this new template
        backend.TEMPLATES.update({product.name: product})

print("TEMPLATES: ", backend.TEMPLATES)
# Add product histories to templates
# for bill in backend.BILLS:
#     for product in bill.products:
#         for key, field in backend.TEMPLATES.items():
#             if product.identifier == field.identifier:
#                 field.history.append(product.history)

for item in backend.TEMPLATES["Geleefrüchte 250g"].history:
    print(item)

# Go through all Bill objects and create product json
# for key, field in backend.TEMPLATES.items():
#     backend.update_product_json(field)
for bill in backend.BILLS:
    for product in bill.products:
        backend.update_product_json(product)

backend.update_product_keys()

# Clear backend.TEMPLATES and read data from the created files
backend.TEMPLATES = {}
backend.read_products()
print("TEMPLATES: ", backend.TEMPLATES)
# Then add history to these entries by iterating through the Bill objects

# Empty the initial history entry to avoid duplicates
for key, field in backend.TEMPLATES.items():
    field.history = []

# Add product histories to templates
for bill in backend.BILLS:
    for product in bill.products:
        for key, field in backend.TEMPLATES.items():
            if product.identifier == field.identifier:
                if product.history == field.history:
                    continue
                else:
                    field.history.append(product.history)

# print("Semmel history: ", backend.TEMPLATES["Semmel"].history)
# # Go through all Bill objects and create product json
# # for key, field in backend.TEMPLATES.items():
# #     backend.update_product_json(field)
# for key, field in backend.TEMPLATES.items():
#     backend.update_product_json(field)

backend.update_product_keys()

# Update stores
backend.STORES = {}
for bill in backend.BILLS:
    temp_dict = {"default_payment": ''}
    backend.STORES.update({bill.store: temp_dict})
backend.update_stores()

# Update payments
backend.PAYMENTS = []
for bill in backend.BILLS:
    if bill.payment not in backend.PAYMENTS:
        backend.PAYMENTS.append(bill.payment)
backend.update_payments()
