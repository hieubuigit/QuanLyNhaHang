import math
import os.path
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk



class TableView:
    path_assets = "{path_assets}".format(path_assets=os.getcwd().replace("Table_Order", "assets"))
    def __init__(self, window):
        super().__init__()
        self.__ds_table = []
        self.table_num_value = tk.StringVar()
        self.seat_num_value = tk.StringVar()
        self.status_value = tk.StringVar()

        for i in range(0, 20):
            self.__ds_table.append(i)
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

        self.__add_content(window, screen_width, screen_height)

        # Đặt sự kiện để cập nhật kích thước của canvas
        self.grid_content.bind("<Configure>", self.on_frame_configure)


    def __add_content(self, window, screen_width, screen_height):
        """Thêm nội dung vào Frame (trong trường hợp này là một grid)"""
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
                    num_table = self.__ds_table[index]
                    self.grid_content.grid_columnconfigure(j, weight=1)
                    img_table = ImageTk.PhotoImage(Image.open(
                        "{path_assets}{img}".format(path_assets=TableView.path_assets, img="/ic_table_visible.png")).resize(
                        (image_size, image_size)))

                    btn = ttk.Button(self.grid_content, text=f"{num_table}", image=img_table, compound='center',
                                     style='Custom.TButton', command=lambda: self.selected_table(window))
                    btn.image = img_table

                    btn.grid(row=i, column=j, sticky="nsew", padx=5, pady=5, ipadx=column_width // 4, ipady=row_height // 4)

    def update_data_table(self):
        pass

    def selected_table(self, window):
        self.create_ui_toplevel(window, "ADD")

    def on_frame_configure(self, event):
        # Cập nhật kích thước của canvas khi nội dung thay đổi
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))


    def create_ui_toplevel(self, window, action_type):
        style = ttk.Style()
        style.theme_use('default')

        toplevel = tk.Toplevel(window)
        toplevel.resizable(True, False)
        toplevel.geometry("300x300")

        validation = window.register(self.validate_input)
        table_popup_frame = tk.Frame(toplevel, pady=20)
        lb_table_num = tk.Label(table_popup_frame, text="Số bàn")
        lb_table_num.grid(row=0, column=0, sticky="nw")
        self.entry_table_num = tk.Entry(table_popup_frame, validate="key", validatecommand=(validation, '%P'))
        self.entry_table_num.grid(row=1, column=0)

        lb_seat_num = tk.Label(table_popup_frame, text="Số ghế")
        lb_seat_num.grid(row=2, column=0, sticky="nw")
        self.entry_seat_num = tk.Entry(table_popup_frame, validate="key", validatecommand=(validation, '%P'))
        self.entry_seat_num.grid(row=3, column=0)

        lb_table_status = tk.Label(table_popup_frame, text="Trạng thái")
        lb_table_status.grid(row=4, column=0, sticky="nw")
        self.status_combox = ttk.Combobox(table_popup_frame, values=("Trống", "Đã đặt"))
        self.status_combox.grid(row=5, column=0)

        btn_save = ttk.Button(table_popup_frame, text="Lưu", command=self.click_button)
        btn_save.grid(row=6, column=0, pady=15)
        if action_type == "ADD":
            toplevel.title("Thêm bàn mới")
        else:
            toplevel.title("Cập nhật thông tin bàn")
            btn_save.config(text="Cập nhật")

        table_popup_frame.pack()

    # Form cập nhật, lấy dữ liệu của bàn theo số bàn
    def load_data_table_popup(self):
        self.table_num_value.set("2")
        pass
    def validate_input(self, new_value):
        # Kiểm tra xem giá trị mới có phải là số không
        try:
            float(new_value)
            return True
        except ValueError:
            return False

    def click_button(self):
        table_num_value = self.entry_table_num.get()
        seat_num_value = self.entry_seat_num.get()
        status_value = self.status_combox.get()
        # Thực hiện thêm vào database
        # Thực hiện cập nhật lại database
        print(table_num_value, seat_num_value, status_value)


if __name__ == '__main__':
    root = tk.Tk()
    root.resizable(True, True)
    root.state('zoomed')  # full scree
    root.title("Restaurant Table")

    home = TableView(root)
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)
    root.mainloop()

