import tkinter as tk
from tkinter import END, ttk
from tkinter.messagebox import showinfo
from tkcalendar import Calendar, DateEntry
import random
from PIL import ImageTk, Image

from employee_controller import EmployeeController
from employee_model import EmployeeModel
from share.common_config import Gender, Action, UserActive
from share.utils import Utils


class EmployeeView(tk.Frame):

    def __init__(self, container: tk.Tk):
        self.controller = EmployeeController()
        self.employee_fields = {}
        self.__tree = None
        # self.__emp_model = EmployeeModel()
        self.init_view(container)

    def init_action_form(self, container: tk.Tk):
        action_frame = ttk.Frame(container)
        # Add button
        add_button = tk.Button(action_frame,
                               text="Thêm",
                               width=10,
                               bg='blue',
                               fg="white")
        add_button.bind("<Button>", lambda event, ctn=container: self.init_add_or_update_popup(ctn, Action.ADD))
        add_button.pack(side=tk.LEFT, padx=10, pady=10, anchor="w")

        # Update button
        update_btn = tk.Button(action_frame,
                               text="Cập nhật",
                               width=10,
                               bg='green',
                               fg="white")
        update_btn.pack(side=tk.LEFT, padx=10, pady=10, anchor="w")
        update_btn.bind("<Button>", lambda event, ctn=container: self.init_add_or_update_popup(ctn, Action.UPDATE))

        # Delete button
        delete_btn = tk.Button(action_frame,
                               text="Xoá",
                               width=10,
                               bg='red',
                               fg="white")
        delete_btn.pack(side=tk.LEFT, padx=10, pady=10, anchor="w")

        # Search controls
        search_frame = tk.Frame(action_frame)
        search_ent = ttk.Entry(master=search_frame)
        search_ent.pack(side=tk.LEFT, fill=tk.X, anchor='center', expand=True, ipadx=5, ipady=5, padx=10, pady=10)
        search_btn = tk.Button(search_frame,
                               text="Tìm",
                               width=10,
                               bg='blue',
                               fg="white")
        search_btn.pack(side=tk.LEFT, fill='x', anchor=tk.W, expand=False)
        search_frame.pack(side=tk.LEFT, expand=True, anchor='center', fill=tk.X, ipadx=5, ipady=5, padx=10, pady=10)

        return action_frame

    def init_add_or_update_popup(self, container: tk.Tk, action: Action):

        # Create child windows
        top = tk.Toplevel(container)

        top.geometry("900x600")
        top.title("Thêm hoặc cập nhật nhân viên")
        top.resizable(True, False)

        emp_frame = tk.Frame(top, width=700)
        column1 = tk.Frame(emp_frame, highlightthickness=1, highlightbackground="#9c9")
        column2 = tk.Frame(emp_frame, highlightthickness=1, highlightbackground="#9c9")
        column3 = tk.Frame(emp_frame, highlightthickness=1, highlightbackground="#9c9")

        label_pack_style = {'side':tk.TOP, 'expand':True, 'padx':10, 'pady':5, 'anchor':tk.W, 'fill':tk.X}
        entry_pack_style = {'side':tk.TOP, 'expand':True, 'anchor':tk.W, 'padx':10, 'pady':5, 'ipadx': 3, 'ipady': 3, 'fill':tk.X}
        sub_frame_style = {'side':tk.TOP, 'expand':True, 'anchor':tk.W, 'pady':10, 'fill':tk.X}

        ## Column 1
        emp_info_lbl = ttk.Label(column1, text="Thông tin nhân viên: ",)
        emp_info_lbl.pack(label_pack_style)

        ### Employee Id
        emp_id_frm = tk.Frame(column1)
        emp_id_lbl = ttk.Label(emp_id_frm, text="Mã nhân viên: ")
        emp_id_lbl.pack(Utils.label_pack_style)
        emp_id_ent = ttk.Entry(master=emp_id_frm)
        if action == Action.UPDATE:
            emp_id_ent.config(state=tk.DISABLED)
        emp_id_ent.pack(Utils.entry_pack_style)
        emp_id_frm.pack(Utils.sub_frame_style)

        first_name_ent = Utils.input_component(column1, {'lbl': "Họ: "})
        first_name_ent = Utils.input_component(column1, {'lbl': "Tên: "})
        birthday_dpk = Utils.date_picker_component(column1, {'lbl': "Ngày sinh: "})
        identity_ent = Utils.input_component(column1, {'lbl': "CCCD/CMND: "})

        ### Gender
        gender_frm = tk.Frame(column1)
        gender_lbl = ttk.Label(gender_frm, text="Giới tính: ")
        gender_lbl.pack(label_pack_style)
        male_rad = ttk.Radiobutton(gender_frm, text='Nam', value=Gender.FEMALE)
        male_rad.pack(side=tk.LEFT, anchor="w")
        female_rad = ttk.Radiobutton(gender_frm, text='Nữ', value=Gender.MALE)
        female_rad.pack(side=tk.LEFT, anchor="w")
        other_rad = ttk.Radiobutton(gender_frm, text='Other', value=Gender.OTHER)
        other_rad.pack(side=tk.LEFT, anchor='w')
        gender_frm.pack(entry_pack_style)

        # Column 2:
        ttk.Label(column2, text="").pack(label_pack_style)

        income_date_dpk = Utils.date_picker_component(column2, {'lbl': "Ngày vào làm: "})
        phone_number_lbl = Utils.input_component(column2, {'lbl': "Số điện thoại: "})
        email_ent = Utils.input_component(column2, {'lbl': "Email: "})

        address_ent = Utils.date_picker_component(column2, {'lbl': "Địa chỉ: "})

        # Column 2
        account_info_lbl = ttk.Label(column3, text="Thông tin tài khoản: ")
        account_info_lbl.pack(label_pack_style)

        username_ent = Utils.input_component(column3, {'lbl': "Tên tài khoản: "})
        password_ent = Utils.input_component(column3, {'lbl': "Mật khẩu: "})

        status_frm = tk.Frame(column3, pady=50)
        status_lbl = ttk.Label(status_frm, text="Trạng thái tài khoản: ")
        status_lbl.pack(label_pack_style)
        active_rad = ttk.Radiobutton(status_frm, text='Hoạt động', value=UserActive.ACTIVE)
        active_rad.pack(side=tk.TOP, anchor="w")
        inactive_rad = ttk.Radiobutton(status_frm, text='Không hoạt động', value=UserActive.INACTIVE)
        inactive_rad.pack(side=tk.TOP, anchor='w')
        status_frm.pack(entry_pack_style, anchor='w')

        type_lbl = ttk.Label(column3, text="Loại tài khoản: ")
        type_lbl.pack(label_pack_style)
        type_cbo = ttk.Combobox(column3)
        type_cbo['value'] = ("Admin", "Bình thường")
        type_lbl.pack(side=tk.TOP, anchor=tk.W, padx=10, pady=5)

        column1.pack(side=tk.LEFT, fill='x', expand=True, anchor='n')
        column2.pack(side=tk.LEFT, fill='x', expand=True, anchor='n')
        column3.pack(side=tk.LEFT, fill='x', expand=True, anchor='n')
        emp_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, anchor='w')

    def set_data_entry(self, field, data):
        pass
        # self.employee_fields[field].delete(0, END)
        # self.employee_fields[field].insert(0, data)

    def row_selected(self, event):
        pass
        # for selected_item in self.employee_fields['tree'].selection():
        #     record = self.employee_fields['tree'].item(selected_item)['values']
        #     print(record)
        #
        #     self.set_data_entry("no", record[0])
        #     self.set_data_entry("userCode", record[1])
        #     self.set_data_entry("fullName", record[2])
        #     self.set_data_entry("birthDate", record[3])
        #     self.set_data_entry("identity", record[4])
        #     self.set_data_entry("gender", record[5])
        #     self.set_data_entry("incomeDate", record[6])
        #     self.set_data_entry("phoneNumber", record[7])
        #     self.set_data_entry("email", record[8])
        #     self.set_data_entry("address", record[9])
        #     self.set_data_entry("userName", record[10])
        #     self.set_data_entry("status", record[11])
        #     self.set_data_entry("type", record[12])
        #     self.set_data_entry("createdDate", record[13])

    def init_employee_grid_data(self, container, emp_list):
        # Define column for grid
        columns = ("no",
                   "userCode",
                   'fullName',
                   'birthDate',
                   'identity',
                   'gender',
                   'incomeDate',
                   'phoneNumber',
                   'email',
                   'address',
                   'userName',
                   'status',
                   'type',
                   'createdDate')

        tree = ttk.Treeview(container, columns=columns, show='headings')

        tree.heading('no', text='Id')
        tree.heading('userCode', text='Mã nhân viên')
        tree.heading('fullName', text='Họ & tên')
        tree.heading('birthDate', text='Ngày sinh')
        tree.heading('identity', text='CCCD/CMND')
        tree.heading('gender', text='Giới tính')
        tree.heading('incomeDate', text='Ngày vào làm')
        tree.heading('phoneNumber', text='Số điện thoại')
        tree.heading('email', text='Email')
        tree.heading('address', text='Địa chỉ')
        tree.heading('userName', text='Tên tài khoản')
        tree.heading('status', text='Trạng thái tài khoản')
        tree.heading('type', text='Loại nhân viên')
        tree.heading('createdDate', text='Ngày tạo')

        tree.column("no", anchor='center', width=50)
        tree.column("userCode", anchor='center')
        tree.column("fullName", anchor='w')
        tree.column("birthDate", anchor='center')
        tree.column("identity", anchor='w')
        tree.column("gender", anchor='center')
        tree.column("incomeDate", anchor='center')
        tree.column("phoneNumber", anchor='center')
        tree.column("email", anchor='w')
        tree.column("address", anchor='w')
        tree.column("userName", anchor='w')
        tree.column("status", anchor='center')
        tree.column("type", anchor='center')
        tree.column("createdDate", anchor='center')

        # Set color for odd and even row in grid
        tree.tag_configure('odd', background='#E8E8E8')
        tree.tag_configure('even', background='#DFDFDF')

        # Fill data to tree
        if emp_list.__len__() > 0:
            for emp in emp_list:
                tree.insert('', tk.END, values=emp)

        # Bind event when row selected
        tree.bind("<<TreeviewSelect>>", self.row_selected)

        return tree

    def init_view(self, container: tk.Tk):
        container.columnconfigure(0, weight=1)
        container.rowconfigure(0, weight=1)
        container.rowconfigure(1, weight=9)

        action_form = self.init_action_form(container)
        action_form.grid(column=0, row=0, sticky='nwse')

        grid_data = self.init_employee_grid_data(container, [])
        grid_data.grid(column=0, row=1, sticky='nwse')

        # Add scroll for grid
        scrollbarx = tk.Scrollbar(container, orient='horizontal', command=grid_data.xview, width=20)
        scrollbary = tk.Scrollbar(container, orient='vertical', command=grid_data.yview, width=20)
        grid_data.configure(xscroll=scrollbarx.set)
        grid_data.configure(yscroll=scrollbary.set)
        scrollbarx.grid(column=0, row=2, sticky='nwse', columnspan=2)
        scrollbary.grid(column=1, row=1, sticky='nwse', rowspan=2)


if __name__ == '__main__':
    # windll.shcore.SetProcessDpiAwareness(1)
    root = tk.Tk()
    root.resizable(True, True)
    root.state('zoomed')  # full screen
    root.iconbitmap('../../assets/restaurant.ico')
    root.title("Restaurant Information")

    employee_view = EmployeeView(root)

    root.mainloop()
