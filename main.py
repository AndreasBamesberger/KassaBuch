""" Reads config file, json files and starts interface """
import backend
from gui import Application


if __name__ == '__main__':
    backend.CONFIG_DICT = backend.read_config("config.json")
    backend.read_product_templates()
    backend.read_stores()
    backend.read_payments()
    backend.read_discount_classes()
    # backend.reset_backup()
    interface = Application()
    interface.loop()
