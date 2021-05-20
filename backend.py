""""
Classes to store information of one item and a bill. Functions to read and
update the json files, to write to output csv files.
"""
import csv  # To write the output into csv files
# import datetime
import json  # To read from and to update json files
# The product template json should be alphabetical
from collections import OrderedDict
import os  # To walk through product json files

# Global data structures which hold the information read from the json files

# TEMPLATES key: product name
# TEMPLATES field: Entry object
TEMPLATES = {}

# STORES key: store name
# STORES field: dict {'default_payment': str}
STORES = {}

# CONFIG_DICT key: config parameter
# CONFIG_DICT field: config parameter choice
CONFIG_DICT = {}

# list of Bill objects
BILLS = []

# list of payment methods as str
PAYMENTS = []

# DISCOUNT_CLASSES key: discount letter as str
# DISCOUNT_CLASSES field: dict holding discount value, description and
#                         applicable store
DISCOUNT_CLASSES = {}


# PRODUCT_KEYS key: product name
# PRODUCT_KEYS field: number corresponding to product name
PRODUCT_KEYS = {}


class Bill:
    """
    Holds all information for one purchase of various items

    ...
    Attributes
    ----------
    date:str
        Date of the purchase, e.g. '2021-02-13'
    discount_sum:float
        Sum of the money saved from all discounts of the entries
    products:tuple
        List or tuple holding the products purchased in this bill.
        Type is backend.Product
    payment:str
        Payment method for this bill, e.g. cash or card
    price_quantity_sum:float
        Sum of 'price for 1 item' * 'quantity bought' of all items. Price of the
        bill without any discounts
    quantity_discount_sum:float
        Sum of all quantity discounts of all items
    sale_sum:float
        Sum af all sale discounts of all items
    store:str
        Name of the store where this was purchased
    time:str
        Time of the purchase, e.g. '12:34'
    total:float
        Sum of all discounted prices of all items
    """

    def __init__(self, products=(), date='', time='',
                 store="", payment='', total=0.0, discount_sum=0.0,
                 quantity_discount_sum=0.0, sale_sum=0.0,
                 price_quantity_sum=0.0):
        self.products = products
        self.date = date
        self.time = time
        self.store = store
        self.payment = payment
        self.total = total
        self.discount_sum = discount_sum
        self.quantity_discount_sum = quantity_discount_sum
        self.sale_sum = sale_sum
        self.price_quantity_sum = price_quantity_sum

    def __repr__(self):
        out_string = (f"Bill\n"
                      f"\tproducts: {self.products}\n"
                      f"\tdate: {self.date}\n"
                      f"\ttime: {self.time}\n"
                      f"\tstore: {self.store}\n"
                      f"\tpayment: {self.payment}\n"
                      f"\tdiscount_sum: {self.discount_sum}\n"
                      f"\tquantity_discount_sum: {self.quantity_discount_sum}\n"
                      f"\tprice_quantity_sum: {self.price_quantity_sum}\n"
                      f"\tsale_sum: {self.sale_sum}\n"
                      f"\ttotal: {self.total}\n")
        return out_string


class Product:
    """
    Class that holds the information of a single item

    ...
    Attributes
    ----------
    discount:float
        Money saved by the discounts for this item
    discount_class:str
        Either a letter which corresponds to an entry in the DISCOUNT_CLASSES
        dictionary or a percentage, e.g. 20 would be 20 percent discount
    history:list of dicts
        List holding all previous purchases
    identifier:int
        Number to identify the product, this corresponds to the json file name
    price_final:float
        price_quantity with discounts applied. Order with which discounts are
        applied depends on the check_button in the GUI
    price_quantity:float
        price_single * quantity
    price_single:float
        Price of 1 item (or 1kg)
    name:str
        Name of the item
    product_class:str
        E.g. 'b' for beer or 'w' for wine
    quantity:float
        How much of this item was purchased. Either item count or weight in kg
    quantity_discount:float
        Number to subtract from price_quantity
    sale:float
        Number to subtract from price_quantity
    unknown:str
        Similar to product_class, e.g. 'l' for food ('Lebensmittel')
    display:bool
        Whether or not to list this product in the template selection
    notes:str
        Extra field for user notes
    """

    def __init__(self, name='', price_single=0.0, quantity=1.0,
                 discount_class='', product_class='', unknown='',
                 price_quantity=0.0, discount=0.0, quantity_discount="0,0",
                 sale="0,0", price_final=0.0, history=None, identifier=-1,
                 display=True, notes=''):
        if history is None:
            history = []
        self.name = name
        self.price_single = price_single
        self.quantity = quantity
        self.discount_class = discount_class
        self.product_class = product_class
        self.unknown = unknown
        self.price_quantity = price_quantity
        self.discount = discount
        self.quantity_discount = quantity_discount
        self.sale = sale
        self.price_final = price_final
        self.history = history
        self.identifier = identifier
        self.display = display
        self.notes = notes

    def __repr__(self):
        out_string = (f"\n---\nProduct\n"
                      f"\tname: {self.name}\n"
                      f"\tidentifier: {self.identifier}\n"
                      f"\tprice_single: {self.price_single}\n"
                      f"\tquantity: {self.quantity}\n"
                      f"\tdiscount_class: {self.discount_class}\n"
                      f"\tproduct_class: {self.product_class}\n"
                      f"\tunknown: {self.unknown}\n"
                      f"\tprice_quantity: {self.price_quantity}\n"
                      f"\tdiscount: {self.discount}\n"
                      f"\tquantity_discount: {self.quantity_discount}\n"
                      f"\tsale: {self.sale}\n"
                      f"\tprice_final: {self.price_final}\n"
                      f"\tdisplay: {self.display}\n"
                      f"\tnotes: {self.notes}\n"
                      f"\thistory: {self.history}\n"
                      f"---\n"
                      )
        return out_string


def read_config(config_path):
    """
    Uses the json module to load the config file and store its contents in
    CONFIG_DICT.

    Parameters:
        config_path (str): Path to the config file
    Returns:
        out_dict (dict): Dictionary holding config file contents
    """
    with open(config_path, 'r', encoding="utf-8") as config_file:
        out_dict = json.load(config_file)
        return out_dict


def format_bill(bill):
    """
    Takes the contents of a Bill object and creates the lines which are written
    into the output csv files

    Parameters:
        bill (Bill): Holds all information for one purchase of various items

    Returns:
        header_line (list): Holds information regarding the purchase, e.g. store
        lines (list of lists): Holds information regarding the purchased items
    """
    store = bill.store
    date = bill.date
    time = bill.time
    total = bill.total

    # In the GUI, the discounts are displayed as negative numbers. This is not
    # the case in the output csv
    discount_sum = bill.discount_sum * -1
    quantity_discount_sum = bill.quantity_discount_sum * -1
    sale_sum = bill.sale_sum * -1

    lines: list = list()

    # For each item in the bill, one line will be printed
    for product in bill.products:
        # If entry.discount_class is a number, divide it so it looks like the
        # percentage and format it to 2 decimal places
        try:
            discount_class = f'{float(product.discount_class) / 100:.2f}'
        except ValueError:
            # If entry.discount_class is one of the stored discounts, keep it as
            # the letter
            if product.discount_class in DISCOUNT_CLASSES:
                discount_class = product.discount_class
            else:
                # Otherwise it becomes 0, reduced to an empty field
                discount_class = ''

        line = ['', '', '',
                product.name,
                product.price_single,
                product.quantity,
                discount_class,
                product.product_class,
                product.unknown,
                product.price_quantity,
                product.discount,
                product.quantity_discount,
                product.sale,
                product.price_final]

        # Format the float values to have 2 decimal places
        # 0 becomes empty string
        for index, item in enumerate(line):
            # Skip formatting on quantity and discount_class
            if index in [5, 6]:
                continue
            # Replace 0 with ''
            if item == 0:
                line[index] = ''
            # Format numbers to have 2 decimal places
            elif isinstance(item, float):
                line[index] = f'{item:.2f}'

        # German format, decimal sign is comma
        line = [str(item).replace('.', ',') for item in line]

        lines.append(line)

    header_line = [date, time, store, bill.payment, len(bill.products), '',
                   '', '', '', bill.price_quantity_sum, discount_sum,
                   quantity_discount_sum, sale_sum, total]

    # Format the float values to have 2 decimal places
    # 0 becomes empty string
    for index, item in enumerate(header_line):
        # Replace 0 with ''
        if item == 0:
            header_line[index] = ''
        # Format numbers to have 2 decimal places
        elif isinstance(item, float):
            header_line[index] = f'{item:.2f}'

    # German format, decimal sign is comma
    header_line = [str(item).replace('.', ',') for item in header_line]

    return header_line, lines


def backup_bill(bill):
    """
    The export_bills() function gets called at the end. This function is called
    after each bill to act as a backup in case the program crashes

    Parameters:
        bill (Bill): Holds all information for one purchase of various items
    """
    # Create file name
    out_path = CONFIG_DICT["output"]
    # Can not have ':' in file name
    date_time_store = bill.date + 'T' + bill.time.replace(':', '-') + '_' \
        + bill.store
    out_path += date_time_store + ".csv"

    header_line, lines = format_bill(bill)

    # windows-1252 encoding so it's easier for excel
    with open(out_path, 'w', newline='', encoding="windows-1252") as out_file:
        file_writer = csv.writer(out_file, delimiter=CONFIG_DICT["delimiter"],
                                 quotechar='|', quoting=csv.QUOTE_MINIMAL)
        file_writer.writerow(header_line)
        for line in lines:
            file_writer.writerow(line)

        file_writer.writerow('')

    update_product_keys()


# def reset_backup():
#     """
#     This function is called at program start to clear out the backup file, so
#     that it only holds information for the current run
#     """
#     out_path = CONFIG_DICT["output_csv"]
#     with open(out_path, 'w', newline='', encoding="windows-1252") as out_file:
#         file_writer = csv.writer(out_file, delimiter=CONFIG_DICT["delimiter"],
#                                  quotechar='|', quoting=csv.QUOTE_MINIMAL)
#
#         file_writer.writerow('')


def export_bills():
    """
    This function is executed when the 'export' button is pressed in the GUI.
    The row count of the output csv is calculated, this value is written into
    field A1. The first row also holds a column description. All stored bills
    are formatted and written into the csv file
    """

    # Create file name
    out_path = CONFIG_DICT["output"]
    bill_count = len(BILLS)
    bill_dates = []
    line_count = 0
    for bill in BILLS:
        # line_count is written into field A1 of the csv so the excel macro
        # knows the row count
        line_count += len(bill.products) + 2
        bill_dates.append(bill.date)
    print("line_count: ", line_count)
    sorted(bill_dates)

    date_range = bill_dates[0] + "_to_" + bill_dates[-1]

    file_name = date_range + "_" + str(bill_count) + "bills.csv"
    out_path += file_name

    if not line_count:
        print("no bills")
        return

    first_line = [line_count, "Zeit", "Händler", "Bezeichnung",
                  "Preis", "Menge", "RK", "WK", "", "Preis", "Rabatt",
                  "Mengenrab", "Aktion", "Preis"]

    with open(out_path, 'w', newline='', encoding="windows-1252") as out_file:
        file_writer = csv.writer(out_file, delimiter=CONFIG_DICT["delimiter"],
                                 quotechar='|', quoting=csv.QUOTE_MINIMAL)
        file_writer.writerow(first_line)

        for bill in BILLS:
            header_line, lines = format_bill(bill)
            file_writer.writerow(header_line)
            for line in lines:
                file_writer.writerow(line)

            file_writer.writerow('')


# # encodings
# # utf-8, 16, 32
# # windows-1252
# # cp273 (german)
# def update_product_templates():
#     """
#     Overwrites the json holding the product templates with an updated version
#     """
#     templates_json = CONFIG_DICT["product_templates_json"]
#     out_dict = {}
#     for key, field in TEMPLATES.items():
#         try:
#             price_single = float(field.price_single.replace(',', '.'))
#         except AttributeError:
#             price_single = float(field.price_single)
#         round(price_single, 2)
#
#         try:
#             quantity = float(field.quantity)
#         except ValueError:
#             quantity = 1
#         temp = {
#             "price_single": price_single,
#             "quantity": quantity,
#             "product_class": field.product_class,
#             "unknown": field.unknown,
#             "history": field.history}
#         out_dict.update({key: temp})
#     # Save a dictionary with alphabetically sorted keys
#     out_dict = OrderedDict(sorted(out_dict.items()))
#     with open(templates_json, 'w', encoding="utf-16") as out_file:
#         json.dump(out_dict, out_file, indent=2)

def update_product_json(product):
    name = product.name
    default_price_per_unit = product.price_single
    default_quantity = product.quantity
    product_class = product.product_class
    unknown = product.unknown
    display = product.display
    notes = product.notes
    filename = "product_" + f"{product.identifier:05}" + ".json"
    path = CONFIG_DICT["product_folder"]

    if os.path.isfile(path + filename):
        with open(path + filename, 'r', encoding="utf-16") as in_file:
            data = json.load(in_file)

        history = []
        for item in data["history"]:
            if item not in history:
                history.append(item)
        # history = data["history"]
        for item in product.history:
            if item not in history:
                history.append(item)
        # history.append(product.history)
    else:
        history = []
        for item in product.history:
            if item not in history:
                history.append(item)

    print("saving ", name, " as ", filename)

    out_dict = {"name": name,
                "default_price_per_unit": default_price_per_unit,
                "default_quantity": default_quantity,
                "product_class": product_class,
                "unknown": unknown,
                "display": display,
                "notes": notes,
                "history": history}

    with open(path + filename, 'w', encoding="utf-16") as out_file:
        json.dump(out_dict, out_file, indent=2)

    # Update PRODUCT_KEYS dict
    PRODUCT_KEYS.update({name: "product_" + f"{product.identifier:05}"})


def update_product_history(product):
    """
    Read data from product json file. Replace history with the current history.
    Write back into product json file

    Parameters:
        product: Product
            The product in question
    """
    filename = "product_" + f"{product.identifier:05}" + ".json"
    path = CONFIG_DICT["product_folder"]

    if not os.path.isfile(path + filename):
        return

    with open(path + filename, 'r', encoding="utf-16") as in_file:
        data = json.load(in_file)

    history = []
    for item in data["history"]:
        if item not in history:
            history.append(item)
    # history = data["history"]
    for item in product.history:
        if item not in history:
            history.append(item)
    # history.append(product.history)

    out_dict = {"name": data["name"],
                "default_price_per_unit": data["default_price_per_unit"],
                "default_quantity": data["default_quantity"],
                "product_class": data["product_class"],
                "unknown": data["unknown"],
                "display": data["display"],
                "notes": data["notes"],
                "history": history}

    with open(path + filename, 'w', encoding="utf-16") as out_file:
        json.dump(out_dict, out_file, indent=2)


def update_stores():
    """
    Overwrites the json holding the stores with an updated version
    """
    stores_json = CONFIG_DICT["stores_json"]
    # out_dict = {}
    # for key, field in STORES.items():
    #     temp = {"default_payment": field}
    #     out_dict.update({key: temp})

    # Sort the dictionary by store name
    # TODO: use keys() instead of items()? or just out_dict?
    out_dict = OrderedDict(sorted(STORES.items()))

    with open(stores_json, 'w', encoding="utf-16") as out_file:
        json.dump(out_dict, out_file, indent=2)


def update_payments():
    """
    Overwrites the json holding the payment methods with an updated version
    """
    payments_json = CONFIG_DICT["payments_json"]
    out_list = sorted(PAYMENTS)
    out_dict = {"payments": out_list}
    with open(payments_json, 'w', encoding="utf-16") as out_file:
        json.dump(out_dict, out_file, indent=2)


def update_product_keys():
    """
    Writes PRODUCT_KEYS dict into json file
    """
    key_json = CONFIG_DICT["product_keys_json"]
    out_dict = OrderedDict(sorted(PRODUCT_KEYS.items()))

    with open(key_json, 'w', encoding="utf-16") as out_file:
        json.dump(out_dict, out_file, indent=2)


# def read_product_templates():
#     """
#     Reads the products stored in the json and stores them in the
#     TEMPLATES dict.
#     """
#     input_json = CONFIG_DICT["product_templates_json"]
#     with open(input_json, 'r', encoding="utf-16") as in_file:
#         data = json.load(in_file)
#         for key, field in data.items():
#             temp = Entry(product=key,
#                          price_single=field["price_single"],
#                          quantity=field["quantity"],
#                          product_class=field["product_class"],
#                          unknown=field["unknown"],
#                          history=field["history"])
#             TEMPLATES.update({key: temp})
#     print("TEMPLATES.keys(): ", TEMPLATES.keys())
#     print("first TEMPLATES entry: ")
#     for x in list(TEMPLATES)[0:1]:
#         print(x, TEMPLATES[x])


# def read_product_keys():
#     input_json = CONFIG_DICT["product_keys_json"]
#     with open(input_json, 'r', encoding="utf-16") as in_file:
#         data = json.load(in_file)
#     PRODUCT_KEYS.update(data)
#     print("PRODUCT_KEYS: ", PRODUCT_KEYS)


def read_products():
    product_folder = CONFIG_DICT["product_folder"]
    for root, _, files in os.walk(product_folder):
        for file in files:
            input_json = os.path.join(root, file)
            with open(input_json, 'r', encoding="utf-16") as in_file:
                data = json.load(in_file)
                identifier = file.replace("product_", '')
                identifier = identifier.replace(".json", '')
                identifier = int(identifier)
                str_id = "product_" + f"{identifier:05}"
                print(str_id, ", data: ", data)
                temp = Product(name=data["name"],
                               price_single=data["default_price_per_unit"],
                               quantity=data["default_quantity"],
                               product_class=data["product_class"],
                               unknown=data["unknown"],
                               history=data["history"],
                               display=data["display"],
                               notes=data["notes"],
                               identifier=identifier)
                TEMPLATES.update({data["name"]: temp})

                PRODUCT_KEYS.update({data["name"]: str_id})
    print("TEMPLATES.keys(): ", TEMPLATES.keys())
    print("first TEMPLATES entry: ")
    for x in list(TEMPLATES)[0:1]:
        print(x, TEMPLATES[x])


def read_stores():
    """
    Reads the store information stored in the json and stores them in the STORES
    dict.
    """
    input_json = CONFIG_DICT["stores_json"]
    with open(input_json, 'r', encoding="utf-16") as in_file:
        data = json.load(in_file)
        for key, field in data.items():
            STORES.update({key: field})
    print("STORES: ", STORES)


def read_discount_classes():
    """
    Reads the discount class information stored in the json and stores them
    in the DISCOUNT_CLASSES dict.
    """
    input_json = CONFIG_DICT["discount_classes_json"]
    with open(input_json, 'r', encoding="utf-16") as in_file:
        data = json.load(in_file)
        for key, field in data.items():
            DISCOUNT_CLASSES.update({key: field})
    print("DISCOUNT_CLASSES: ", DISCOUNT_CLASSES)


def read_payments():
    """
    Reads the payment method information stored in the json and stores them
    in the PAYMENTS list.
    """
    global PAYMENTS
    input_json = CONFIG_DICT["payments_json"]
    with open(input_json, 'r', encoding="utf-16") as in_file:
        data = json.load(in_file)
        PAYMENTS = data["payments"]
    print("PAYMENTS: ", PAYMENTS)
