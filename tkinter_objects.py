import tkinter as tk
from tkinter import ttk

import backend

# TODO: create parent gui object class
import gui


class Label:
    def __init__(self, frame_key, dict_key, text, column, row, sticky, font):
        self.frame_key = frame_key
        self.dict_key = dict_key
        self.text = text
        self.column = column
        self.row = row
        self.sticky = sticky
        self.font = font
        self.bg = "light grey"
        self.fg = "black"
        self.object = None

    def create(self, frame, row):
        if not row:
            row = self.row

        self.object = tk.Label(frame, text=self.text, bg=self.bg, fg=self.fg,
                               font=self.font)
        self.object.grid(row=row, column=self.column, sticky=self.sticky)


class Entry:
    def __init__(self, frame_key, dict_key, column, row, width, bg, fg):
        self.frame_key = frame_key
        self.dict_key = dict_key
        self.column = column
        self.row = row
        self.width = width
        self.sticky = 'w'
        self.bg = bg
        self.fg = fg
        self.object = None

    def create(self, frame, row):
        if not row:
            row = self.row

        self.object = tk.Entry(frame, width=self.width, bg=self.bg, fg=self.fg)
        self.object.grid(row=row, column=self.column, sticky=self.sticky)

    def change_bg(self, new_colour):
        self.object.configure(bg=new_colour)


class Button:
    def __init__(self, frame_key, dict_key, text, func, column, row, font):
        self.frame_key = frame_key
        self.dict_key = dict_key
        self.text = text
        self.func = func
        self.column = column
        self.row = row
        self.font = font
        self.sticky = "news"
        self.object = None

    def create(self, frame, row):
        if not row:
            row = self.row

        def command():
            self.func(row)

        self.object = tk.Button(frame, text=self.text, width=len(self.text),
                                command=command, font=self.font)
        self.object.grid(row=row, column=self.column, sticky=self.sticky)

    # TODO: change colour method


class ComboBox:
    def __init__(self, frame_key, dict_key, func, values, state, column, row,
                 width, sticky):
        self.frame_key = frame_key
        self.dict_key = dict_key
        self.func = func
        self.values = values
        self.state = state
        self.column = column
        self.row = row
        self.width = width
        self.sticky = sticky
        self.object = None
        self.trace_var = None

    def create(self, frame, row):
        if not row:
            row = self.row

        def command(*_):
            self.func(interface)

        self.trace_var = tk.StringVar()
        self.trace_var.set('')
        self.trace_var.trace('w', command)

        self.object = ttk.Combobox(frame, width=self.width,
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
        self.object.grid(row=row, column=self.column, sticky=self.sticky)


class CheckButton:
    def __init__(self, frame, dict_key, command, text, column, sticky):
        self.frame = frame
        self.dict_key = dict_key
        self.command = command
        self.text = text
        self.column = column
        self.sticky = sticky
