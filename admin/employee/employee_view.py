import tkinter as tk
from tkinter import END, ttk
from ctypes import windll
from employee_controller import EmployeeController
from employee_model import EmployeeModel
from share.common_config import Gender, Action, UserActive
from share.utils import Utils

class EmployeeView:

    def __init__(self, container: tk.Tk):
        self.controller = EmployeeController()
        self.__tree = None
        self.__add_or_update_form = dict()
        self.__employee_model = EmployeeModel()
        self.init_view(container)

    def init_action_form(self, container: tk.Tk):
        # Create form include Them, Xoa, Cap Nhat and Tim Kiem by full name, employee id, user name

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
        # Create add new or update employee information popup

        # Form fields:
        # empId = tk.StringVar()
        # firstName = tk.StringVar()

        top = tk.Toplevel(container)

        top.geometry("900x600")
        top.title("Thêm hoặc cập nhật nhân viên")
        top.resizable(True, False)

        emp_frame = tk.Frame(top, width=700)
        column1 = tk.Frame(emp_frame)
        column2 = tk.Frame(emp_frame)
        column3 = tk.Frame(emp_frame)

        # Column 1;
        emp_info_lbl = ttk.Label(column1, text="Thông tin nhân viên: ", font=('TkDefaultFont', 11, 'bold'))
        emp_info_lbl.pack(Utils.heading_group_pack)

        # Employee Id
        emp_id_frm = tk.Frame(column1)
        emp_id_lbl = ttk.Label(emp_id_frm, text="Mã nhân viên: ")
        emp_id_lbl.pack(Utils.label_pack_style)
        self.__add_or_update_form['employee_id'] = ttk.Entry(master=emp_id_frm)
        if action == Action.UPDATE:
            self.__add_or_update_form['employee_id'].config(state=tk.DISABLED)
        self.__add_or_update_form['employee_id'].pack(Utils.entry_pack_style)
        emp_id_frm.pack(Utils.sub_frame_style)

        self.__add_or_update_form['first_name_ent'] = Utils.input_component(column1, {'lbl': "Họ: "})
        self.__add_or_update_form['last_name_ent'] = Utils.input_component(column1, {'lbl': "Tên: "})
        self.__add_or_update_form['birthday_dpk'] = Utils.date_picker_component(column1, {'lbl': "Ngày sinh: "})
        self.__add_or_update_form['identity_ent'] = Utils.input_component(column1, {'lbl': "CCCD/CMND: "})

        # Column 2:
        ttk.Label(column2, text="").pack(Utils.label_pack_style)

        # Gender
        self.__add_or_update_form['gender'] = tk.StringVar()
        gender_frm = tk.Frame(column2)
        gender_lbl = ttk.Label(gender_frm, text="Giới tính: ")
        gender_lbl.pack(Utils.label_pack_style)
        male_rad = ttk.Radiobutton(gender_frm, text='Nam', value=Gender.MALE, variable=self.__add_or_update_form['gender'])
        male_rad.pack(side=tk.LEFT, anchor="center", fill=tk.BOTH, expand=True)
        female_rad = ttk.Radiobutton(gender_frm, text='Nữ', value=Gender.FEMALE, variable=self.__add_or_update_form['gender'])
        female_rad.pack(side=tk.LEFT, anchor="center", fill=tk.BOTH, expand=True)
        other_rad = ttk.Radiobutton(gender_frm, text='Khác', value=Gender.OTHER, variable=self.__add_or_update_form['gender'])
        other_rad.pack(side=tk.LEFT, anchor='center', fill=tk.BOTH, expand=True)
        gender_frm.pack(Utils.radio_group_style)

        self.__add_or_update_form['income_date_dpk'] = Utils.date_picker_component(column2, {'lbl': "Ngày vào làm: "})
        self.__add_or_update_form['phone_number_ent'] = Utils.input_component(column2, {'lbl': "Số điện thoại: "})
        self.__add_or_update_form['email_ent'] = Utils.input_component(column2, {'lbl': "Email: "})
        self.__add_or_update_form['address_ent'] = Utils.input_component(column2, {'lbl': "Địa chỉ: "})

        # Column 3:
        account_info_lbl = ttk.Label(column3, text="Thông tin tài khoản: ", font=('TkDefaultFont', 11, 'bold'))
        account_info_lbl.pack(Utils.heading_group_pack)

        self.__add_or_update_form['username_ent'] = Utils.input_component(column3, {'lbl': "Tên tài khoản: "})
        self.__add_or_update_form['password_ent'] = Utils.input_component(column3, {'lbl': "Mật khẩu: "})

        # Account status
        self.__add_or_update_form['status'] = tk.StringVar()
        status_frm = tk.Frame(column3)
        status_lbl = ttk.Label(status_frm, text="Trạng thái tài khoản: ")
        status_lbl.pack(Utils.label_pack_style)
        active_rad = ttk.Radiobutton(status_frm, text='Hoạt động', value=UserActive.ACTIVE, variable=self.__add_or_update_form['status'])
        active_rad.pack(side=tk.TOP, anchor="w")
        inactive_rad = ttk.Radiobutton(status_frm, text='Không hoạt động', value=UserActive.INACTIVE, variable=self.__add_or_update_form['status'])
        inactive_rad.pack(side=tk.TOP, anchor='w')
        status_frm.pack(Utils.entry_pack_style, anchor='w')

        # Account Type
        type_lbl = ttk.Label(column3, text="Loại tài khoản: ")
        type_lbl.pack(Utils.label_pack_style)
        self.__add_or_update_form['type_cbo'] = ttk.Combobox(column3)
        self.__add_or_update_form['type_cbo']['value'] = ("Admin", "Bình thường")
        self.__add_or_update_form['type_cbo'].pack(Utils.entry_pack_style)

        column1.pack(side=tk.LEFT, fill='x', expand=True, anchor='n')
        column2.pack(side=tk.LEFT, fill='x', expand=True, anchor='n')
        column3.pack(side=tk.LEFT, fill='x', expand=True, anchor='n')
        emp_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, anchor='w')

        # Add or Update botton
        save_or_update_txt = ""
        if action == Action.UPDATE:
            save_or_update_txt = "Cập nhật"
        else:
            save_or_update_txt = "Thêm"
        button_grp = tk.Frame(top)
        save_or_update_btn = tk.Button(button_grp,
                                       text=save_or_update_txt,
                                       width=10,
                                       bg='blue',
                                       fg="white",
                                       command=self.save_data)
        save_or_update_btn.pack(side=tk.LEFT, padx=10, pady=10, anchor="center", fill="x", expand=True)

        # Clear button
        clear_btn = tk.Button(button_grp,
                              text="Làm sạch",
                              width=10,
                              bg='grey',
                              fg="white")
        clear_btn.bind("<Button>", self.clear_data())
        clear_btn.pack(side=tk.LEFT, padx=10, pady=10, anchor="center", fill="x", expand=True)
        button_grp.pack(side=tk.TOP, padx=10, pady=10, anchor="center", fill=tk.BOTH, expand=True)

    def clear_data(self):
        pass

    def save_data(self):
        employeeId = self.__add_or_update_form['employee_id'].get()
        firstName = self.__add_or_update_form['first_name_ent'].get()
        lastName = self.__add_or_update_form['last_name_ent'].get()
        birthday = self.__add_or_update_form['birthday_dpk'].get()
        identity = self.__add_or_update_form['identity_ent'].get()
        gender = self.__add_or_update_form['gender'].get()
        incomeDate = self.__add_or_update_form['income_date_dpk'].get()
        phone_number = self.__add_or_update_form['phone_number_ent'].get()
        email = self.__add_or_update_form['email_ent'].get()
        address = self.__add_or_update_form['address_ent'].get()
        username = self.__add_or_update_form['username_ent'].get()
        password = self.__add_or_update_form['password_ent'].get()
        status = self.__add_or_update_form['status'].get()
        type = self.__add_or_update_form['type_cbo'].get()
        print(employeeId, firstName, lastName, birthday, identity, gender, incomeDate, phone_number, email, address, username, password, status, type)


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
        # scrollbarx = tk.Scrollbar(container, orient='horizontal', command=grid_data.xview, width=20)
        # scrollbary = tk.Scrollbar(container, orient='vertical', command=grid_data.yview, width=20)
        # grid_data.configure(xscroll=scrollbarx.set)
        # grid_data.configure(yscroll=scrollbary.set)
        # scrollbarx.grid(column=0, row=2, sticky='nwse', columnspan=2)
        # scrollbary.grid(column=1, row=1, sticky='nwse', rowspan=2)


if __name__ == '__main__':
    windll.shcore.SetProcessDpiAwareness(1)
    root = tk.Tk()
    root.resizable(True, True)
    root.state('zoomed')  # full screen
    root.iconbitmap('../../assets/restaurant.ico')
    root.title("Restaurant Information")

    employee_view = EmployeeView(root)

    root.mainloop()
