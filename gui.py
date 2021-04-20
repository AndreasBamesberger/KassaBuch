"""" file that holds Line and GUI classes"""
import tkinter as tk
from tkinter import ttk

import backend

# TODO: add label with line number


class Line:
    # TODO: update
    """
    Creates a line in the scroll region of the GUI

    ...

    Attributes
    ----------
    row: int
        in which row this line is placed
    labels: dict
        all tkinter Label objects of this line
    entries: dict
        all tkinter Entry objects of this line
    buttons: dict
        all tkinter Button objects of this line
    combo_boxes: dict
        all tkinter Combobox objects of this line
    check_buttons: list of tkinter.Checkbutton
        the tkinter Checkbutton object of this line
    trace_vars: list
        list that holds all tkinter.StringVar variables of the entry fields and
        the combo box

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
        """ Destroy all tkinter objects of this line """
        print("deleting row ", self.row)
        print(self.labels)
        for key, field in self.labels.items():
            field.destroy()
        # for key, field in self.labels.items():
        #     field.destroy()
        for key, field in self.entries.items():
            field.destroy()
        for key, field in self.buttons.items():
            field.destroy()
        for key, field in self.combo_boxes.items():
            field.destroy()
        for key, field in self.check_buttons.items():
            field.destroy()

    def __repr__(self):
        out_string = (f"Line object:\n"
                      f"\trow: {self.row}\n"
                      f"\tlabels: \n{self.labels}\n"
                      f"\tentries: \n{self.entries}\n"
                      f"\tbuttons: \n{self.buttons}\n"
                      f"\tcombo_boxes: \n{self.combo_boxes}\n")
        return out_string


class Application:
    # TODO: update
    """
    Creates window using tkinter

    ...

    Attributes
    ----------
    _font: str
        font of texts
    _scaling: float/double
        scaling factor of the tkinter window, for different screen resolutions
    _width: int
        horizontal tkinter window resolution
    _height: int
        vertical tkinter window resolution
    _canvas_width: int
        horizontal resolution of the scrollable region
    _canvas_height: int
        vertical resolution of the scrollable region
    _color_frame: str
        color of the background
    _color_label_fg: str
        color of the tkinter label foreground
    _color_label_bg: str
        color of the tkinter label background
    _row_count: int
        number of rows generated in the scrollable region. this value never
        decreases, even when a line is deleted
    _line_list: list
        list of all currently active lines in the scrollable region
    _root: tkinter.Tk
        the main tkinter window object
    _label_list: list
        list of the parameters with which the labels inside the scrollable lines
        are created
    _entry_list: list
        list of the parameters with which the entries inside the scrollable
        lines are created
    _button_list: list
        list of the parameters with which the buttons inside the scrollable
        lines are created
    _template_names: list
        list which gets displayed in the line combo_boxes, this list holds all
        names of previously saved products
    _frame_main: tkinter.Frame
        frame inside the main root window
    _frame_canvas: tkinter.Frame
        frame to create the scrollable region
    _canvas: tkinter.Canvas
        the scrollable region
    _frame_fields: tk.Frame
        frame that holds the lines inside the scrollable region
    _vsb: tkinter.Scrollbar
        vertical scrollbar for the scrollable region

    Methods
    -------
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
        self._func_dict_no_param: dict = {"save_bill": self._button_save,
                                          "export_bills":
                                              self._button_export_bills,
                                          "write_bills": self._button_type,
                                          "trace_store": self._trace_store,
                                          "trace_payment": self._trace_payment,
                                          "add_new_row":
                                              self._button_add_new_row}
        self._func_dict_one_param: dict = {"update": self._trace_update_entries,
                                           "delete_row": self._button_del_row,
                                           "trace_template":
                                               self._trace_template,
                                           "save_template":
                                               self._button_save_template,
                                           }

        self._objects: dict = backend.read_config(
            backend.CONFIG_DICT["tkinter_objects"])

        self._font: str = "none " + backend.CONFIG_DICT["font"] + " bold"
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

        # self._return_pressed = False

        self._root = tk.Tk()
        style = ttk.Style(self._root)
        style.configure("TFrame", background="red", foreground="blue")

        # self._root.bind_all('<KeyPress>', self._key_press)
        self._root.bind_all('<KeyRelease>', self._key_release)

        try:
            self._label_list = self._objects["label_list"]
        except KeyError:
            self._label_list = []
        try:
            self._entry_list = self._objects["entry_list"]
        except KeyError:
            self._entry_list = []
        try:
            self._button_list = self._objects["button_list"]
        except KeyError:
            self._button_list = []
        try:
            self._combo_box_list = self._objects["combo_box_list"]
        except KeyError:
            self._combo_box_list = []
        try:
            self._check_button_list = self._objects["check_button_list"]
        except KeyError:
            self._check_button_list = []

        self._template_names = [template.product for template in
                                backend.TEMPLATES]

        self._frame_main = tk.Frame(self._root, bg=self._color_frame)
        self._frame_canvas = tk.Frame(self._frame_main)
        self._canvas = tk.Canvas(self._frame_canvas, bg=self._color_frame)
        self._frame_fields = tk.Frame(self._canvas, bg=self._color_frame)
        self._vsb = tk.Scrollbar(self._frame_canvas, orient="vertical",
                                 command=self._canvas.yview)

        self._frame_dict = {"frame_fields": self._frame_fields,
                            "frame_main": self._frame_main}

        self._setup_root_window()

        self._setup_canvas_window()

        self._button_add_new_row()

        self._root_objects.entries["date"].focus_set()

    def loop(self):
        self._root.mainloop()

    def _setup_root_window(self):
        self._root.geometry(str(self._width) + 'x' + str(self._height))
        self._root.tk.call('tk', 'scaling', self._scaling)
        self._root.title("Kassabuch v05")
        self._root.configure(background=self._color_frame)

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

        self._root_objects = Line(-1, labels, entries, buttons, combo_boxes,
                                  check_buttons, trace_vars)

    def _setup_canvas_window(self):
        self._frame_main.grid(sticky="news")

        self._frame_canvas.grid(row=9, column=0, padx=(0, 0), pady=(5, 5),
                                sticky='nw')

        self._frame_canvas.grid_rowconfigure(0, weight=1)

        self._frame_canvas.grid_columnconfigure(0, weight=1)

        self._frame_canvas.grid_propagate(False)

        self._canvas.grid(row=0, column=0, sticky="news")

        self._vsb.grid(row=0, column=1, sticky="ns")
        self._canvas.configure(yscrollcommand=self._vsb.set)

        self._canvas.create_window((0, 0), window=self._frame_fields,
                                   anchor="nw")

        # # Update buttons frames idle tasks to let tkinter calculate buttons
        # # sizes
        self._frame_fields.update_idletasks()

        self._frame_canvas.config(width=self._canvas_width +
                                  self._vsb.winfo_width(),
                                  height=self._canvas_height)

        # Set the canvas scrolling region
        self._canvas.config(scrollregion=self._canvas.bbox("all"))

    def _reset(self):
        self._row_count = 0
        self._line_list = list()

    def _clear_screen(self):
        for key, field in self._root_objects.labels.items():
            if key.endswith("var"):
                field.config(text='')

        for key, field in self._root_objects.entries.items():
            if key == "date":
                continue
            field.delete(0, "end")

        for _, field in self._root_objects.combo_boxes.items():
            field.delete(0, "end")

        for line in self._line_list:
            line.delete()

    def _button_add_new_row(self):
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

        # self._setup_canvas_window()

        self._root.update()
        # Set the canvas scrolling region
        self._canvas.config(scrollregion=self._canvas.bbox("all"))

        self._row_count += 1
        print("self._row_count = ", self._row_count)

        self._canvas.yview_scroll(2, "units")

    def _button_del_row(self, row):
        print("_button_del_row")
        for index, line in enumerate(self._line_list):
            if line.row == row:
                line.delete()
                self._line_list.pop(index)
                if self._row_count < 0:
                    raise SystemError
                break
        print("self._row_count = ", self._row_count)
        self._calculate_total()

        self._root.update()
        # Set the canvas scrolling region
        self._canvas.config(scrollregion=self._canvas.bbox("all"))

    def _button_save(self):
        print("_button_save")
        bill = self._create_output()

        backend.BILLS.append(bill)
        backend.backup_bill(bill)

        self._clear_screen()
        self._reset()

        self._button_add_new_row()

    def _button_export_bills(self):
        print("_button_export_bills")
        self._button_save()
        backend.export_bills()
        raise SystemExit

    def _button_type(self):
        print("_button_type")
        self._button_save()

        # keyboard.write_to_program()

        self._clear_screen()
        self._reset()

        self._button_add_new_row()

    def _create_output(self):
        store = self._read_entry(self._root_objects.combo_boxes["store"], "str")

        if store not in backend.STORES and store != '':
            backend.STORES.append(store)
            backend.update_stores()

        payment = self._read_entry(self._root_objects.combo_boxes["payment"],
                                   "str")

        if payment not in backend.PAYMENTS and payment != '':
            backend.PAYMENTS.append(payment)
            backend.update_payments()

        date = self._read_entry(self._root_objects.entries["date"], "str")
        time = self._read_entry(self._root_objects.entries["time"], "str")
        # replacement so it's easier to type via numpad
        time = time.replace('-', ':')
        discount_sum = self._read_label(self._root_objects.
                                        labels["discount_sum_var"], "float")
        quantity_discount_sum = self._read_label(
            self._root_objects.labels["quantity_discount_sum_var"], "float")
        sale_sum = self._read_label(self._root_objects.labels["sale_sum_var"],
                                    "float")
        total = self._read_label(self._root_objects.labels["total_var"], "float")
        price_quantity_sum = 0.0

        discount_sum *= -1
        quantity_discount_sum *= -1
        sale_sum *= -1

        print("store = ", store)
        print("date = ", date)
        print("time = ", time)
        print("discount_sum = ", discount_sum)
        print("quantity_discount_sum = ", quantity_discount_sum)
        print("sale_sum = ", sale_sum)
        print("total = ", total)

        print("self._row_count = ", self._row_count)

        entry_list = list()
        for line in self._line_list:
            # template = line.template_input
            entry = self._get_entry_from_line(line)
            if entry.product == '' and entry.price_final == 0:
                continue

            entry_list.append(entry)

        # discount_sum: float = 0.0
        # quantity_discount_sum: float = 0.0
        # sale_sum: float = 0.0

        for entry in entry_list:
            if not entry.product and not entry.quantity and \
                    not entry.price_final:
                continue
            if float(entry.quantity) == 1:
                entry.quantity = ''
            else:
                entry.quantity = float(entry.quantity)

            price_quantity_sum += entry.price_quantity

            # try:
            #     discount_sum += float(entry.discount)
            # except ValueError:
            #     pass
            # try:
            #     quantity_discount_sum += float(entry.quantity_discount)
            # except ValueError:
            #     pass
            # try:
            #     sale_sum += float(entry.sale)
            # except ValueError:
            #     pass
        price_quantity_sum = round(price_quantity_sum, 2)

        print("price_quantity_sum = ", price_quantity_sum)

        bill = backend.Bill(entries=entry_list, date=date, time=time,
                            store=store, payment=payment, total=total,
                            discount_sum=discount_sum,
                            quantity_discount_sum=quantity_discount_sum,
                            sale_sum=sale_sum,
                            price_quantity_sum=price_quantity_sum)
        print("bill = ", bill)

        return bill

    def _get_entry_from_line(self, line):
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
        sale = self._read_entry(line.entries["sale"], "str")
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

    def _button_save_template(self, row):
        print("_button_save_template")
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

        entry.price_single = str(entry.price_single).replace('.', ',')
        entry.quantity = str(entry.quantity).replace('.', ',')

        for index, template in enumerate(backend.TEMPLATES):
            if template.product == entry.product:
                backend.TEMPLATES.pop(index)
                break

        backend.TEMPLATES.append(entry)
        backend.update_product_templates()

        self._template_names = [template.product for template in
                                backend.TEMPLATES]
        sorted(self._template_names)

        for line in self._line_list:
            line.combo_boxes["template"]["values"] = self._template_names

        self._root_objects.combo_boxes["store"]["values"] = sorted(backend.
                                                                   STORES)

    def _trace_template(self, row):
        curr_line = None
        for index, line in enumerate(self._line_list):
            if line.row == row:
                curr_line = self._line_list[index]
                break

        if curr_line is None:
            raise SystemError

        template_input = self._read_entry(curr_line.combo_boxes["template"],
                                          "str").lower()

        temp_list = list()
        for template in backend.TEMPLATES:
            if template_input in template.product.lower():
                temp_list.append(template)

        name_list = [template.product for template in temp_list]
        name_list.sort()
        print(name_list)
        curr_line.combo_boxes["template"]["values"] = name_list

        if len(temp_list) == 0:
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

        elif len(temp_list) == 1:
            curr_temp = temp_list[0]

            curr_line.entries["product"].delete(0, "end")
            curr_line.entries["product"].insert(0, curr_temp.product)
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
            curr_line.entries["quantity_discount"].\
                insert(0, curr_temp.quantity_discount)
            curr_line.entries["price_final"].delete(0, "end")
            curr_line.entries["price_final"].insert(0, curr_temp.price_final)

        else:
            for index, suggestion in enumerate(temp_list):
                if template_input == suggestion.product.lower():
                    curr_temp = temp_list[index]

                    curr_line.entries["product"].delete(0, "end")
                    curr_line.entries["product"].insert(0, curr_temp.product)
                    curr_line.entries["price_single"].delete(0, "end")
                    curr_line.entries["price_single"].\
                        insert(0, curr_temp.price_single)
                    curr_line.entries["sale"].delete(0, "end")
                    curr_line.entries["sale"].insert(0, curr_temp.sale)
                    curr_line.entries["quantity"].delete(0, "end")
                    curr_line.entries["quantity"].insert(0, curr_temp.quantity)
                    curr_line.entries["discount_class"].delete(0, "end")
                    curr_line.entries["discount_class"].\
                        insert(0, curr_temp.discount_class)
                    curr_line.entries["product_class"].delete(0, "end")
                    curr_line.entries["product_class"].\
                        insert(0, curr_temp.product_class)
                    curr_line.entries["unknown"].delete(0, "end")
                    curr_line.entries["unknown"].insert(0, curr_temp.unknown)
                    curr_line.entries["price_quantity"].delete(0, "end")
                    curr_line.entries["price_quantity"].\
                        insert(0, curr_temp.price_quantity)
                    curr_line.entries["discount"].delete(0, "end")
                    curr_line.entries["discount"].insert(0, curr_temp.discount)
                    curr_line.entries["quantity_discount"].delete(0, "end")
                    curr_line.entries["quantity_discount"].\
                        insert(0, curr_temp.quantity_discount)
                    curr_line.entries["price_final"].delete(0, "end")
                    curr_line.entries["price_final"]. \
                        insert(0, curr_temp.price_final)
                    break
                else:
                    # template_name = self._read_entry(
                    #     curr_line.combo_boxes["template"],
                    #     "str")
                    curr_line.entries["product"].delete(0, "end")
                    # curr_line.entries["product"].insert(0, template_name)
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
        store_input = self._read_entry(self._root_objects.combo_boxes["store"],
                                       "str").lower()

        store_list = list()
        for store in backend.STORES:
            if store_input in store.lower():
                store_list.append(store)

        store_list.sort()

        print(store_list)
        self._root_objects.combo_boxes["store"]["values"] = store_list

    def _trace_payment(self):
        payment_input = self._read_entry(
            self._root_objects.combo_boxes["payment"], "str").lower()

        payment_list = list()
        for payment in backend.PAYMENTS:
            if payment_input in payment.lower():
                payment_list.append(payment)

        payment_list.sort()
        print(payment_list)
        self._root_objects.combo_boxes["payment"]["values"] = payment_list

    def _trace_update_entries(self, current_line):
        print("_trace_update_entries")
        # current_line = None
        # for index, line in enumerate(self._line_list):
        #     if line.row == row:
        #         current_line = line
        #         break
        #
        # if not current_line:
        #     return

        self._calculate_price_quantity(current_line)
        self._calculate_discount(current_line)
        self._calculate_price_final(current_line)
        self._calculate_total()

        discount_sum: float = 0.0
        quantity_discount_sum: float = 0.0
        sale_sum: float = 0.0

        for line in self._line_list:
            discount_sum += self._read_entry(line.entries["discount"], "float")
            quantity_discount_sum += self._read_entry(line.entries
                                                      ["quantity_discount"],
                                                      "float")
            sale_sum += self._read_entry(line.entries["sale"], "float")

        # self._root_objects.entries["discount_sum"].delete(0, "end")
        # self._root_objects.entries["discount_sum"].\
        #     insert(0, str(round(discount_sum, 2)).replace('.', ','))
        # self._root_objects.entries["quantity_discount_sum"].delete(0, "end")
        # self._root_objects.entries["quantity_discount_sum"]. \
        #     insert(0, str(round(quantity_discount_sum, 2)).replace('.', ','))
        # self._root_objects.entries["sale_sum"].delete(0, "end")
        # self._root_objects.entries["sale_sum"]. \
        #     insert(0, str(round(sale_sum, 2)).replace('.', ','))
        text = str(round(discount_sum, 2)).replace('.', ',')
        self._root_objects.labels["discount_sum_var"].config(text=text)
        text = str(round(quantity_discount_sum, 2)).replace('.', ',')
        self._root_objects.labels["quantity_discount_sum_var"].config(text=text)
        text = str(round(sale_sum, 2)).replace('.', ',')
        self._root_objects.labels["sale_sum_var"].config(text=text)

        price_quantity_sum = 0.0
        for line in self._line_list:
            price_quantity_sum += self._read_entry(
                line.entries["price_quantity"], "float")
        text = str(round(price_quantity_sum, 2)).replace('.', ',')
        self._root_objects.labels["price_quantity_sum_var"].config(text=text)

        # if current_line.row == self._row_count - 1:
        #     for line in self._line_list:
        #         if line.row == self._row_count - 1:
        #             if self._read_entry(line.entries["price_final"], "float"):
        #                 self._button_add_new_row()
        #
        #                 # Set the canvas scrolling region
        #                 self._canvas.config(scrollregion=self.
        #                                     _canvas.bbox("all"))

    def _calculate_price_quantity(self, line):
        print("_calculate_price_quantity")
        price_single = self._read_entry(line.entries["price_single"], "float")
        quantity = self._read_entry(line.entries["quantity"], "float")

        if not quantity:
            quantity = 1

        price_quantity = round(price_single * quantity, 2)
        price_quantity = str(price_quantity).replace('.', ',')

        line.entries["price_quantity"].delete(0, "end")
        line.entries["price_quantity"].insert(0, price_quantity)

    def _calculate_discount(self, line):
        print("_calculate_discount")
        price_quantity = self._read_entry(line.entries["price_quantity"],
                                          "float")

        discount_class = self._read_entry(line.entries["discount_class"], "str")
        discount_class = discount_class.replace(',', '.')

        if discount_class.lower() in ['a', 'f']:
            discount_class = 25
        else:
            try:
                discount_class = float(discount_class)
            except ValueError:
                discount_class = 0.0

        sale = self._read_entry(line.entries["sale"], "float")

        quantity_discount = self._read_entry(line.entries["quantity_discount"],
                                             "float")

        minus_first = self._read_entry(
            line.trace_vars["discount_check_button"], "float")

        if minus_first:
            discount = sale + quantity_discount + price_quantity
            discount *= discount_class / 100
        else:
            discount = price_quantity * discount_class / 100

        discount *= -1
        discount = round(discount, 2)
        discount = str(discount).replace('.', ',')
        line.entries["discount"].delete(0, "end")
        line.entries["discount"].insert(0, discount)

    def _calculate_price_final(self, line):
        print("_calculate_price_final")
        # discount_class = self._read_entry(line.entries["discount_class"],
        #                                   "str")
        # discount_class = discount_class.replace(',', '.')
        # if discount_class.lower() == 'a':
        #     discount_class = 25
        # else:
        #     try:
        #         discount_class = float(discount_class)
        #     except ValueError:
        #         discount_class = 0.0
        #
        # sale = self._read_entry(line.entries["sale"], "float")
        #
        # quantity_discount = self._read_entry(
        #     line.entries["quantity_discount"], "float")

        price_quantity = self._read_entry(line.entries["price_quantity"],
                                          "float")

        # discount_first = self._read_entry(
        #     line.trace_vars["discount_check_button"], "float")
        # # print("discount_first: ", discount_first)
        # if discount_first:
        #     price_final = (price_quantity - sale - quantity_discount) * \
        #                   (1 - (discount_class / 100))
        # else:
        #     price_final = (price_quantity * (1 - (discount_class / 100)) -
        #                    sale - quantity_discount)
        discount = self._read_entry(line.entries["discount"], "float")
        sale = self._read_entry(line.entries["sale"], "float")

        quantity_discount = self._read_entry(line.entries["quantity_discount"],
                                             "float")
        price_final = price_quantity + discount + quantity_discount + sale
        price_final = round(price_final, 2)
        price_final = str(price_final).replace('.', ',')

        line.entries["price_final"].delete(0, "end")
        line.entries["price_final"].insert(0, price_final)

    def _calculate_total(self):
        print("_calculate_total")
        total = 0.0
        for line in self._line_list:
            price_final = self._read_entry(line.entries["price_final"], "float")

            total += price_final

        total = round(total, 2)
        total = str(total).replace('.', ',')
        self._root_objects.labels["total_var"].config(text=total)
        # self._root_objects.entries["total"].delete(0, "end")
        # self._root_objects.entries["total"].insert(0, total)

    def _create_label(self, frame_key, text, column, row, sticky, font):
        frame = self._frame_dict[frame_key]
        temp = tk.Label(frame, text=text, bg=self._color_label_bg,
                        fg=self._color_label_fg,
                        font=font)
        temp.grid(row=row, column=column, sticky=sticky)
        return temp

    def _create_entry(self, frame_key, column, row: int, width, func_key):
        frame = self._frame_dict[frame_key]

        if func_key != '':
            def command(*_):
                if func_key in self._func_dict_one_param.keys():
                    self._func_dict_one_param[func_key](row)
                else:
                    self._func_dict_no_param[func_key]()

            trace_var = tk.StringVar()
            trace_var.set('')
            trace_var.trace('w', command)
        else:
            trace_var = None

        temp = tk.Entry(frame, textvariable=trace_var, width=width, bg="white")
        temp.grid(row=row, column=column, sticky=tk.W)
        return temp, trace_var

    def _create_button(self, frame_key, text, column, row: int, font, func_key):
        frame = self._frame_dict[frame_key]

        def command():
            if func_key in self._func_dict_one_param.keys():
                self._func_dict_one_param[func_key](row)
            else:
                self._func_dict_no_param[func_key]()

        temp = tk.Button(frame, text=text, width=len(text),
                         command=command, font=font)
        temp.grid(row=row, column=column, sticky="news")
        return temp

    def _create_combo_box(self, frame_key, func_key, values, state, column, row,
                          width, sticky):
        frame = self._frame_dict[frame_key]

        if func_key:
            def command(*_):
                if func_key in self._func_dict_one_param.keys():
                    self._func_dict_one_param[func_key](row)
                else:
                    self._func_dict_no_param[func_key]()

            trace_var = tk.StringVar()
            trace_var.set('')
            trace_var.trace('w', command)
        else:
            trace_var = ''

        temp = ttk.Combobox(frame, width=width, textvariable=trace_var)
        # temp["values"] = sorted(self._template_names)
        if values == "templates":
            temp["values"] = sorted(self._template_names)
        if values == "stores":
            temp["values"] = sorted(backend.STORES)
        if values == "payments":
            temp["values"] = sorted(backend.PAYMENTS)
        temp["state"] = state
        temp.grid(row=row, column=column, sticky=sticky)
        return temp, trace_var

    def _create_check_button(self, frame_key, func_key, text, column, row,
                             sticky):
        frame = self._frame_dict[frame_key]
        trace_var = tk.IntVar()

        def command():
            if func_key in self._func_dict_one_param.keys():
                self._func_dict_one_param[func_key](row)
            elif func_key in self._func_dict_no_param.keys():
                self._func_dict_no_param[func_key]()

        check_box = tk.Checkbutton(frame, text=text, variable=trace_var,
                                   onvalue=1, offvalue=0, command=command)
        check_box.grid(row=row, column=column, sticky=sticky)

        return check_box, trace_var

    @staticmethod
    def _read_entry(entry, data_type):
        value = entry.get()
        if data_type == "str":
            return value
        elif data_type == "float":
            if isinstance(value, str):
                value = value.replace(',', '.')
            try:
                value = float(value)
            except ValueError:
                value = 0.0
            return value

    @staticmethod
    def _read_label(label, data_type):
        value = label["text"]
        if data_type == "str":
            return value
        elif data_type == "float":
            if isinstance(value, str):
                value = value.replace(',', '.')
            try:
                value = float(value)
            except ValueError:
                value = 0.0
            return value

    # def _key_press(self, event):
    #     print("event.keysym: ", event.keysym)
    #     if event.keysym == "Return":
    #         print("Enter Key pressed")
    #         self._return_pressed = True

    def _key_release(self, event):
        print("event.keysym: ", event.keysym)
        if event.keysym == "F1":
            # print("Enter Key released")
            # print("focus_get(): ", self._root.focus_get())
            # self._return_pressed = False
            # print(self._row_count)
            for line in self._line_list:
                self._trace_update_entries(line)
            self._button_add_new_row()
            self._line_list[-1].combo_boxes["template"].focus_set()
        elif event.keysym == "F2":
            self._button_add_new_row()
            self._line_list[-1].combo_boxes["template"].focus_set()
        elif event.keysym == "F3":
            self._root_objects.entries["date"].focus_set()
        elif event.keysym == "F4":
            self._line_list[-1].combo_boxes["template"].focus_set()
        elif event.keysym == "F5":
            for line in self._line_list:
                self._trace_update_entries(line)


