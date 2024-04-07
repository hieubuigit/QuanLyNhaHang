import os
import tkinter as tk
from tkinter import END, ttk
from ctypes import windll
from tkinter.messagebox import showinfo
from tkcalendar import Calendar
import random
from PIL import ImageTk, Image
from admin.employee.employee_model import EmployeeModel

class EmployeeUI:

    def __init__(self, emp: EmployeeModel):
        self.controller = None
        self.employee_fields = {}
        self.__emp_model = EmployeeModel(emp)

    @property
    def emp_model(self):
        return self.__emp_model

    @emp_model.setter
    def emp_model(self, emp):
        self.__emp_model = emp

    def set_controller(self, controller):
        """Set controller use for this view"""
        self.controller = controller

    def save_emp(self):
        """Save employee information"""
        showinfo('Click save button', "Test save")
        return True

    def update_emp(self, event):
        """Update employee information"""
        print(event)
        showinfo('Click update button', "Update employee info")

    def change_avatar(self, event):
        """ Open file explorer change choose file to update avatar"""
        print(event)
        os.system("start C:/")

    def set_data_entry(self, field, data):
        self.employee_fields[field].delete(0, END)
        self.employee_fields[field].insert(0, data)

    def row_selected(self, event):
        for selected_item in self.employee_fields['tree'].selection():
            record = self.employee_fields['tree'].item(selected_item)['values']
            print(record)
            self.set_data_entry("emp_id", record[0])
            self.set_data_entry("first_name", record[1])
            self.set_data_entry("last_name", record[2])
            # self.set_data_entry("birthday", record[3])
            self.employee_fields["gender"] = record[4]
            self.set_data_entry("phone_number", record[5])
            self.set_data_entry("email", record[6])
            self.set_data_entry("basic_salary", record[7])
            self.set_data_entry("address", record[8])
            self.set_data_entry("material_status", record[9])

    def reset_form(self):
        pass

    def form_data(self):
        data = {}
        return data

    def init_emp_frame(self, container):
        """Create Employee form input form user"""
        emp_frame = ttk.Frame(container)

        emp_frame.columnconfigure(0, weight=1)
        emp_frame.columnconfigure(1, weight=3)
        emp_frame.columnconfigure(2, weight=3)

        # Column 1
        # Avatar
        try:
            os.chdir(r"D:\$ STUDY\Learn University at UIT\Semester 3\Python\project\QuanLyNhaHang\assets\employee_avatar")
            avatar = ImageTk.PhotoImage(Image.open("a2.jpg").resize((290, 320)))
            avatar_lbl = tk.Label(emp_frame, image=avatar, background='white', text="Employee Avatar", compound='top', borderwidth=2, relief='solid')
            avatar_lbl.image = avatar
            avatar_lbl.bind("<Button>", self.change_avatar)
            avatar_lbl.grid(row=0, column=0, ipadx=5, ipady=10, sticky='ne')
        except Exception as ex:
            print("[!] Error load avatar image: ", ex)

        # Employee Id
        column1 = ttk.Frame(emp_frame)
        column1.columnconfigure(0, weight=1)
        column1.columnconfigure(0, weight=3)
        column1.grid(column=1, row=0, sticky='n')

        self.employee_fields['empId_lbl'] = ttk.Label(column1, text="Employee ID: ")
        self.employee_fields['empId_lbl'].grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)
        self.employee_fields['emp_id'] = ttk.Entry(master=column1)
        self.employee_fields['emp_id'].grid(column=1, row=0, sticky='we', padx=5, pady=5)

        #First name
        self.employee_fields['first_name_lbl'] = tk.Label(column1, text='First Name:')
        self.employee_fields['first_name_lbl'].grid(column=0, row=1, sticky=tk.W, padx=5, pady=5)
        self.employee_fields['first_name'] = ttk.Entry(master=column1)
        self.employee_fields['first_name'].grid(column=1, row=1, sticky='we', padx=5, pady=5)

        #Last name
        self.employee_fields['last_name_lbl'] = tk.Label(column1, text='Last Name:')
        self.employee_fields['last_name_lbl'].grid(column=0, row=2, sticky=tk.W, padx=5, pady=5)
        self.employee_fields['last_name'] = ttk.Entry(master=column1)
        self.employee_fields['last_name'].grid(column=1, row=2, sticky='we', padx=5, pady=5)

        # Birthday
        self.employee_fields['birthday_lbl'] = tk.Label(column1, text='Birthday:')
        self.employee_fields['birthday_lbl'].grid(column=0, row=3, sticky=tk.W, padx=5, pady=5)
        self.employee_fields['birthday'] = Calendar(column1)
        self.employee_fields['birthday'].grid(column=1, row=3, sticky='we', padx=5, pady=5)


        # Column 2
        column2 = ttk.Frame(emp_frame)
        column2.columnconfigure(0, weight=1)
        column2.columnconfigure(0, weight=3)
        column2.grid(column=2, row=0, sticky='nw')

        # Gender
        self.employee_fields['gender_lbl'] = tk.Label(column2, text='Gender:')
        self.employee_fields['gender_lbl'].grid(column=0, row=0, sticky='w', padx=5, pady=5)
        self.employee_fields['gender'] = tk.StringVar()
        r1 = ttk.Radiobutton(column2, text='Male', value=0, variable=self.employee_fields['gender'])
        r2 = ttk.Radiobutton(column2, text='Female', value=1, variable=self.employee_fields['gender'])
        r3 = ttk.Radiobutton(column2, text='Other', value=2, variable=self.employee_fields['gender'])
        r1.grid(column=1, row=0, sticky='we', padx=5, pady=5)
        r2.grid(column=1, row=1, sticky='we', padx=5, pady=5)
        r3.grid(column=1, row=2, sticky='we', padx=5, pady=5)

        #Phone number
        self.employee_fields['phone_number_lbl'] = tk.Label(column2, text='Phone Number:')
        self.employee_fields['phone_number_lbl'].grid(column=0, row=3, sticky='nw', padx=5, pady=5)
        self.employee_fields['phone_number'] = ttk.Entry(master=column2)
        self.employee_fields['phone_number'].grid(column=1, row=3, sticky='we', padx=5, pady=5)

        # Email
        self.employee_fields['email_lbl'] = tk.Label(column2, text='Email:')
        self.employee_fields['email_lbl'].grid(column=0, row=4, sticky='nw', padx=5, pady=5)
        self.employee_fields['email'] = tk.Entry(master=column2)
        self.employee_fields['email'].grid(column=1, row=4, sticky='we', padx=5, pady=5)

        # Basic salary
        self.employee_fields['basic_salary_lbl'] = tk.Label(column2, text='Basic Salary:')
        self.employee_fields['basic_salary_lbl'].grid(column=0, row=5, sticky='nw', padx=5, pady=5)
        self.employee_fields['basic_salary'] = tk.Entry(column2)
        self.employee_fields['basic_salary'].grid(column=1, row=5, sticky='we', padx=5, pady=5)

        # Address
        self.employee_fields['address_lbl'] = ttk.Label(column2, text='Address:')
        self.employee_fields['address_lbl'].grid(column=0, row=6, sticky='nw', padx=5, pady=5)
        self.employee_fields['address'] = ttk.Entry(column2)
        self.employee_fields['address'].grid(column=1, row=6, sticky='we', padx=5, pady=5)

        # Material Status
        self.employee_fields['material_status_lbl'] = ttk.Label(column2, text='Material Status:')
        self.employee_fields['material_status_lbl'].grid(column=0, row=7, sticky='nw', padx=5, pady=5)
        self.employee_fields['material_status'] = ttk.Combobox(column2)
        self.employee_fields['material_status']['value'] = ("Alone", "Married", "Other")
        self.employee_fields['material_status'].grid(column=1, row=7, sticky='we', padx=5, pady=5)


        # Column 3
        column3 = ttk.Frame(emp_frame)
        column3.columnconfigure(0, weight=1)
        column3.columnconfigure(1, weight=1)
        column3.columnconfigure(2, weight=1)
        column3.grid(column=1, row=2, sticky='ne')

        # Save button
        save_button = tk.Button(column3,
                                text="Save",
                                width=10,
                                bg='blue',
                                fg="white",
                                command=self.save_emp)
        save_button.grid(column=0, row=2, padx=10)

        # Update button
        update_btn = tk.Button(master=column3, text='Update', width=10, bg='orange', fg="black")
        update_btn.bind('<Button>', self.update_emp)
        update_btn.grid(column=1, row=2, padx=10)

        # Reset button
        reset_btn = tk.Button(master=column3, text='Reset', width=10, bg='gray', fg="white")
        reset_btn.bind('<Button>', self.reset_form)
        reset_btn.grid(column=2, row=2, padx=10)
        return emp_frame


    def init_employee_grid_data(self, container, empList):
        """Grid data contain employee data"""

        style = ttk.Style()
        style.configure("Treeview", lightcolor="red", bordercolor="#454545", darkcolor="yellow", font=('Segoe UI', 10, ''))
        style.configure("Treeview.Heading", fg='#00337f',font=('Segoe UI', 11, 'bold'))

        columnTitles = ("employee_id", "first_name", 'last_name', 'birthday', 'gender', 'email', 'phone_number', 'basic_salary', 'address', 'material_status')
        self.employee_fields['tree'] = ttk.Treeview(container, columns=columnTitles, show='headings')
        self.employee_fields['tree'].heading('employee_id', text='Employee Id')
        self.employee_fields['tree'].column("employee_id", anchor='center')
        self.employee_fields['tree'].heading('first_name', text='First Name')
        self.employee_fields['tree'].column("first_name", anchor='center')
        self.employee_fields['tree'].heading('last_name', text='Last Name')
        self.employee_fields['tree'].column("last_name", anchor='center')
        self.employee_fields['tree'].heading('birthday', text='Birthday')
        self.employee_fields['tree'].column("birthday", anchor='center')
        self.employee_fields['tree'].heading('gender', text='Gender')
        self.employee_fields['tree'].column("gender", anchor='center')
        self.employee_fields['tree'].heading('email', text='Email')
        self.employee_fields['tree'].column("email", anchor='center')
        self.employee_fields['tree'].heading('phone_number', text='Phone number')
        self.employee_fields['tree'].column("phone_number", anchor='center')
        self.employee_fields['tree'].heading('basic_salary', text='Basic salary')
        self.employee_fields['tree'].column("basic_salary", anchor='center')
        self.employee_fields['tree'].heading('address', text='Address')
        self.employee_fields['tree'].column("address", anchor='w')
        self.employee_fields['tree'].heading('material_status', text='Material Status')
        self.employee_fields['tree'].column("material_status", anchor='center')

        # Set color for odd and even row in grid
        self.employee_fields['tree'].tag_configure('odd', background='#E8E8E8')
        self.employee_fields['tree'].tag_configure('even', background='#DFDFDF')

        # Init sample data
        records = []
        for i in range(1, 100):
            records.append((f'Id{i}', f'first {i}', f'last {i}', f'{i}/{i}/{i}', random.randrange(0, 3, 1), f'email{i}@gmail.com', random.randrange(3000000, 5000000, 100), f'Salary: {i}', f'Address {i}', f'Material status {i}'))
        # Add add to tree
        for r in records:
            self.employee_fields['tree'].insert('', tk.END, values=r)

        self.employee_fields['tree'].bind("<<TreeviewSelect>>", self.row_selected)

        return self.employee_fields['tree']


    def create_main_window(self):
        """Create init main windows include employee form and grid data"""
        windll.shcore.SetProcessDpiAwareness(1)     # improve quality on UI
        root = tk.Tk()

        root.iconbitmap(r'D:\$ STUDY\Learn University at UIT\Semester 3\Python\project\QuanLyNhaHang\assets\restaurant.ico')
        root.title("Employee Information")

        root.resizable(True, True)
        root.state('zoomed')  # full screen

        root.rowconfigure(0, weight=1)
        root.rowconfigure(1, weight=9)
        root.columnconfigure(0, weight=9)
        root.columnconfigure(1, weight=1)

        root['bg'] = 'gray'

        # Employee input form
        emp_form = self.init_emp_frame(root)
        emp_form.grid(column=0, row=0, sticky='nwse', columnspan=2)

        # Employee grid
        grid_data = self.init_employee_grid_data(root, [])
        grid_data.grid(column=0, row=1, sticky='nwse')

        scrollbarx = tk.Scrollbar(root, orient='horizontal', command=grid_data.xview, width=20)
        scrollbary = tk.Scrollbar(root, orient='vertical', command=grid_data.yview, width=20)
        grid_data.configure(xscroll=scrollbarx.set)
        grid_data.configure(yscroll=scrollbary.set)
        scrollbarx.grid(column=0, row=2, sticky='nwse', columnspan=2)
        scrollbary.grid(column=1, row=1, sticky='nwse', rowspan=2)

        root.mainloop()

if __name__ == '__main__':
    empApp = EmployeeUI()
    empApp.create_main_window()
