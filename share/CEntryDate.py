from datetime import datetime
from PIL import Image
import customtkinter as ctk
import tkcalendar as tkc
from tkinter import ttk
import tkinter as tk

class CEntryDate(ctk.CTkFrame):
    def __init__(self, parent,
                 style=None,
                 state="readonly"):
        """style: primary, success, danger"""
        super().__init__(parent)
        self._textvariable = ctk.StringVar()
        self.configure(fg_color="white")
        self.__entry = ctk.CTkEntry(self, corner_radius=0,
                                    border_color="gray",
                                    border_width=1,
                                    fg_color="white",
                                    text_color="black",
                                    textvariable=self._textvariable,
                                    state=state)
        self.__entry.pack(side="left")
        icon_btn = ctk.CTkImage(Image.open("../assets/calendar_primary.png"), size=(20, 20))
        if style == "success":
            icon_btn = ctk.CTkImage(Image.open("../assets/calendar_success.png"), size=(20, 20))
        elif style == "danger":
            icon_btn = ctk.CTkImage(Image.open("../assets/calendar_danger.png"), size=(20, 20))
        self.__btn = ctk.CTkButton(master=self, text="",
                                   corner_radius=0,
                                   width=30,
                                   image=icon_btn,
                                   hover_color="white",
                                   fg_color="white",
                                   border_color="gray",
                                   border_width=1,
                                   command=lambda: self.onclick_button())
        self.__btn.pack(expand=0)
        self._textvariable.set(datetime.now().strftime("%Y-%m-%d"))
        self.after_idle(self.update_height_button)


    @property
    def date_text(self):
        return self._textvariable.get()
    @date_text.setter
    def date_text(self, value):
        self._textvariable.set(value)

    def create_ui_calendar(self):
        global cal, top
        # style = ttk.Style(self)
        # style.theme_use('default')
        top = tk.Toplevel(master=self)
        top.title("Lịch")
        top.geometry("250x220")
        main_fr = ctk.CTkFrame(top)
        main_fr.pack(fill="both", expand=1)
        cal = tkc.Calendar(master=main_fr, date_pattern="y-mm-dd", selectmode='day', selectbackground="DodgerBlue1")
        cal.bind("<<CalendarSelected>>", lambda e: self.calendar_selected())
        cal.pack(fill="both", expand=True, padx=10, pady=10)
        date_obj = datetime.strptime(self._textvariable.get(), "%Y-%m-%d")
        cal.selection_set(date_obj)
        self.update_idletasks()


    def onclick_button(self):
        self.create_ui_calendar()

    def calendar_selected(self):
        self._textvariable.set(cal.get_date())
        top.destroy()

    def update_height_button(self):

        self.update_idletasks()
        self.__btn.configure(height=self.__entry.winfo_height())

