""" Reads config file, json files and starts interface """
import libs.backend as backend
from libs.gui import Application


if __name__ == '__main__':
    backend.CONFIG = backend.read_config("config.txt")
    backend.read_products()
    backend.read_stores()
    backend.read_payments()
    backend.read_discount_classes()
    interface = Application()
    interface.loop()
