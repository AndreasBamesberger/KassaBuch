"""
Contains container classes for the tkinter objects and functions to instantiate
them
"""
import tkinter as tk
from tkinter import ttk

import libs.backend as backend


# TODO: create parent gui object class?


class LabelContainer:
    """
    All information to create a tkinter.Label object as well as the created
    object

    ...

    Attributes
    ----------
    bg: str
        Background colour
    column: str
        Horizontal grid value
    fg: str
        Foreground (= font) colour
    font: str
        Text font
    frame: tkinter.Frame
        Where this object will be displayed
    object: tkinter.Label
        The actual tkinter object
    row: int
        Vertical grid value
    sticky: str
        To which side of the grid box will the object stick
    text: str
        Text to be displayed

    Methods
    -------
    create(self):
        Create the tkinter object and position it using grid()
    """
    def __init__(self, frame, text, column, row, sticky, font):
        self.frame = frame
        self.text = text
        self.column = column
        self.row = row
        self.sticky = sticky
        self.font = font
        self.bg = "light grey"
        self.fg = "black"
        self.object = None

    def create(self):
        """
        Create the tkinter object and position it using grid()
        """
        self.object = tk.Label(self.frame, text=self.text, bg=self.bg,
                               fg=self.fg, font=self.font)
        self.object.grid(row=self.row, column=self.column, sticky=self.sticky)


class EntryContainer:
    """
    All information to create a tkinter.Entry object as well as the created
    object

    ...

    Attributes
    ----------
    bg: str
        Background colour
    column: str
        Horizontal grid value
    fg: str
        Foreground (= font) colour
    frame: tkinter.Frame
        Where this object will be displayed
    object: tkinter.Label
        The actual tkinter object
    row: int
        Vertical grid value
    sticky: str
        To which side of the grid box will the object stick
    width: int
        Horizontal size of the entry field

    Methods
    -------
    change_bg(self, new_colour):
        Change the background colour of the field
    create(self):
        Create the tkinter object and position it using grid()
    """

    def __init__(self, frame, column, row, width, bg, fg):
        self.frame = frame
        self.column = column
        self.row = row
        self.width = width
        self.sticky = 'w'
        self.bg = bg
        self.fg = fg
        self.object = None

    def create(self):
        """
        Create the tkinter object and position it using grid()
        """
        self.object = tk.Entry(self.frame, width=self.width, bg=self.bg,
                               fg=self.fg)
        self.object.grid(row=self.row, column=self.column, sticky=self.sticky)

    def change_bg(self, new_colour):
        """
        Change the background colour of the field

        Parameters:
            new_colour: str
                The new background colour
        """
        self.object.configure(bg=new_colour)


class ButtonContainer:
    """
    All information to create a tkinter.Button object as well as the created
    object

    ...

    Attributes
    ----------
    bg: str
        Background colour
    column: str
        Horizontal grid value
    font: str
        Text font
    frame: tkinter.Frame
        Where this object will be displayed
    func: function
        Function to execute when button is pressed
    object: tkinter.Label
        The actual tkinter object
    param: ?
        Parameter to be passed to func
    row: int
        Vertical grid value
    sticky: str
        To which side of the grid box will the object stick
    text: str
        Text to be displayed

    Methods
    -------
    change_bg(self, new_colour):
        Change the background colour of the field
    create(self):
        Create the tkinter object and position it using grid()
    """
    def __init__(self, frame, text, func, param, column, row, font):
        self.frame = frame
        self.text = text
        self.func = func
        self.param = param
        self.column = column
        self.row = row
        self.font = font
        self.bg = "white"
        self.sticky = "news"
        self.object = None

    def create(self):
        """
        Create the tkinter object and position it using grid()
        """
        def command():
            if self.param is not None:
                self.func(self.param)
            else:
                self.func()

        self.object = tk.Button(self.frame, text=self.text,
                                width=len(self.text), command=command,
                                font=self.font)
        self.object.grid(row=self.row, column=self.column, sticky=self.sticky)

    def change_bg(self, new_colour):
        """
        Change the background colour of the field

        Parameters:
            new_colour: str
                The new background colour
        """
        self.object.configure(bg=new_colour)


class ComboBoxContainer:
    """
    All information to create a tkinter.ttk.ComboBox object as well as the
    created object

    ...

    Attributes
    ----------
    column: str
        Horizontal grid value
    frame: tkinter.Frame
        Where this object will be displayed
    func: function
        Function to execute when button is pressed
    object: tkinter.Label
        The actual tkinter object
    param: ?
        Parameter to be passed to func
    row: int
        Vertical grid value
    state: str
        Behaviour of the ComboBox
    sticky: str
        To which side of the grid box will the object stick
    trace_var: tkinter.StringVar
        Variable linked to the input field, calls function if changed
    values: list
        List of values to be displayed in the drop-down
    width: int
        Horizontal size of the entry field

    Methods
    -------
    create(self):
        Create the tkinter object and position it using grid()
    """
    def __init__(self, frame, func, param, values, state, column, row,
                 width, sticky):
        self.frame = frame
        self.func = func
        self.param = param
        self.values = values
        self.state = state
        self.column = column
        self.row = row
        self.width = width
        self.sticky = sticky
        self.object = None
        self.trace_var = None

    def create(self):
        """
        Create the tkinter object and position it using grid()
        """
        def command(*_):
            if not self.func:
                return
            if self.param is not None:
                self.func(self.param)
            else:
                self.func()

        self.trace_var = tk.StringVar()
        self.trace_var.set('')
        self.trace_var.trace('w', command)

        self.object = ttk.Combobox(self.frame, width=self.width,
                                   textvariable=self.trace_var)

        box_list = list()
        if self.values == "templates":
            box_list = sorted([key for key, field in backend.TEMPLATES.items()
                               if field.display])
        elif self.values == "stores":
            box_list = sorted(backend.STORES)
        elif self.values == "payments":
            box_list = sorted(backend.PAYMENTS)
        self.object["values"] = box_list
        self.object["state"] = self.state
        self.object.grid(row=self.row, column=self.column, sticky=self.sticky)


class CheckButtonContainer:
    """
    All information to create a tkinter.ttk.ComboBox object as well as the
    created object

    ...

    Attributes
    ----------
    column: str
        Horizontal grid value
    frame: tkinter.Frame
        Where this object will be displayed
    object: tkinter.Label
        The actual tkinter object
    row: int
        Vertical grid value
    sticky: str
        To which side of the grid box will the object stick
    text: str
        Text to be displayed
    trace_var: tkinter.StringVar
        Variable linked to the input field, calls function if changed

    Methods
    -------
    create(self):
        Create the tkinter object and position it using grid()
    """
    def __init__(self, frame, text, column, row, sticky):
        self.frame = frame
        self.text = text
        self.column = column
        self.row = row
        self.sticky = sticky
        self.object = None
        self.trace_var = None

    def create(self):
        """
        Create the tkinter object and position it using grid()
        """
        def command():
            pass
        # TODO: call trace_update_entries when value changes

        self.trace_var = tk.IntVar()
        self.trace_var.set(1)  # Requested to be 1 by default

        self.object = tk.Checkbutton(self.frame, text=self.text,
                                     variable=self.trace_var, onvalue=1,
                                     offvalue=0, command=command)
        self.object.grid(row=self.row, column=self.column, sticky=self.sticky)


def create_labels(interface, frame):
    """
    Creates all LabelContainer objects for the chosen frame so the tkinter.Label
    object can later be created with correctly linked callback functions and
    frames

    Parameters:
        interface: gui.Application
            Object that created the window where these objects will be displayed
        frame: tkinter.Frame
            Frame where these objects will be displayed
    Returns:
        dict
            key: label description
            field: LabelContainer
    """
    if frame == interface.frame_main:
        return {
            "help_f1": LabelContainer(interface.frame_main,
                                      "F1: Auswerten & neue Zeile", 0, 0, "w",
                                      "none 8 bold"),
            "help_f2": LabelContainer(interface.frame_main, "F2: Neue Zeile", 0,
                                      1, "w", "none 8 bold"),
            "help_f3": LabelContainer(interface.frame_main,
                                      "F3: Zu Datum springen",
                                      0, 2, "w", "none 8 bold"),
            "help_f4": LabelContainer(interface.frame_main,
                                      "F4: In unterste Zeile springen", 0, 3,
                                      "w", "none 8 bold"),
            "help_f5": LabelContainer(interface.frame_main, "F5: Auswerten", 0,
                                      4, "w", "none 8 bold"),
            "help_f6": LabelContainer(interface.frame_main, "F6: Pickerl", 0, 5,
                                      "w", "none 8 bold"),
            "date": LabelContainer(interface.frame_main, "Datum (dd-mm): ", 1,
                                   0, "e", "none 14 bold"),
            "time": LabelContainer(interface.frame_main, "Uhrzeit (hh-mm): ", 1,
                                   1, "e", "none 14 bold"),
            "store": LabelContainer(interface.frame_main, "Geschäft: ", 1, 2,
                                    "e", "none 14 bold"),
            "payment": LabelContainer(interface.frame_main, "Zahlungsart: ", 1,
                                      3, "e", "none 14 bold"),
            "price_quantity_sum": LabelContainer(interface.frame_main,
                                                 "Summe Mengenpreise: ", 1, 4,
                                                 "e", "none 14 bold"),
            "price_quantity_sum_var": LabelContainer(interface.frame_main,
                                                     "", 2, 4, "w",
                                                     "none 14 bold"),
            "discount_sum": LabelContainer(interface.frame_main,
                                           "Summe Rabatte: ", 1, 5, "e",
                                           "none 14 bold"),
            "discount_sum_var": LabelContainer(interface.frame_main, "", 2, 5,
                                               "w", "none 14 bold"),
            "quantity_discount_sum": LabelContainer(interface.frame_main,
                                                    "Summe Mengenrabatte", 1, 6,
                                                    "e", "none 14 bold"),
            "quantity_discount_sum_var": LabelContainer(interface.frame_main,
                                                        "", 2, 6, "w",
                                                        "none 14 bold"),
            "sale_sum": LabelContainer(interface.frame_main, "Summe Aktionen: ",
                                       1, 7, "e", "none 14 bold"),
            "sale_sum_var": LabelContainer(interface.frame_main, "", 2, 7, "w",
                                           "none 14 bold"),
            "total": LabelContainer(interface.frame_main, "Gesamt: ", 1, 8, "e",
                                    "none 14 bold"),
            "total_var": LabelContainer(interface.frame_main, "", 2, 8, "w",
                                        "none 14 bold"),
            "description": LabelContainer(interface.frame_main,
                                          "Vorlage                            "
                                          "            Produkt                "
                                          "             Menge Preis  RK PK  U "
                                          "  Preis   Rabatt "
                                          "MRabt  Aktion Preis",
                                          0, 8, "w", "none 12 bold")
        }
    elif frame == interface.frame_fields:
        pass
    else:
        raise SystemError


def create_entries(interface, frame, row):
    """
    Creates all EntryContainer objects for the chosen frame so the tkinter.Entry
    object can later be created with correctly linked callback functions and
    frames

    Parameters:
        interface: gui.Application
            Object that created the window where these objects will be displayed
        frame: tkinter.Frame
            Frame where these objects will be displayed
        row: int
            Row in the scrollable region
    Returns:
        dict
            key: label description
            field: EntryContainer
    """
    if frame == interface.frame_main:
        return {
            "date": EntryContainer(interface.frame_main, 2, 0, 20, "white",
                                   "black"),
            "time": EntryContainer(interface.frame_main, 2, 1, 20, "white",
                                   "black"),
        }
    elif frame == interface.frame_fields:
        return {
            "name": EntryContainer(interface.frame_fields, 3, row, 30, "gray75",
                                   "black"),
            "quantity": EntryContainer(interface.frame_fields, 5, row, 8,
                                       "white", "black"),
            "price_single": EntryContainer(interface.frame_fields, 7, row, 8,
                                           "white", "black"),
            "discount_class": EntryContainer(interface.frame_fields, 9, row, 4,
                                             "salmon", "black"),
            "product_class": EntryContainer(interface.frame_fields, 11, row, 4,
                                            "white", "black"),
            "unknown": EntryContainer(interface.frame_fields, 13, row, 4,
                                      "light sky blue", "black"),
            "price_quantity": EntryContainer(interface.frame_fields, 15, row, 8,
                                             "gray75", "black"),
            "discount": EntryContainer(interface.frame_fields, 17, row, 8,
                                       "gray75", "black"),
            "quantity_discount": EntryContainer(interface.frame_fields, 19, row,
                                                8, "white", "black"),
            "sale": EntryContainer(interface.frame_fields, 21, row, 8, "white",
                                   "black"),
            "price_final": EntryContainer(interface.frame_fields, 23, row, 8,
                                          "gray75", "black")
        }
    else:
        raise SystemError


def create_buttons(interface, frame, row):
    """
    Creates all ButtonContainer objects for the chosen frame so the
    tkinter.Button object can later be created with correctly linked callback
    functions and frames

    Parameters:
        interface: gui.Application
            Object that created the window where these objects will be displayed
        frame: tkinter.Frame
            Frame where these objects will be displayed
        row: int
            Row in the scrollable region
    Returns:
        dict
            key: label description
            field: ButtonContainer
    """
    if frame == interface.frame_main:
        return {
            "new_row": ButtonContainer(interface.frame_main, "Neue Zeile",
                                       interface.add_new_row, None, 3, 0,
                                       "none 14 bold"),
            "save_bill": ButtonContainer(interface.frame_main, "Speichern",
                                         interface.save_bill, None, 3, 1,
                                         "none 14 bold"),
            "export_bills": ButtonContainer(interface.frame_main, "Export",
                                            interface.export_bills, None, 3, 2,
                                            "none 14 bold"),
        }
    elif frame == interface.frame_fields:
        return {
            "delete_row": ButtonContainer(interface.frame_fields, "Löschen",
                                          interface.delete_row, row, 24, row,
                                          "none 10 bold"),
            "save_template": ButtonContainer(interface.frame_fields,
                                             "Speichern",
                                             interface.save_template,
                                             row, 25, row, "none 10 bold")
        }
    else:
        raise SystemError


def create_combo_boxes(interface, frame, row):
    """
    Creates all ComboBoxContainer objects for the chosen frame so the
    tkinter.ttk.ComboBox object can later be created with correctly linked
    callback functions and frames

    Parameters:
        interface: gui.Application
            Object that created the window where these objects will be displayed
        frame: tkinter.Frame
            Frame where these objects will be displayed
        row: int
            Row in the scrollable region
    Returns:
        dict
            key: label description
            field: ComboBoxContainer
    """
    if frame == interface.frame_main:
        return {
            "store": ComboBoxContainer(interface.frame_main,
                                       interface.trace_store, None, "stores",
                                       "normal", 2, 2, 20, "news"),
            "payment": ComboBoxContainer(interface.frame_main,
                                         interface.trace_payment, None,
                                         "payments", "normal", 2, 3, 20, "news")
        }
    elif frame == interface.frame_fields:
        return {
            "template": ComboBoxContainer(interface.frame_fields,
                                          interface.trace_template, row,
                                          "templates", "normal", 0, row, 35,
                                          "news")
        }
    else:
        raise SystemError


def create_check_buttons(interface, frame, row):
    """
    Creates all CheckButtonContainer objects for the chosen frame so the
    tkinter.CheckButton object can later be created with correctly linked
    callback functions and frames

    Parameters:
        interface: gui.Application
            Object that created the window where these objects will be displayed
        frame: tkinter.Frame
            Frame where these objects will be displayed
        row: int
            Row in the scrollable region
    Returns:
        dict
            key: label description
            field: CheckButtonContainer
    """
    if frame == interface.frame_main:
        pass
    elif frame == interface.frame_fields:
        return {
            "minus_first": CheckButtonContainer(interface.frame_fields,
                                                "Minus zuerst", 26, row, "news")
        }
    else:
        raise SystemError
