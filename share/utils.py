import customtkinter as ctk
# from tkcalendar import DateEntry
from entities.models import User
import tkinter as tk
import datetime
from share.common_config import UserType, Gender
# from ttkbootstrap import DateEntry


class Utils:
    # Contain information to set role on UI and features
    global user_profile
    user_profile = User()

    user_type = ("Admin", "Bình thường")
    gender = ("Nam", "Nữ", "Khác")

    def __init__(self):
        pass

    # Employee page
    heading_group_pack = {'side': tk.TOP, 'expand': True, 'padx': 5, 'pady': 3, 'anchor': tk.W, 'fill': tk.X}
    label_pack_style = {'side': tk.TOP, 'expand': True, 'padx': 5, 'pady': 3, 'anchor': tk.W, 'fill': tk.X}
    entry_pack_style = {'side': tk.TOP, 'expand': True, 'anchor': tk.W, 'padx': 5, 'pady': 3, 'ipadx': 3, 'ipady': 3,
                        'fill': tk.X}
    sub_frame_style = {'side': tk.TOP, 'expand': True, 'anchor': tk.W, 'pady': 5, 'fill': tk.X}
    radio_group_style = {'side': tk.TOP, 'expand': True, 'anchor': tk.W, 'padx': (0, 100), 'pady': 3, 'ipadx': 3,
                         'ipady': 3, 'fill': tk.BOTH}
    pack_style_1 = {'side': tk.LEFT, 'expand': True, 'fill': tk.BOTH}

    # Login page
    pack_control_item = {"side": 'left', 'fill': tk.NONE, 'expand': tk.YES, 'pady': '20', 'anchor': "w"}
    BLUE = '#3224ff'
    WHITE = '#fff'
    BLACK = '#000'

    @staticmethod
    def input_component(parent, kw: dict):
        frame_item = ctk.CTkFrame(master=parent)
        my_label = ctk.CTkLabel(frame_item, text=kw["lbl"], justify=ctk.LEFT)
        my_label.pack(**Utils.label_pack_style)
        if "type" in kw and kw["type"] == "password":
            my_entry = ctk.CTkEntry(master=frame_item, show="*")
        else:
            my_entry = ctk.CTkEntry(master=frame_item)
        my_entry.pack(**Utils.entry_pack_style)
        frame_item.pack(**Utils.sub_frame_style)
        return my_entry

    @staticmethod
    # def date_picker_component(parent, kw: dict):
    #     frame_item = ctk.CTkFrame(master=parent)
    #     label = ctk.CTkLabel(master=frame_item, text=kw['lbl'])
    #     label.pack(**Utils.label_pack_style)
    #     date_picker = DateEntry(master=frame_item, dateformat="%d/%m/%Y")
    #     date_picker.pack(**Utils.entry_pack_style)
    #     frame_item.pack(**Utils.sub_frame_style)
    #     return date_picker

    @staticmethod
    def format_date(date_str):
        # Format date with (yyyy-MM-dd) to save before save to database
        dt = datetime.datetime.strptime(date_str, '%d/%m/%Y')
        return dt.strftime("%Y-%m-%d")

    @staticmethod
    def get_account_type_value(str_value):
        if str_value == Utils.user_type[0]:
            return UserType.ADMIN.value
        elif str_value == Utils.user_type[1]:
            return UserType.NORMAL.value

    @staticmethod
    def get_account_type_str(user_type_enum):
        if user_type_enum == UserType.ADMIN.value:
            return Utils.user_type[0]
        elif user_type_enum == UserType.NORMAL.value:
            return Utils.user_type[1]

    @staticmethod
    def get_gender(gender_enum):
        if gender_enum == Gender.MALE.value:
            return Utils.gender[0]
        elif gender_enum == Gender.FEMALE.value:
            return Utils.gender[1]
        elif gender_enum == Gender.OTHER.value:
            return Utils.gender[2]
        return None

    @staticmethod
    def set_appearance_mode(ctk):
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")


