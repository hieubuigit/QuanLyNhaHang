import tkinter as tk
import customtkinter as ctk
from login.login_controller import LoginController
from share.utils import Utils
import tkinter.messagebox as tkMsgBox


class ChangePasswordView:
    def __init__(self):
        self.__form_controls: dict = {}
        self.__login_controller = LoginController()

    def init_change_password_popup(self, parent: ctk.CTkFrame):
        # Init popup data
        common_pack = {'side': tk.TOP, 'expand': False, 'padx': 2, 'pady': 2, 'anchor': tk.W, 'fill': tk.X}
        btn_pack = {'side': tk.LEFT, 'padx': 5, 'pady': 5, 'expand': False}

        # Create add new or update employee information popup
        self.__popup = ctk.CTkToplevel(parent)

        self.__popup.geometry("300x350")
        self.__popup.title("Đổi mật khẩu")
        self.__popup.resizable(False, False)
        form = ctk.CTkFrame(self.__popup, fg_color=Utils.WHITE)
        self.__popup.wm_attributes("-topmost", True)

        # Old password
        self.__form_controls['old_pw_ent'] = Utils.input_component(form, {'lbl': "Mật khẩu hiện tại: "})
        self.__form_controls['old_pw_ent'].pack(**common_pack)

        # New password
        self.__form_controls['new_password_ent'] = Utils.input_component(form, {'lbl': "Mật khẩu mới: "})
        self.__form_controls['new_password_ent'].pack(**common_pack)

        # Repeat password
        self.__form_controls['repeat_password_ent'] = Utils.input_component(form, {'lbl': "Nhập lại mật khẩu mới: "})
        self.__form_controls['repeat_password_ent'].pack(**common_pack)

        # Add or Update button
        button_container = ctk.CTkFrame(master=form, fg_color=Utils.WHITE)
        button_grp = ctk.CTkFrame(button_container, fg_color=Utils.WHITE)
        save_or_update_btn = ctk.CTkButton(button_grp,
                                           text='Cập nhật',
                                           width=10,
                                           fg_color="blue",
                                           command=lambda: self.update_clicked())
        save_or_update_btn.pack(**btn_pack)

        form.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, anchor='nw', padx=10, pady=10)
        button_grp.pack(side=tk.TOP, padx=10, pady=10, anchor="center", fill=tk.NONE, expand=False)
        button_container.pack(side=tk.TOP, fill=tk.BOTH, expand=False)

    def update_clicked(self):
        old_pass = self.__form_controls['old_pw_ent'].get()
        new_pass = self.__form_controls['new_password_ent'].get()
        repeat_pass = self.__form_controls['repeat_password_ent'].get()
        if old_pass == '' or new_pass == '' or repeat_pass == '':
            tkMsgBox.showerror("Lỗi", 'Nhập đủ 3 trường dữ liệu trên!')
            return

        if new_pass and repeat_pass and new_pass != repeat_pass:
            tkMsgBox.showerror("Lỗi", 'Mật khẩu mới không trùng nhau!')
            return

        if not self.__login_controller.check_old_password(old_pass):
            tkMsgBox.showerror("Lỗi", 'Mật khẩu cũ của bạn không đúng!')
            return

        if self.__login_controller.change_password(new_pass) == 1:
            tkMsgBox.showinfo("Thông báo", 'Đổi mật khẩu thành công!')
            self.__popup.destroy()
            return
        else:
            tkMsgBox.showinfo("Thông báo", 'Đổi mật khẩu thất bại!')
            return

