import csv
import datetime
import json


TEMPLATES = []
STORES = []
CONFIG_DICT = {}
BILLS = []
PAYMENTS = []


class Bill:
    def __init__(self, entries=(), date=datetime.date, time=datetime.time,
                 store="", payment='', total=0.0):
        self.entries = entries
        self.date = date
        self.time = time
        self.store = store
        self.payment = payment
        self.total = total

    def __repr__(self):
        out_string = (f"Bill\n"
                      f"\tentries: {self.entries}\n"
                      f"\tdate: {self.date}\n"
                      f"\ttime: {self.time}\n"
                      f"\tstore: {self.store}\n"
                      f"\ttotal: {self.total}\n")
        return out_string


class Entry:
    def __init__(self, product='', price_single=0.0, quantity=1.0,
                 discount_class='', product_class='', unknown='',
                 price_quantity=0.0, discount=0.0, quantity_discount=0.0,
                 sale=0.0, price_final=0.0):
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
                      f"---\n"
                      )
        return out_string


def read_config(config_path):
    with open(config_path, 'r', encoding="utf-8") as config_file:
        return json.load(config_file)


# def setup_output_file():
#     columns = ["Geschäft",
#                "Datum",
#                "Uhrzeit",
#                "Produkt",
#                "Preis Einzel",
#                "Menge",
#                "Rabattklasse",
#                "Produktklasse",
#                "Unbekannt",
#                "Preis Menge",
#                "Rabatt",
#                "Mengenrabatt",
#                "Aktion",
#                "Preis Gesamt",
#                "Preis Einkauf"]
#     out_path = CONFIG_DICT["output_csv"]
#     if not os.path.isfile(out_path):
#         with open(out_path, 'w', encoding="utf-8") as out_file:
#             file_writer = csv.writer(out_file, delimiter=',', quotechar='|',
#                                      quoting=csv.QUOTE_MINIMAL)
#             file_writer.writerow(columns)
#         return True
#     return False


def save_to_csv(bill):
    out_path = CONFIG_DICT["output_csv"]

    store = bill.store
    date = bill.date
    time = bill.time
    total = bill.total

    # quantity = 0.0
    # discount = 0.0
    # quantity_discount = 0.0
    # sale = 0.0

    discount_sum: float = 0.0
    quantity_discount_sum: float = 0.0
    sale_sum: float = 0.0

    lines: list = list()

    for entry in bill.entries:
        if not entry.product and not entry.quantity and not entry.price_final:
            continue
        if float(entry.quantity) == 1:
            entry.quantity = ''
        else:
            entry.quantity = float(entry.quantity)
        # if float(entry.discount) == 0:
        #     discount = ''
        # else:
        #     discount = float(entry.discount)
        # if entry.quantity_discount == 0:
        #     quantity_discount = ''
        # else:
        #     quantity_discount = float(entry.quantity_discount)
        # if entry.sale == 0:
        #     sale = ''
        # else:
        #     sale = float(entry.sale)

        line = ['', '', '', '',
                entry.product.replace(',', '.'),
                entry.price_single,
                entry.quantity,
                entry.discount_class,
                entry.product_class,
                entry.unknown,
                entry.price_quantity,
                entry.discount,
                entry.quantity_discount,
                entry.sale,
                entry.price_final]
        lines.append(line)

        try:
            discount_sum += float(entry.discount)
        except ValueError:
            pass
        try:
            quantity_discount_sum += float(entry.quantity_discount)
        except ValueError:
            pass
        try:
            sale_sum += float(entry.sale)
        except ValueError:
            pass

    try:
        total = float(total)
    except ValueError:
        total = 0

    total_new = float(total) - discount_sum - quantity_discount_sum - sale_sum
    header_line = ['', date, time, store, bill.payment, len(bill.entries), '',
                   '', '', '', total, discount_sum, quantity_discount_sum,
                   sale_sum, total_new]

    with open(out_path, 'a', encoding="utf-8", newline='') as out_file:
        file_writer = csv.writer(out_file, delimiter=",", quotechar='|',
                                 quoting=csv.QUOTE_MINIMAL)
        file_writer.writerow(header_line)
        for line in lines:
            file_writer.writerow(line)

        file_writer.writerow('')


def update_product_templates():
    templates_json = CONFIG_DICT["product_templates_json"]
    with open(templates_json, 'w', encoding='utf-8') as out_file:
        out_list = []
        for template in TEMPLATES:
            out_dict = {"product": template.product,
                        "price_single": template.price_single,
                        "quantity": template.quantity,
                        "discount_class": template.discount_class,
                        "product_class": template.product_class,
                        "unknown": template.unknown,
                        "price_quantity": template.price_quantity,
                        "discount": template.discount,
                        "quantity_discount": template.quantity_discount,
                        "sale": template.sale,
                        "price_final": template.price_final}
            out_list.append(out_dict)
        out_list = sorted(out_list, key=lambda item: item["product"])
        json.dump(out_list, out_file, indent=2)


def update_stores():
    stores_json = CONFIG_DICT["stores_json"]
    with open(stores_json, 'w', encoding='utf-8') as out_file:
        out_list = sorted(STORES)
        out_dict = {"stores": out_list}
        json.dump(out_dict, out_file, indent=2)


def update_payments():
    payments_json = CONFIG_DICT["payments_json"]
    with open(payments_json, 'w', encoding='utf-8') as out_file:
        out_list = sorted(PAYMENTS)
        out_dict = {"payments": out_list}
        json.dump(out_dict, out_file, indent=2)


def read_product_templates():
    input_json = CONFIG_DICT["product_templates_json"]
    with open(input_json, 'r', encoding="utf-8") as in_file:
        data = json.load(in_file)
        for item in data:
            temp = Entry(product=item["product"],
                         price_single=item["price_single"],
                         quantity=item["quantity"],
                         discount_class=item["discount_class"],
                         product_class=item["product_class"],
                         unknown=item["unknown"],
                         price_quantity=item["price_quantity"],
                         discount=item["discount"],
                         quantity_discount=item["quantity_discount"],
                         sale=item["sale"],
                         price_final=item["price_final"])
            TEMPLATES.append(temp)


def read_stores():
    input_json = CONFIG_DICT["stores_json"]
    with open(input_json, 'r', encoding="utf-8") as in_file:
        data = json.load(in_file)
        for item in data["stores"]:
            STORES.append(item)
    print(STORES)


def read_payments():
    input_json = CONFIG_DICT["payments_json"]
    with open(input_json, 'r', encoding="utf-8") as in_file:
        data = json.load(in_file)
        for item in data["payments"]:
            PAYMENTS.append(item)
    print(PAYMENTS)
