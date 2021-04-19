import backend
from gui import Application

# TODO: ausgerechnete Felder auch in gui
# TODO: Rundungsfehler einbauen
# TODO: differenz zwischen 2 total Feldern
# TODO: wenn combobox input leer dann alles löschen

# TODO: improve gui grid
# TODO: ctrl-s
# TODO: enter -> move cursor to next row combobox

if __name__ == '__main__':
    backend.CONFIG_DICT = backend.read_config("config.json")
    backend.read_product_templates()
    backend.read_stores()
    backend.read_payments()
    interface = Application()
    interface.loop()
