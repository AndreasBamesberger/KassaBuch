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
                                          "write_bills": self._button_type,
                                          "trace_store": self._trace_store,
                                          "add_new_row":
                                              self._button_add_new_row}
        self._func_dict_one_param: dict = {"update": self._trace_update_entries,
                                           "delete_row": self._button_del_row,
                                           "trace_template":
                                               self._trace_template,
                                           "save_template":
                                               self._button_save_template}

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

        self._root = tk.Tk()
        style = ttk.Style(self._root)
        style.configure("TFrame", background="red", foreground="blue")

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

    def loop(self):
        self._root.mainloop()

    def _setup_root_window(self):
        self._root.geometry(str(self._width) + 'x' + str(self._height))
        self._root.tk.call('tk', 'scaling', self._scaling)
        self._root.title("Kassabuch v05")
        self._root.configure(background=self._color_frame)

        trace_vars: dict = {}

        combo_boxes: dict = {}
        for frame_key, dict_key, func_key, values, state, column, row, width, \
                sticky in self._combo_box_list:
            if frame_key == "frame_main":
                combo_box, trace_var_combo_box = self._create_combo_box(
                    frame_key, func_key, values, state, column, row, width,
                    sticky)
                trace_vars.update({dict_key: trace_var_combo_box})
                combo_boxes.update({dict_key: combo_box})

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

        self._frame_canvas.grid(row=5, column=0, padx=(5, 0), pady=(5, 0),
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
        for _, field in self._root_objects.entries.items():
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
        backend.save_to_csv(bill)

        self._clear_screen()
        self._reset()

        self._button_add_new_row()

    def _button_type(self):
        print("_button_type")
        self._button_save()

        # keyboard.write_to_program()

        self._clear_screen()
        self._reset()

        self._button_add_new_row()

    def _create_output(self):
        store = self._root_objects.combo_boxes["store"].get()

        if store not in backend.STORES and store != '':
            backend.STORES.append(store)
            backend.update_stores()

        date = self._root_objects.entries["date"].get()
        time = self._root_objects.entries["time"].get()
        payment = self._root_objects.entries["payment"].get()
        total = self._root_objects.entries["total"].get()

        print("store = ", store)
        print("date = ", date)

        print("self._row_count = ", self._row_count)

        entry_list = list()
        for line in self._line_list:
            # template = line.template_input
            entry = self._get_entry_from_line(line)

            entry_list.append(entry)

        bill = backend.Bill(entries=entry_list, date=date, time=time,
                            store=store, payment=payment, total=total)
        print("bill = ", bill)

        return bill

    @staticmethod
    def _get_entry_from_line(line):
        entry = backend.Entry(product=line.entries["product"].get(),
                              price_single=line.entries[
                                  "price_single"].get(),
                              sale=line.entries["sale"].get(),
                              quantity=line.entries["quantity"].get(),
                              discount_class=line.entries[
                                  "discount_class"].get(),
                              product_class=line.entries[
                                  "product_class"].get(),
                              unknown=line.entries["unknown"].get(),
                              price_quantity=line.entries[
                                  "price_quantity"].get(),
                              discount=line.entries["discount"].get(),
                              quantity_discount=line.entries[
                                  "quantity_discount"]
                              .get(),
                              price_final=line.entries["price_final"].get(),
                              )
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
        template_input = None
        index = None
        for index, line in enumerate(self._line_list):
            if line.row == row:
                template_input = line.combo_boxes["template"].get().lower()
                break

        if index is None:
            raise SystemError

        temp_list = list()
        for template in backend.TEMPLATES:
            if template_input in template.product.lower():
                temp_list.append(template)

        name_list = [template.product for template in temp_list]
        name_list.sort()
        print(name_list)
        self._line_list[index].combo_boxes["template"]["values"] = name_list

        if len(temp_list) == 0:
            curr_line = self._line_list[index]
            template_name = curr_line.combo_boxes["template"].get()
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

        if len(temp_list) == 1:
            curr_temp = temp_list[0]

            self._line_list[index].entries["product"].delete(0, "end")
            self._line_list[index].entries["product"]. \
                insert(0, curr_temp.product)
            self._line_list[index].entries["price_single"].delete(0, "end")
            self._line_list[index].entries["price_single"]. \
                insert(0, curr_temp.price_single)
            self._line_list[index].entries["sale"].delete(0, "end")
            self._line_list[index].entries["sale"]. \
                insert(0, curr_temp.sale)
            self._line_list[index].entries["quantity"].delete(0, "end")
            self._line_list[index].entries["quantity"]. \
                insert(0, curr_temp.quantity)
            self._line_list[index].entries["discount_class"].delete(0, "end")
            self._line_list[index].entries["discount_class"]. \
                insert(0, curr_temp.discount_class)
            self._line_list[index].entries["product_class"].delete(0, "end")
            self._line_list[index].entries["product_class"]. \
                insert(0, curr_temp.product_class)
            self._line_list[index].entries["unknown"].delete(0, "end")
            self._line_list[index].entries["unknown"]. \
                insert(0, curr_temp.unknown)
            self._line_list[index].entries["price_quantity"].delete(0, "end")
            self._line_list[index].entries["price_quantity"]. \
                insert(0, curr_temp.price_quantity)
            self._line_list[index].entries["discount"].delete(0, "end")
            self._line_list[index].entries["discount"]. \
                insert(0, curr_temp.discount)
            self._line_list[index].entries["quantity_discount"].delete(0, "end")
            self._line_list[index].entries["quantity_discount"]. \
                insert(0, curr_temp.quantity_discount)
            self._line_list[index].entries["price_final"].delete(0, "end")
            self._line_list[index].entries["price_final"]. \
                insert(0, curr_temp.price_final)

    def _trace_store(self):
        store_input = self._root_objects.combo_boxes["store"].get().lower()

        temp_list = list()
        for store in backend.STORES:
            if store_input in store.lower():
                temp_list.append(store)

        temp_list.sort()
        print(temp_list)
        self._root_objects.combo_boxes["store"]["values"] = temp_list

    def _trace_update_entries(self, row):
        # print("_trace_update_entries")
        current_line = None
        for index, line in enumerate(self._line_list):
            if line.row == row:
                current_line = line
                break

        if not current_line:
            return

        self._calculate_price_quantity(current_line)
        self._calculate_discount(current_line)
        self._calculate_price_final(current_line)
        self._calculate_total()

        if current_line.row == self._row_count - 1:
            for line in self._line_list:
                if line.row == self._row_count - 1:
                    if line.entries["price_final"].get():
                        self._button_add_new_row()

                        # Set the canvas scrolling region
                        self._canvas.config(scrollregion=self.
                                            _canvas.bbox("all"))

    @staticmethod
    def _calculate_price_quantity(line):
        # print("_calculate_price_quantity")
        price_single = line.entries["price_single"].get()
        quantity = line.entries["quantity"].get()

        if price_single == '':
            return

        if quantity == '':
            quantity = 1

        try:
            price_single = float(price_single)
            quantity = float(quantity)
        except ValueError:
            return
        price_quantity = round(price_single * quantity, 2)

        line.entries["price_quantity"].delete(0, "end")
        line.entries["price_quantity"].insert(0, price_quantity)

    @staticmethod
    def _calculate_discount(line):
        # print("_calculate_discount")
        price_quantity = line.entries["price_quantity"].get()
        if price_quantity == '':
            return
        else:
            try:
                price_quantity = float(price_quantity)
            except ValueError:
                return

        discount_class = line.entries["discount_class"].get()
        if discount_class == '':
            discount_class = 0.0
        elif discount_class.lower() == 'a':
            discount_class = 25
        else:
            try:
                discount_class = float(discount_class)
            except ValueError:
                discount_class = 0.0

        discount = price_quantity * discount_class / 100
        discount = round(discount, 2)
        line.entries["discount"].delete(0, "end")
        line.entries["discount"].insert(0, discount)

    @staticmethod
    def _calculate_price_final(line):
        # print("_calculate_price_final")
        discount_class = line.entries["discount_class"].get()
        if discount_class == '':
            discount_class = 0.0
        elif discount_class.lower() == 'a':
            discount_class = 25
        else:
            try:
                discount_class = float(discount_class)
            except ValueError:
                discount_class = 0.0

        sale = line.entries["sale"].get()
        if sale == '':
            sale = 0.0
        else:
            try:
                sale = float(sale)
            except ValueError:
                sale = 0.0

        quantity_discount = line.entries["quantity_discount"].get()
        if quantity_discount == '':
            quantity_discount = 0.0
        else:
            try:
                quantity_discount = float(quantity_discount)
            except ValueError:
                quantity_discount = 0.0

        price_quantity = line.entries["price_quantity"].get()
        if price_quantity == '':
            return
        else:
            try:
                price_quantity = float(price_quantity)
            except ValueError:
                price_quantity = 0.0

        discount_first = line.trace_vars["discount_check_button"].get()
        # print("discount_first: ", discount_first)
        if discount_first:
            price_final = (price_quantity - sale - quantity_discount) * \
                          (1 - (discount_class / 100))
        else:
            price_final = (price_quantity * (1 - (discount_class / 100)) -
                           sale - quantity_discount)
        price_final = round(price_final, 2)
        if price_final < 0:
            price_final = 0

        line.entries["price_final"].delete(0, "end")
        line.entries["price_final"].insert(0, price_final)

    def _calculate_total(self):
        # print("_calculate_total")
        total = 0.0
        for line in self._line_list:
            price_final = line.entries["price_final"].get()
            if price_final == '':
                price_final = 0.0
            try:
                price_final = float(price_final)
            except ValueError:
                return

            total += price_final

        total = round(total, 2)
        self._root_objects.entries["total"].delete(0, "end")
        self._root_objects.entries["total"].insert(0, total)

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
        temp["state"] = state
        temp.grid(row=self._row_count, column=column, sticky=sticky)
        return temp, trace_var

    def _create_check_button(self, frame_key, func_key, text, column, row,
                             sticky):
        frame = self._frame_dict[frame_key]
        trace_var = tk.IntVar()

        def command():
            if func_key in self._func_dict_one_param.keys():
                self._func_dict_one_param[func_key](row)
            else:
                self._func_dict_no_param[func_key]()

        check_box = tk.Checkbutton(frame, text=text, variable=trace_var,
                                   onvalue=1, offvalue=0, command=command)
        check_box.grid(row=row, column=column, sticky=sticky)

        return check_box, trace_var
