import tkinter as tk
from tkinter import ttk
from employee.employee_controller import EmployeeController
from employee.employee_model import EmployeeModel
from share.common_config import Gender, Action, UserStatus
from share.utils import Utils
import customtkinter as ctk
import tkinter.messagebox as tkMsgBox
import datetime


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
               'col1',
               'col2'
               'col3'
               )

    def __init__(self, parent: ctk.CTkFrame):
        ctk.set_default_color_theme("../share/theme.json")
        self.__controller = EmployeeController()
        self.__employee_model = EmployeeModel()

        # Tree view
        self.__tree = None
        self.__id_selected = -1

        # Init UI
        self.__add_or_update_form = dict()
        self.init_view(parent)
        self.__popup = None

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
                                   command=lambda: self.delete_item())
        delete_btn.pack(side=tk.LEFT, padx=10, pady=10, anchor="w")

        # Search controls
        search_frame = ctk.CTkFrame(action_frame, fg_color=Utils.WHITE)
        search_ent = ctk.CTkEntry(master=search_frame, width=500)
        search_ent.pack(side=tk.LEFT, fill='none', anchor='e', expand=True, padx=5, pady=5)
        search_btn = ctk.CTkButton(search_frame,
                                   text="Tìm",
                                   width=100,
                                   fg_color="purple",
                                   command=lambda: self.search(search_ent.get()))
        search_btn.pack(side=tk.LEFT, fill='x', anchor=tk.W, expand=False)
        search_frame.pack(side=tk.LEFT, expand=True, anchor='center', fill=tk.X, ipadx=5, ipady=5, padx=5, pady=5)
        return action_frame

    def init_add_or_update_popup(self, parent: ctk.CTkFrame, action: Action):

        if action == Action.UPDATE and self.__id_selected < 1:
            return

        # Create add new or update employee information popup
        self.__popup = ctk.CTkToplevel(parent)

        self.__popup.geometry("900x600")
        self.__popup.title("Thông tin nhân viên")
        self.__popup.resizable(False, False)
        self.__popup.wm_attributes("-topmost", True)

        emp_frame = ctk.CTkFrame(self.__popup, width=700)
        column1 = ctk.CTkFrame(emp_frame, fg_color=Utils.WHITE)
        column2 = ctk.CTkFrame(emp_frame, fg_color=Utils.WHITE)
        column3 = ctk.CTkFrame(emp_frame, fg_color=Utils.WHITE)

        # Column 1;
        emp_info_lbl = ctk.CTkLabel(column1, text="Thông tin nhân viên: ", font=('TkDefaultFont', 16, 'bold'))
        emp_info_lbl.pack(**Utils.heading_group_pack)

        # Employee Id
        emp_id_frm = ctk.CTkFrame(column1)
        emp_id_lbl = ctk.CTkLabel(emp_id_frm, text="Mã nhân viên: ")
        emp_id_lbl.pack(**Utils.label_pack_style)

        emp_id_var = tk.StringVar()
        if action == Action.ADD:
            new_emp_id = self.__controller.get_new_emp_id()
            emp_id_var.set(new_emp_id)
            self.__add_or_update_form['employee_id'] = ctk.CTkEntry(master=emp_id_frm, state=tk.DISABLED,
                                                                    textvariable=emp_id_var)
        if action == Action.UPDATE:
            self.__add_or_update_form['employee_id'] = ctk.CTkEntry(master=emp_id_frm, state=tk.DISABLED,
                                                                    textvariable=emp_id_var)

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
        gender_frm = ctk.CTkFrame(column2, width=100)
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
        gender_style = Utils.radio_group_style
        gender_style['pady'] = (3, 20)
        gender_frm.pack(**gender_style)

        self.__add_or_update_form['income_date_dpk'] = Utils.date_picker_component(column2, {'lbl': "Ngày vào làm: "})
        self.__add_or_update_form['phone_number_ent'] = Utils.input_component(column2, {'lbl': "Số điện thoại: "})
        self.__add_or_update_form['email_ent'] = Utils.input_component(column2, {'lbl': "Email: "})
        self.__add_or_update_form['address_ent'] = Utils.input_component(column2, {'lbl': "Địa chỉ: "})

        # Column 3:
        account_info_lbl = ctk.CTkLabel(column3, text="Thông tin tài khoản: ", font=('TkDefaultFont', 16, 'bold'))
        account_info_lbl.pack(**Utils.heading_group_pack)

        self.__add_or_update_form['username_ent'] = Utils.input_component(column3, {'lbl': "Tên tài khoản: "})
        self.__add_or_update_form['password_ent'] = Utils.input_component(column3,
                                                                          {'lbl': "Mật khẩu: ", "type": "password"})

        # Account status
        self.__add_or_update_form['status'] = tk.StringVar()
        status_frm = ctk.CTkFrame(column3)

        status_lbl = ctk.CTkLabel(status_frm, text="Trạng thái tài khoản: ")
        status_lbl.pack(**Utils.label_pack_style)
        self.__add_or_update_form['active_rad'] = ctk.CTkRadioButton(status_frm, text='Hoạt động',
                                                                     value=UserStatus.ACTIVE.value,
                                                                     variable=self.__add_or_update_form['status'])
        self.__add_or_update_form['active_rad'].pack(side=tk.TOP, anchor="w")
        self.__add_or_update_form['inactive_rad'] = ctk.CTkRadioButton(status_frm, text='Không hoạt động',
                                                                       value=UserStatus.INACTIVE.value,
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
            self.set_value_for_widget(emp_by_id)

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

        button_container = ctk.CTkFrame(master=self.__popup, fg_color=Utils.WHITE)
        button_grp = ctk.CTkFrame(button_container, fg_color=Utils.WHITE)
        save_or_update_btn = ctk.CTkButton(button_grp,
                                           text=save_or_update_txt,
                                           width=10,
                                           fg_color="blue",
                                           command=lambda: self.save_data(action))
        save_or_update_btn.pack(side=tk.LEFT, padx=10, pady=10, expand=False)

        # Clear button
        clear_btn = ctk.CTkButton(button_grp,
                                  text="Làm sạch",
                                  width=10,
                                  fg_color="gray",
                                  command = lambda: self.clear_data())
        clear_btn.pack(side=tk.LEFT, padx=10, pady=10, expand=True)
        button_grp.pack(side=tk.TOP, padx=10, pady=10, anchor="center", fill=tk.NONE, expand=False)
        button_container.pack(side=tk.TOP, fill=tk.BOTH, expand=False)

    def set_value_for_widget(self, data):
        # Set data for update employee popup
        if data:
            self.set_value_for_entry('employee_id', data.user_code, is_disabled=True)
            self.set_value_for_entry('first_name_ent', data.first_name)
            self.set_value_for_entry('last_name_ent', data.last_name)
            self.set_value_for_date_entry('birthday_dpk', data.birth_date)
            self.set_value_for_entry('identity_ent', data.identity)
            self.set_value_for_radio_btn(data.gender, 0)
            self.set_value_for_date_entry('income_date_dpk', data.income_date)
            self.set_value_for_entry('phone_number_ent', data.phone_number)
            self.set_value_for_entry('email_ent', data.email)
            self.set_value_for_entry('address_ent', data.address)
            self.set_value_for_entry('username_ent', data.user_name, is_disabled=False)
            self.set_value_for_entry('password_ent', data.password, is_disabled=True)
            self.set_value_for_radio_btn(data.status, 1)
            self.set_value_for_combobox('type_cbo', Utils.get_account_type_str(data.type))

    def set_value_for_combobox(self, widget_name: str, new_value):
        self.__add_or_update_form[widget_name].set(new_value)

    def set_value_for_date_entry(self, widget_name: str, new_value: datetime.date):
        self.__add_or_update_form[widget_name].set_date(new_value.strftime('%d/%m/%Y'))

    def set_value_for_radio_btn(self, value, rad_type):
        # rad_type is gender (0) or status(1)
        if rad_type == 0:
            if value == Gender.MALE.value:
                self.__add_or_update_form['male_rad'].select()
            elif value == Gender.FEMALE.value:
                self.__add_or_update_form['female_rad'].select()
            elif value == Gender.OTHER.value:
                self.__add_or_update_form['other_rad'].select()
        elif rad_type == 1:
            if value == UserStatus.ACTIVE.value:
                self.__add_or_update_form['active_rad'].select()
            elif value == UserStatus.INACTIVE.value:
                self.__add_or_update_form['inactive_rad'].select()

    def set_value_for_entry(self, widget_name: str, new_value = None, is_disabled=False):
        if is_disabled:
            self.__add_or_update_form[widget_name].configure(state='normal')
        self.__add_or_update_form[widget_name].delete(0, ctk.END)
        if new_value is not None:
            self.__add_or_update_form[widget_name].insert(0, new_value)
        if is_disabled:
            self.__add_or_update_form[widget_name].configure(state='disabled')

    def delete_item(self):
        # Delete an item from grid
        answer = tkMsgBox.askyesno("Thông báo", "Bạn có chắc muốn xoá không?")
        if answer:
            result = self.__controller.delete(self.__id_selected)
            if result == 1:
                self.__id_selected = -1
                self.reload_tree_data()
                tkMsgBox.showinfo("Thông báo", f"Xoá thành công!")
            else:
                self.reload_tree_data()
                tkMsgBox.showinfo("Thông báo", f"Xoá thất bại!")
        print(self.__id_selected)

    def search(self, keyword: str):
        if keyword is None:
            return
        else:
            search_cond = {"keyword": keyword}
            emp_list = self.__controller.get_list(**search_cond)

            for record in self.__tree.get_children():
                self.__tree.delete(record)

            if emp_list is not None and len(emp_list) > 0:
                for emp in emp_list:
                    self.__tree.insert('', tk.END, values=emp)

    def clear_data(self):
        # Clear all data that user input in popup
        self.set_value_for_entry('first_name_ent')
        self.set_value_for_entry('last_name_ent')
        self.set_value_for_date_entry('birthday_dpk', datetime.date.today())
        self.set_value_for_entry('identity_ent')
        self.set_value_for_radio_btn('gender', 0)
        self.set_value_for_date_entry('income_date_dpk', datetime.date.today())
        self.set_value_for_entry('phone_number_ent')
        self.set_value_for_entry('email_ent')
        self.set_value_for_entry('address_ent')
        self.set_value_for_entry('username_ent')
        self.set_value_for_entry('password_ent')
        self.set_value_for_combobox('status', "")
        self.set_value_for_combobox('type_cbo', "")

    def validation_add_or_update_form(self, **form_data):
        # Validation data from form before save to database
        err_msg = ""
        if "first_name" in form_data and form_data["first_name"] == "":
            err_msg += "Vui lòng nhập trường Họ \n"
        if "last_name" in form_data and form_data["last_name"] == "":
            err_msg += "Vui lòng nhập trường Tên \n"
        if "identity" in form_data and form_data["identity"] == "":
            err_msg += "Vui lòng nhập trường CCCD/CMND \n"
        if "gender" in form_data and form_data["gender"] == "":
            err_msg += "Vui lòng chọn trường Giới tính \n"
        if "phone_number" in form_data and form_data["phone_number"] == "":
            err_msg += "Vui lòng nhập trường Số điện thoại\n"
        if "user_name" in form_data and form_data["user_name"] == "":
            err_msg += "Vui lòng nhập trường Tên người dùng \n"
        if "password" in form_data and form_data["password"] == "":
            err_msg += "Vui lòng nhập trường Mật khẩu \n"
        if err_msg != "":
            tkMsgBox.showwarning("Chú ý", err_msg)
            return False
        else:
            return True

    def save_data(self, action: Action):
        # Get data from form to save to database
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

        if not self.validation_add_or_update_form(**data): return

        result = None
        result_msg = ""
        if action == Action.ADD:
            result_msg = "Thêm"
            result = self.__controller.save(**data)
        elif action == Action.UPDATE:
            result_msg = "Cập nhật"
            result = self.__controller.update(self.__id_selected, data)
        if result == 1:
            self.reload_tree_data()
            self.__popup.destroy()
            tkMsgBox.showinfo("Thông báo", f"{result_msg} thành công!")
        else:
            self.reload_tree_data()
            self.__popup.destroy()
            tkMsgBox.showinfo("Thông báo", f"{result_msg} thất bại!")

    def on_row_selected(self, event):
        # Catch event that user click on grid to choose what employee can update information
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
        self.__tree.heading(EmployeeView.columns[14], text='')
        self.__tree.heading(EmployeeView.columns[15], text='')
        self.__tree.heading(EmployeeView.columns[16], text='')

        self.__tree.column(EmployeeView.columns[0], width=50, anchor='center')
        self.__tree.column(EmployeeView.columns[1], anchor='center')
        self.__tree.column(EmployeeView.columns[2], anchor='w')
        self.__tree.column(EmployeeView.columns[3], anchor='center')
        self.__tree.column(EmployeeView.columns[4], anchor='w')
        self.__tree.column(EmployeeView.columns[5], anchor='center')
        self.__tree.column(EmployeeView.columns[6], anchor='center')
        self.__tree.column(EmployeeView.columns[7], anchor='center')
        self.__tree.column(EmployeeView.columns[8], anchor='center')
        self.__tree.column(EmployeeView.columns[9], width=300, anchor='w')
        self.__tree.column(EmployeeView.columns[10], anchor='center')
        self.__tree.column(EmployeeView.columns[11], anchor='center')
        self.__tree.column(EmployeeView.columns[12], anchor='center')
        self.__tree.column(EmployeeView.columns[13], anchor='center')
        self.__tree.column(EmployeeView.columns[14], width=0, stretch=False) # Hide column
        self.__tree.column(EmployeeView.columns[15], width=0, stretch=False) # Hide column
        self.__tree.column(EmployeeView.columns[16], width=0, stretch=False) # Hide column

        # Set color for odd and even row in grid
        self.__tree.tag_configure('odd', background='#E8E8E8')
        self.__tree.tag_configure('even', background='#DFDFDF')

        self.load_tree_data()

        # Bind event when row selected
        self.__tree.bind("<<TreeviewSelect>>", self.on_row_selected)

    def load_tree_data(self):
        # Get all record and show in page
        emp_list = self.__controller.get_list()
        if emp_list is not None and len(emp_list) > 0:
            for emp in emp_list:
                self.__tree.insert('', tk.END, values=emp)

    def reload_tree_data(self):
        # Reload data on grid after add new or update employee information
        for record in self.__tree.get_children():
            self.__tree.delete(record)
        self.load_tree_data()

    def init_view(self, parent: ctk.CTkFrame):
        # Init view, include action form and grid
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(0, weight=1)
        parent.rowconfigure(1, weight=9)

        action_form = self.init_action_form(parent)
        action_form.grid(column=0, row=0, sticky='nwse')

        wrap_grid = ctk.CTkFrame(parent)
        self.init_employee_grid_data(wrap_grid)

        # Add scroll for grid
        tree_scroll_x = ctk.CTkScrollbar(wrap_grid, command=self.__tree.xview, height=15, orientation=ctk.HORIZONTAL)
        tree_scroll_x.pack(side=ctk.BOTTOM, fill=ctk.X)
        tree_scroll_y = ctk.CTkScrollbar(wrap_grid, command=self.__tree.yview, width=15, orientation=ctk.VERTICAL)
        tree_scroll_y.pack(side=ctk.RIGHT, fill=ctk.Y)

        self.__tree.configure(xscrollcommand=tree_scroll_x.set)
        self.__tree.configure(yscrollcommand=tree_scroll_y.set)

        self.__tree.pack(side=ctk.BOTTOM, fill=tk.BOTH, expand=True)
        wrap_grid.grid(row=1, column=0, sticky='nsew')


if __name__ == '__main__':
    root = ctk.CTk()
    root.state("zoomed")  # full screen
    root.resizable(True, True)
    root.focus_set()
    # root.iconbitmap('../assets/restaurant.ico')
    root.title("Restaurant Information")
    exFrame = ctk.CTkFrame(root)
    exFrame.pack(side='top', fill='both', expand=True)
    employee_view = EmployeeView(exFrame)
    root.mainloop()
