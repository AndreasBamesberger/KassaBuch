""" Reads config file, json files and starts interface """
import backend
from gui import Application


if __name__ == '__main__':
    backend.CONFIG = backend.read_config("config.txt")
    # backend.read_product_templates()
    # backend.read_product_keys()
    backend.read_products()
    backend.read_stores()
    backend.read_payments()
    backend.read_discount_classes()
    interface = Application()
    interface.loop()
