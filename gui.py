"""
Classes to create and run the GUI
"""
import json
import os  # To check if product json files exist
import sys  # For exit()
import tkinter as tk
from tkinter import ttk  # For style and Combobox

import backend
import tkinter_objects as tko


class Line:
    """
    Creates a line in the scrollable region of the GUI. This represents one
    category of item in the bill.

    ...

    Attributes
    ----------
    buttons: dict
        All tkinter ButtonContainer objects of this line
    check_buttons: dict
        All tkinter Checkbutton objects of this line
    combo_boxes: dict
        All tkinter Combobox objects of this line
    entries: dict
        All tkinter EntryContainer objects of this line
    frame: tkinter.Frame
        Frame where this Line should be displayed
    interface: Application
        Object that created the window
    labels: dict
        All tkinter LabelContainer objects of this line
    row: int
        In which row of the scroll region this line is placed
    values: dict
        Dictionary holding user input in this Line

    Methods
    -------
    delete(self):
        Destroy all tkinter objects of this line
    """

    def __init__(self, interface, frame, row: int, labels: dict, entries: dict,
                 buttons: dict, combo_boxes: dict, check_buttons: dict):
        self.interface = interface
        self.frame = frame
        self.row: int = row
        self.labels: dict = labels
        self.entries: dict = entries
        self.buttons: dict = buttons
        self.combo_boxes: dict = combo_boxes
        self.check_buttons: dict = check_buttons
        self.values = dict()

        def labels():
            if self.labels:
                for key, field in self.labels.items():
                    field.create()

        def entries():
            if self.entries:
                for key, field in self.entries.items():
                    field.create()

        def buttons():
            if self.buttons:
                for key, field in self.buttons.items():
                    field.create()

        def combo_boxes():
            if self.combo_boxes:
                for key, field in self.combo_boxes.items():
                    field.create()

        def check_buttons():
            if self.check_buttons:
                for key, field in self.check_buttons.items():
                    field.create()

        if self.frame == self.interface.frame_main:
            labels()
            entries()
            combo_boxes()
            buttons()
            check_buttons()
        elif self.frame == self.interface.frame_fields:
            labels()
            combo_boxes()
            entries()
            buttons()
            check_buttons()
        else:
            raise SystemError

    def delete(self):
        """
        Destroy all tkinter objects of this line
        """
        print("deleting row ", self.row)
        if self.labels:
            for _, field in self.labels.items():
                field.object.destroy()
        if self.entries:
            for _, field in self.entries.items():
                field.object.destroy()
        if self.buttons:
            for _, field in self.buttons.items():
                field.object.destroy()
        if self.combo_boxes:
            for _, field in self.combo_boxes.items():
                field.object.destroy()
        if self.check_buttons:
            for _, field in self.check_buttons.items():
                field.object.destroy()

    def __repr__(self):
        out_string = (f"Line object:\n"
                      f"\trow: {self.row}\n"
                      f"\tlabels: \n{self.labels}\n"
                      f"\tentries: \n{self.entries}\n"
                      f"\tbuttons: \n{self.buttons}\n"
                      f"\tcombo_boxes: \n{self.combo_boxes}\n"
                      f"\tcheck_buttons: \n{self.check_buttons}\n"
                      f"\tvalues: \n{self.values}\n")
        return out_string


class Application:
    """
    Creates window using tkinter and handles input/output of the created
    graphical objects

    ...

    Attributes
    ----------
    _canvas: tkinter.Canvas
        The scrollable region
    _canvas_height: int
        Vertical resolution of the scrollable region
    _canvas_width: int
        Horizontal resolution of the scrollable region
    _colour_frame: str
        Color of the background
    _frame_canvas: tkinter.Frame
        Frame to create the scrollable region
    _line_list: list
        List of all currently active Line objects in the scrollable region
    _root: tkinter.Tk
        The main window object
    _root_height: int
        Vertical tkinter window resolution
    _root_objects: Line
        All tkinter objects of the root window
    _root_width: int
        Horizontal tkinter window resolution
    _row_count: int
        Number of rows generated in the scrollable region. This value never
        decreases, even when a line is deleted
    _scaling: float
        Scaling factor of the tkinter window, for different screen resolutions
    _vsb: tkinter.Scrollbar
        Vertical tkinter Scrollbar for the scrollable region
    frame_fields: tkinter.Frame
        Frame that holds the lines inside the scrollable region
    frame_main: tkinter.Frame
        Frame inside the main root window

    Methods
    -------
    _calculate_discount(self, line):
        Calculates "discount" based on "quantity_discount", "sale" and
        "discount_class" of the given Line in the scrollable region. This value
        is then displayed
    _calculate_price_final(self, line):
        Calculates "price_final" based on "price_quantity", "discount",
        "quantity_discount" and "sale" of the given Line in the scrollable
        region. This value is then displayed
    _calculate_price_quantity(self, line):
        Calculates "price_quantity" from the "price_single" and "quantity" of
        the given Line in the scrollable region. This value is then displayed
    _calculate_total(self):
        Add all "price_final" from all items and display the result in the main
        frame
    _clear_screen(self):
        All objects in the _root window are deleted and all lines inside the
        scrollable region are deleted
    _compare_line_to_file(self, line):
        Compare fields in line with corresponding values in product json.
        If there is a difference, change the colour of the "save" button
    _create_line(self, frame, row):
        Look through all lists of tkinter objects, if they have the correct
        frame_key, create them and store them in a Line object.
    _float2str(in_float):
        Format a float value into a str. Round to 2 decimal places, replace '.'
        with ','
    _get_active_row(self):
        Return the row where the cursor is currently at from the active entry
        box or combo box
    _key_release(self, event):
        Gets called when a keyboard key is released. Based on the key, calls a
        method
    _read_entry(entry, data_type):
        Read user input from the given EntryContainer object
    _read_label(label, data_type):
        Read user input from the given LabelContainer object
    _read_line_values(self, line):
        Read price_single, quantity, discount_class, quantity_discount and sale
        and store them in a dict
    _read_product_from_line(self, line, new_product):
        Read all EntryContainer objects of a given line in the scrollable region
        and save their information as a backend.EntryContainer object, then
        return it
    _reset(self):
        _row_count is reset to 0 and _line_list is emptied
    _setup_canvas_window(self):
        Configures the root window, creates all necessary tkinter objects
    _setup_root_window(self):
        Configures the root window, creates all necessary tkinter objects
    add_new_row(self):
        Iterate through all lists holding tkinter object information and create
        a new line in the scrollable region with the necessary objects. Then
        append this Line object to _line_list
    delete_row(self):
        Search _line_list for a Line object with Line.row = row, call its
        delete() method and remove it from _line_lists. Then, recalculate the
        bill's total price
    export_bills(self):
        Save the current bill, then write all bills of this session to the
        output csv and close the program
    loop(self):
        This method is called by the main function, it runs the mainloop()
        method of the root window
    save_bill(self):
        Read all the user input, call backend.create_bill to turn it into a Bill
        object and save it as a csv file. Afterwards, the screen is reset.
    save_template(self, row):
        Called when the "save" button in a line is pressed. Take the input of a
        line in the scrollable region, create a new product template, add it to
        the dictionary of product templates and update the json holding these
        templates
    trace_payment(self):
        Gets called when the StringVar of the "payment" Combobox changes.
        Searches the payment list for a match
    trace_store(self):
        Gets called when the StringVar of the "store" Combobox changes. Searches
        the dictionary of stores for a match with the user input. If a match is
        found, the payment method may be changed based on the dictionary entry
    trace_template(self, row):
        Gets called when the StringVar of a Combobox in the scrollable region
        changes. Searches the dictionary of templates for a match with the
        user input. If a match is found, its contents are displayed in the GUI.
    trace_update_entries(self, curr_line):
        Calls all "calculate" methods for a given Line in the scrollable region.
        Then calculates the sums that are displayed in the main frame and
        changes the format of the time input
    """

    def __init__(self):
        self._scaling: float = backend.CONFIG["GRAPHICS"]["scaling"]
        self._root_width: float = backend.CONFIG["GRAPHICS"]["main width"]
        self._root_height: float = backend.CONFIG["GRAPHICS"]["main height"]
        self._canvas_width: float = backend.CONFIG["GRAPHICS"][
            "canvas width"]
        self._canvas_height: float = backend.CONFIG["GRAPHICS"][
            "canvas height"]
        self._colour_frame: str = backend.CONFIG["GRAPHICS"]["colour frame"]

        self._row_count: int = 0
        self._line_list: list = []

        # Create root window
        self._root = tk.Tk()
        style = ttk.Style(self._root)
        # Background and foreground are never visible so flashy colours are
        # chosen to highlight an error
        style.configure("TFrame", background="red", foreground="blue")

        # Bind all key releases to a callback method
        self._root.bind_all('<KeyRelease>', self._key_release)

        # Create the different frames and canvasses
        # All this is done so that _vsb can scroll the _canvas
        self.frame_main = tk.Frame(self._root, bg=self._colour_frame)
        self._frame_canvas = tk.Frame(self.frame_main)
        self._canvas = tk.Canvas(self._frame_canvas, bg=self._colour_frame)
        self.frame_fields = tk.Frame(self._canvas, bg=self._colour_frame)
        # Create the scrollbar
        self._vsb = tk.Scrollbar(self._frame_canvas, orient="vertical",
                                 command=self._canvas.yview)

        self._setup_root_window()
        self._setup_canvas_window()

        # Create an initial item row so the scrollable region is not empty at
        # program start
        self.add_new_row()

        # User input starts with date so the cursor is set there
        self._root_objects.entries["date"].object.focus_set()

    def loop(self):
        """
        This method is called by the main function, it runs the mainloop()
        method of the root window
        """
        self._root.mainloop()

    def _setup_root_window(self):
        """
        Configures the root window, creates all necessary tkinter objects
        """
        # The geometry() method needs a string like "800x600"
        self._root.geometry(str(self._root_width) + 'x' +
                            str(self._root_height))
        self._root.tk.call('tk', 'scaling', self._scaling)
        self._root.title("Kassabuch")
        self._root.configure(background=self._colour_frame)

        self._root_objects = self._create_line(self.frame_main, -1)

    def _setup_canvas_window(self):
        """
        Configures the root window, creates all necessary tkinter objects
        """
        self.frame_main.grid(sticky="news")

        # Place _frame_canvas inside the _root grid
        self._frame_canvas.grid(row=9, column=0, padx=(0, 0), pady=(5, 5),
                                sticky='nw')

        self._frame_canvas.grid_rowconfigure(0, weight=1)
        self._frame_canvas.grid_columnconfigure(0, weight=1)
        self._frame_canvas.grid_propagate(False)

        # Place _canvas inside the grid of _frame_canvas
        self._canvas.grid(row=0, column=0, sticky="news")

        # Place _vsb inside the grid of _frame_canvas, right of _canvas
        self._vsb.grid(row=0, column=1, sticky="ns")
        # Link _vsb to _canvas scrolling
        self._canvas.configure(yscrollcommand=self._vsb.set)

        # Create the frame_fields (where the rows will be placed) inside
        # _canvas
        self._canvas.create_window((0, 0), window=self.frame_fields,
                                   anchor="nw")

        # # Update frames idle tasks to let tkinter calculate tkinter object
        # sizes
        self.frame_fields.update_idletasks()

        self._frame_canvas.config(width=self._canvas_width,
                                  height=self._canvas_height)

        # Set the _canvas scrolling region
        self._canvas.config(scrollregion=self._canvas.bbox("all"))

    def _reset(self):
        """
        _row_count is reset to 0 and _line_list is emptied
        """
        self._row_count = 0
        self._line_list = list()

    def _clear_screen(self):
        """
        All objects in the _root window are deleted and all lines inside the
        scrollable region are deleted
        """
        # Clear the text of all LabelContainer objects that display information
        # of the current bill
        for key, field in self._root_objects.labels.items():
            if key.endswith("_var"):
                field.object.config(text='')

        # TODO: do these actually need to be deleted?
        for key, field in self._root_objects.entries.items():
            if key == "date":
                continue
            field.object.delete(0, "end")

        # TODO: do these actually need to be deleted?
        for _, field in self._root_objects.combo_boxes.items():
            field.object.delete(0, "end")

        for line in self._line_list:
            line.delete()

    def add_new_row(self):
        """
        Iterate through all lists holding tkinter object information and create
        a new line in the scrollable region with the necessary objects. Then
        append this Line object to _line_list
        """
        print("add_new_row")
        line = self._create_line(self.frame_fields, self._row_count)
        self._line_list.append(line)

        self._root.update()

        # Set the canvas scrolling region
        self._canvas.config(scrollregion=self._canvas.bbox("all"))

        self._row_count += 1
        print("self._row_count = ", self._row_count)

        # Scroll down so the new line is visible
        self._canvas.yview_scroll(2, "units")

    def delete_row(self, row):
        """
        Search _line_list for a Line object with Line.row = row, call its
        delete() method and remove it from _line_lists. Then, recalculate the
        bill's total price

        Parameters:
            row: int
                The index of the row that will be deleted
        """
        print("delete_row")
        for index, line in enumerate(self._line_list):
            if line.row == row:
                line.delete()
                self._line_list.pop(index)
                break
        print("self._row_count = ", self._row_count)
        self._calculate_total()

        self._root.update()
        # Set the canvas scrolling region again
        self._canvas.config(scrollregion=self._canvas.bbox("all"))

    def save_bill(self):
        """
        Read all the user input, call backend.create_bill to turn it into a Bill
        object and save it as a csv file. Afterwards, the screen is reset.
        """
        print("save_bill")
        # Update all fields
        for line in self._line_list:
            self.trace_update_entries(line)

        store = self._read_entry(self._root_objects.combo_boxes["store"], "str")
        payment = self._read_entry(self._root_objects.combo_boxes["payment"],
                                   "str")
        date: str = self._read_entry(self._root_objects.entries["date"], "str")

        time: str = self._read_entry(self._root_objects.entries["time"], "str")
        discount_sum = self._read_label(self._root_objects.
                                        labels["discount_sum_var"], "float")
        quantity_discount_sum = self._read_label(
            self._root_objects.labels["quantity_discount_sum_var"], "float")
        sale_sum = self._read_label(self._root_objects.labels["sale_sum_var"],
                                    "float")
        total = self._read_label(self._root_objects.labels["total_var"],
                                 "float")

        product_list = list()
        for line in self._line_list:
            product = self._read_product_from_line(line, False)
            # Skip empty line
            if product.name == '' and product.price_final == 0:
                continue

            product_list.append(product)

        user_input = {"store": store,
                      "payment": payment,
                      "date": date,
                      "time": time,
                      "discount_sum": discount_sum,
                      "quantity_discount_sum": quantity_discount_sum,
                      "sale_sum": sale_sum,
                      "total": total,
                      "product_list": product_list}

        backend.create_bill(user_input)

        self._clear_screen()
        self._reset()

        # Don't leave the scrollable region empty
        self.add_new_row()

        # Set cursor focus to time
        self._root_objects.entries["time"].object.focus_set()

    def export_bills(self):
        """
        Save the current bill, then write all bills of this session to the
        output csv and close the program
        """
        print("export_bills")
        self.save_bill()
        backend.export_bills()
        sys.exit()

    def _read_product_from_line(self, line, new_product):
        """
        Read all EntryContainer objects of a given line in the scrollable region
        and save their information as a backend.EntryContainer object, then
        return it

        Parameters:
            line: Line
                The Line object from which information will be read
            new_product: bool
                If true, the product has not yet been saved as a json file

        Returns:
            product: backend.Product
                Information of all tkinter EntryContainer objects of the given
                line
        """
        name = self._read_entry(line.entries["name"], "str").rstrip()
        price_single = self._read_entry(line.entries["price_single"], "float")
        quantity = self._read_entry(line.entries["quantity"], "float")
        discount_class = self._read_entry(line.entries["discount_class"], "str")
        product_class = self._read_entry(line.entries["product_class"], "str")
        unknown = self._read_entry(line.entries["unknown"], "str")
        price_quantity = self._read_entry(line.entries["price_quantity"],
                                          "float")
        discount = self._read_entry(line.entries["discount"], "float")
        quantity_discount = self._read_entry(line.entries["quantity_discount"],
                                             "float")
        sale = self._read_entry(line.entries["sale"], "float")
        price_final = self._read_entry(line.entries["price_final"], "float")

        user_input = {"name": name,
                      "price_single": price_single,
                      "quantity": quantity,
                      "discount_class": discount_class,
                      "product_class": product_class,
                      "unknown": unknown,
                      "price_quantity": price_quantity,
                      "discount": discount,
                      "quantity_discount": quantity_discount,
                      "sale": sale,
                      "price_final": price_final}

        return backend.create_product(user_input, new_product)

    def save_template(self, row):
        """
        Called when the "save" button in a line is pressed. Take the input of a
        line in the scrollable region, create a new product template, add it to
        the dictionary of product templates and update the json holding these
        templates

        Parameters:
            row: int
                Which row in the scrollable region should be saved as a new
                product template
        """

        print("save_template")
        # Search for the Line object with the correct row number
        curr_line = None
        for line in self._line_list:
            if line.row == row:
                curr_line = line
                break
        if not curr_line:
            raise SystemError

        product = self._read_product_from_line(curr_line, True)
        backend.create_template(product)

        # Alphabetically sort the list that is passed to the Combobox
        name_list = sorted([key for key, _ in backend.TEMPLATES.items()])

        # Update all Comboboxes so they show this new template
        for line in self._line_list:
            line.combo_boxes["template"].object["values"] = name_list

        # TODO: why is this here?
        self._root_objects.combo_boxes["store"].object["values"] = \
            sorted(backend. STORES)

        # Compare current values in line with template to change button colour
        # back to normal
        self._compare_line_to_file(curr_line)

    def trace_template(self, row):
        """
        Gets called when the StringVar of a Combobox in the scrollable region
        changes. Searches the dictionary of templates for a match with the
        user input. If a match is found, its contents are displayed in the GUI.

        Parameters:
            row: int
                The user input of the Combobox in this row should be compared to
                the product template dictionary
        """
        # Search for the Line object with the correct row number
        curr_line = None
        for index, line in enumerate(self._line_list):
            if line.row == row:
                curr_line = self._line_list[index]
                break

        if curr_line is None:
            raise SystemError

        # Read user input from the Combobox
        template_input = self._read_entry(curr_line.combo_boxes["template"],
                                          "str").lower()

        temp_dict = dict()
        if backend.CONFIG["DEFAULT"]["regex"]:
            # Treat the user input as regex pattern and find matching product
            # names
            temp_dict = backend.regex_search(template_input)
        else:
            # Add all template entries who contain the user input
            for key, field in backend.TEMPLATES.items():
                if template_input in key.lower():
                    temp_dict.update({key: field})

        print("len(temp_dict): ", len(temp_dict))

        # Show the matching entries in the dropdown of the current Combobox
        name_list = sorted([key for key, field in temp_dict.items()
                            if field.display])
        curr_line.combo_boxes["template"].object["values"] = name_list

        # If no matches, clear all values in this row
        if len(temp_dict) == 0:
            template_name = self._read_entry(curr_line.combo_boxes["template"],
                                             "str")
            curr_line.entries["name"].object.delete(0, "end")
            curr_line.entries["name"].object.insert(0, template_name)
            curr_line.entries["price_single"].object.delete(0, "end")
            curr_line.entries["sale"].object.delete(0, "end")
            curr_line.entries["quantity"].object.delete(0, "end")
            curr_line.entries["discount_class"].object.delete(0, "end")
            curr_line.entries["product_class"].object.delete(0, "end")
            curr_line.entries["unknown"].object.delete(0, "end")
            curr_line.entries["price_quantity"].object.delete(0, "end")
            curr_line.entries["discount"].object.delete(0, "end")
            curr_line.entries["quantity_discount"].object.delete(0, "end")
            curr_line.entries["price_final"].object.delete(0, "end")

        # If 1 match, display the template values in the current row
        elif len(temp_dict) == 1:
            product = None
            curr_temp = None
            for key, field in temp_dict.items():
                product = key
                curr_temp = field

            curr_line.entries["name"].object.delete(0, "end")
            curr_line.entries["name"].object.insert(0, product)
            curr_line.entries["price_single"].object.delete(0, "end")
            curr_line.entries["price_single"].object.\
                insert(0, curr_temp.price_single)
            curr_line.entries["quantity"].object.delete(0, "end")
            curr_line.entries["quantity"].object.insert(0, curr_temp.quantity)
            curr_line.entries["product_class"].object.delete(0, "end")
            curr_line.entries["product_class"].object.\
                insert(0, curr_temp.product_class)
            curr_line.entries["unknown"].object.delete(0, "end")
            curr_line.entries["unknown"].object.insert(0, curr_temp.unknown)

        # If there are multiple matches, there are 2 options
        else:
            # If one match doesn't just contain the user input but is equal to
            # it, treat it like a single match occurred
            for key, field in temp_dict.items():
                if template_input == key.lower():
                    product = key
                    curr_temp = field

                    curr_line.entries["name"].object.delete(0, "end")
                    curr_line.entries["name"].object.insert(0, product)
                    curr_line.entries["price_single"].object.delete(0, "end")
                    curr_line.entries["price_single"].object. \
                        insert(0, curr_temp.price_single)
                    curr_line.entries["quantity"].object.delete(0, "end")
                    curr_line.entries["quantity"].object.\
                        insert(0, curr_temp.quantity)
                    curr_line.entries["product_class"].object.delete(0, "end")
                    curr_line.entries["product_class"].object. \
                        insert(0, curr_temp.product_class)
                    curr_line.entries["unknown"].object.delete(0, "end")
                    curr_line.entries["unknown"].object.\
                        insert(0, curr_temp.unknown)
                    break
                # If there are multiple matches and no exact match, treat it
                # like no match occurred
                else:
                    curr_line.entries["name"].object.delete(0, "end")
                    curr_line.entries["price_single"].object.delete(0, "end")
                    curr_line.entries["sale"].object.delete(0, "end")
                    curr_line.entries["quantity"].object.delete(0, "end")
                    curr_line.entries["discount_class"].object.delete(0, "end")
                    curr_line.entries["product_class"].object.delete(0, "end")
                    curr_line.entries["unknown"].object.delete(0, "end")
                    curr_line.entries["price_quantity"].object.delete(0, "end")
                    curr_line.entries["discount"].object.delete(0, "end")
                    curr_line.entries["quantity_discount"].object.delete(0,
                                                                         "end")
                    curr_line.entries["price_final"].object.delete(0, "end")

    def trace_store(self):
        """
        Gets called when the StringVar of the "store" Combobox changes. Searches
        the dictionary of stores for a match with the user input. If a match is
        found, the payment method may be changed based on the dictionary entry
        """
        # Read user input from store Combobox
        store_input = self._read_entry(self._root_objects.combo_boxes["store"],
                                       "str").lower()

        # Find matching entries in the stores dictionary
        store_list = list()
        for key in backend.STORES:
            if store_input in key.lower():
                store_list.append(key)

        store_list.sort()

        print("Matching stores: ", store_list)

        # Show the matching entries in the dropdown of the current Combobox
        self._root_objects.combo_boxes["store"].object["values"] = store_list

        print("STORES: ", backend.STORES)
        if len(store_list) == 0:
            self._root_objects.combo_boxes["payment"].object.set('')
        # if store is Billa, Billa Plus or Merkur: change payment to Karte
        if len(store_list) == 1:
            # Set text in Combobox to matching store
            # self._root_objects.trace_vars["store"].object.set(store_list[0])
            self._root_objects.combo_boxes["store"].trace_var.set(store_list[0])
            payment = backend.STORES[store_list[0]]["default_payment"]
            print("payment: ", payment)
            # if store_list[0] in ["Billa", "Billa Plus", "Merkur"]:
            self._root_objects.combo_boxes["payment"].object.set(payment)
        # special case for Billa: if "Billa" is typed in,
        # it still matches "Billa" and "Billa Plus"
        else:
            for key, field in backend.STORES.items():
                if store_input == key.lower():
                    # Set text in Combobox to matching store
                    self._root_objects.trace_vars["store"].set(key)
                    payment = field["default_payment"]
                    print("payment: ", payment)
                    self._root_objects.combo_boxes["payment"].set(payment)
                    break
                else:
                    self._root_objects.combo_boxes["payment"].object.set('')

    def trace_payment(self):
        """
        Gets called when the StringVar of the "payment" Combobox changes.
        Searches the payment list for a match
        """
        # Read user input from the Combobox
        payment_input = self._read_entry(
            self._root_objects.combo_boxes["payment"], "str").lower()

        # Find all matching payment methods
        payment_list = list()
        for payment in backend.PAYMENTS:
            if payment_input in payment.lower():
                payment_list.append(payment)

        payment_list.sort()
        print("Payment methods: ", payment_list)
        self._root_objects.combo_boxes["payment"].object["values"] = \
            payment_list

    def trace_update_entries(self, curr_line):
        """
        Calls all "calculate" methods for a given Line in the scrollable region.
        Then calculates the sums that are displayed in the main frame and
        changes the format of the time input

        Parameters:
            curr_line: Line
                Which Line object should be calculated
        """
        print("trace_update_entries")

        self._read_line_values(curr_line)
        self._calculate_price_quantity(curr_line)
        self._calculate_discount(curr_line)
        self._calculate_price_final(curr_line)
        self._compare_line_to_file(curr_line)
        self._calculate_total()

        # Add values of "price_quantity", "discount", "quantity_discount" and
        # "sale" from all Line objects in the scrollable region
        discount_sum = 0.0
        quantity_discount_sum = 0.0
        sale_sum = 0.0

        for line in self._line_list:
            discount_sum += self._read_entry(line.entries["discount"], "float")
            quantity_discount_sum += self._read_entry(line.entries
                                                      ["quantity_discount"],
                                                      "float")
            sale_sum += self._read_entry(line.entries["sale"], "float")

        # Display the calculated values in the root window
        discount_sum = self._float2str(discount_sum)
        quantity_discount_sum = self._float2str(quantity_discount_sum)
        sale_sum = self._float2str(sale_sum)

        self._root_objects.labels["discount_sum_var"].object.\
            config(text=discount_sum)
        self._root_objects.labels["quantity_discount_sum_var"].object.\
            config(text=quantity_discount_sum)
        self._root_objects.labels["sale_sum_var"].object.config(text=sale_sum)

        # TODO: integrate this into the loop above
        price_quantity_sum = 0.0
        for line in self._line_list:
            price_quantity_sum += self._read_entry(
                line.entries["price_quantity"], "float")
        price_quantity_sum = self._float2str(price_quantity_sum)
        self._root_objects.labels["price_quantity_sum_var"].object.\
            config(text=price_quantity_sum)

        # in "time" label, replace '-' with ':'
        time = self._read_entry(self._root_objects.entries["time"], "str")
        time = time.replace('-', ':')
        self._root_objects.entries["time"].object.delete(0, "end")
        self._root_objects.entries["time"].object.insert(0, time)

    def _compare_line_to_file(self, line):
        """
        Compare fields in line with corresponding values in product json.
        If there is a difference, change the colour of the "save" button

        Parameters:
            line: Line
                The current Line object holding the values of the current line
        """
        print("_compare_line_to_template")
        # Get product identifier
        line_name = line.entries["name"].object.get().rstrip()
        if not line_name:
            return
        if line_name not in backend.PRODUCT_KEYS:
            # self._change_button_colour(line.buttons["save_template"], "red")
            line.buttons["save_template"].change_bg("red")
            return

        identifier = backend.PRODUCT_KEYS[line_name]
        print("line_name: ", line_name)
        filename = identifier + ".json"
        path = backend.CONFIG["FOLDERS"]["product folder"]
        encoding = backend.CONFIG["DEFAULT"]["encoding"]
        if line.values == {}:
            return
        if os.path.isfile(path + filename):
            with open(path + filename, 'r', encoding=encoding) as in_file:
                data = json.load(in_file)
            template_price_single = data["default_price_per_unit"]
            template_quantity = data["default_quantity"]
            if template_quantity == 0:
                template_quantity = 1
            template_product_class = data["product_class"]
            template_unknown = data["unknown"]

            line_price_single = line.values["price_single"]
            line_quantity = line.values["quantity"]
            line_product_class = self._read_entry(line.entries["product_class"],
                                                  "str")
            line_unknown = self._read_entry(line.entries["unknown"], "str")

            eq_ps = not (template_price_single == line_price_single)
            eq_q = not (template_quantity == line_quantity)
            eq_pc = not (template_product_class == line_product_class)
            eq_u = not (template_unknown == line_unknown)

            if eq_ps:
                line.entries["price_single"].change_bg("gold")
            else:
                default_colour = line.entries["price_single"].bg
                line.entries["price_single"].change_bg(default_colour)

            if eq_q:
                line.entries["quantity"].change_bg("gold")
            else:
                default_colour = line.entries["quantity"].bg
                line.entries["quantity"].change_bg(default_colour)

            if eq_pc:
                line.entries["product_class"].change_bg("gold")
            else:
                default_colour = line.entries["product_class"].bg
                line.entries["product_class"].change_bg(default_colour)

            if eq_u:
                line.entries["unknown"].change_bg("gold")
            else:
                default_colour = line.entries["unknown"].bg
                line.entries["unknown"].change_bg(default_colour)

            if eq_ps or eq_q or eq_pc or eq_u:
                line.buttons["save_template"].change_bg("gold")
            else:
                default_colour = line.buttons["save_template"].bg
                line.buttons["save_template"].change_bg(default_colour)

        else:
            line.buttons["save_template"].change_bg("red")

    def _read_line_values(self, line):
        """
        Read price_single, quantity, discount_class, quantity_discount and sale
        and store them in a dict
        """
        price_single = self._read_entry(line.entries["price_single"], "float")
        quantity = self._read_entry(line.entries["quantity"], "float")

        if not quantity:
            quantity = 1

        discount_class = self._read_entry(line.entries["discount_class"], "str")
        discount_class = discount_class.replace(',', '.')

        # Search the DISCOUNT_CLASSES dict for an entry matching the user input
        for key, field in backend.DISCOUNT_CLASSES.items():
            if discount_class == key:
                discount_class = field["discount"]
                break

        # If no match was found, try to convert the user input to a float.
        # If it fails, set it to 0
        if not isinstance(discount_class, float):
            try:
                discount_class = float(discount_class)
            except ValueError:
                discount_class = 0.0

        print("discount_class: ", discount_class)

        sale = self._read_entry(line.entries["sale"], "float")

        quantity_discount = self._read_entry(line.entries["quantity_discount"],
                                             "float")

        line.values.update({"price_single": price_single,
                            "quantity": quantity,
                            "discount_class": discount_class,
                            "sale": sale,
                            "quantity_discount": quantity_discount})

    @staticmethod
    def _calculate_price_quantity(line):
        """
        Calculates "price_quantity" from the "price_single" and "quantity" of
        the given Line in the scrollable region. This value is then displayed

        Parameters:
            line: Line
                Which Line object should be calculated
        """
        print("_calculate_price_quantity")
        price_single = line.values["price_single"]
        quantity = line.values["quantity"]
        price_quantity = round(price_single * quantity, 2)
        line.values.update({"price_quantity": price_quantity})

        line.entries["price_quantity"].object.delete(0, "end")
        line.entries["price_quantity"].object.insert(0, price_quantity)

    @staticmethod
    def _calculate_discount(line):
        """
        Calculates "discount" based on "quantity_discount", "sale" and
        "discount_class" of the given Line in the scrollable region. This value
        is then displayed

        Parameters:
            line: Line
                Which Line object should be calculated
        """
        print("_calculate_discount")

        sale = line.values["sale"]
        quantity_discount = line.values["quantity_discount"]
        price_quantity = line.values["price_quantity"]
        discount_class = line.values["discount_class"]
        minus_first = line.check_buttons["minus_first"].trace_var.get()

        if minus_first:
            discount = sale + quantity_discount + price_quantity
            discount *= discount_class / 100
        else:
            discount = price_quantity * discount_class / 100

        # TODO: change this into 1 line
        discount *= -1
        discount = round(discount, 2)

        line.values.update({"discount": discount})

        line.entries["discount"].object.delete(0, "end")
        line.entries["discount"].object.insert(0, discount)

    @staticmethod
    def _calculate_price_final(line):
        """
        Calculates "price_final" based on "price_quantity", "discount",
        "quantity_discount" and "sale" of the given Line in the scrollable
        region. This value is then displayed

        Parameters:
            line: Line
                Which Line object should be calculated
        """
        print("_calculate_price_final")
        price_quantity = line.values["price_quantity"]
        discount = line.values["discount"]
        quantity_discount = line.values["quantity_discount"]
        sale = line.values["sale"]
        price_final = price_quantity + discount + quantity_discount + sale
        price_final = round(price_final, 2)
        line.values.update({"price_final": price_final})

        line.entries["price_final"].object.delete(0, "end")
        line.entries["price_final"].object.insert(0, price_final)

    def _calculate_total(self):
        """
        Add all "price_final" from all items and display the result in the main
        frame
        """
        print("_calculate_total")
        total = 0.0
        for line in self._line_list:
            # If there is a row where calculation has not yet happened
            try:
                price_final = line.values["price_final"]
            except KeyError:
                return

            total += price_final

        total = self._float2str(total)
        self._root_objects.labels["total_var"].object.config(text=total)

    # TODO: split into 2 methods entry2str and entry2float
    @staticmethod
    def _read_entry(entry, data_type):
        """
        Read user input from the given EntryContainer object

        Parameters:
            entry: tkinter.EntryContainer
                EntryContainer object to read text from
            data_type: str
                What data type should be returned
        Returns:
            value: float or str
                Text of the EntryContainer object,
        """
        value = entry.object.get()
        if data_type == "str":
            return value
        elif data_type == "float":
            if isinstance(value, str):
                # German format, decimal sign is comma
                value = value.replace(',', '.')
            try:
                value = float(value)
            except ValueError:
                value = 0.0
            return value

    @staticmethod
    def _read_label(label, data_type):
        """
        Read user input from the given LabelContainer object

        Parameters:
            label: tkinter.LabelContainer
                LabelContainer object to read text from
            data_type: str
                What data type should be returned
        Returns:
            value: float or str
                Text of the LabelContainer object,
        """
        value = label.object["text"]
        if data_type == "str":
            return value
        elif data_type == "float":
            if isinstance(value, str):
                # German format, decimal sign is comma
                value = value.replace(',', '.')
            try:
                value = float(value)
            except ValueError:
                value = 0.0
            return value

    def _key_release(self, event):
        """
        Gets called when a keyboard key is released. Based on the key, calls a
        method

        Parameters:
            event: tkinter.Event
                Event triggered by a key release
        """
        # F1: Calculate all, create a new Line object in the scrollable region
        #     and move the cursor to its Combobox
        if event.keysym == "F1":
            for line in self._line_list:
                self.trace_update_entries(line)
            self.add_new_row()
            self._line_list[-1].combo_boxes["template"].object.focus_set()
        # F2: Create a new Line object in the scrollable region and move the
        #     cursor to its Combobox
        elif event.keysym == "F2":
            self.add_new_row()
            self._line_list[-1].combo_boxes["template"].object.focus_set()
        # F3: Move the cursor to the "date" EntryContainer field
        elif event.keysym == "F3":
            self._root_objects.entries["date"].object.focus_set()
        # F4: Move the cursor to the Combobox of the Line at the very bottom of
        #     the scrollable region
        elif event.keysym == "F4":
            self._line_list[-1].combo_boxes["template"].object.focus_set()
        # F5: Calculate all
        elif event.keysym == "F5":
            for line in self._line_list:
                self.trace_update_entries(line)
        # F6: Insert default discount class into active row
        #     If a discount value is already present, delete it
        elif event.keysym == "F6":
            active_row = self._get_active_row()
            print("active row: ", active_row)

            for line in self._line_list:
                if line.row == active_row:
                    # Get current discount class input
                    curr_discount_class = self._read_entry(
                        line.entries["discount_class"], "str")

                    if curr_discount_class == "":
                        store = self._read_entry(
                            self._root_objects.combo_boxes["store"].object,
                            "str")
                        if store in backend.STORES:
                            discount_class = backend.STORES[store][
                                "default_discount_class"]
                        else:
                            return
                        line.entries["discount_class"].object.delete(0, "end")
                        line.entries["discount_class"].object.\
                            insert(0, discount_class)
                    else:
                        line.entries["discount_class"].object.delete(0, "end")

            for line in self._line_list:
                self.trace_update_entries(line)

    def _get_active_row(self):
        """
        Return the row where the cursor is currently at from the active entry
        box or combo box

        Returns:
            row: int
                Row value of the active tkinter widget
        """
        current_focus = str(self._root.focus_get())
        if "entry" in current_focus:
            # Iterate through all line objects and compare entry IDs with the
            # current focus
            for line in self._line_list:
                for key, field in line.entries.items():
                    if str(field) == current_focus:
                        print("active object: ", key, field)
                        return line.row

        elif "combobox" in current_focus:
            # Iterate through all line objects and compare combobox IDs with the
            # current focus
            for line in self._line_list:
                for key, field in line.combo_boxes.items():
                    if str(field) == current_focus:
                        print("active object: ", key, field)
                        return line.row

        return -1

    @staticmethod
    def _float2str(in_float):
        """
        Format a float value into a str. Round to 2 decimal places, replace '.'
        with ','

        Parameters:
            in_float: float
                Float value to be formatted
        Returns:
            out_str: str
                Formatted float
        """
        in_float = round(in_float, 2)
        in_float = f'{in_float:.2f}'
        # out_str = str(in_float).replace('.', ',')
        out_str = str(in_float)
        return out_str

    def _create_line(self, frame, row):
        """
        Look through all lists of tkinter objects, if they have the correct
        frame_key, create them and store them in a Line object.

        Parameters:
            frame: tkinter.Frame
                Frame where the Line will be created
            row: int
                In which row is the new Line object
        Returns:
            line:Line
                The created Line object
        """
        labels: dict = tko.create_labels(self, frame)
        entries: dict = tko.create_entries(self, frame, row)
        buttons: dict = tko.create_buttons(self, frame, row)
        combo_boxes: dict = tko.create_combo_boxes(self, frame, row)
        check_buttons: dict = tko.create_check_buttons(self, frame, row)

        line = Line(self, frame, row, labels, entries, buttons, combo_boxes,
                    check_buttons)
        return line
