import backend
from gui import Application

# TODO: differenz zwischen 2 total Feldern

# TODO: try place method
# TODO: improve gui grid

# TODO: billa, billa plus, merkur: payment default to karte
# TODO: don't save empty bill
# TODO: suppress 0,0 in gui
# TODO: when F1, check if last row has changed template,
#       show message box to ask if save changes
# TODO: change - in time to : in gui
# TODO: in config variable to choose if quantity_discount and sale input with
#       minus
# TODO: rework config file into txt
# TODO: minus zuerst as standard
# TODO: navigate with arrow keys
# TODO: save if this is the lowest price, save this in product_templates?



if __name__ == '__main__':
    backend.CONFIG_DICT = backend.read_config("config.json")
    backend.read_product_templates()
    backend.read_stores()
    backend.read_payments()
    backend.read_discount_classes()
    backend.reset_backup()
    interface = Application()
    interface.loop()
