import tkinter as tk
from datetime import datetime
from tkinter import ttk
import customtkinter as ctk
from pay_grade.pay_grade_controller import PayGradeController
from share.common_config import Action
from share.utils import Utils
import tkinter.messagebox as tkMsgBox


class PayGradeView:
    def __init__(self, parent: ctk.CTkFrame):
        self.__pay_grade_controller = PayGradeController()
        self.__main_frame = parent
        self.__id_selected = 0
        self.__popup = None
        self.__form_controls = dict()
        self.__tree = None
        self.__cols = ["#", "type", "allowance", "pay_per_hours", "created_date", "updated_date"]
        self.init_view(parent)
        parent.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def init_view(self, parent: ctk.CTkFrame):
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
        action_frame = ctk.CTkFrame(parent, fg_color=Utils.WHITE)
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
        return action_frame

    def init_tree(self, parent: ctk.CTkFrame):
        # Define column for grid

        self.__tree = ttk.Treeview(parent, columns=self.__cols, show='headings')

        self.__tree.heading(self.__cols[0], text='#')
        self.__tree.heading(self.__cols[1], text='Loại nhân viên')
        self.__tree.heading(self.__cols[2], text='Trợ cấp')
        self.__tree.heading(self.__cols[3], text='Lương theo giờ')
        self.__tree.heading(self.__cols[4], text='Ngày tạo')
        self.__tree.heading(self.__cols[5], text='Ngày cập nhật')

        self.__tree.column(self.__cols[0], width=50, anchor='center')
        self.__tree.column(self.__cols[1], anchor='center')
        self.__tree.column(self.__cols[2], anchor='w')
        self.__tree.column(self.__cols[3], anchor='center')

        # Set color for odd and even row in grid
        self.__tree.tag_configure('odd', background='#E8E8E8')
        self.__tree.tag_configure('even', background='#DFDFDF')

        self.load_tree_data()

        # Bind event when row selected
        self.__tree.bind("<<TreeviewSelect>>", self.row_clicked)

    def load_tree_data(self):
        # Get all record and show in page
        pay_grade_list = self.__pay_grade_controller.get_all()
        if pay_grade_list is not None and len(pay_grade_list) > 0:
            for pg in pay_grade_list:
                self.__tree.insert('', tk.END, values=pg)

    def reload_tree_data(self):
        # Reload data on grid after add new or update employee information
        for record in self.__tree.get_children():
            self.__tree.delete(record)
        self.load_tree_data()

    def row_clicked(self, event):
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
            result = self.__pay_grade_controller.delete_by_id(self.__id_selected)
            if result == 1:
                self.__id_selected = -1
                self.reload_tree_data()
                tkMsgBox.showinfo("Thông báo", f"Xoá thành công!")
            else:
                self.reload_tree_data()
                tkMsgBox.showinfo("Thông báo", f"Xoá thất bại!")

    def init_add_or_update_popup(self, parent: ctk.CTkFrame, action: Action):
        # Init popup data
        common_pack = {'side': tk.TOP, 'expand': True, 'padx': 2, 'pady': 2, 'anchor': tk.W, 'fill': tk.X}
        btn_pack = {'side': tk.LEFT, 'padx': 10, 'pady': 10, 'expand': False}

        if action == Action.UPDATE and self.__id_selected < 1:
            return

        # Create add new or update employee information popup
        self.__popup = ctk.CTkToplevel(parent)

        self.__popup.geometry("300x350")
        self.__popup.title("Thông tin bậc lương")
        self.__popup.resizable(False, False)
        self.__popup.wm_attributes("-topmost", True)
        form = ctk.CTkFrame(self.__popup, fg_color=Utils.WHITE)

        # Account Type
        type_lbl = ctk.CTkLabel(form, text="Loại tài khoản: ")
        type_lbl.pack(**Utils.label_pack_style)
        self.__form_controls['type_cbo'] = ctk.CTkComboBox(form, values=["Admin", "Bình thường"])
        self.__form_controls['type_cbo'].pack(**common_pack)

        # Allowance
        self.__form_controls['allowance_ent'] = Utils.input_component(form, {'lbl': "Trợ cấp: "})
        self.__form_controls['allowance_ent'].pack(**common_pack)

        # Pay per hours
        self.__form_controls['pay_per_hours_ent'] = Utils.input_component(form, {'lbl': "Tiền lương theo giờ: "})
        self.__form_controls['pay_per_hours_ent'].pack(**common_pack)

        # Add or Update button
        if action == Action.UPDATE:
            save_or_update_txt = "Cập nhật"
            pay_grade_by_id = self.__pay_grade_controller.get_by_id(self.__id_selected)
            self.set_value_for_widget(pay_grade_by_id)
        else:
            save_or_update_txt = "Thêm"

        button_container = ctk.CTkFrame(master=form, fg_color=Utils.WHITE)
        button_grp = ctk.CTkFrame(button_container, fg_color=Utils.WHITE)
        save_or_update_btn = ctk.CTkButton(button_grp,
                                           text=save_or_update_txt,
                                           width=10,
                                           fg_color="blue",
                                           command=lambda: self.save_or_update_btn_clicked(action))
        save_or_update_btn.pack(**btn_pack)

        # Clear button
        clear_btn = ctk.CTkButton(button_grp,
                                  text="Làm sạch",
                                  width=10,
                                  fg_color="gray",
                                  command=lambda: self.clear_clicked())
        clear_btn.pack(**btn_pack)

        form.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, anchor='nw', padx=10, pady=10)
        button_grp.pack(side=tk.TOP, padx=10, pady=10, anchor="center", fill=tk.NONE, expand=False)
        button_container.pack(side=tk.TOP, fill=tk.BOTH, expand=False)

    def save_or_update_btn_clicked(self, action: Action):
        # Get data from form to save to database
        type = self.__form_controls['type_cbo'].get()
        type_value = Utils.get_account_type_value(type)
        allowance = self.__form_controls['allowance_ent'].get()
        pay_per_hours = self.__form_controls['pay_per_hours_ent'].get()

        if not Utils.is_number(allowance):
            tkMsgBox.showwarning(title='Thông báo', message="Trợ cấp không phải là số và định dạng không đúng!")
            return
        if not Utils.is_number(pay_per_hours):
            tkMsgBox.showwarning(title='Thông báo', message="Lương theo giờ không phải là số và định dạng không đúng!")
            return

        data = {'type': type_value,
                'allowance': allowance,
                'pay_per_hours': pay_per_hours,
                'created_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

        if action == Action.UPDATE:
            data['updated_date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        result = None
        result_msg = ""
        if action == Action.ADD:
            result_msg = "Thêm"
            result = self.__pay_grade_controller.add_new(**data)
        elif action == Action.UPDATE:
            result_msg = "Cập nhật"
            result = self.__pay_grade_controller.update_by_id(self.__id_selected, data)
        if result == 1:
            self.reload_tree_data()
            self.__popup.destroy()
            tkMsgBox.showinfo("Thông báo", f"{result_msg} thành công!")
        else:
            self.reload_tree_data()
            self.__popup.destroy()
            tkMsgBox.showwarning("Thông báo", f"{result_msg} thất bại!")

    def clear_clicked(self):
        # Clear all data in form
        self.__form_controls["type_cbo"].set("")
        self.set_value_for_entry('allowance_ent')
        self.set_value_for_entry('pay_per_hours_ent')

    def set_value_for_entry(self, widget_name: str, new_value=None, is_disabled=False):
        if is_disabled:
            self.__form_controls[widget_name].configure(state='normal')
        self.__form_controls[widget_name].delete(0, ctk.END)
        if new_value is not None:
            self.__form_controls[widget_name].insert(0, new_value)
        if is_disabled:
            self.__form_controls[widget_name].configure(state='disabled')

    def set_value_for_widget(self, data):
        print("===")
        print(data.type)
        print(data.allowance)
        print(data.pay_per_hours)

        # Set data for update page grade popup
        if data:
            self.__form_controls['type_cbo'].set(Utils.get_account_type_str(data.type))
            self.set_value_for_entry('allowance_ent', data.allowance)
            self.set_value_for_entry('pay_per_hours_ent', data.pay_per_hours)
