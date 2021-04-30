"""
Classes to create and run the GUI
"""
import sys  # For exit()
import tkinter as tk
from tkinter import ttk  # For style and combo_box

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
                 combo_boxes: dict, check_buttons: dict, trace_vars: dict):
        self.row: int = row
        self.labels: dict = labels
        self.entries: dict = entries
        self.buttons: dict = buttons
        self.combo_boxes: dict = combo_boxes
        self.check_buttons: dict = check_buttons
        self.trace_vars: dict = trace_vars

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
                      f"\tcheck_buttons: \n{self.check_buttons}")
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
    _color_frame: str
        Color of the background
    _color_label_bg: str
        Color of the tkinter Label object background
    _color_label_fg: str
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
    # TODO: don't forget to update this
    loop(self):
    _setup_root_window(self):
    _setup_canvas_window(self):
    _reset(self):
    _clear_screen(self):
    _button_add_new_row(self):
    _button_del_row(self, row):
    _button_save(self):
    _button_export_bills(self):
    _button_type(self):
    _create_output(self):
    _get_entry_from_line(self, line):
    _button_save_template(self, row):
    _trace_template(self, row):
    _trace_store(self):
    _trace_payment(self):
    _trace_update_entries(self, current_line):
    _calculate_price_quantity(self, line):
    _calculate_discount(self, line):
    _calculate_price_final(self, line):
    _calculate_total(self):
    _create_label(self, frame_key, text, column, row, sticky, font):
    _create_entry(self, frame_key, column, row, width, func_key):
    _create_button(self, frame_key, text, column, row, font, func_key):
    _create_combo_box(self, frame_key, func_key, values, state, column, row,
                      width, sticky):
    _create_check_button(self, frame_key, func_key, text, column, row, sticky):
    _read_entry(entry, data_type):
    _read_label(label, data_type):
    _key_released(self, event):
    _float2str(in_float):





    loop():
        gets executed by main.py
    _setup_root_window():
        configures the root window, creates tkinter objects inside this window
    _setup_canvas_window():
        configures the canvas window and the scrollbar within
    _reset():
        _row_count and _line_list are reset
    _clear_screen():
        text in the entry fields of the root window are deleted and all lines
        are deleted
    _button_add_new_row():
        creates the tkinter objects of a new line in the scrollable region and
        stores them in a Line object which is appended to _line_list
    _button_del_row(row):
        searches the _line_list for the correct row number and calls the delete
        method of this Line object
    _button_save():
        creates a Bill object from the text inside all combo_boxes and entry
        fields. this Bill is appended to the backend.BILLS list and written to
        the output csv file. afterwards, the screen is cleared
    _button_type():
        saves the current inputs as a new Bill. then writes all Bill objects to
        the program specified in the config file
    _create_output(): backend.Bill
        creates a Bill object from the inputs in the root window and from every
        Line
    _get_entry_from_line(line): backend.Entry
        takes all input from entry and combo_box fields of a given line and
        creates a new Entry object
    _button_save_template(row):
        called by the "save" button in every row of the scrollable region. takes
        the input of the Line with the specified row and creates a new Template.
        if there is already a Template with the same name then the old one is
        deleted. the new template is then stored in backend.TEMPLATES. all
        active combo_boxes in the scrollable region are then updated to display
        this new template
    _trace_template(row):
        called when something is written in a combo_box in the scrollable
        region. the input is compared to existing Template objects in the
        backend.TEMPLATES list. if there is a match with one template, the
        contents of this template are displayed in the according entry fields
        of the row
    _trace_update_entries(row):
        called when something is written in the entry fields in the scrollable
        region. in the specified row, all outputs are recalculated. the total
        sum which is displayed in the root window is also updated
    _calculate_price_quantity(line):
        called by _trace_update_entries(row). multiplies price_single with
        quantity and writes the result in the according entry field
    _calculate_price_discount(line):
        called by _trace_update_entries(row). calculates the price after
        discounts based on the given discounts and the order of operation which
        is specified by using the checkbox
    _calculate_total():
        calculates the sum of all discount-prices and writes it in the
        according entry field in the root window
    _create_label(frame:tkinter.Frame, text:str,
                  column:int, row:int): tkinter.Label
        creates and returns a tkinter Label
    _create_entry(frame:tkinter.Frame, column:int,
                  width:int, text_var:tkinter.StringVar): tkinter.Entry
        creates and returns a tkinter Entry
    _create_button(frame:tkinter.Frame, text:str, row:int, column:int,
                   func:function, font:str): tkinter.Button
        creates and returns a tkinter Button
    _create_combo_box(frame:tkinter.Frame,
                      text_var:tkinter.StringVar): ttk.Combobox
        creates and returns a tkinter Combobox
    """

    def __init__(self):
        # In the tkinter_objects json file the entry, button, combo_box and
        # check_button objects have a value "command" which corresponds to the
        # keys in these method dictionaries. This is used to bind method calls
        # to these tkinter objects
        self._method_dict_no_param: dict = \
            {"save_bill": self._button_save,
             "export_bills": self._button_export_bills,
             "write_bills": self._button_type,
             "trace_store": self._trace_store,
             "trace_payment": self._trace_payment,
             "add_new_row": self._button_add_new_row}
        self._method_dict_one_param: dict = \
            {"update": self._trace_update_entries,
             "delete_row": self._button_del_row,
             "trace_template": self._trace_template,
             "save_template": self._button_save_template}

        # Store all parameters for the tkinter objects in this dictionary
        self._objects: dict = backend.read_config(
            backend.CONFIG_DICT["tkinter_objects"])

        # Read parameters from the config file
        self._font: str = "none " + backend.CONFIG_DICT["font_size"] + " bold"
        self._scaling: float = backend.CONFIG_DICT["scaling"]
        self._width: float = backend.CONFIG_DICT["main_width"]
        self._height: float = backend.CONFIG_DICT["main_height"]
        self._canvas_width: float = backend.CONFIG_DICT["canvas_width"]
        self._canvas_height: float = backend.CONFIG_DICT["canvas_height"]

        self._color_frame: str = backend.CONFIG_DICT["color_frame"]
        self._color_label_fg: str = backend.CONFIG_DICT["color_label_fg"]
        self._color_label_bg: str = backend.CONFIG_DICT["color_label_bg"]

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
        self._frame_main = tk.Frame(self._root, bg=self._color_frame)
        self._frame_canvas = tk.Frame(self._frame_main)
        self._canvas = tk.Canvas(self._frame_canvas, bg=self._color_frame)
        self._frame_fields = tk.Frame(self._canvas, bg=self._color_frame)
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
        self._root.configure(background=self._color_frame)

        # Create all tkinter objects with frame_key "frame_main"
        trace_vars: dict = {}

        entries: dict = {}
        for frame_key, dict_key, _, column, row, width in self._entry_list:
            if frame_key == "frame_main":
                entry, trace_var_entry = self._create_entry(frame_key, column,
                                                            row, width, '')
                entries.update({dict_key: entry})
                trace_vars.update({dict_key: trace_var_entry})

        labels: dict = {}
        for frame_key, dict_key, text, column, row, sticky, font in \
                self._label_list:
            if frame_key == "frame_main":
                label = self._create_label(frame_key, text, column, row, sticky,
                                           font)
                labels.update({dict_key: label})

        combo_boxes: dict = {}
        for frame_key, dict_key, func_key, values, state, column, row, width, \
                sticky in self._combo_box_list:
            if frame_key == "frame_main":
                combo_box, trace_var_combo_box = self._create_combo_box(
                    frame_key, func_key, values, state, column, row, width,
                    sticky)
                trace_vars.update({dict_key: trace_var_combo_box})
                combo_boxes.update({dict_key: combo_box})

        buttons: dict = {}
        for frame_key, dict_key, text, func_key, column, row, font in \
                self._button_list:
            if frame_key == "frame_main":
                button = self._create_button(frame_key, text, column, row, font,
                                             func_key)
                buttons.update({dict_key: button})

        check_buttons: dict = {}

        # Create a Line object which stores all created tkinter objects
        self._root_objects = Line(-1, labels, entries, buttons, combo_boxes,
                                  check_buttons, trace_vars)

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
        row: int = self._row_count
        trace_vars = {}

        combo_boxes = {}
        for frame_key, dict_key, func_key, values, state, column, _, width, \
                sticky in self._combo_box_list:
            if frame_key == "frame_fields":
                combo_box, trace_var_combo_box = self._create_combo_box(
                    frame_key, func_key, values, state, column, row, width,
                    sticky)
                trace_vars.update({dict_key: trace_var_combo_box})
                combo_boxes.update({dict_key: combo_box})

        labels = {}
        for frame_key, dict_key, text, column, _, sticky, font in \
                self._label_list:
            if frame_key == "frame_fields":
                label = self._create_label(frame_key, text, column, row,
                                           sticky, font)
                labels.update({dict_key: label})

        entries = {}
        for frame_key, dict_key, func_key, column, _, width in self._entry_list:
            if frame_key == "frame_fields":
                entry, trace_var_entry = self._create_entry(frame_key,
                                                            column,
                                                            row,
                                                            width,
                                                            func_key)
                entries.update({dict_key: entry})
                trace_vars.update({dict_key: trace_var_entry})

        buttons = {}
        for frame_key, dict_key, text, func_key, column, _, font in \
                self._button_list:
            if frame_key == "frame_fields":
                buttons.update({dict_key: self._create_button(frame_key, text,
                                                              column, row, font,
                                                              func_key)})

        check_buttons = {}
        for frame_key, dict_key, func_key, text, column, sticky in \
                self._check_button_list:
            check_button, trace_var_check_button = self._create_check_button(
                frame_key, func_key, text, column, row, sticky)
            check_buttons.update({dict_key: check_button})
            trace_vars.update({dict_key: trace_var_check_button})

        entry = Line(self._row_count, labels, entries, buttons, combo_boxes,
                     check_buttons, trace_vars)
        self._line_list.append(entry)

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
        bill = self._create_output()

        # Don't save an empty bill
        if bill.entries:
            backend.BILLS.append(bill)
            backend.backup_bill(bill)

        self._clear_screen()
        self._reset()

        # Don't leave the scrollable region empty
        self._button_add_new_row()

    def _button_export_bills(self):
        """
        Save the current bill, then write all bills of this session to the
        output csv and close the program
        """
        print("_button_export_bills")
        self._button_save()
        backend.export_bills()
        sys.exit()

    def _button_type(self):
        """
        Saves the current bill. Then, uses the keyboard module to take control
        of the keyboard and directly types the bills into a specified program.
        Afterwards, the screen is reset to accept another bill
        """
        print("_button_type")
        self._button_save()

        # keyboard.write_to_program()

        self._clear_screen()
        self._reset()

        # Don't leave the scrollable region empty
        self._button_add_new_row()

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
        # Replacement so it's easier to type via numpad
        time = time.replace('-', ':')

        discount_sum = self._read_label(self._root_objects.
                                        labels["discount_sum_var"], "float")
        quantity_discount_sum = self._read_label(
            self._root_objects.labels["quantity_discount_sum_var"], "float")
        sale_sum = self._read_label(self._root_objects.labels["sale_sum_var"],
                                    "float")
        total = self._read_label(self._root_objects.labels["total_var"],
                                 "float")
        price_quantity_sum = 0.0

        # Add year to date if len(date) fits the "dd-mm" input
        # TODO: maybe check this using regex
        if len(date) == 5:
            date = date + '-' + backend.CONFIG_DICT["year"]

        # Get the item data from _line_list
        # TODO: combine this and the next for-loop
        entry_list = list()
        for line in self._line_list:
            entry = self._get_entry_from_line(line)
            # Skip empty line
            if entry.product == '' and entry.price_final == 0:
                continue

            entry_list.append(entry)

        for entry in entry_list:
            # Skip empty line
            if not entry.product and not entry.quantity and \
                    not entry.price_final:
                continue
            # TODO: don't do this formatting here, do this only in the
            #  backend.format_bill
            # Quantity = 1 should not be shown in final excel file
            if float(entry.quantity) == 1:
                entry.quantity = ''
            else:
                entry.quantity = float(entry.quantity)

            price_quantity_sum += entry.price_quantity

            # update entry history with this purchase
            date_time = date + 'T' + time
            # price_per_unit includes discounts
            price_per_unit = 0
            if isinstance(entry.quantity, str) or entry.quantity == 0:
                # if quantity is '' then it is 1
                price_per_unit = entry.price_final
            elif isinstance(entry.quantity, float):
                price_per_unit = entry.price_final / entry.quantity
            round(price_per_unit, 2)
            # TODO: history dict instead of list would be better
            entry.history.update({date_time: [store, price_per_unit]})

            backend.TEMPLATES.update({entry.product: entry})
            backend.update_product_templates()

        price_quantity_sum = round(price_quantity_sum, 2)

        bill = backend.Bill(entries=entry_list, date=date, time=time,
                            store=store, payment=payment, total=total,
                            discount_sum=discount_sum,
                            quantity_discount_sum=quantity_discount_sum,
                            sale_sum=sale_sum,
                            price_quantity_sum=price_quantity_sum)
        print("bill = ", bill)

        return bill

    def _get_entry_from_line(self, line):
        """
        Read all Entry objects of a given line in the scrollable region and save
        their information as a backend.Entry object, then return it

        Parameters:
            line: Line
                The Line object from which information will be read

        Returns:
            entry: backend.Entry
                Information of all tkinter Entry objects of the given line

        """
        # TODO: make a list or something through which we can loop to reduce
        #  repetition
        product = self._read_entry(line.entries["product"], "str")
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
        entry = backend.Entry(product=product,
                              price_single=price_single,
                              quantity=quantity,
                              discount_class=discount_class,
                              product_class=product_class,
                              unknown=unknown,
                              price_quantity=price_quantity,
                              discount=discount,
                              quantity_discount=quantity_discount,
                              sale=sale,
                              price_final=price_final)
        return entry

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

        entry = self._get_entry_from_line(curr_line)
        if entry.product == '':
            return
        if entry.quantity == 0:
            entry.quantity = 1

        # German format, decimal sign is comma
        entry.price_single = str(entry.price_single).replace('.', ',')
        entry.quantity = str(entry.quantity).replace('.', ',')

        # If template already exists, delete the old entry
        try:
            backend.TEMPLATES.pop(entry.product)
        except KeyError:
            pass

        # Add new template to dictionary
        backend.TEMPLATES.update({entry.product: entry})

        # Update the product json file
        backend.update_product_templates()

        # Alphabetically sort the list that is passed to the Combobox
        name_list = sorted([key for key, _ in backend.TEMPLATES.items()])

        # Update all Comboboxes so they show this new template
        for line in self._line_list:
            line.combo_boxes["template"]["values"] = name_list

        # TODO: why is this here?
        self._root_objects.combo_boxes["store"]["values"] = sorted(backend.
                                                                   STORES)

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

        # Add all template entries who contain the user input
        temp_dict = dict()
        for key, field in backend.TEMPLATES.items():
            if template_input in key.lower():
                temp_dict.update({key: field})

        # Show the matching entries in the dropdown of the current Combobox
        name_list = [key for key, _ in temp_dict.items()]
        name_list.sort()
        curr_line.combo_boxes["template"]["values"] = name_list

        # If no matches, clear all values in this row
        if len(temp_dict) == 0:
            template_name = self._read_entry(curr_line.combo_boxes["template"],
                                             "str")
            curr_line.entries["product"].delete(0, "end")
            curr_line.entries["product"].insert(0, template_name)
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

            curr_line.entries["product"].delete(0, "end")
            curr_line.entries["product"].insert(0, product)
            curr_line.entries["price_single"].delete(0, "end")
            curr_line.entries["price_single"].insert(0, curr_temp.price_single)
            curr_line.entries["sale"].delete(0, "end")
            curr_line.entries["sale"].insert(0, curr_temp.sale)
            curr_line.entries["quantity"].delete(0, "end")
            curr_line.entries["quantity"].insert(0, curr_temp.quantity)
            curr_line.entries["discount_class"].delete(0, "end")
            curr_line.entries["discount_class"].insert(0,
                                                       curr_temp.discount_class)
            curr_line.entries["product_class"].delete(0, "end")
            curr_line.entries["product_class"].insert(0,
                                                      curr_temp.product_class)
            curr_line.entries["unknown"].delete(0, "end")
            curr_line.entries["unknown"].insert(0, curr_temp.unknown)
            curr_line.entries["price_quantity"].delete(0, "end")
            curr_line.entries["price_quantity"].insert(0,
                                                       curr_temp.price_quantity)
            curr_line.entries["discount"].delete(0, "end")
            curr_line.entries["discount"].insert(0, curr_temp.discount)
            curr_line.entries["quantity_discount"].delete(0, "end")
            curr_line.entries["quantity_discount"]. \
                insert(0, curr_temp.quantity_discount)
            curr_line.entries["price_final"].delete(0, "end")
            curr_line.entries["price_final"].insert(0, curr_temp.price_final)

        # If there are multiple matches, there are 2 options
        else:
            # If one match doesn't just contain the user input but is equal to
            # it, treat it like a single match occurred
            for key, field in temp_dict.items():
                if template_input == key.lower():
                    product = key
                    curr_temp = field

                    curr_line.entries["product"].delete(0, "end")
                    curr_line.entries["product"].insert(0, product)
                    curr_line.entries["price_single"].delete(0, "end")
                    curr_line.entries["price_single"]. \
                        insert(0, curr_temp.price_single)
                    curr_line.entries["sale"].delete(0, "end")
                    curr_line.entries["sale"].insert(0, curr_temp.sale)
                    curr_line.entries["quantity"].delete(0, "end")
                    curr_line.entries["quantity"].insert(0, curr_temp.quantity)
                    curr_line.entries["discount_class"].delete(0, "end")
                    curr_line.entries["discount_class"]. \
                        insert(0, curr_temp.discount_class)
                    curr_line.entries["product_class"].delete(0, "end")
                    curr_line.entries["product_class"]. \
                        insert(0, curr_temp.product_class)
                    curr_line.entries["unknown"].delete(0, "end")
                    curr_line.entries["unknown"].insert(0, curr_temp.unknown)
                    curr_line.entries["price_quantity"].delete(0, "end")
                    curr_line.entries["price_quantity"]. \
                        insert(0, curr_temp.price_quantity)
                    curr_line.entries["discount"].delete(0, "end")
                    curr_line.entries["discount"].insert(0, curr_temp.discount)
                    curr_line.entries["quantity_discount"].delete(0, "end")
                    curr_line.entries["quantity_discount"]. \
                        insert(0, curr_temp.quantity_discount)
                    curr_line.entries["price_final"].delete(0, "end")
                    curr_line.entries["price_final"]. \
                        insert(0, curr_temp.price_final)
                    break
                # If there are multiple matches and no exact match, treat it
                # like no match occurred
                else:
                    curr_line.entries["product"].delete(0, "end")
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

        if len(store_list) == 0:
            self._root_objects.combo_boxes["payment"].set('')
        # if store is Billa, Billa Plus or Merkur: change payment to Karte
        if len(store_list) == 1:
            payment = backend.STORES[store_list[0]]["default_payment"]
            # if store_list[0] in ["Billa", "Billa Plus", "Merkur"]:
            self._root_objects.combo_boxes["payment"].set(payment)
        # special case for Billa: if "Billa" is typed in,
        # it still matches "Billa" and "Billa Plus"
        else:
            for key, field in backend.STORES.items():
                if store_input == key.lower():
                    payment = field["default_payment"]
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

    def _trace_update_entries(self, current_line):
        """
        Calls all "calculate" methods for a given Line in the scrollable region.
        Then calculates the sums that are displayed in the main frame and
        changes the format of the time input

        Parameters:
            current_line: Line
                Which Line object should be calculated
        """
        print("_trace_update_entries")

        self._calculate_price_quantity(current_line)
        self._calculate_discount(current_line)
        self._calculate_price_final(current_line)
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
        self._root_objects.labels["quantity_discount_sum_var"].\
            config(text=quantity_discount_sum)
        self._root_objects.labels["sale_sum_var"].config(text=sale_sum)

        # TODO: integrate this into the loop above
        price_quantity_sum = 0.0
        for line in self._line_list:
            price_quantity_sum += self._read_entry(
                line.entries["price_quantity"], "float")
        price_quantity_sum = self._float2str(price_quantity_sum)
        self._root_objects.labels["price_quantity_sum_var"].\
            config(text=price_quantity_sum)

        # in "time" label, replace '-' with ':'
        time = self._read_entry(self._root_objects.entries["time"], "str")
        time = time.replace('-', ':')
        self._root_objects.entries["time"].delete(0, "end")
        self._root_objects.entries["time"].insert(0, time)

    def _calculate_price_quantity(self, line):
        """
        Calculates "price_quantity" from the "price_single" and "quantity" of
        the given Line in the scrollable region. This value is then displayed

        Parameters:
            line: Line
                Which Line object should be calculated
        """
        print("_calculate_price_quantity")
        price_single = self._read_entry(line.entries["price_single"], "float")
        quantity = self._read_entry(line.entries["quantity"], "float")

        if not quantity:
            quantity = 1

        price_quantity = round(price_single * quantity, 2)

        # German format, decimal sign is comma
        price_quantity = str(price_quantity).replace('.', ',')

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
        price_quantity = self._read_entry(line.entries["price_quantity"],
                                          "float")

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

        # For some items, first quantity_discount and sale are subtracted from
        # the price and then the result is multiplied with the discount_class
        # (minus_first = True).
        # For other items, multiplication is the first step
        # (minus_first = False)
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

        # German format, decimal sign is comma
        discount = str(discount).replace('.', ',')

        line.entries["discount"].delete(0, "end")
        line.entries["discount"].insert(0, discount)

    def _calculate_price_final(self, line):
        """
        Calculates "price_final" based on "price_quantity", "discount",
        "quantity_discount" and "sale" of the given Line in the scrollable
        region. This value is then displayed

        Parameters:
            line: Line
                Which Line object should be calculated
        """
        print("_calculate_price_final")

        price_quantity = self._read_entry(line.entries["price_quantity"],
                                          "float")

        discount = self._read_entry(line.entries["discount"], "float")
        sale = self._read_entry(line.entries["sale"], "float")

        quantity_discount = self._read_entry(line.entries["quantity_discount"],
                                             "float")
        price_final = price_quantity + discount + quantity_discount + sale
        price_final = round(price_final, 2)

        # German format, decimal sign is comma
        price_final = str(price_final).replace('.', ',')

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
            price_final = self._read_entry(line.entries["price_final"], "float")

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
        temp = tk.Label(frame, text=text, bg=self._color_label_bg,
                        fg=self._color_label_fg,
                        font=font)
        temp.grid(row=row, column=column, sticky=sticky)
        return temp

    # TODO: change func_key into method_key everywhere
    def _create_entry(self, frame_key, column, row: int, width, func_key):
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

        temp = tk.Entry(frame, textvariable=trace_var, width=width, bg="white")
        temp.grid(row=row, column=column, sticky=tk.W)
        return temp, trace_var

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
            box_list = sorted([key for key, _ in backend.TEMPLATES.items()])
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
        out_str = str(in_float).replace('.', ',')
        return out_str
