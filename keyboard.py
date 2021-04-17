from pynput.keyboard import Controller, Key
# import time
import win32gui

import backend


def window_enumeration_handler(hwnd, top_windows):
    top_windows.append((hwnd, win32gui.GetWindowText(hwnd)))


def write_to_program():
    program = backend.CONFIG_DICT["type_to_program"]
    if program == '':
        print("empty program string")
        return
    change_to_program(program)
    write_bills()


def change_to_program(program):
    top_windows = []

    win32gui.EnumWindows(window_enumeration_handler, top_windows)

    for window in top_windows:
        if program in window[1].lower():
            win32gui.ShowWindow(window[0], 5)
            win32gui.SetForegroundWindow(window[0])
            break


def write_bills():
    keyboard = Controller()

    for bill in backend.BILLS:

        header = [bill.date,
                  bill.time,
                  bill.store,
                  "Zahlungsart",
                  "Artikelmenge",
                  '',
                  '',
                  '',
                  '',
                  bill.total,
                  "Rabatt",
                  '',
                  '',
                  bill.total]

        for item in header:
            # # make bold
            # keyboard.press(Key.ctrl)
            # keyboard.press(Key.shift)
            # keyboard.press('f')
            # time.sleep(0.1)
            # keyboard.release('f')
            # keyboard.release(Key.ctrl)
            # keyboard.release(Key.shift)
            # time.sleep(0.1)
            keyboard.type(item)
            # time.sleep(0.1)

            keyboard.press(Key.tab)
            keyboard.release(Key.tab)

        keyboard.press(Key.enter)
        keyboard.release(Key.enter)

        for entry in bill.entries:
            line = [entry.product.replace(',', '.'),
                    entry.price_single,
                    entry.quantity,
                    entry.discount_class,
                    entry.product_class,
                    entry.unknown,
                    entry.price_quantity,
                    entry.discount,
                    entry.quantity_discount,
                    entry.sale,
                    entry.price_final,
                    ]
            for item in line:
                keyboard.type(item)
                keyboard.press(Key.tab)
                keyboard.release(Key.tab)

            keyboard.press(Key.enter)
            keyboard.release(Key.enter)

        keyboard.press(Key.enter)
        keyboard.release(Key.enter)

    with keyboard.pressed(Key.alt):
        keyboard.press(Key.tab)
        keyboard.release(Key.tab)
