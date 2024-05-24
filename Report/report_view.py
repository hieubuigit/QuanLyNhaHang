
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class ReportView:
    def __init__(self, window):
        self.__ui_main_content(window)

    def __ui_main_content(self, root):
        style = ttk.Style()
        style.theme_use('default')
        style.configure("BG.TFrame", background="#7AC5CD")
        main_fr = ttk.Frame(root, style="BG.TFrame")
        main_fr.pack(fill="both", expand=True)
        self.__ui_left_view(root, main_fr)
        style = ttk.Style()
        style.theme_use('default')
        style.configure("BGR1.TFrame", background="#CC6600")

        self.right_fr = ttk.Frame(main_fr, borderwidth=1, border=1, relief=tk.RIDGE)
        self.right_fr.pack(fill=tk.Y, expand=0, side="right")
        # default right content
        self.__report_page()

    def __ui_left_view(self,root, main_fr):
        style = ttk.Style()
        style.theme_use('default')
        left_fr = ttk.Frame(main_fr, borderwidth=1, border=1, relief=tk.RIDGE)
        left_fr.pack(fill=tk.Y, expand=0, side="left", anchor="nw")
        revenue_btn = ttk.Button(left_fr, text="Doanh thu", width=20, command=lambda: self.__switch_page(root, main_fr, page=""))
        revenue_btn.grid(row=0, column=0)
        salary_btn = ttk.Button(left_fr, text="Lương nhân viên", width=20, command=lambda: self.__switch_page(root, main_fr, page="SALARY"))
        salary_btn.grid(row=1, column=0)

    def ui_right_content_view(self):

        header_fr = ttk.Frame(self.right_fr)
        header_fr.grid(row=0, column=0, sticky="NE", pady=5)
        search_entry = ttk.Entry(header_fr, width=70)
        search_entry.grid(row=0, column=0)
        search_btn = ttk.Button(header_fr, text="Tìm kiếm")
        search_btn.grid(row=0, column=1)

        table_fr = ttk.Frame(self.right_fr, style="BGR1.TFrame")
        table_fr.grid(row=1, column=0)

        self.t = ttk.Treeview(table_fr)
        self.t.pack(fill=tk.BOTH, expand=1, padx=20)
        self.t["columns"] = ("thu", "chi")
        self.t["show"] = "headings"
        self.t.column("thu", anchor="center", width=80)
        self.t.column("chi", anchor="center", width=80)

        self.t.heading("thu", text="Thu")
        self.t.heading("chi", text="Chi")

        self.t.tag_configure("normal", background="white")
        self.t.tag_configure("blue", background="lightblue")
        bills = self.data_example()
        self.t.insert("", "end", iid=bills[0], text=bills[0],
                      values=(bills[0], bills[1]))
        self.open_pie_chart(table_fr)


    def __switch_page(self, root, main_fr, page):
        for fr in self.right_fr.winfo_children():
            fr.destroy()
            root.update()
        if page == "SALARY":
            self.salary_page(main_fr)
        else:
            self.__report_page()
    def data_example(self):
        bills = (200, 300)
        return bills

    def open_pie_chart(self, main_fr):
        data = self.data_example()
        input_text = [data.__getitem__(0), data.__getitem__(1)]
        frame_pie_chart = tk.Frame(main_fr)
        frame_pie_chart.pack()
        vehicles = ['Thu', 'Chi']
        fig = plt.Figure()
        ax = fig.add_subplot(111)
        ax.pie(input_text, radius=1, labels=vehicles)
        chart1 = FigureCanvasTkAgg(fig, frame_pie_chart)
        chart1.get_tk_widget().pack()

    def __report_page(self):
        self.ui_right_content_view()

    def salary_page(self, main_fr):
        # add employee frame
        salary_fr = ttk.Frame(self.right_fr)
        lb = ttk.Label(salary_fr, text="Salary Page")
        lb.pack()
        salary_fr.pack()






if __name__ == '__main__':
    root = tk.Tk()
    root.resizable(True, True)
    root.state('zoomed')  # full screen
    root.title("Report Information")
    root.config(background="blue")
    rp = ReportView(root)
    root.mainloop()





# import tkinter as tk
# from tkinter import ttk
#
# root = tk.Tk()
#
# button = tk.Button(root, text='right click this')
# button.pack()
#
# button.bind("<Button-2>", lambda e: print('You right clicked'))
#
# root.mainloop()