import backend
from gui import Application


if __name__ == '__main__':
    backend.CONFIG_DICT = backend.read_config("config.json")
    backend.read_product_templates()
    backend.read_stores()
    interface = Application()
    interface.loop()
