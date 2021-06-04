import backend
import json
import os
from collections import OrderedDict

"""
Takes the TEMPLATES dictionary, changes the data format and
saves it in the product template json
"""
backend.CONFIG = backend.read_config("config.json")

product_folder = backend.CONFIG["FOLDERS"]["product folder"]
for root, _, files in os.walk(product_folder):
    for file in files:
        input_json = os.path.join(root, file)
        with open(input_json, 'r', encoding="utf-16") as in_file:
            data = json.load(in_file)
        data2 = {
            "name": data["name"],
            "default_price_per_unit": data["default_price_per_unit"],
            "default_quantity": data["default_quantity"],
            "product_class": data["product_class"],
            "unknown": data["unknown"],
            "history": data["history"]
        }
        with open(input_json, 'w', encoding="utf-16") as out_file:
            json.dump(data2, out_file, indent=2)

# backend.read_product_templates()
# backend.read_stores()
# backend.read_payments()
# backend.read_discount_classes()
# templates_json = backend.CONFIG["product_templates_json"]
#
# out_folder = backend.CONFIG["output"] + "products\\"
# counter = 0
# product_dict = {}
#
# for key, field in backend.TEMPLATES.items():
#     out_dict = {"product": key,
#                 "default_price_per_unit": field.price_single,
#                 "default_quantity": field.quantity,
#                 "product_class": field.product_class,
#                 "unknown": field.unknown,
#                 "history": field.history}
#     # key = key.replace('\\', '-')
#     # key = key.replace('/', '-')
#     # key = key.replace(':', '-')
#     # key = key.replace('*', '-')
#     # key = key.replace('?', '-')
#     # key = key.replace('"', '-')
#     # key = key.replace('<', '-')
#     # key = key.replace('>', '-')
#     # key = key.replace('|', '-')
#     out_path = out_folder + "product_" + f"{counter:05}" + ".json"
#
#     product_dict.update({key: "product_" + f"{counter:05}"})
#
#     with open(out_path, 'w', encoding="utf-16") as out_file:
#         json.dump(out_dict, out_file, indent=2)
#
#     counter += 1
#
# with open(backend.CONFIG["output"] + "product_keys.json", "w",
#           encoding="utf-16") as key_file:
#     json.dump(product_dict, key_file, indent=2)
#
#
# # for _, field in backend.TEMPLATES.items():
# #     temp = []
# #     for item in field.history:
# #         print(item)
# #         date_time = item["date_time"]
# #         store = item["store"]
# #         price_per_unit = item["price_final_per_unit"]
# #         temp.append({"date_time": date_time,
# #                      "store": store,
# #                      "price_single": field.price_single,
# #                      "quantity": field.quantity,
# #                      "price_quantity": field.price_quantity,
# #                      "discount_class": field.discount_class,
# #                      "quantity_discount": 0.0,
# #                      "sale": 0.0,
# #                      "discount": field.discount,
# #                      "price_final": field.price_final,
# #                      "price_final_per_unit": price_per_unit})
# #     field.history = temp
# #
# # # print(backend.TEMPLATES)
# #
# # out_dict = {}
# # for key, field in backend.TEMPLATES.items():
# #     temp = {"product": key,
# #             "price_single": field.price_single,
# #             "quantity": field.quantity,
# #             "product_class": field.product_class,
# #             "unknown": field.unknown,
# #             "history": field.history}
# #     out_dict.update({key: temp})
# # out_dict = OrderedDict(sorted(out_dict.items()))
# #
# #
# # with open(templates_json, 'w', encoding="utf-16") as out_file:
# #     json.dump(out_dict, out_file, indent=2)
