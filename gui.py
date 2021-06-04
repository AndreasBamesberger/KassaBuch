"""
Classes to create and run the GUI
"""
import json
import os  # To check if product json files exist
import sys  # For exit()
import tkinter as tk
from tkinter import ttk  # For style and Combobox

import backend


class Line:
    """
    Creates a line in the scrollable region of the GUI. This represents one
    category of item in the bill.

    ...

    Attributes
    ----------
    buttons: dict
        All tkinter Button objects of this line
    check_buttons: dict
        All tkinter Checkbutton objects of this line
    combo_boxes: dict
        All tkinter Combobox objects of this line
    entries: dict
        All tkinter Entry objects of this line
    labels: dict
        All tkinter Label objects of this line
    row: int
        In which row of the scroll region this line is placed
    trace_vars: dict
        Dict that holds all tkinter StringVar and IntVar variables of the
        tkinter objects of this line

    Methods
    -------
    delete():
        Destroy all tkinter objects of this line
    """

    def __init__(self, row: int, labels: dict, entries: dict, buttons: dict,
                 combo_boxes: dict, check_buttons: dict, trace_vars: dict,
                 values: dict):
        self.row: int = row
        self.labels: dict = labels
        self.entries: dict = entries
        self.buttons: dict = buttons
        self.combo_boxes: dict = combo_boxes
        self.check_buttons: dict = check_buttons
        self.trace_vars: dict = trace_vars
        self.values: dict = values

    def delete(self):
        """
        Destroy all tkinter objects of this line
        """
        print("deleting row ", self.row)
        for _, field in self.labels.items():
            field.destroy()
        for _, field in self.entries.items():
            field.destroy()
        for _, field in self.buttons.items():
            field.destroy()
        for _, field in self.combo_boxes.items():
            field.destroy()
        for _, field in self.check_buttons.items():
            field.destroy()
        # TODO: also delete trace_vars?

    def __repr__(self):
        out_string = (f"Line object:\n"
                      f"\trow: {self.row}\n"
                      f"\tlabels: \n{self.labels}\n"
                      f"\tentries: \n{self.entries}\n"
                      f"\tbuttons: \n{self.buttons}\n"
                      f"\tcombo_boxes: \n{self.combo_boxes}\n"
                      f"\tcheck_buttons: \n{self.check_buttons}\n"
                      f"\ttrace_vars: \n{self.trace_vars}\n"
                      f"\tvalues: \n{self.values}\n")
        return out_string


class Application:
    """
    Creates window using tkinter and handles input/output of the created
    graphical objects

    ...

    Attributes
    ----------
    _button_list: list
        List of the parameters with which the tkinter Button objects are created
    _canvas: tkinter.Canvas
        The scrollable region
    _canvas_height: int
        Vertical resolution of the scrollable region
    _canvas_width: int
        Horizontal resolution of the scrollable region
    _check_button_list: list
        List of the parameters with which the tkinter Checkbutton objects are
        created
    _colour_frame: str
        Color of the background
    _colour_label_bg: str
        Color of the tkinter Label object background
    _colour_label_fg: str
        Color of the tkinter Label text/foreground
    _combo_box_list: list
        List of the parameters with which the tkinter Combobox objects are
        created
    _entry_list: list
        List of the parameters with which the tkinter Entry objects are created
    _font: str
        Font of the texts
    _frame_canvas: tkinter.Frame
        Frame to create the scrollable region
    _frame_dict: dict
        Dictionary that holds the available frames.
    _frame_fields: tk.Frame
        Frame that holds the lines inside the scrollable region
    _frame_main: tk.Frame
        Frame inside the main root window
    _height: int
        Vertical tkinter window resolution
    _label_list: list
        List of the parameters with which the tkinter Label objects are created
    _line_list: list
        List of all currently active Line objects in the scrollable region
    _method_dict_no_param: dict
        Dictionary that holds references to GUI methods without parameters.
        This is used to bind a method to a tkinter object
    _method_dict_one_param: dict
        Dictionary that holds references to GUI methods with 2 parameters.
        This is used to bind a method to a tkinter object
    _objects: dict
        Dictionary of all values in the tkinter_objects json
    _root: tkinter.Tk
        The main window object
    _root_objects: Line
        All tkinter objects of the root window
    _row_count: int
        Number of rows generated in the scrollable region. This value never
        decreases, even when a line is deleted
    _scaling: float
        Scaling factor of the tkinter window, for different screen resolutions
    _vsb: tkinter.Scrollbar
        Vertical tkinter Scrollbar for the scrollable region
    _width: int
        Horizontal tkinter window resolution

    Methods
    -------
    loop(self):
        This method is called by the main function, it runs the mainloop()
        method of the root window
    _setup_root_window(self):
        Configures the root window, creates all necessary tkinter objects
    _setup_canvas_window(self):
        Configures the root window, creates all necessary tkinter objects
    _reset(self):
        _row_count is reset to 0 and _line_list is emptied
    _clear_screen(self):
        All objects in the _root window are deleted and all lines inside the
        scrollable region are deleted
    _button_add_new_row(self):
        Iterate through all lists holding tkinter object information and create
        a new line in the scrollable region with the necessary objects. Then
        append this Line object to _line_list
    _button_del_row(self, row):
        Search _line_list for a Line object with Line.row = row, call its
        delete() method and remove it from _line_lists. Then, recalculate the
        bill's total price
    _button_save(self):
        Create a backend.Bill from the user input, append this Bill to
        backend.BILLS and save it to the backup csv file. Then, reset and clear
        the screen to accept a new bill
    _button_export_bills(self):
        Save the current bill, then write all bills of this session to the
        output csv and close the program
    _button_type(self):
        Saves the current bill. Then, uses the keyboard module to take control
        of the keyboard and directly types the bills into a specified program.
        Afterwards, the screen is reset to accept another bill
    _create_output(self):
        Read the user input from the tkinter objects and create a backend.Bill
        object which is then returned
    _get_product_from_line(self, line):
        Read all Entry objects of a given line in the scrollable region and save
        their information as a backend.Product object, then return it
    _button_save_template(self, row):
        Called when the "save" button in a line is pressed. Take the input of a
        line in the scrollable region, create a new product template, add it to
        the dictionary of product templates and update the json holding these
        templates
    _trace_template(self, row):
        Gets called when the StringVar of a Combobox in the scrollable region
        changes. Searches the dictionary of templates for a match with the
        user input. If a match is found, its contents are displayed in the GUI.
    _trace_store(self):
        Gets called when the StringVar of the "store" Combobox changes. Searches
        the dictionary of stores for a match with the user input. If a match is
        found, the payment method may be changed based on the dictionary entry
    _trace_payment(self):
        Gets called when the StringVar of the "payment" Combobox changes.
        Searches the payment list for a match
    _trace_update_entries(self, current_line):
        Calls all "calculate" methods for a given Line in the scrollable region.
        Then calculates the sums that are displayed in the main frame and
        changes the format of the time input
    _calculate_price_quantity(self, line):
        Calculates "price_quantity" from the "price_single" and "quantity" of
        the given Line in the scrollable region. This value is then displayed
    _calculate_discount(self, line):
        Calculates "discount" based on "quantity_discount", "sale" and
        "discount_class" of the given Line in the scrollable region. This value
        is then displayed
    _calculate_price_final(self, line):
        Calculates "price_final" based on "price_quantity", "discount",
        "quantity_discount" and "sale" of the given Line in the scrollable
        region. This value is then displayed
    _calculate_total(self):
        Add all "price_final" from all items and display the result in the main
        frame
    _create_label(self, frame_key, text, column, row, sticky, font):
        Create a tkinter Label object based on the given parameters and return
        the created object
    _create_entry(self, frame_key, column, row, width, func_key):
        Create a tkinter Entry object based on the given parameters and return
        the created object
    _create_button(self, frame_key, text, column, row, font, func_key):
        Create a tkinter Button object based on the given parameters and return
        the created object
    _create_combo_box(self, frame_key, func_key, values, state, column, row,
                      width, sticky):
        Create a tkinter Combobox object based on the given parameters and
        return the created object
    _create_check_button(self, frame_key, func_key, text, column, row, sticky):
        Create a tkinter Checkbutton object based on the given parameters and
        return the created object
    _read_entry(entry, data_type):
        Read user input from the given Entry object
    _read_label(label, data_type):
        Read user input from the given Label object
    _key_released(self, event):
        Gets called when a keyboard key is released. Based on the key, calls a
        method
    _float2str(in_float):
        Format a float value into a str. Round to 2 decimal places, replace '.'
        with ','
    """

    def __init__(self):
        # In the tkinter_objects json file the entry, button, combo_box and
        # check_button objects have a value "command" which corresponds to the
        # keys in these method dictionaries. This is used to bind method calls
        # to these tkinter objects
        self._method_dict_no_param: dict = \
            {"save_bill": self._button_save,
             "export_bills": self._button_export_bills,
             # "write_bills": self._button_type,
             "trace_store": self._trace_store,
             "trace_payment": self._trace_payment,
             "add_new_row": self._button_add_new_row}
        self._method_dict_one_param: dict = \
            {"update": self._trace_update_entries,
             "delete_row": self._button_del_row,
             "trace_template": self._trace_template,
             "save_template": self._button_save_template}

        # Store all parameters for the tkinter objects in this dictionary
        self._objects: dict = backend.read_json(
            backend.CONFIG["FILES"]["tkinter objects json"])

        # Read parameters from the config file
        self._font: str = "none " + \
                          backend.CONFIG["GRAPHICS"]["font size"] + " bold"
        self._scaling: float = backend.CONFIG["GRAPHICS"]["scaling"]
        self._width: float = backend.CONFIG["GRAPHICS"]["main width"]
        self._height: float = backend.CONFIG["GRAPHICS"]["main height"]
        self._canvas_width: float = backend.CONFIG["GRAPHICS"][
            "canvas width"]
        self._canvas_height: float = backend.CONFIG["GRAPHICS"][
            "canvas height"]

        self._colour_frame: str = backend.CONFIG["GRAPHICS"]["colour frame"]
        self._colour_label_fg: str = backend.CONFIG["GRAPHICS"][
            "colour label fg"]
        self._colour_label_bg: str = backend.CONFIG["GRAPHICS"][
            "colour label bg"]

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

        # Split up the _objects dict into the different object types
        try:
            self._label_list = self._objects["label_list"]
            self._entry_list = self._objects["entry_list"]
            self._button_list = self._objects["button_list"]
            self._combo_box_list = self._objects["combo_box_list"]
            self._check_button_list = self._objects["check_button_list"]
        except KeyError:
            print("Error while reading tkinter objects from file")
            raise SystemError

        # Create the different frames and canvasses
        # All this is done so that _vsb can scroll the _canvas
        self._frame_main = tk.Frame(self._root, bg=self._colour_frame)
        self._frame_canvas = tk.Frame(self._frame_main)
        self._canvas = tk.Canvas(self._frame_canvas, bg=self._colour_frame)
        self._frame_fields = tk.Frame(self._canvas, bg=self._colour_frame)
        # Create the scrollbar
        self._vsb = tk.Scrollbar(self._frame_canvas, orient="vertical",
                                 command=self._canvas.yview)

        # In the tkinter_objects json file all objects have a value "frame"
        # which corresponds to the keys in these method dictionaries. This is
        # used to declare the target tkinter frame in the json file
        self._frame_dict = {"frame_fields": self._frame_fields,
                            "frame_main": self._frame_main}

        self._setup_root_window()
        self._setup_canvas_window()

        # Create an initial item row so the scrollable region is not empty at
        # program start
        self._button_add_new_row()

        # User input starts with date so the cursor is set there
        self._root_objects.entries["date"].focus_set()

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
        self._root.geometry(str(self._width) + 'x' + str(self._height))
        self._root.tk.call('tk', 'scaling', self._scaling)
        self._root.title("Kassabuch")
        self._root.configure(background=self._colour_frame)

        self._root_objects = self._create_line("frame_main", -1)

    def _setup_canvas_window(self):
        """
        Configures the root window, creates all necessary tkinter objects
        """
        self._frame_main.grid(sticky="news")

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

        # Create the _frame_fields (where the rows will be placed) inside
        # _canvas
        self._canvas.create_window((0, 0), window=self._frame_fields,
                                   anchor="nw")

        # # Update frames idle tasks to let tkinter calculate tkinter object
        # sizes
        self._frame_fields.update_idletasks()

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
        # Clear the text of all Label objects that display information of the
        # current bill
        for key, field in self._root_objects.labels.items():
            if key.endswith("_var"):
                field.config(text='')

        # TODO: do these actually need to be deleted?
        for key, field in self._root_objects.entries.items():
            if key == "date":
                continue
            field.delete(0, "end")

        # TODO: do these actually need to be deleted?
        for _, field in self._root_objects.combo_boxes.items():
            field.delete(0, "end")

        for line in self._line_list:
            line.delete()

    def _button_add_new_row(self):
        """
        Iterate through all lists holding tkinter object information and create
        a new line in the scrollable region with the necessary objects. Then
        append this Line object to _line_list
        """
        print("_button_add_new_row")
        line = self._create_line("frame_fields", self._row_count)
        self._line_list.append(line)

        self._root.update()

        # Set the canvas scrolling region
        self._canvas.config(scrollregion=self._canvas.bbox("all"))

        self._row_count += 1
        print("self._row_count = ", self._row_count)

        # Scroll down so the new line is visible
        self._canvas.yview_scroll(2, "units")

    def _button_del_row(self, row):
        """
        Search _line_list for a Line object with Line.row = row, call its
        delete() method and remove it from _line_lists. Then, recalculate the
        bill's total price

        Parameters:
            row: int
                The index of the row that will be deleted
        """
        print("_button_del_row")
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

    def _button_save(self):
        """
        Create a backend.Bill from the user input, append this Bill to
        backend.BILLS and save it to the backup csv file. Then, reset and clear
        the screen to accept a new bill
        """
        print("_button_save")
        # Update all fields
        for line in self._line_list:
            self._trace_update_entries(line)
        bill = self._create_output()

        # Don't save an empty bill
        if bill.products:
            backend.BILLS.append(bill)
            backend.backup_bill(bill)

        self._clear_screen()
        self._reset()

        # Don't leave the scrollable region empty
        self._button_add_new_row()

        # Set cursor focus to time
        self._root_objects.entries["time"].focus_set()

    def _button_export_bills(self):
        """
        Save the current bill, then write all bills of this session to the
        output csv and close the program
        """
        print("_button_export_bills")
        self._button_save()
        backend.export_bills()
        sys.exit()

    # def _button_type(self):
    #     """
    #     Saves the current bill. Then, uses the keyboard module to take control
    #     of the keyboard and directly types the bills into a specified program.
    #     Afterwards, the screen is reset to accept another bill
    #     """
    #     print("_button_type")
    #     self._button_save()
    #
    #     # keyboard.write_to_program()
    #
    #     self._clear_screen()
    #     self._reset()
    #
    #     # Don't leave the scrollable region empty
    #     self._button_add_new_row()

    def _create_output(self):
        """
        Read the user input from the tkinter objects and create a backend.Bill
        object which is then returned

        Returns:
            bill: backend.Bill
                The Bill object created from user input
        """
        store = self._read_entry(self._root_objects.combo_boxes["store"], "str")

        # TODO: As soon as message windows are a thing, make one to ask the user
        #  for default payment string
        if store not in backend.STORES and store != '':
            backend.STORES.update({store: {"default_payment": ''}})
            backend.update_stores()

        payment = self._read_entry(self._root_objects.combo_boxes["payment"],
                                   "str")

        # If payment method is new, store it and update the payments json
        if payment not in backend.PAYMENTS and payment != '':
            backend.PAYMENTS.append(payment)
            backend.update_payments()

        date: str = self._read_entry(self._root_objects.entries["date"], "str")

        time: str = self._read_entry(self._root_objects.entries["time"], "str")
        # Time is written with '-' as a separator because it's easier to type in
        # on the numpad
        try:
            hours, minutes = time.split(':')
            # If user wrote hours or minutes as one digit, add the leading zero
            if len(hours) == 1:
                hours = '0' + hours
            if len(minutes) == 1:
                minutes = '0' + minutes
            time = hours + ':' + minutes
        except ValueError:
            # If user did not enter time
            time = "00:00"

        discount_sum = self._read_label(self._root_objects.
                                        labels["discount_sum_var"], "float")
        quantity_discount_sum = self._read_label(
            self._root_objects.labels["quantity_discount_sum_var"], "float")
        sale_sum = self._read_label(self._root_objects.labels["sale_sum_var"],
                                    "float")
        total = self._read_label(self._root_objects.labels["total_var"],
                                 "float")
        price_quantity_sum = 0.0

        # Date user input is dd-mm
        # Transform it into yyyy-mm-dd
        try:
            day, month = date.split('-')
        except ValueError:
            day = "00"
            month = "00"

        # If user wrote day or month as one digit, add the leading zero
        if len(day) == 1:
            day = '0' + day
        if len(month) == 1:
            month = '0' + month

        date = backend.CONFIG["DEFAULT"]["year"] + '-' + month + '-' + day

        # Get the item data from _line_list
        # TODO: combine this and the next for-loop
        product_list = list()
        for line in self._line_list:
            product = self._get_product_from_line(line, False)
            # Skip empty line
            if product.name == '' and product.price_final == 0:
                continue

            product_list.append(product)

        for product in product_list:
            # Skip empty line
            if not product.name and not product.quantity and \
                    not product.price_final:
                continue
            # TODO: don't do this formatting here, do this only in the
            #  backend.format_bill
            # Quantity = 1 should not be shown in final excel file
            if float(product.quantity) == 1:
                product.quantity = ''
            else:
                product.quantity = float(product.quantity)

            price_quantity_sum += product.price_quantity

            if backend.CONFIG["DEFAULT"]["save_history"]:
                # update product history with this purchase
                date_time = date + 'T' + time
                # price_per_unit includes discounts
                price_per_unit = 0
                if isinstance(product.quantity, str) or product.quantity == 0:
                    # if quantity is '' then it is 1
                    price_per_unit = product.price_final
                elif isinstance(product.quantity, float):
                    price_per_unit = product.price_final / product.quantity
                price_per_unit = round(price_per_unit, 2)
                # product.history.append([date_time, store, price_per_unit])
                product.history.append({
                    "date_time": date_time,
                    "store": store,
                    "payment": payment,
                    "price_single": product.price_single,
                    "quantity": product.quantity,
                    "price_quantity": product.price_quantity,
                    "discount_class": product.discount_class,
                    "quantity_discount": product.quantity_discount,
                    "sale": product.sale,
                    "discount": product.discount,
                    "price_final": product.price_final,
                    "price_final_per_unit": price_per_unit
                })

            backend.TEMPLATES.update({product.name: product})

            backend.update_product_history(product)

        price_quantity_sum = round(price_quantity_sum, 2)

        bill = backend.Bill(products=product_list, date=date, time=time,
                            store=store, payment=payment, total=total,
                            discount_sum=discount_sum,
                            quantity_discount_sum=quantity_discount_sum,
                            sale_sum=sale_sum,
                            price_quantity_sum=price_quantity_sum)
        print("bill = ", bill)

        return bill

    def _get_product_from_line(self, line, new_product):
        """
        Read all Entry objects of a given line in the scrollable region and save
        their information as a backend.Entry object, then return it

        Parameters:
            line: Line
                The Line object from which information will be read
            new_product: bool
                If true, the product has not yet been saved as a json file

        Returns:
            product: backend.Product
                Information of all tkinter Entry objects of the given line

        """
        # TODO: make a list or something through which we can loop to reduce
        #  repetition
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

        identifier = -1

        # Get history from backend.TEMPLATES
        if new_product:
            history = []
            display = True
            notes = ''
        else:
            if name == '':
                history = []
                display = True
                notes = ''
            else:
                if name in backend.TEMPLATES:
                    history = backend.TEMPLATES[name].history
                    display = backend.TEMPLATES[name].display
                    notes = backend.TEMPLATES[name].notes
                else:
                    # If the product is new and has not been saved as a new
                    # template
                    history = []
                    display = True
                    notes = ''

        # Search backend.TEMPLATES for this product and give it the correct
        # identifier. If it is a new product, give it an identifier that has not
        # yet been used
        new_product = True
        for key, field in backend.TEMPLATES.items():
            if name == key:
                identifier = field.identifier
                new_product = False
                break
        if new_product:
            # Get all used identifier numbers, sort them, create a new one that
            # is one higher
            used_identifiers = [field.identifier
                                for _, field in backend.TEMPLATES.items()]
            used_identifiers = sorted(used_identifiers)
            new_identifier = used_identifiers[-1] + 1
            # To be safe, check if the new identifier hasn't been used so far
            for _, field in backend.TEMPLATES.items():
                if new_identifier == field.identifier:
                    raise SystemError
            identifier = new_identifier

        product = backend.Product(name=name,
                                  price_single=price_single,
                                  quantity=quantity,
                                  discount_class=discount_class,
                                  product_class=product_class,
                                  unknown=unknown,
                                  price_quantity=price_quantity,
                                  discount=discount,
                                  quantity_discount=quantity_discount,
                                  sale=sale,
                                  price_final=price_final,
                                  history=history,
                                  identifier=identifier,
                                  display=display,
                                  notes=notes)
        return product

    # TODO: use Line instead of row
    def _button_save_template(self, row):
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

        print("_button_save_template")
        # Search for the Line object with the correct row number
        curr_line = None
        for line in self._line_list:
            if line.row == row:
                curr_line = line
                break
        if not curr_line:
            raise SystemError

        product = self._get_product_from_line(curr_line, True)

        # Delete trailing whitespaces from product name
        product.name = product.name.rstrip()

        if product.name == '':
            return
        if product.quantity == 0:
            product.quantity = 1

        # # German format, decimal sign is comma
        # product.price_single = str(product.price_single).replace('.', ',')
        # product.quantity = str(product.quantity).replace('.', ',')

        # If template already exists, delete the old product
        try:
            backend.TEMPLATES.pop(product.name)
        except KeyError:
            pass

        # Add new template to dictionary
        backend.TEMPLATES.update({product.name: product})

        # Update the product json file or create a new one
        backend.update_product_json(product)

        # Alphabetically sort the list that is passed to the Combobox
        name_list = sorted([key for key, _ in backend.TEMPLATES.items()])

        # Update all Comboboxes so they show this new template
        for line in self._line_list:
            line.combo_boxes["template"]["values"] = name_list

        # TODO: why is this here?
        self._root_objects.combo_boxes["store"]["values"] = sorted(backend.
                                                                   STORES)

        # Compare current values in line with template to change button colour
        # back to normal
        self._compare_line_to_file(curr_line)

    def _trace_template(self, row):
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
        curr_line.combo_boxes["template"]["values"] = name_list

        # If no matches, clear all values in this row
        if len(temp_dict) == 0:
            template_name = self._read_entry(curr_line.combo_boxes["template"],
                                             "str")
            curr_line.entries["name"].delete(0, "end")
            curr_line.entries["name"].insert(0, template_name)
            curr_line.entries["price_single"].delete(0, "end")
            curr_line.entries["sale"].delete(0, "end")
            curr_line.entries["quantity"].delete(0, "end")
            curr_line.entries["discount_class"].delete(0, "end")
            curr_line.entries["product_class"].delete(0, "end")
            curr_line.entries["unknown"].delete(0, "end")
            curr_line.entries["price_quantity"].delete(0, "end")
            curr_line.entries["discount"].delete(0, "end")
            curr_line.entries["quantity_discount"].delete(0, "end")
            curr_line.entries["price_final"].delete(0, "end")

        # If 1 match, display the template values in the current row
        elif len(temp_dict) == 1:
            product = None
            curr_temp = None
            for key, field in temp_dict.items():
                product = key
                curr_temp = field

            curr_line.entries["name"].delete(0, "end")
            curr_line.entries["name"].insert(0, product)
            curr_line.entries["price_single"].delete(0, "end")
            curr_line.entries["price_single"].insert(0, curr_temp.price_single)
            # curr_line.entries["sale"].delete(0, "end")
            # curr_line.entries["sale"].insert(0, curr_temp.sale)
            curr_line.entries["quantity"].delete(0, "end")
            curr_line.entries["quantity"].insert(0, curr_temp.quantity)
            # curr_line.entries["discount_class"].delete(0, "end")
            # curr_line.entries["discount_class"].insert(0,
            #                                            curr_temp.discount_class)
            curr_line.entries["product_class"].delete(0, "end")
            curr_line.entries["product_class"].insert(0,
                                                      curr_temp.product_class)
            curr_line.entries["unknown"].delete(0, "end")
            curr_line.entries["unknown"].insert(0, curr_temp.unknown)
            # curr_line.entries["price_quantity"].delete(0, "end")
            # curr_line.entries["price_quantity"].insert(0,
            #                                            curr_temp.price_quantity)
            # curr_line.entries["discount"].delete(0, "end")
            # curr_line.entries["discount"].insert(0, curr_temp.discount)
            # curr_line.entries["quantity_discount"].delete(0, "end")
            # curr_line.entries["quantity_discount"]. \
            #     insert(0, curr_temp.quantity_discount)
            # curr_line.entries["price_final"].delete(0, "end")
            # curr_line.entries["price_final"].insert(0, curr_temp.price_final)

        # If there are multiple matches, there are 2 options
        else:
            # If one match doesn't just contain the user input but is equal to
            # it, treat it like a single match occurred
            for key, field in temp_dict.items():
                if template_input == key.lower():
                    product = key
                    curr_temp = field

                    curr_line.entries["name"].delete(0, "end")
                    curr_line.entries["name"].insert(0, product)
                    curr_line.entries["price_single"].delete(0, "end")
                    curr_line.entries["price_single"]. \
                        insert(0, curr_temp.price_single)
                    # curr_line.entries["sale"].delete(0, "end")
                    # curr_line.entries["sale"].insert(0, curr_temp.sale)
                    curr_line.entries["quantity"].delete(0, "end")
                    curr_line.entries["quantity"].insert(0, curr_temp.quantity)
                    # curr_line.entries["discount_class"].delete(0, "end")
                    # curr_line.entries["discount_class"]. \
                    #     insert(0, curr_temp.discount_class)
                    curr_line.entries["product_class"].delete(0, "end")
                    curr_line.entries["product_class"]. \
                        insert(0, curr_temp.product_class)
                    curr_line.entries["unknown"].delete(0, "end")
                    curr_line.entries["unknown"].insert(0, curr_temp.unknown)
                    # curr_line.entries["price_quantity"].delete(0, "end")
                    # curr_line.entries["price_quantity"]. \
                    #     insert(0, curr_temp.price_quantity)
                    # curr_line.entries["discount"].delete(0, "end")
                    # curr_line.entries["discount"].insert(0,
                    #                                      curr_temp.discount)
                    # curr_line.entries["quantity_discount"].delete(0, "end")
                    # curr_line.entries["quantity_discount"]. \
                    #     insert(0, curr_temp.quantity_discount)
                    # curr_line.entries["price_final"].delete(0, "end")
                    # curr_line.entries["price_final"]. \
                    #     insert(0, curr_temp.price_final)
                    break
                # If there are multiple matches and no exact match, treat it
                # like no match occurred
                else:
                    curr_line.entries["name"].delete(0, "end")
                    curr_line.entries["price_single"].delete(0, "end")
                    curr_line.entries["sale"].delete(0, "end")
                    curr_line.entries["quantity"].delete(0, "end")
                    curr_line.entries["discount_class"].delete(0, "end")
                    curr_line.entries["product_class"].delete(0, "end")
                    curr_line.entries["unknown"].delete(0, "end")
                    curr_line.entries["price_quantity"].delete(0, "end")
                    curr_line.entries["discount"].delete(0, "end")
                    curr_line.entries["quantity_discount"].delete(0, "end")
                    curr_line.entries["price_final"].delete(0, "end")

    def _trace_store(self):
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
        self._root_objects.combo_boxes["store"]["values"] = store_list

        print("STORES: ", backend.STORES)
        if len(store_list) == 0:
            self._root_objects.combo_boxes["payment"].set('')
        # if store is Billa, Billa Plus or Merkur: change payment to Karte
        if len(store_list) == 1:
            # Set text in Combobox to matching store
            self._root_objects.trace_vars["store"].set(store_list[0])
            payment = backend.STORES[store_list[0]]["default_payment"]
            print("payment: ", payment)
            # if store_list[0] in ["Billa", "Billa Plus", "Merkur"]:
            self._root_objects.combo_boxes["payment"].set(payment)
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
                    self._root_objects.combo_boxes["payment"].set('')

    def _trace_payment(self):
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
        self._root_objects.combo_boxes["payment"]["values"] = payment_list

    def _trace_update_entries(self, curr_line):
        """
        Calls all "calculate" methods for a given Line in the scrollable region.
        Then calculates the sums that are displayed in the main frame and
        changes the format of the time input

        Parameters:
            curr_line: Line
                Which Line object should be calculated
        """
        print("_trace_update_entries")

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

        self._root_objects.labels["discount_sum_var"].config(text=discount_sum)
        self._root_objects.labels["quantity_discount_sum_var"]. \
            config(text=quantity_discount_sum)
        self._root_objects.labels["sale_sum_var"].config(text=sale_sum)

        # TODO: integrate this into the loop above
        price_quantity_sum = 0.0
        for line in self._line_list:
            price_quantity_sum += self._read_entry(
                line.entries["price_quantity"], "float")
        price_quantity_sum = self._float2str(price_quantity_sum)
        self._root_objects.labels["price_quantity_sum_var"]. \
            config(text=price_quantity_sum)

        # in "time" label, replace '-' with ':'
        time = self._read_entry(self._root_objects.entries["time"], "str")
        time = time.replace('-', ':')
        self._root_objects.entries["time"].delete(0, "end")
        self._root_objects.entries["time"].insert(0, time)

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
        line_name = line.entries["name"].get().rstrip()
        if not line_name:
            return
        if line_name not in backend.PRODUCT_KEYS:
            self._change_button_colour(line.buttons["save_template"], "red")
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

            # Get default background colour from entry list
            bg_ps = ''
            bg_q = ''
            bg_pc = ''
            bg_u = ''
            for _, dict_key, _, _, _, _, background, _ in self._entry_list:
                if dict_key == "price_single":
                    bg_ps = background
                elif dict_key == "quantity":
                    bg_q = background
                elif dict_key == "product_class":
                    bg_pc = background
                elif dict_key == "unknown":
                    bg_u = background

            if eq_ps:
                self._change_entry_colour(line.entries["price_single"], "gold")
            else:
                self._change_entry_colour(line.entries["price_single"], bg_ps)

            if eq_q:
                self._change_entry_colour(line.entries["quantity"], "gold")
            else:
                self._change_entry_colour(line.entries["quantity"], bg_q)

            if eq_pc:
                self._change_entry_colour(line.entries["product_class"], "gold")
            else:
                self._change_entry_colour(line.entries["product_class"], bg_pc)

            if eq_u:
                self._change_entry_colour(line.entries["unknown"], "gold")
            else:
                self._change_entry_colour(line.entries["unknown"], bg_u)

            if eq_ps or eq_q or eq_pc or eq_u:
                self._change_button_colour(line.buttons["save_template"],
                                           "gold")
            else:
                self._change_button_colour(line.buttons["save_template"],
                                           "white")

        else:
            self._change_button_colour(line.buttons["save_template"], "red")

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
        # price_single = self._read_entry(line.entries["price_single"], "float")
        # quantity = self._read_entry(line.entries["quantity"], "float")
        #
        # if not quantity:
        #     quantity = 1
        #
        price_single = line.values["price_single"]
        quantity = line.values["quantity"]
        price_quantity = round(price_single * quantity, 2)
        line.values.update({"price_quantity": price_quantity})

        # # German format, decimal sign is comma
        # price_quantity = str(price_quantity).replace('.', ',')

        line.entries["price_quantity"].delete(0, "end")
        line.entries["price_quantity"].insert(0, price_quantity)

    def _calculate_discount(self, line):
        """
        Calculates "discount" based on "quantity_discount", "sale" and
        "discount_class" of the given Line in the scrollable region. This value
        is then displayed

        Parameters:
            line: Line
                Which Line object should be calculated
        """
        print("_calculate_discount")
        # price_quantity = self._read_entry(line.entries["price_quantity"],
        #                                   "float")
        #
        # discount_class = self._read_entry(line.entries["discount_class"],
        # "str")
        # # discount_class = discount_class.replace(',', '.')
        #
        # Search the DISCOUNT_CLASSES dict for an entry matching the user input
        # for key, field in backend.DISCOUNT_CLASSES.items():
        #     if discount_class == key:
        #         discount_class = field["discount"]
        #         break
        #
        # # If no match was found, try to convert the user input to a float.
        # # If it fails, set it to 0
        # if not isinstance(discount_class, float):
        #     try:
        #         discount_class = float(discount_class)
        #     except ValueError:
        #         discount_class = 0.0
        #
        # print("discount_class: ", discount_class)
        #
        # sale = self._read_entry(line.entries["sale"], "float")
        #
        # quantity_discount = self._read_entry(line.entries
        #                                      ["quantity_discount"], "float")

        # For some items, first quantity_discount and sale are subtracted from
        # the price and then the result is multiplied with the discount_class
        # (minus_first = True).
        # For other items, multiplication is the first step
        # (minus_first = False)

        sale = line.values["sale"]
        quantity_discount = line.values["quantity_discount"]
        price_quantity = line.values["price_quantity"]
        discount_class = line.values["discount_class"]

        minus_first = self._read_entry(
            line.trace_vars["discount_check_button"], "float")

        if minus_first:
            discount = sale + quantity_discount + price_quantity
            discount *= discount_class / 100
        else:
            discount = price_quantity * discount_class / 100

        # TODO: change this into 1 line
        discount *= -1
        discount = round(discount, 2)

        line.values.update({"discount": discount})

        # # German format, decimal sign is comma
        # discount = str(discount).replace('.', ',')

        line.entries["discount"].delete(0, "end")
        line.entries["discount"].insert(0, discount)

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

        # price_quantity = self._read_entry(line.entries["price_quantity"],
        #                                   "float")
        #
        # discount = self._read_entry(line.entries["discount"], "float")
        # sale = self._read_entry(line.entries["sale"], "float")
        #
        # quantity_discount = self._read_entry(line.entries
        # ["quantity_discount"], "float")
        price_quantity = line.values["price_quantity"]
        discount = line.values["discount"]
        quantity_discount = line.values["quantity_discount"]
        sale = line.values["sale"]
        price_final = price_quantity + discount + quantity_discount + sale
        price_final = round(price_final, 2)
        line.values.update({"price_final": price_final})

        # # German format, decimal sign is comma
        # price_final = str(price_final).replace('.', ',')

        line.entries["price_final"].delete(0, "end")
        line.entries["price_final"].insert(0, price_final)

    def _calculate_total(self):
        """
        Add all "price_final" from all items and display the result in the main
        frame
        """
        print("_calculate_total")
        total = 0.0
        for line in self._line_list:
            # TODO: turn this into 1 line
            # price_final = self._read_entry(line.entries["price_final"],
            # "float")

            # If there is a row where calculation has not yet happened
            try:
                price_final = line.values["price_final"]
            except KeyError:
                return

            total += price_final

        total = self._float2str(total)
        self._root_objects.labels["total_var"].config(text=total)

    def _create_label(self, frame_key, text, column, row, sticky, font):
        """
        Create a tkinter Label object based on the given parameters and return
        the created object

        Parameters:
            frame_key:str
                Key for the _frame_dict dictionary
            text: str
                Text to be displayed in this Label
            column: int
                Horizontal position value for the grid system
            row: int
                Vertical position value for the grid system
            sticky: str
                In which direction should the created object stick to the grid.
                Combination of letters 'n', 'e', 's', 'w'
            font: str
                Font of the text to be displayed in this Label

        Returns:
            temp: tkinter.Label
                The created Label object
        """
        frame = self._frame_dict[frame_key]
        temp = tk.Label(frame, text=text, bg=self._colour_label_bg,
                        fg=self._colour_label_fg,
                        font=font)
        temp.grid(row=row, column=column, sticky=sticky)
        return temp

    # TODO: change func_key into method_key everywhere
    def _create_entry(self, frame_key, column, row: int, width, func_key, bg,
                      fg):
        """
        Create a tkinter Entry object based on the given parameters and return
        the created object

        Parameters:
            frame_key:str
                Key for the _frame_dict dictionary
            column: int
                Horizontal position value for the grid system
            row: int
                Vertical position value for the grid system
            width: int
                Horizontal size of the object
            func_key: str
                Key for the _method_dict_one_param and _method_dict_on_param
                dictionaries
            bg: str
                Background colour
            fg: str
                Text colour

        Returns:
            temp: tkinter.Label
                The created Label object
            trace_var: tkinter.StringVar
                Variable that traces user input in this object and calls the
                command function
        """
        frame = self._frame_dict[frame_key]

        # If the user has specified a method to be executed, search both method
        # dictionaries for a matching entry and define a function that calls the
        # method with the correct parameter
        if func_key != '':
            def command(*_):
                if func_key in self._method_dict_one_param.keys():
                    self._method_dict_one_param[func_key](row)
                else:
                    self._method_dict_no_param[func_key]()

            trace_var = tk.StringVar()
            trace_var.set('')
            trace_var.trace('w', command)
        else:
            trace_var = None

        temp = tk.Entry(frame, textvariable=trace_var, width=width, bg=bg,
                        fg=fg)
        temp.grid(row=row, column=column, sticky=tk.W)
        return temp, trace_var

    @staticmethod
    def _change_entry_colour(entry, colour):
        entry.configure(bg=colour)

    def _create_button(self, frame_key, text, column, row: int, font, func_key):
        """
        Create a tkinter Button object based on the given parameters and return
        the created object

        Parameters:
            frame_key:str
                Key for the _frame_dict dictionary
            text: str
                Text to be displayed in this Button
            column: int
                Horizontal position value for the grid system
            row: int
                Vertical position value for the grid system
            font: str
                Font of the text to be displayed in this Button
            func_key: str
                Key for the _method_dict_one_param and _method_dict_on_param
                dictionaries

        Returns:
            temp: tkinter.Button
                The created Button object
        """
        frame = self._frame_dict[frame_key]

        # Search both method dictionaries for a matching entry and define a
        # function that calls the method with the correct parameter
        def command():
            if func_key in self._method_dict_one_param.keys():
                self._method_dict_one_param[func_key](row)
            else:
                self._method_dict_no_param[func_key]()

        temp = tk.Button(frame, text=text, width=len(text), command=command,
                         font=font)
        temp.grid(row=row, column=column, sticky="news")
        return temp

    @staticmethod
    def _change_button_colour(button, colour):
        button.config(bg=colour)

    def _create_combo_box(self, frame_key, func_key, values, state, column, row,
                          width, sticky):
        """
        Create a tkinter Combobox object based on the given parameters and
        return the created object

        Parameters:
            frame_key:str
                Key for the _frame_dict dictionary
            func_key: str
                Key for the _method_dict_one_param and _method_dict_on_param
                dictionaries
            values: str
                What kind of information the dropdown menu should display
            state: str
                Behaviour of the Combobox, e.g. readonly
            column: int
                Horizontal position value for the grid system
            row: int
                Vertical position value for the grid system
            width: int
                Horizontal size of the object
            sticky: str
                In which direction should the created object stick to the grid.
                Combination of letters 'n', 'e', 's', 'w'

        Returns:
            temp: tkinter.ttk.Combobox
                The created Combobox object
            trace_var: tkinter.StringVar
                Variable that traces user input in this object and calls the
                command function
        """
        frame = self._frame_dict[frame_key]

        # If the user has specified a method to be executed, search both method
        # dictionaries for a matching entry and define a function that calls the
        # method with the correct parameter
        if func_key:
            def command(*_):
                if func_key in self._method_dict_one_param.keys():
                    self._method_dict_one_param[func_key](row)
                else:
                    self._method_dict_no_param[func_key]()

            trace_var = tk.StringVar()
            trace_var.set('')
            trace_var.trace('w', command)
        else:
            trace_var = ''

        temp = ttk.Combobox(frame, width=width, textvariable=trace_var)
        box_list = None

        # Connect the values of the Combobox to a list of values
        if values == "templates":
            # Only show products that user wants displayed
            box_list = sorted([key for key, field in backend.TEMPLATES.items()
                               if field.display])
        if values == "stores":
            box_list = sorted(backend.STORES)
        if values == "payments":
            box_list = sorted(backend.PAYMENTS)
        temp["values"] = box_list
        temp["state"] = state
        temp.grid(row=row, column=column, sticky=sticky)
        return temp, trace_var

    def _create_check_button(self, frame_key, func_key, text, column, row,
                             sticky):
        """
        Create a tkinter Checkbutton object based on the given parameters and
        return the created object

        Parameters:
            frame_key:str
                Key for the _frame_dict dictionary
            func_key: str
                Key for the _method_dict_one_param and _method_dict_on_param
                dictionaries
            text: str
                Text to be displayed in this Button
            column: int
                Horizontal position value for the grid system
            row: int
                Vertical position value for the grid system
            sticky: str
                In which direction should the created object stick to the grid.
                Combination of letters 'n', 'e', 's', 'w'

        Returns:
            temp: tkinter.Checkbutton
                The created Checkbutton object
            trace_var: tkinter.IntVar
                Variable that traces user input in this object
        """
        frame = self._frame_dict[frame_key]
        trace_var = tk.IntVar()
        trace_var.set(1)  # requested to be on by default

        # TODO: change command from "" to update all
        # Search both method dictionaries for a matching entry and define a
        # function that calls the method with the correct parameter
        def command():
            if func_key in self._method_dict_one_param.keys():
                self._method_dict_one_param[func_key](row)
            elif func_key in self._method_dict_no_param.keys():
                self._method_dict_no_param[func_key]()

        check_box = tk.Checkbutton(frame, text=text, variable=trace_var,
                                   onvalue=1, offvalue=0, command=command)
        check_box.grid(row=row, column=column, sticky=sticky)

        return check_box, trace_var

    # TODO: split into 2 methods entry2str and entry2float
    @staticmethod
    def _read_entry(entry, data_type):
        """
        Read user input from the given Entry object

        Parameters:
            entry: tkinter.Entry
                Entry object to read text from
            data_type: str
                What data type should be returned
        Returns:
            value: float or str
                Text of the Entry object,
        """
        value = entry.get()
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
        Read user input from the given Label object

        Parameters:
            label: tkinter.Label
                Label object to read text from
            data_type: str
                What data type should be returned
        Returns:
            value: float or str
                Text of the Label object,
        """
        value = label["text"]
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
                self._trace_update_entries(line)
            self._button_add_new_row()
            self._line_list[-1].combo_boxes["template"].focus_set()
        # F2: Create a new Line object in the scrollable region and move the
        #     cursor to its Combobox
        elif event.keysym == "F2":
            self._button_add_new_row()
            self._line_list[-1].combo_boxes["template"].focus_set()
        # F3: Move the cursor to the "date" Entry field
        elif event.keysym == "F3":
            self._root_objects.entries["date"].focus_set()
        # F4: Move the cursor to the Combobox of the Line at the very bottom of
        #     the scrollable region
        elif event.keysym == "F4":
            self._line_list[-1].combo_boxes["template"].focus_set()
        # F5: Calculate all
        elif event.keysym == "F5":
            for line in self._line_list:
                self._trace_update_entries(line)
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
                            self._root_objects.combo_boxes["store"],
                            "str")
                        if store in backend.STORES:
                            discount_class = backend.STORES[store][
                                "default_discount_class"]
                        else:
                            return
                        line.entries["discount_class"].delete(0, "end")
                        line.entries["discount_class"].insert(0, discount_class)
                    else:
                        line.entries["discount_class"].delete(0, "end")

            for line in self._line_list:
                self._trace_update_entries(line)

    def _get_active_row(self):
        """
        Return the row where the cursor is currently at from the active entry
        box or combo box
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

    def _create_line(self, frame_key_choice, line_row):
        """

        """
        trace_vars: dict = {}

        entries: dict = {}
        for frame_key, dict_key, func_key, column, row, width, bg, fg in \
                self._entry_list:
            if frame_key == frame_key_choice:
                if row == "":
                    row = line_row
                entry, trace_var_entry = self._create_entry(frame_key, column,
                                                            row, width,
                                                            func_key, bg, fg)
                entries.update({dict_key: entry})
                trace_vars.update({dict_key: trace_var_entry})

        labels: dict = {}
        for frame_key, dict_key, text, column, row, sticky, font in \
                self._label_list:
            if frame_key == frame_key_choice:
                if row == "":
                    row = line_row
                label = self._create_label(frame_key, text, column, row, sticky,
                                           font)
                labels.update({dict_key: label})

        combo_boxes: dict = {}
        for frame_key, dict_key, func_key, values, state, column, row, width, \
                sticky in self._combo_box_list:
            if frame_key == frame_key_choice:
                if row == "":
                    row = line_row
                combo_box, trace_var_combo_box = self._create_combo_box(
                    frame_key, func_key, values, state, column, row, width,
                    sticky)
                trace_vars.update({dict_key: trace_var_combo_box})
                combo_boxes.update({dict_key: combo_box})

        buttons: dict = {}
        for frame_key, dict_key, text, func_key, column, row, font in \
                self._button_list:
            if frame_key == frame_key_choice:
                if row == "":
                    row = line_row
                button = self._create_button(frame_key, text, column, row, font,
                                             func_key)
                buttons.update({dict_key: button})

        check_buttons: dict = {}
        for frame_key, dict_key, func_key, text, column, sticky in \
                self._check_button_list:
            if frame_key == frame_key_choice:
                check_button, trace_var_check_button = \
                    self._create_check_button(frame_key, func_key, text, column,
                                              line_row, sticky)
                check_buttons.update({dict_key: check_button})
                trace_vars.update({dict_key: trace_var_check_button})

        # Create a Line object which stores all created tkinter objects
        return Line(line_row, labels, entries, buttons, combo_boxes,
                    check_buttons, trace_vars, {})
