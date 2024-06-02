import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from payslip.pay_slip_controller import PaySlipController
from share.common_config import Action
from share.utils import Utils
import tkinter.messagebox as tkMsgBox


class PaySlipView:
    def __init__(self, parent: ctk.CTkFrame):
        self.__pay_slip_controller = PaySlipController()
        self.__main_frame = parent
        self.__id_selected = 0  # To save row id where will update, delete or remove database
        self.__popup = None
        self.__form_controls = dict()
        self.__tree = None
        self.__pay_slip_popup = None
        self.__cols = ["no", "user_code", "full_name", 'user_name', "gender", 'birth_date', 'identity', 'type', 'id',
                       'hours', 'total_salary', "created_date", "updated_date", 'user_id']
        self.init_view(parent)

    def init_view(self, parent):
        # Action button: Add new, Delete, Update
        action_frm = self.init_actions(parent)
        action_frm.grid(column=0, row=0, sticky='nwse')

        # Init tree view
        wrap_grid = ctk.CTkFrame(parent)
        self.init_tree(wrap_grid)

        # Add scroll for grid
        tree_scroll_x = ctk.CTkScrollbar(wrap_grid, command=self.__tree.xview, height=15, orientation=ctk.HORIZONTAL)
        tree_scroll_x.pack(side=ctk.BOTTOM, fill=ctk.X)
        tree_scroll_y = ctk.CTkScrollbar(wrap_grid, command=self.__tree.yview, width=15, orientation=ctk.VERTICAL)
        tree_scroll_y.pack(side=ctk.RIGHT, fill=ctk.Y)

        self.__tree.pack(side=ctk.BOTTOM, fill=tk.BOTH, expand=True)
        wrap_grid.grid(row=1, column=0, sticky='nsew')

    def init_actions(self, parent: ctk.CTkFrame):
        # Create form include: Them, Xoa, Cap Nhat and Tim Kiem by full name, employee id, username

        action_frame = ctk.CTkFrame(parent)
        btn_pack = {'side': tk.LEFT, 'padx': 10, 'pady': 10, 'anchor': "w"}

        # Add button
        add_button = ctk.CTkButton(action_frame,
                                   text="Thêm",
                                   width=100,
                                   fg_color="blue",
                                   command=lambda: self.init_add_or_update_popup(parent, Action.ADD))
        add_button.pack(**btn_pack)

        # Update button
        update_btn = ctk.CTkButton(action_frame,
                                   text="Cập nhật",
                                   width=100,
                                   fg_color="green",
                                   command=lambda: self.init_add_or_update_popup(parent, Action.UPDATE))
        update_btn.pack(**btn_pack)

        # Delete button
        delete_btn = ctk.CTkButton(action_frame,
                                   text="Xoá",
                                   width=100,
                                   fg_color="red",
                                   command=lambda: self.delete_clicked())
        delete_btn.pack(**btn_pack)

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

    def init_tree(self, parent: ctk.CTkFrame):
        # Define column for grid

        self.__tree = ttk.Treeview(parent, columns=self.__cols, show='headings')

        self.__tree.heading(self.__cols[0], text='#')
        self.__tree.heading(self.__cols[1], text='Mã nhân viên')
        self.__tree.heading(self.__cols[2], text='Họ & tên')
        self.__tree.heading(self.__cols[2], text='Tên tài khoản')
        self.__tree.heading(self.__cols[3], text='Giới tính')
        self.__tree.heading(self.__cols[4], text='Ngày sinh')
        self.__tree.heading(self.__cols[5], text='CCCD/CMND')
        self.__tree.heading(self.__cols[6], text='Loại nhân viên')
        self.__tree.heading(self.__cols[7], text='Mã phiếu lương')
        self.__tree.heading(self.__cols[8], text='Số giờ làm việc')
        self.__tree.heading(self.__cols[9], text='Tiền lương')
        self.__tree.heading(self.__cols[10], text='Ngày tạo')
        self.__tree.heading(self.__cols[11], text='Ngày cập nhật')

        self.__tree.column(self.__cols[0], width=50, anchor='center')
        self.__tree.column(self.__cols[1], anchor='center')
        self.__tree.column(self.__cols[2], anchor='w')
        self.__tree.column(self.__cols[3], anchor='center')
        self.__tree.column(self.__cols[4], anchor='w')
        self.__tree.column(self.__cols[5], anchor='center')
        self.__tree.column(self.__cols[6], anchor='center')
        self.__tree.column(self.__cols[7], anchor='center')
        self.__tree.column(self.__cols[8], anchor='center')
        self.__tree.column(self.__cols[9], anchor='w')
        self.__tree.column(self.__cols[10], anchor='w')
        self.__tree.column(self.__cols[11], anchor='w')

        # Set color for odd and even row in grid
        self.__tree.tag_configure('odd', background='#E8E8E8')
        self.__tree.tag_configure('even', background='#DFDFDF')

        self.load_tree_data()

        # Bind event when row selected
        self.__tree.bind("<<TreeviewSelect>>", self.row_clicked())

    def load_tree_data(self):
        # Get all record and show in page
        pay_slip_list = self.__pay_slip_controller.get_all()
        if pay_slip_list is not None and len(pay_slip_list) > 0:
            for psl in pay_slip_list:
                self.__tree.insert('', tk.END, values=psl)

    def reload_tree_data(self):
        # Reload data on grid after add new or update employee information
        for record in self.__tree.get_children():
            self.__tree.delete(record)
        self.load_tree_data()

    def row_clicked(self):
        # Catch event that user click on grid to choose what employee can update information
        for item in self.__tree.selection():
            record = self.__tree.item(item)['values']
            if record[len(record) - 1]:
                self.__id_selected = record[len(record) - 1]

    def delete_clicked(self):
        # Delete on item from grid
        if self.__id_selected == 0:
            tkMsgBox.showinfo("Thông báo", f"Chọn 1 dòng muốn xoá!")
            return

        answer = tkMsgBox.askyesno("Thông báo", "Bạn có chắc muốn xoá không?")
        if answer:
            result = self.__pay_slip_controller.delete_by_id(self.__id_selected)
            if result == 1:
                self.__id_selected = -1
                self.reload_tree_data()
                tkMsgBox.showinfo("Thông báo", f"Xoá thành công!")
            else:
                self.reload_tree_data()
                tkMsgBox.showinfo("Thông báo", f"Xoá thất bại!")

    def init_add_or_update_popup(self, parent: ctk.CTkFrame, action: Action):
        # Init popup data
        common_pack = {'side': tk.TOP, 'expand': True, 'padx': 5, 'pady': 5, 'anchor': tk.W, 'fill': tk.X}
        btn_pack = {'side': tk.LEFT, 'padx': 10, 'pady': 10, 'expand': False}
        text_pack = {'side': tk.TOP, 'anchor': 'w'}

        if action == Action.UPDATE and self.__id_selected < 1:
            return

        # Create add new or update payslip information popup
        self.__popup = ctk.CTkToplevel(parent)
        self.__popup.geometry("500x600")
        self.__popup.title("Thực hiện tính lương")
        self.__popup.resizable(False, False)

        main_frm = ctk.CTkFrame(self.__popup, fg_color=Utils.WHITE)

        # ------------ Left column: contain employee information, who will calculate salary ------------
        left_frm = ctk.CTkFrame(main_frm, fg_color=Utils.WHITE)

        # Employee Id
        choose_emp = ctk.CTkFrame(left_frm, fg_color=Utils.WHITE)
        self.__form_controls['emp_id_ent'] = Utils.input_component(choose_emp, {'lbl': "Chọn nhân viên: "})
        self.__form_controls['emp_id_ent'].pack(side=tk.LEFT)
        get_info_btn = ctk.CTkButton(choose_emp,
                                     text="Thông tin",
                                     width=10,
                                     fg_color="gray",
                                     command=lambda: self.get_emp_info_clicked())
        get_info_btn.pack(side=tk.LEFT)
        choose_emp.pack(**common_pack)

        # Hours: input here to calculate data
        self.__form_controls['hour_ent'] = Utils.input_component(left_frm, {'lbl': "Nhập số giờ làm việc: "})
        self.__form_controls['hour_ent'].pack(**common_pack)

        # User code
        user_code_frm = Utils.init_label_and_value(parent=left_frm, data={'lbl': 'Mã nhân viên: ', 'value': ''})
        user_code_frm['frm'].pack(**common_pack)

        # User name
        user_name_frm = Utils.init_label_and_value(parent=left_frm, data={'lbl': 'Tên tài khoản: ', 'value': ''})
        user_name_frm['frm'].pack(**common_pack)

        # Full name
        full_name_frm = Utils.init_label_and_value(parent=left_frm, data={'lbl': 'Tên nhân viên: ', 'value': ''})
        full_name_frm['frm'].pack(**common_pack)

        # Gender
        gender_frm = Utils.init_label_and_value(parent=left_frm, data={'lbl': 'Giới tính: ', 'value': ''})
        gender_frm['frm'].pack(**common_pack)

        # Birthday
        birthday_frm = Utils.init_label_and_value(parent=left_frm, data={'lbl': 'Ngày sinh: ', 'value': ''})
        birthday_frm['frm'].pack(**common_pack)

        # Identity
        identity_frm = Utils.init_label_and_value(parent=left_frm, data={'lbl': 'CMND/CCCD: ', 'value': ''})
        identity_frm['frm'].pack(**common_pack)

        # Employee type (Account type)
        user_type_frm = Utils.init_label_and_value(parent=left_frm, data={'lbl': 'Loại nhân viên: ', 'value': ''})
        user_type_frm['frm'].pack(**common_pack)

        left_frm.pack(side=tk.LEFT, anchor='nw', padx=5, pady=5, expand=True, fill=tk.X)

        # ------------ Right column: Payslip information ------------
        right_frm = ctk.CTkFrame(main_frm, fg_color=Utils.WHITE)

        # Payslip month that pay salary
        months = list(map(lambda x: str(x), range(1, 13)))

        # Choose month
        month_frm = ctk.CTkFrame(master=right_frm, fg_color=Utils.WHITE)
        type_lbl = ctk.CTkLabel(month_frm, text="Kỳ lương tháng: ")
        type_lbl.pack(**Utils.label_pack_style)
        self.__form_controls['month'] = ctk.CTkComboBox(master=month_frm, values=months)
        self.__form_controls['month'].pack(**Utils.entry_pack_style)
        month_frm.pack(**common_pack)

        # Payslip id
        psl_id_frm = Utils.init_label_and_value(parent=right_frm, data={'lbl': 'Mã số: ', 'value': ''})
        psl_id_frm['frm'].pack(**common_pack)

        # Payslip hours
        hours_frm = Utils.init_label_and_value(parent=right_frm, data={'lbl': 'Giờ làm việc: ', 'value': ''})
        hours_frm['frm'].pack(**common_pack)

        # Payslip total salary
        total_salary_frm = Utils.init_label_and_value(parent=right_frm,
                                                      data={'lbl': 'Tiền lương: ', 'value': ''})
        total_salary_frm['frm'].pack(**common_pack)

        # Payslip the date created payslip
        salary_pay_date_frm = Utils.init_label_and_value(parent=right_frm,
                                                         data={'lbl': 'Ngày tạo: ', 'value': ''})
        salary_pay_date_frm['frm'].pack(**common_pack)

        right_frm.pack(side=tk.LEFT, anchor='nw', padx=5, pady=5, expand=True, fill=tk.X)
        main_frm.pack(side=ctk.TOP, fill=tk.BOTH, expand=True)

        # Add or Update button
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
                                           command=lambda: self.save_or_update_btn_clicked(action))
        save_or_update_btn.pack(**btn_pack)

        cal_salary_btn = ctk.CTkButton(button_grp,
                                           text='Tính lương',
                                           width=10,
                                           fg_color="green",
                                           command=lambda: self.cal_salary())
        cal_salary_btn.pack(**btn_pack)

        button_grp.pack(side=tk.TOP, padx=10, pady=10, anchor="center", fill=tk.NONE, expand=False)
        button_container.pack(side=tk.TOP, fill=tk.BOTH, expand=False)

    def cal_salary(self):
        pass

    def get_emp_info_clicked(self):
        # Call all employee who will calculate salary
        employeeId = self.__form_controls['emp_id_ent'].get()
        print(employeeId)

        data = self.__pay_slip_controller.get_pay_slip_by_user_id(employeeId)
        print('^^:', data)


    def save_or_update_btn_clicked(self, action: Action):
        # Get data from form to save to database
        type = self.__form_controls['type_cbo'].get()
        allowance = self.__form_controls['allowance_ent'].get()
        pay_per_hours = self.__form_controls['pay_per_hours_ent'].get()
        data = {'type': type,
                'allowances': allowance,
                'pay_per_hours': pay_per_hours}

        result = None
        result_msg = ""
        if action == Action.ADD:
            result_msg = "Thêm"
            result = self.__pay_slip_controller.add_new(**data)
        elif action == Action.UPDATE:
            result_msg = "Cập nhật"
            result = self.__pay_slip_controller.update_by_id(self.__id_selected, data)
        if result == 1:
            self.reload_tree_data()
            self.__popup.destroy()
            tkMsgBox.showinfo("Thông báo", f"{result_msg} thành công!")
        else:
            self.reload_tree_data()
            self.__popup.destroy()
            tkMsgBox.showwarning("Thông báo", f"{result_msg} thất bại!")

    def set_value_for_entry(self, widget_name: str, new_value=None, is_disabled=False):
        if is_disabled:
            self.__form_controls[widget_name].configure(state='normal')
        self.__form_controls[widget_name].delete(0, ctk.END)
        if new_value is not None:
            self.__form_controls[widget_name].insert(0, new_value)
        if is_disabled:
            self.__form_controls[widget_name].configure(state='disabled')


if __name__ == '__main__':
    root = ctk.CTk()

    root.state("zoomed")  # full screen
    root.resizable(True, True)
    root.focus_set()

    root.iconbitmap('../assets/restaurant.ico')
    root.title("Restaurant Information")

    main_frame = ctk.CTkFrame(root)
    pay_slip_frame = PaySlipView(main_frame)
    main_frame.pack(side='top', fill='both', expand=True)

    root.mainloop()
