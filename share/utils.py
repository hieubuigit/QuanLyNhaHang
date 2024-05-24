from tkcalendar import DateEntry

user_profile = {} # User
import tkinter as tk
from tkinter import END, ttk


class Utils:
    def __init__(self):
        pass

    heading_group_pack = {'side':tk.TOP, 'expand':True, 'padx':5, 'pady':3, 'anchor':tk.W, 'fill':tk.X}
    label_pack_style = {'side':tk.TOP, 'expand':True, 'padx':5, 'pady':3, 'anchor':tk.W, 'fill':tk.X}
    entry_pack_style = {'side':tk.TOP, 'expand':True, 'anchor':tk.W, 'padx':5, 'pady':3, 'ipadx': 3, 'ipady': 3, 'fill':tk.X}
    sub_frame_style = {'side':tk.TOP, 'expand':True, 'anchor':tk.W, 'pady':5, 'fill':tk.X}
    radio_group_style = {'side':tk.TOP, 'expand':True, 'anchor':tk.W, 'padx':(0, 100), 'pady':3, 'ipadx': 3, 'ipady': 3, 'fill':tk.BOTH}
    pack_style_1 = {'side': tk.LEFT, 'expand': True, 'fill': tk.BOTH}

    pack_control_item = {"side":'left', 'fill': tk.NONE, 'expand': tk.YES, 'pady':'20', 'anchor': "w"}

    @staticmethod
    def input_component(parent, kw: dict):
        frame_item = tk.Frame(master=parent)
        my_label = ttk.Label(frame_item, text=kw["lbl"])
        my_label.pack(Utils.label_pack_style)
        my_entry = ttk.Entry(master=frame_item)
        my_entry.pack(Utils.entry_pack_style)
        frame_item.pack(Utils.sub_frame_style)
        return my_entry

    @staticmethod
    def date_picker_component(parent, kw: dict):
        frame_item = tk.Frame(master=parent)
        label = ttk.Label(frame_item, text=kw['lbl'])
        label.pack(Utils.label_pack_style)
        date_picker = DateEntry(frame_item, dateformat='%d/%m/%Y', bootstyle='', date_pattern='dd/mm/yyyy')
        date_picker.pack(Utils.entry_pack_style)
        frame_item.pack(Utils.sub_frame_style)
        return date_picker

