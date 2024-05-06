import math
import os.path
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

from Table_Order.table_model import TableModel


class TableView:
    path_assets = "{path_assets}".format(path_assets=os.getcwd().replace("Table_Order", "assets"))
    def __init__(self, window):
        super().__init__()
        self.__ds_table = []
        for i in range(0, 20):
            self.__ds_table.append(TableModel(i, i))
        screen_width = window.winfo_width()
        screen_height = window.winfo_height()

        # Tạo một lưới
        self.grid_frame = tk.Frame(window, bg="yellow")
        self.grid_frame.pack(fill="both", expand=True)

        # Tạo thanh cuộn ngang
        self.horizontal_scrollbar = tk.Scrollbar(self.grid_frame, orient="horizontal")
        self.horizontal_scrollbar.pack(side="bottom", fill="x")

        # Tạo thanh cuộn dọc
        self.vertical_scrollbar = tk.Scrollbar(self.grid_frame, orient="vertical")
        self.vertical_scrollbar.pack(side="right", fill="y")

        # Tạo một canvas để chứa lưới
        self.canvas = tk.Canvas(self.grid_frame, xscrollcommand=self.horizontal_scrollbar.set,
                                yscrollcommand=self.vertical_scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)

        # Kết nối thanh cuộn với canvas
        self.horizontal_scrollbar.config(command=self.canvas.xview)
        self.vertical_scrollbar.config(command=self.canvas.yview)

        # Tạo một frame con để chứa nội dung của lưới
        self.grid_content = tk.Frame(self.canvas, bg="green")
        self.canvas.create_window((0, 0), window=self.grid_content, anchor="nw")
        # self.grid_content.pack(fill=tk.BOTH, expand=1)

        # Thêm nội dung vào lưới
        self.add_content(screen_width, screen_height)

        # Đặt sự kiện để cập nhật kích thước của canvas
        self.grid_content.bind("<Configure>", self.on_frame_configure)


    def add_content(self, screen_width, screen_height):
        # Thêm nội dung vào Frame (trong trường hợp này là một grid)
        style = ttk.Style()
        style.theme_use('default')
        style.configure('Custom.TButton', background='#DFD6D6')
        num_columns = 6
        image_size = 180
        column_width = screen_width // 8
        row_height = screen_height // 8

        num_rows = math.ceil(len(self.__ds_table) / 6)
        index = 0
        for i in range(num_rows):
            for j in range(num_columns):
                index = i * num_columns + j
                if index < len(self.__ds_table):
                    num_table = self.__ds_table[index].num_table
                    self.grid_content.grid_columnconfigure(j, weight=1)
                    img_table = ImageTk.PhotoImage(Image.open(
                        "{path_assets}{img}".format(path_assets=TableView.path_assets, img="/ic_table_visible.png")).resize(
                        (image_size, image_size)))

                    btn = ttk.Button(self.grid_content, text=f"{num_table}", image=img_table, compound='center',
                                     style='Custom.TButton', command=lambda: self.selected_table())
                    btn.image = img_table

                    btn.grid(row=i, column=j, sticky="nsew", padx=5, pady=5, ipadx=column_width // 4, ipady=row_height // 4)

    def update_data_table(self):
        pass

    def selected_table(self):
        print("Click table")

    def on_frame_configure(self, event):
        # Cập nhật kích thước của canvas khi nội dung thay đổi
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))





if __name__ == '__main__':
    root = tk.Tk()
    root.resizable(True, True)
    root.state('zoomed')  # full scree
    root.title("Restaurant Table")

    home = TableView(root)
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)
    root.mainloop()

