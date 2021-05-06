"""
Read all product json files, delete duplicates in the history list and store the
modified data
"""
import backend
import json
import os
backend.CONFIG_DICT = backend.read_config("config.json")

product_folder = backend.CONFIG_DICT["product_folder"]
for root, _, files in os.walk(product_folder):
    for file in files:
        input_json = os.path.join(root, file)
        with open(input_json, 'r', encoding="utf-16") as in_file:
            data = json.load(in_file)
        out_dict = {
            "name": data["name"],
            "default_price_per_unit": data["default_price_per_unit"],
            "default_quantity": data["default_quantity"],
            "product_class": data["product_class"],
            "unknown": data["unknown"]}

        # Delete duplicates from history
        history_list = []
        [history_list.append(item) for item in data["history"]
         if item not in history_list]
        out_dict.update({"history": history_list})

        with open(input_json, 'w', encoding="utf-16") as out_file:
            json.dump(out_dict, out_file, indent=2)
