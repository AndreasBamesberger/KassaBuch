""""
Classes to store information of one item and a bill. Functions to read and
update the json files, to write to output csv files.
"""
import configparser  # To read config file
import csv  # To write the output into csv files
import json  # To read from and write to update json files
import os  # To walk through product json files
import re  # To match user input with product templates
import sqlite3

# The product template json should be alphabetical product names
from collections import OrderedDict

# Global data structures which hold the information read from the json files

# # TEMPLATES key: product name
# # TEMPLATES field: Product object
# TEMPLATES = {}

# # STORES key: store name
# # STORES field: dict {"default_payment": str, "default_discount_class": str}
# STORES = {}

# configparser.ConfigParser
CONFIG: configparser.ConfigParser()

# list of Bill objects
BILLS = []

# # list of payment methods as str
# PAYMENTS = []

# # DISCOUNT_CLASSES key: discount letter
# # DISCOUNT_CLASSES field: dict {"discount": float/int, "text": str,
# #                               "store": str}
# DISCOUNT_CLASSES = {}

# # PRODUCT_KEYS key: product name
# # PRODUCT_KEYS field: str, "product_" + number corresponding to product name
# PRODUCT_KEYS = {}

# sql objects
C = None
CONN = None

class Bill:
    """
    Holds all information for one purchase of various items

    ...
    Attributes
    ----------
    date: str
        Date of the purchase, e.g. '2021-02-13'
    discount_sum: float
        Sum of the money saved from all discounts of the entries
    payment: str
        Payment method for this bill, e.g. cash or card
    price_quantity_sum: float
        Sum of 'price for 1 item' * 'quantity bought' of all items. Price of the
        bill without any discounts
    products: tuple
        List holding the products purchased in this bill. Type is Product
    quantity_discount_sum: float
        Sum of all quantity discounts of all items
    sale_sum: float
        Sum af all sale discounts of all items
    store: str
        Name of the store where this was purchased
    time: str
        Time of the purchase, e.g. '12:34'
    total: float
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
    discount: float
        Money saved by the discounts for this item
    discount_class: str
        Either a letter which corresponds to an entry in the DISCOUNT_CLASSES
        dictionary or a percentage, e.g. 20 would be 20 percent discount
    display: bool
        Whether or not to list this product in the template selection
    history: list of dicts
        List holding all previous purchases
    identifier: int
        Number to identify the product, this corresponds to the json file name
    name: str
        Name of the item
    notes: str
        Extra field for user notes
    price_final: float
        price_quantity with discounts applied. Order with which discounts are
        applied depends on the "minus_first" check_button in the GUI
    price_quantity: float
        price_single * quantity
    price_single: float
        Price of 1 item (or 1kg)
    product_class: str
        E.g. 'b' for beer or 'w' for wine
    quantity: float
        How much of this item was purchased. Either item count or weight in kg
    quantity_discount: float
        Number to subtract from price_quantity
    sale: float
        Number to subtract from price_quantity
    unknown: str
        Similar to product_class, e.g. 'l' for food ('Lebensmittel')
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
                      f"\thistory: {len(self.history)} items\n"
                      f"---\n"
                      )
        return out_string


def read_config(config_path):
    """
    Uses the configparser module to extract information from the config file.

    Parameters:
        config_path (str): Windows path to the config file

    Returns:
        config (configparser.ConfigParser): Output created by configparser
    """
    config = configparser.ConfigParser()
    config.read(config_path)
    return config


def read_json(file_path):
    """
    Opens a json file and reads it using the json module

    Parameters:
        file_path (str): Windows path to the config file
    Returns:
        out_dict (dict): Output created by json.load()
    """
    with open(file_path, 'r', encoding="utf-8") as json_file:
        out_dict = json.load(json_file)
        return out_dict


def read_database():
    global C, CONN

    path = CONFIG["FOLDERS"]["sql database"]
    CONN = sqlite3.connect(path)
    C = CONN.cursor()

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
        # TODO don't do this to the product name
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


def create_unique_filename(file_path):
    """
    Check if a backup bill file with the output name already exists. If it does,
    add a number to its name and check again

    Parameters:
        file_path (str): Windows path to save the file

    Returns:
        new_path (str): The new Windows path where the file will be saved
    """

    if not os.path.isfile(file_path + ".csv"):
        return file_path

    counter = 0
    while True:
        new_path = file_path + "_" + f"{counter:02}"
        if not os.path.isfile(new_path + ".csv"):
            return new_path
        else:
            counter += 1


def backup_bill(bill):
    """
    In contrast to the export_bills function, this function gets called after
    each bill is saved to act as as backup in case the program crashes. The bill
    is saved as a csv file

    Parameters:
        bill (Bill): Holds all information for one purchase of various items
    """
    # Create file name
    out_path = CONFIG["FOLDERS"]["output"] + "bill_backups\\"
    encoding = CONFIG["DEFAULT"]["encoding"]
    # Can not have ':' in file name
    time = bill.time.replace(':', '-')
    store = bill.store.replace(':', '-')
    store = store.replace(' ', '_')
    date_time_store = bill.date + 'T' + time + '_' + store
    out_path += date_time_store

    out_path = create_unique_filename(out_path)

    out_path += ".csv"

    header_line, lines = format_bill(bill)

    with open(out_path, 'w', newline='', encoding=encoding) as out_file:
        file_writer = csv.writer(out_file,
                                 delimiter=CONFIG["DEFAULT"]["delimiter"],
                                 quotechar='|', quoting=csv.QUOTE_MINIMAL)
        file_writer.writerow(header_line)
        for line in lines:
            file_writer.writerow(line)

        file_writer.writerow('')

    update_product_keys()


def export_bills():
    """
    This function is executed when the 'export' button is pressed in the GUI.
    The row count of the output csv is calculated, this value is written into
    field A1. The first row also holds a column description. All stored bills
    are formatted and written into a csv file
    """
    if not BILLS:
        return

    # Create file name
    out_path = CONFIG["FOLDERS"]["output"] + "export\\"
    encoding = CONFIG["DEFAULT"]["encoding"]
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

    file_name = date_range + "_" + str(bill_count) + "bills"
    out_path += file_name

    out_path = create_unique_filename(out_path)

    out_path += ".csv"

    first_line = [line_count, "Zeit", "Händler", "Bezeichnung",
                  "Preis", "Menge", "RK", "WK", "", "Preis", "Rabatt",
                  "Mengenrab", "Aktion", "Preis"]

    with open(out_path, 'w', newline='', encoding=encoding) as out_file:
        file_writer = csv.writer(out_file,
                                 delimiter=CONFIG["DEFAULT"]["delimiter"],
                                 quotechar='|', quoting=csv.QUOTE_MINIMAL)
        file_writer.writerow(first_line)

        for bill in BILLS:
            header_line, lines = format_bill(bill)
            file_writer.writerow(header_line)
            for line in lines:
                file_writer.writerow(line)

            file_writer.writerow('')


def update_product_json(product):
    """
    Reads the purchase history from the json file, adds the current purchase and
    overwrites the json with this updated information

    Parameters:
        product (Product): Object holding the data to be saved as a json
    """
    name = product.name
    default_price_per_unit = product.price_single
    default_quantity = product.quantity
    product_class = product.product_class
    unknown = product.unknown
    display = product.display
    notes = product.notes
    filename = "product_" + f"{product.identifier:05}" + ".json"
    path = CONFIG["FOLDERS"]["product folder"]
    encoding = CONFIG["DEFAULT"]["encoding"]

    if os.path.isfile(path + filename):
        with open(path + filename, 'r', encoding=encoding) as in_file:
            data = json.load(in_file)

        history = []
        for item in data["history"]:
            if item not in history:
                history.append(item)
        for item in product.history:
            if item not in history:
                history.append(item)
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

    with open(path + filename, 'w', encoding=encoding) as out_file:
        json.dump(out_dict, out_file, indent=2)

    # Update PRODUCT_KEYS dict
    PRODUCT_KEYS.update({name: "product_" + f"{product.identifier:05}"})
    update_product_keys()


def update_product_history(product):
    """
    Read data from product json file. Replace history with the current history.
    Write back into product json file

    Parameters:
        product (Product): The product in question
    """
    filename = "product_" + f"{product.identifier:05}" + ".json"
    path = CONFIG["FOLDERS"]["product folder"]
    encoding = CONFIG["DEFAULT"]["encoding"]

    if not os.path.isfile(path + filename):
        return

    with open(path + filename, 'r', encoding=encoding) as in_file:
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

    with open(path + filename, 'w', encoding=encoding) as out_file:
        json.dump(out_dict, out_file, indent=2)


def update_stores():
    """
    Overwrites the json holding the stores with an updated version
    """
    stores_json = CONFIG["FILES"]["stores json"]
    encoding = CONFIG["DEFAULT"]["encoding"]
    # out_dict = {}
    # for key, field in STORES.items():
    #     temp = {"default_payment": field}
    #     out_dict.update({key: temp})

    # Sort the dictionary by store name
    # TODO: use keys() instead of items()? or just out_dict?
    out_dict = OrderedDict(sorted(STORES.items()))

    with open(stores_json, 'w', encoding=encoding) as out_file:
        json.dump(out_dict, out_file, indent=2)


def update_payments():
    """
    Overwrites the json holding the payment methods with an updated version
    """
    payments_json = CONFIG["FILES"]["payments json"]
    encoding = CONFIG["DEFAULT"]["encoding"]
    out_list = sorted(PAYMENTS)
    out_dict = {"payments": out_list}
    with open(payments_json, 'w', encoding=encoding) as out_file:
        json.dump(out_dict, out_file, indent=2)


def update_product_keys():
    """
    Writes PRODUCT_KEYS dict into json file
    """
    key_json = CONFIG["FILES"]["product keys json"]
    encoding = CONFIG["DEFAULT"]["encoding"]
    out_dict = OrderedDict(sorted(PRODUCT_KEYS.items()))

    with open(key_json, 'w', encoding=encoding) as out_file:
        json.dump(out_dict, out_file, indent=2)


def read_products():
    """
    Crawls through every file in the "products" folder, reads its contents and
    saves it as a new product template in TEMPLATES
    """
    product_folder = CONFIG["FOLDERS"]["product folder"]
    encoding = CONFIG["DEFAULT"]["encoding"]
    for root, _, files in os.walk(product_folder):
        for index, file in enumerate(files):
            input_json = os.path.join(root, file)
            with open(input_json, 'r', encoding=encoding) as in_file:
                data = json.load(in_file)
                identifier = file.replace("product_", '')
                identifier = identifier.replace(".json", '')
                identifier = int(identifier)
                str_id = "product_" + f"{identifier:05}"
                # print(str_id, ", data: ", data)
                # print(str_id)
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

            # Print status message every 500 files to show user that program is
            # still running
            if index % 500 == 0:
                print("Reading file: ", str_id)

    print("TEMPLATES.keys(): ", TEMPLATES.keys())
    print("first TEMPLATES entry: ")
    for x in list(TEMPLATES)[0:1]:
        print(x, TEMPLATES[x])


def read_stores():
    """
    Reads the store information stored in the json and stores them in the STORES
    dict.
    """
    input_json = CONFIG["FILES"]["stores json"]
    encoding = CONFIG["DEFAULT"]["encoding"]
    with open(input_json, 'r', encoding=encoding) as in_file:
        data = json.load(in_file)
        for key, field in data.items():
            STORES.update({key: field})
    print("STORES: ", STORES)


def read_discount_classes():
    """
    Reads the discount class information stored in the json and stores them
    in the DISCOUNT_CLASSES dict.
    """
    input_json = CONFIG["FILES"]["discount classes json"]
    encoding = CONFIG["DEFAULT"]["encoding"]
    with open(input_json, 'r', encoding=encoding) as in_file:
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
    input_json = CONFIG["FILES"]["payments json"]
    encoding = CONFIG["DEFAULT"]["encoding"]
    with open(input_json, 'r', encoding=encoding) as in_file:
        data = json.load(in_file)
        PAYMENTS = data["payments"]
    print("PAYMENTS: ", PAYMENTS)


def regex_search(input_str):
    """
    Treat the user template input as a regex pattern and match it with every
    product name.

    Parameters:
        input_str (str): The user input
    Returns:
        out_dict (dict): Dict holding all matching products.
                         Key = TEMPLATES.key, Field = TEMPLATES.field
    """

    """
    regex: match all alphanumeric and whitespace characters
    .: Any character except newline
    *: Zero or more of
    """
    input_str = input_str.replace('*', ".*")
    # Add ".*" in front so the user input can match strings anywhere without
    # typing '*' in front
    input_str = ".*" + input_str
    try:
        pattern = re.compile(input_str)
    except re.error:
        return None
    out_dict = dict()

    for key, field in TEMPLATES.items():
        match = pattern.match(key.lower())
        if match:
            out_dict.update({key: field})

    return out_dict


def create_template(product: Product):
    """
    Add the new Product to the TEMPLATES list or update an old entry. Then save
    the product info as a json file.

    Parameters:
        product (Product): The Product object from which the new template is
                           created
    """

    # Delete trailing whitespaces from product name
    product.name = product.name.rstrip()

    if product.name == '':
        return

    if product.quantity == 0:
        product.quantity = 1

    # # German format, decimal sign is comma
    # product.price_single = str(product.price_single).replace('.', ',')
    # product.quantity = str(product.quantity).replace('.', ',')

    # If template already exists, delete the old product
    try:
        TEMPLATES.pop(product.name)
    except KeyError:
        pass

    # Add new template to dictionary
    TEMPLATES.update({product.name: product})

    # Update the product json file or create a new one
    update_product_json(product)


def create_product(user_input: dict, new_product: bool):
    """
    Create a new Product object from the user input.

    Parameters:
        user_input (dict): Dictionary holding all user input
        new_product (bool): If true, the product has not yet been saved as a
                            json file

    Returns:
        product (Product): The created Product object
    """

    identifier = -1

    # Get history from backend.TEMPLATES
    if new_product:
        history = []
        display = True
        notes = ''
    else:
        if user_input["name"] == '':
            history = []
            display = True
            notes = ''
        else:
            if user_input["name"] in TEMPLATES:
                history = TEMPLATES[user_input["name"]].history
                display = TEMPLATES[user_input["name"]].display
                notes = TEMPLATES[user_input["name"]].notes
            else:
                # If the product is new and has not been saved as a new
                # template
                history = []
                display = True
                notes = ''

    # Search backend.TEMPLATES for this product and give it the correct
    # identifier. If it is a new product, give it an identifier that has not
    # yet been used
    new_product = True
    for key, field in TEMPLATES.items():
        if user_input["name"] == key:
            identifier = field.identifier
            new_product = False
            break
    if new_product:
        # Get all used identifier numbers, sort them, create a new one that
        # is one higher
        used_identifiers = [field.identifier
                            for _, field in TEMPLATES.items()]
        used_identifiers = sorted(used_identifiers)
        new_identifier = used_identifiers[-1] + 1
        # To be safe, check if the new identifier hasn't been used so far
        for _, field in TEMPLATES.items():
            if new_identifier == field.identifier:
                raise SystemError
        identifier = new_identifier

    product = Product(name=user_input["name"],
                      price_single=user_input["price_single"],
                      quantity=user_input["quantity"],
                      discount_class=user_input["discount_class"],
                      product_class=user_input["product_class"],
                      unknown=user_input["unknown"],
                      price_quantity=user_input["price_quantity"],
                      discount=user_input["discount"],
                      quantity_discount=user_input["quantity_discount"],
                      sale=user_input["sale"],
                      price_final=user_input["price_final"],
                      history=history,
                      identifier=identifier,
                      display=display,
                      notes=notes)
    return product


def create_bill(user_input: dict):
    """
    Create a Bill object from the user input. Then store it in the BILLS list
    and save it as a csv file.

    Parameters:
        user_input (dict): Dictionary holding all user input
    """
    # If store is new, store it and update the stores json
    if user_input["store"] not in STORES and user_input["store"] != '':
        STORES.update({user_input["store"]: {"default_payment": '',
                                             "default_discount_class": ''}})
        update_stores()

    # If payment method is new, store it and update the payments json
    if user_input["payment"] not in PAYMENTS and user_input["payment"] != '':
        PAYMENTS.append(user_input["payment"])
        update_payments()

    # Time is written with '-' as a separator because it's easier to type in
    # on the numpad
    try:
        hours, minutes = user_input["time"].split(':')
        # If user wrote hours or minutes as one digit, add the leading zero
        if len(hours) == 1:
            hours = '0' + hours
        if len(minutes) == 1:
            minutes = '0' + minutes
        time = hours + ':' + minutes
    except ValueError:
        # If user did not enter time
        time = "00:00"

    price_quantity_sum = 0.0

    # Date user input is dd-mm
    # Transform it into yyyy-mm-dd
    try:
        day, month = user_input["date"].split('-')
    except ValueError:
        day = "00"
        month = "00"

    # If user wrote day or month as one digit, add the leading zero
    if len(day) == 1:
        day = '0' + day
    if len(month) == 1:
        month = '0' + month

    date = CONFIG["DEFAULT"]["year"] + '-' + month + '-' + day

    for product in user_input["product_list"]:
        # Skip empty line
        if not product.name and not product.quantity and \
                not product.price_final:
            continue
        # TODO: don't do this formatting here, do this only in the
        #  backend.format_bill
        # Quantity = 1 should not be shown in final excel file
        if float(product.quantity) == 1:
            product.quantity = ''
        else:
            product.quantity = float(product.quantity)

        price_quantity_sum += product.price_quantity

        if CONFIG["DEFAULT"]["save history"]:
            # update product history with this purchase
            date_time = date + 'T' + time
            # price_per_unit includes discounts
            price_per_unit = 0
            if isinstance(product.quantity, str) or product.quantity == 0:
                # if quantity is '' then it is 1
                price_per_unit = product.price_final
            elif isinstance(product.quantity, float):
                price_per_unit = product.price_final / product.quantity
            price_per_unit = round(price_per_unit, 2)
            # product.history.append([date_time, store, price_per_unit])
            product.history.append({
                "date_time": date_time,
                "store": user_input["store"],
                "payment": user_input["payment"],
                "price_single": product.price_single,
                "quantity": product.quantity,
                "price_quantity": product.price_quantity,
                "discount_class": product.discount_class,
                "quantity_discount": product.quantity_discount,
                "sale": product.sale,
                "discount": product.discount,
                "price_final": product.price_final,
                "price_final_per_unit": price_per_unit
            })

        TEMPLATES.update({product.name: product})

        update_product_history(product)

    price_quantity_sum = round(price_quantity_sum, 2)

    bill = Bill(products=user_input["product_list"], date=date, time=time,
                store=user_input["store"], payment=user_input["payment"],
                total=user_input["total"],
                discount_sum=user_input["discount_sum"],
                quantity_discount_sum=user_input["quantity_discount_sum"],
                sale_sum=user_input["sale_sum"],
                price_quantity_sum=price_quantity_sum)
    print("bill = ", bill)

    # Don't save an empty bill
    if bill.products:
        BILLS.append(bill)
        backup_bill(bill)

def get_stores():
    C.execute("SELECT name FROM stores")
    return [item[0] for item in C.fetchall()]

def get_payments():
    C.execute("SELECT name FROM payments")
    return [item[0] for item in C.fetchall()]

def get_product_names(condition_str):
    if condition_str:
        C.execute("SELECT name FROM products " +  condition_str)
    else:
        C.execute("SELECT name FROM products")
    out_list = [item[0] for item in C.fetchall()]
    return out_list



