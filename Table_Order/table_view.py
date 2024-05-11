import math
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from ttkthemes.themed_style import ThemedStyle

from share.common_config import Action
from ttkthemes import ThemedTk


class TableView:
    def __init__(self, window, controller, tables):
        self.__tables = []
        self.__tables = tables
        self.__controller = controller
        self.table_num_value = tk.StringVar()
        self.seat_num_value = tk.StringVar()
        self.status_value = tk.StringVar()

        screen_width = window.winfo_width()
        screen_height = window.winfo_height()
        style = ttk.Style()
        style.theme_use('default')
        self.grid_frame = ttk.Frame(window)
        self.grid_frame.pack(fill="both", expand=True)

        # Tạo thanh cuộn ngang
        self.horizontal_scrollbar = ttk.Scrollbar(self.grid_frame, orient="horizontal")
        self.horizontal_scrollbar.pack(side="bottom", fill="x")

        # Tạo thanh cuộn dọc
        self.vertical_scrollbar = ttk.Scrollbar(self.grid_frame, orient="vertical")
        self.vertical_scrollbar.pack(side="right", fill="y")

        # Tạo một canvas để chứa lưới
        self.canvas = tk.Canvas(self.grid_frame, xscrollcommand=self.horizontal_scrollbar.set,
                                yscrollcommand=self.vertical_scrollbar.set)
        self.canvas.pack(side="left", fill=tk.BOTH, expand=True)

        # Kết nối thanh cuộn với canvas
        self.horizontal_scrollbar.config(command=self.canvas.xview)
        self.vertical_scrollbar.config(command=self.canvas.yview)

        # Tạo một frame con để chứa bàn
        self.grid_content = ttk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.grid_content, anchor="nw")

        # Thêm ds bàn vào grid content
        self.__add_content(window, screen_width, screen_height)

        # Đặt sự kiện để cập nhật kích thước của canvas
        self.grid_content.bind("<Configure>", self.on_frame_configure)


    def __add_content(self, window, screen_width, screen_height):
        """Thêm nội dung vào Frame (trong trường hợp này là một grid)"""
        style = ttk.Style()
        style.theme_use('default')
        style.configure('Custom.TButton', background='#DFD6D6')
        num_columns = 6
        column_width = screen_width // 8
        row_height = screen_height // 8
        if len(self.__tables) < 10:
            num_columns = 4
        image_size = 180
        num_rows = math.ceil(len(self.__tables) / num_columns)
        for i in range(num_rows):
            for j in range(num_columns):
                index = i * num_columns + j
                if index < len(self.__tables):
                    num_table = self.__tables[index].tableNum
                    self.grid_content.grid_columnconfigure(j, weight=1)
                    img_table = ImageTk.PhotoImage(Image.open("../assets/ic_table_visible.png").resize(
                        (image_size, image_size)))

                    btn = ttk.Button(self.grid_content, text=f"{num_table}", image=img_table, compound='center',
                                     style='Custom.TButton', command=lambda: self.selected_table(window))
                    btn.image = img_table

                    btn.grid(row=i, column=j, sticky="nsew", padx=5, pady=5, ipadx=column_width // 4, ipady=row_height // 4)

    def update_data_table(self):
        pass

    def selected_table(self, window):
        print("selected table")
        self.create_ui_toplevel(window, Action.ADD)

    def on_frame_configure(self, event):
        # Cập nhật kích thước của canvas khi nội dung thay đổi
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))


    def create_ui_toplevel(self, window, action_type):
        style = ttk.Style()
        style.theme_use('default')

        self.toplevel = tk.Toplevel(window)
        self.toplevel.resizable(True, False)
        self.toplevel.geometry("290x250")
        validation = window.register(self.validate_input)
        table_popup_frame = ttk.Frame(self.toplevel)
        lb_table_num = ttk.Label(table_popup_frame, text="Số bàn")
        lb_table_num.place(x=10, y=20)
        self.entry_table_num = ttk.Entry(table_popup_frame, validate="key", validatecommand=(validation, '%P'))
        self.entry_table_num.place(x=80, y=20)

        lb_seat_num = ttk.Label(table_popup_frame, text="Số ghế")
        lb_seat_num.place(x=10, y=60)
        self.entry_seat_num = ttk.Entry(table_popup_frame, validate="key", validatecommand=(validation, '%P'))
        self.entry_seat_num.place(x=80, y=60)

        lb_table_status = ttk.Label(table_popup_frame, text="Trạng thái")
        lb_table_status.place(x=10, y=100)
        self.status_combox = ttk.Combobox(table_popup_frame, values=("Trống", "Đã đặt"))
        self.status_combox.place(x=80, y=100)
        self.lb_validate_table_info = ttk.Label(table_popup_frame, text="", foreground="red")
        self.lb_validate_table_info.place(x=60, y=140)
        style.configure("Save.TButton", bg="Red")
        btn_save = ttk.Button(table_popup_frame, text="Lưu", style="Save.TButton", command=lambda :self.click_button(action_type))
        btn_save.pack(fill=tk.Y, expand=0, side="bottom", pady=40)
        if action_type == Action.ADD:
            self.toplevel.title("Thêm bàn mới")
        else:
            self.toplevel.title("Cập nhật thông tin bàn")
            btn_save.config(text="Cập nhật")

        table_popup_frame.pack(fill=tk.BOTH, expand=1)

    # Form cập nhật, lấy dữ liệu của bàn theo số bàn
    def load_data_table_popup(self):
        pass
    def validate_input(self, new_value):
        # Kiểm tra xem giá trị mới có phải là số không
        try:
            float(new_value)
            return True
        except ValueError:
            return False

    def click_button(self, action_type):
        table_num_value = self.entry_table_num.get()
        seat_num_value = self.entry_seat_num.get()
        status_value = self.status_combox.get()
        if action_type == Action.ADD:
            if table_num_value == '' and seat_num_value == '':
                self.lb_validate_table_info.configure(text="Vui lòng điền đầy đủ thông tin")
                return
            else:
                # Thực hiện thêm vào database
                self.__controller.add_table_to_db(table_num_value, seat_num_value, status_value)
                self.toplevel.destroy()
        else:
            # Thực hiện cập nhật lại database
            self.__controller.update_table_to_db(table_num_value, seat_num_value, status_value)
        print(table_num_value, seat_num_value, status_value)


