import tkinter as tk
from tkinter import ttk
from ctypes import windll
from employee_controller import EmployeeController
from employee_model import EmployeeModel
from share.common_config import Gender, Action, UserActive
from share.utils import Utils
import customtkinter as ctk
import tkinter.messagebox as tkMsgBox


class EmployeeView:
    columns = ("no",
               "user_code",
               'full_name',
               'birth_date',
               'identity',
               'gender',
               'income_date',
               'phone_number',
               'email',
               'address',
               'user_name',
               'password',
               'status',
               'type',
               'created_date',
               'updated_date')

    def __init__(self, parent: ctk.CTkFrame):
        ctk.set_default_color_theme("../../share/theme.json")
        self.__controller = EmployeeController()
        self.__employee_model = EmployeeModel()

        # Tree
        self.__tree = None
        self.__id_selected = -1

        # Init UI
        self.__add_or_update_form = dict()
        self.init_view(parent)

    def init_action_form(self, container: ctk.CTkFrame):
        # Create form include: Them, Xoa, Cap Nhat and Tim Kiem by full name, employee id, username
        action_frame = ctk.CTkFrame(container)

        # Add button
        add_button = ctk.CTkButton(action_frame,
                                text="Thêm",
                                width=100,
                                fg_color="blue",
                                command=lambda: self.init_add_or_update_popup(container, Action.ADD))
        add_button.pack(side=tk.LEFT, padx=10, pady=10, anchor="w")

        # Update button
        update_btn = ctk.CTkButton(action_frame,
                               text="Cập nhật",
                               width=100,
                               fg_color="green",
                                command=lambda: self.init_add_or_update_popup(container, Action.UPDATE))
        update_btn.pack(side=tk.LEFT, padx=10, pady=10, anchor="w")

        # Delete button
        delete_btn = ctk.CTkButton(action_frame,
                               text="Xoá",
                               width=100,
                               fg_color="red",
                                command = lambda: self.delete_item())
        delete_btn.pack(side=tk.LEFT, padx=10, pady=10, anchor="w")

        # Search controls
        search_frame = ctk.CTkFrame(action_frame)
        search_ent = ctk.CTkEntry(master=search_frame, width=500)
        search_ent.pack(side=tk.LEFT, fill='none', anchor='e', expand=True ,padx=5, pady=5)
        search_btn = ctk.CTkButton(search_frame,
                               text="Tìm",
                               width=100,
                               fg_color="purple",
                                command=lambda: self.search(search_ent.get()))
        search_btn.pack(side=tk.LEFT, fill='x', anchor=tk.W, expand=False)
        search_frame.pack(side=tk.LEFT, expand=True, anchor='center', fill=tk.X, ipadx=5, ipady=5, padx=5, pady=5)
        return action_frame

    def init_add_or_update_popup(self, parent: ctk.CTkFrame, action: Action):
        # Create add new or update employee information popup
        top = ctk.CTkToplevel(parent)

        top.geometry("900x600")
        top.title("Thông tin nhân viên")
        top.resizable(True, False)

        emp_frame = ctk.CTkFrame(top, width=700)
        column1 = ctk.CTkFrame(emp_frame)
        column2 = ctk.CTkFrame(emp_frame)
        column3 = ctk.CTkFrame(emp_frame)

        # Column 1;
        emp_info_lbl = ctk.CTkLabel(column1, text="Thông tin nhân viên: ", font=('TkDefaultFont', 11, 'bold'))
        emp_info_lbl.pack(**Utils.heading_group_pack)

        # Employee Id
        emp_id_frm = ctk.CTkFrame(column1)
        emp_id_lbl = ctk.CTkLabel(emp_id_frm, text="Mã nhân viên: ")
        emp_id_lbl.pack(**Utils.label_pack_style)

        emp_id_var = tk.StringVar()
        if action == Action.ADD:
            new_emp_id = self.__controller.get_new_emp_id()
            emp_id_var.set(new_emp_id)
            self.__add_or_update_form['employee_id'] = ctk.CTkEntry(master=emp_id_frm, state=tk.DISABLED, textvariable=emp_id_var)
        if action == Action.UPDATE:
            self.__add_or_update_form['employee_id'] = ctk.CTkEntry(master=emp_id_frm, state=tk.DISABLED, textvariable=emp_id_var)

        self.__add_or_update_form['employee_id'].pack(**Utils.entry_pack_style)
        emp_id_frm.pack(**Utils.sub_frame_style)

        self.__add_or_update_form['first_name_ent'] = Utils.input_component(column1, {'lbl': "Họ: "})
        self.__add_or_update_form['last_name_ent'] = Utils.input_component(column1, {'lbl': "Tên: "})
        self.__add_or_update_form['birthday_dpk'] = (Utils.date_picker_component(column1, {'lbl': "Ngày sinh: "}))
        self.__add_or_update_form['identity_ent'] = Utils.input_component(column1, {'lbl': "CCCD/CMND: "})

        # Column 2:
        ctk.CTkLabel(column2, text="").pack(**Utils.label_pack_style)

        # Gender
        self.__add_or_update_form['gender'] = tk.StringVar()
        gender_frm = ctk.CTkFrame(column2)
        gender_lbl = ctk.CTkLabel(gender_frm, text="Giới tính: ")
        gender_lbl.pack(**Utils.label_pack_style)
        self.__add_or_update_form['male_rad'] = ctk.CTkRadioButton(gender_frm, text='Nam', value=Gender.MALE.value,
                                   variable=self.__add_or_update_form['gender'])
        self.__add_or_update_form['male_rad'].pack(side=tk.LEFT, anchor="center", fill=tk.BOTH, expand=True)
        self.__add_or_update_form['female_rad'] = ctk.CTkRadioButton(gender_frm, text='Nữ', value=Gender.FEMALE.value,
                                     variable=self.__add_or_update_form['gender'])
        self.__add_or_update_form['female_rad'].pack(side=tk.LEFT, anchor="center", fill=tk.BOTH, expand=True)
        self.__add_or_update_form['other_rad'] = ctk.CTkRadioButton(gender_frm, text='Khác', value=Gender.OTHER.value,
                                    variable=self.__add_or_update_form['gender'])
        self.__add_or_update_form['other_rad'].pack(side=tk.LEFT, anchor='center', fill=tk.BOTH, expand=True)
        gender_frm.pack(**Utils.radio_group_style)

        self.__add_or_update_form['income_date_dpk'] = Utils.date_picker_component(column2, {'lbl': "Ngày vào làm: "})
        self.__add_or_update_form['phone_number_ent'] = Utils.input_component(column2, {'lbl': "Số điện thoại: "})
        self.__add_or_update_form['email_ent'] = Utils.input_component(column2, {'lbl': "Email: "})
        self.__add_or_update_form['address_ent'] = Utils.input_component(column2, {'lbl': "Địa chỉ: "})

        # Column 3:
        account_info_lbl = ctk.CTkLabel(column3, text="Thông tin tài khoản: ", font=('TkDefaultFont', 11, 'bold'))
        account_info_lbl.pack(**Utils.heading_group_pack)

        self.__add_or_update_form['username_ent'] = Utils.input_component(column3, {'lbl': "Tên tài khoản: "})
        self.__add_or_update_form['password_ent'] = Utils.input_component(column3, {'lbl': "Mật khẩu: "})

        # Account status
        self.__add_or_update_form['status'] = tk.StringVar()
        status_frm = ctk.CTkFrame(column3)

        status_lbl = ctk.CTkLabel(status_frm, text="Trạng thái tài khoản: ")
        status_lbl.pack(**Utils.label_pack_style)
        self.__add_or_update_form['active_rad'] = ctk.CTkRadioButton(status_frm, text='Hoạt động', value=UserActive.ACTIVE.value,
                                     variable=self.__add_or_update_form['status'])
        self.__add_or_update_form['active_rad'].pack(side=tk.TOP, anchor="w")
        self.__add_or_update_form['inactive_rad'] = ctk.CTkRadioButton(status_frm, text='Không hoạt động', value=UserActive.INACTIVE.value,
                                       variable=self.__add_or_update_form['status'])
        self.__add_or_update_form['inactive_rad'].pack(side=tk.TOP, anchor='w')
        status_frm.pack(**Utils.entry_pack_style)

        # Account Type
        type_lbl = ctk.CTkLabel(column3, text="Loại tài khoản: ")
        type_lbl.pack(**Utils.label_pack_style)
        self.__add_or_update_form['type_cbo'] = ctk.CTkComboBox(column3, values=["Admin", "Bình thường"])
        self.__add_or_update_form['type_cbo'].pack(**Utils.entry_pack_style)

        # Set data for entry on update form
        if action == Action.UPDATE:
            emp_by_id = self.__controller.get_emp_by_id(self.__id_selected)
            self.set_value_for_entry(emp_by_id)

        column1.pack(side=tk.LEFT, fill='x', expand=True, anchor='n')
        column2.pack(side=tk.LEFT, fill='x', expand=True, anchor='n')
        column3.pack(side=tk.LEFT, fill='x', expand=True, anchor='n')
        emp_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, anchor='w')

        # Add or Update button
        save_or_update_txt = ""
        if action == Action.UPDATE:
            save_or_update_txt = "Cập nhật"
        else:
            save_or_update_txt = "Thêm"
        button_grp = ctk.CTkFrame(top)
        save_or_update_btn = ctk.CTkButton(button_grp,
                                       text=save_or_update_txt,
                                       width=10,
                                       fg_color="blue",
                                       command=self.save_data)
        save_or_update_btn.pack(side=tk.LEFT, padx=10, pady=10, expand=False)

        # Clear button
        clear_btn = ctk.CTkButton(button_grp,
                              text="Làm sạch",
                              width=10,
                              fg_color="gray")
        clear_btn.bind("<Button>", self.clear_data())
        clear_btn.pack(side=tk.LEFT, padx=10, pady=10, expand=True)
        button_grp.pack(side=tk.TOP, padx=10, pady=10, anchor="center", fill=tk.BOTH, expand=False)

    def set_value_for_entry(self, data):
        if data:
            self.set_value_for_widget('employee_id', data.user_code)
            self.set_value_for_widget('first_name_ent', data.first_name)
            self.set_value_for_widget('last_name_ent', data.last_name)
            self.set_value_for_widget('birthday_dpk', data.birth_date)
            self.set_value_for_widget('identity_ent', data.identity)
            # self.set_value_for_widget('gender', Utils.get_gender(data.gender))

            # self.__add_or_update_form['gender'].set(Utils.get_gender(data.gender))


            self.set_value_for_widget('income_date_dpk', data.income_date)
            self.set_value_for_widget('phone_number_ent', data.phone_number)
            self.set_value_for_widget('email_ent', data.email)
            self.set_value_for_widget('address_ent', data.address)
            self.set_value_for_widget('username_ent', data.user_name)
            self.set_value_for_widget('password_ent', data.password)
            self.set_value_for_widget('status', data.status)
            self.set_value_for_widget('type_cbo', Utils.get_account_type_str(data.type))

    def set_value_for_radio_btn(self, value, rad_type):
        # rad_type is gender (0) or status(1)
        print("gender:", value)
        if rad_type == 0:
            if value == Gender.MALE:
                self.__add_or_update_form['male_rad'].select()
            elif value == Gender.FEMALE:
                self.__add_or_update_form['female_rad'].select()
            elif value == Gender.OTHER:
                self.__add_or_update_form['other_rad'].select()
        elif rad_type == 1:
            if value == UserActive.ACTIVE:
                self.__add_or_update_form['active_rad'].select()
            elif value == UserActive.INACTIVE:
                self.__add_or_update_form['inactive_rad'].select()




    def set_value_for_entry(self, widget_name:str, new_value):
        self.__add_or_update_form[widget_name].delete(0, ctk.END)
        self.__add_or_update_form[widget_name].insert(0, new_value)

    def delete_item(self):
        print("Delete item")

    def search(self, keyword: str):
       print("keyword: ", keyword)

    def clear_data(self):
        pass

    def validation_add_or_update_form(self, **form_data):
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
        data = {'user_code': employeeId,
                'first_name': firstName,
                'last_name': lastName,
                'birth_date': birthday,
                'identity': identity,
                'gender': gender,
                'income_date': incomeDate,
                'phone_number': phone_number,
                'email': email,
                'address': address,
                'user_name': username,
                'password': password,
                "status": status,
                "type": Utils.get_account_type_value(type)}
        self.validation_add_or_update_form(**data)
        if self.__controller.save(**data) == 1:
            tkMsgBox.showinfo("Thông báo", "Thêm thành công!")
        else:
            tkMsgBox.showinfo("Thông báo", "Thêm thất bại!")

    def set_data_entry(self, field, data):
        pass
        # self.employee_fields[field].delete(0, END)
        # self.employee_fields[field].insert(0, data)

    def on_row_selected(self, event):
        for item in self.__tree.selection():
            record = self.__tree.item(item)['values']
            if record[len(record) - 1]:
                self.__id_selected = record[len(record) - 1]

    def init_employee_grid_data(self, parent):
        # Define column for grid
        self.__tree = ttk.Treeview(parent, columns=EmployeeView.columns, show='headings')

        self.__tree.heading(EmployeeView.columns[0], text='No')
        self.__tree.heading(EmployeeView.columns[1], text='Mã nhân viên')
        self.__tree.heading(EmployeeView.columns[2], text='Họ & tên')
        self.__tree.heading(EmployeeView.columns[3], text='Ngày sinh')
        self.__tree.heading(EmployeeView.columns[4], text='CCCD/CMND')
        self.__tree.heading(EmployeeView.columns[5], text='Giới tính')
        self.__tree.heading(EmployeeView.columns[6], text='Ngày vào làm')
        self.__tree.heading(EmployeeView.columns[7], text='Số điện thoại')
        self.__tree.heading(EmployeeView.columns[8], text='Email')
        self.__tree.heading(EmployeeView.columns[9], text='Địa chỉ')
        self.__tree.heading(EmployeeView.columns[10], text='Tên tài khoản')
        self.__tree.heading(EmployeeView.columns[11], text='Trạng thái tài khoản')
        self.__tree.heading(EmployeeView.columns[12], text='Loại nhân viên')
        self.__tree.heading(EmployeeView.columns[13], text='Ngày tạo')

        self.__tree.column(EmployeeView.columns[0], width=50, anchor='center')
        self.__tree.column(EmployeeView.columns[1], anchor='center')
        self.__tree.column(EmployeeView.columns[2], anchor='center')
        self.__tree.column(EmployeeView.columns[3], anchor='center')
        self.__tree.column(EmployeeView.columns[4], anchor='center')
        self.__tree.column(EmployeeView.columns[5], anchor='center')
        self.__tree.column(EmployeeView.columns[6], anchor='center')
        self.__tree.column(EmployeeView.columns[7], anchor='center')
        self.__tree.column(EmployeeView.columns[8], anchor='center')
        self.__tree.column(EmployeeView.columns[9], anchor='center')
        self.__tree.column(EmployeeView.columns[10], anchor='center')
        self.__tree.column(EmployeeView.columns[11], anchor='center')
        self.__tree.column(EmployeeView.columns[12], anchor='center')
        self.__tree.column(EmployeeView.columns[13], anchor='center')

        # Set color for odd and even row in grid
        self.__tree.tag_configure('odd', background='#E8E8E8')
        self.__tree.tag_configure('even', background='#DFDFDF')

        # Fill data to tree
        emp_list = self.__controller.get_list()
        if len(emp_list) > 0:
            for emp in emp_list:
                self.__tree.insert('', tk.END, values=emp)

        # Bind event when row selected
        self.__tree.bind("<<TreeviewSelect>>", self.on_row_selected)

    def init_view(self, parent: ctk.CTkFrame):

        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(0, weight=1)
        parent.rowconfigure(1, weight=9)

        action_form = self.init_action_form(parent)
        action_form.grid(column=0, row=0, sticky='nwse')

        wrap_grid = ctk.CTkFrame(parent)

        self.init_employee_grid_data(wrap_grid)
        self.__tree.grid(column=0, row=0, sticky='ns')

        # Add scroll for grid
        tree_scroll = ctk.CTkScrollbar(wrap_grid, command=self.__tree.xview, width=200, orientation="horizontal")
        tree_scroll.grid(row=1, column=0, sticky="ew")

        self.__tree.configure(xscrollcommand=tree_scroll.set)

        wrap_grid.grid(row=1, column=0, sticky='ns')


if __name__ == '__main__':
    windll.shcore.SetProcessDpiAwareness(1)
    root = ctk.CTk()
    # root.attributes('-fullscreen', True)
    root.state("zoomed")  # full screen
    root.resizable(True, True)
    # root.wm_attributes("-topmost", 1)
    root.focus_set()
    root.iconbitmap('../../assets/restaurant.ico')
    root.title("Restaurant Information")

    exFrame = ctk.CTkFrame(root)
    exFrame.pack(side='top', fill='both', expand=True)

    employee_view = EmployeeView(exFrame)

    root.mainloop()
