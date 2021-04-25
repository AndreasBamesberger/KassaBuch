""""
Classes to store information of one item and a bill. Functions to read and
update the json files, to write to output csv files.
"""
import csv  # To write the output into csv files
# import datetime
import json  # To read from and to update json files
# The product template json should be alphabetical
from collections import OrderedDict


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
    entries:tuple
        List or tuple holding the products purchased in this bill.
        Type is backend.Entry
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
    def __init__(self, entries=(), date='', time='',
                 store="", payment='', total=0.0, discount_sum=0.0,
                 quantity_discount_sum=0.0, sale_sum=0.0,
                 price_quantity_sum=0.0):
        self.entries = entries
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
                      f"\tentries: {self.entries}\n"
                      f"\tdate: {self.date}\n"
                      f"\ttime: {self.time}\n"
                      f"\tstore: {self.store}\n"
                      f"\tdiscount_sum: {self.discount_sum}\n"
                      f"\tquantity_discount_sum: {self.quantity_discount_sum}\n"
                      f"\tsale_sum: {self.sale_sum}\n"
                      f"\ttotal: {self.total}\n")
        return out_string


class Entry:
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
    history:dict
        Dictionary holding all previous purchases. Key is the timestamp of the
        purchase, e.g. '23-03-2021T12:34'. Field is a list holding the store
        name as string and the price for a single item (or 1kg)
    price_final:float
        price_quantity with discounts applied. Order with which discounts are
        applied depends on the check_button in the GUI
    price_quantity:float
        price_single * quantity
    price_single:float
        Price of 1 item (or 1kg)
    product:str
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
    """
    def __init__(self, product='', price_single=0.0, quantity=1.0,
                 discount_class='', product_class='', unknown='',
                 price_quantity=0.0, discount=0.0, quantity_discount="0,0",
                 sale="0,0", price_final=0.0, history=None):
        if history is None:
            history = dict()
        self.product = product
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

    def __repr__(self):
        out_string = (f"\n---\nEntry\n"
                      f"\tproduct: {self.product}\n"
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
    for entry in bill.entries:
        # If entry.discount_class is a number, divide it so it looks like the
        # percentage and format it to 2 decimal places
        try:
            discount_class = f'{float(entry.discount_class) / 100:.2f}'
        except ValueError:
            # If entry.discount_class is one of the stored discounts, keep it as
            # the letter
            if entry.discount_class in DISCOUNT_CLASSES:
                discount_class = entry.discount_class
            else:
                # Otherwise it becomes 0, reduced to an empty field
                discount_class = ''

        line = ['', '', '',
                entry.product,
                entry.price_single,
                entry.quantity,
                discount_class,
                entry.product_class,
                entry.unknown,
                entry.price_quantity,
                entry.discount,
                entry.quantity_discount,
                entry.sale,
                entry.price_final]

        # Format the float values to have 2 decimal places
        # 0 becomes empty string
        for index, item in enumerate(line):
            # Skip formatting on quantity and discount_class
            if index in [6, 7]:
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

    header_line = [date, time, store, bill.payment, len(bill.entries), '',
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
    out_path = CONFIG_DICT["output_csv"]

    header_line, lines = format_bill(bill)

    # windows-1252 encoding so it's easier for excel
    with open(out_path, 'a', newline='', encoding="windows-1252") as out_file:
        file_writer = csv.writer(out_file, delimiter=CONFIG_DICT["delimiter"],
                                 quotechar='|', quoting=csv.QUOTE_MINIMAL)
        file_writer.writerow(header_line)
        for line in lines:
            file_writer.writerow(line)

        file_writer.writerow('')


def reset_backup():
    """
    This function is called at program start to clear out the backup file, so
    that it only holds information for the current run
    """
    out_path = CONFIG_DICT["output_csv"]
    with open(out_path, 'w', newline='', encoding="windows-1252") as out_file:
        file_writer = csv.writer(out_file, delimiter=CONFIG_DICT["delimiter"],
                                 quotechar='|', quoting=csv.QUOTE_MINIMAL)

        file_writer.writerow('')


def export_bills():
    """
    This function is executed when the 'export' button is pressed in the GUI.
    The row count of the output csv is calculated, this value is written into
    field A1. The first row also holds a column description. All stored bills
    are formatted and written into the csv file
    """
    out_path = CONFIG_DICT["final_csv"]
    line_count = 0
    for bill in BILLS:
        line_count += len(bill.entries) + 2
    print("line_count: ", line_count)

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


# encodings
# utf-8, 16, 32
# windows-1252
# cp273 (german)
def update_product_templates():
    """
    Overwrites the json holding the product templates with an updated version
    """
    templates_json = CONFIG_DICT["product_templates_json"]
    with open(templates_json, 'w', encoding="utf-16") as out_file:
        out_dict = {}
        for key, field in TEMPLATES.items():
            temp = {"price_single": field.price_single,
                    "quantity": field.quantity,
                    "product_class": field.product_class,
                    "unknown": field.unknown,
                    "history": field.history}
            out_dict.update({key: temp})
            # TODO: use ordered dict here
        json.dump(out_dict, out_file, indent=2)


def update_stores():
    """
    Overwrites the json holding the stores with an updated version
    """
    stores_json = CONFIG_DICT["stores_json"]
    with open(stores_json, 'w', encoding="utf-16") as out_file:
        out_dict = {}
        for store in sorted(STORES):
            temp = {"default_payment": ""}
            out_dict.update({store: temp})

        # Sort the dictionary by store name
        # TODO: use keys() instead of items()? or just out_dict?
        out_dict = OrderedDict(sorted(out_dict.items()))

        json.dump(out_dict, out_file, indent=2)


def update_payments():
    """
    Overwrites the json holding the payment methods with an updated version
    """
    payments_json = CONFIG_DICT["payments_json"]
    with open(payments_json, 'w', encoding="utf-16") as out_file:
        out_list = sorted(PAYMENTS)
        out_dict = {"payments": out_list}
        json.dump(out_dict, out_file, indent=2)


def read_product_templates():
    """
    Reads the products stored in the json and stores them in the TEMPLATES dict.
    """
    input_json = CONFIG_DICT["product_templates_json"]
    with open(input_json, 'r', encoding="utf-16") as in_file:
        data = json.load(in_file)
        for key, field in data.items():
            temp = Entry(product=key,
                         price_single=field["price_single"],
                         quantity=field["quantity"],
                         product_class=field["product_class"],
                         unknown=field["unknown"],
                         history=field["history"])
            TEMPLATES.update({key: temp})
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
        PAYMENTS = data
    print("PAYMENTS: ", PAYMENTS)
