import tkinter as tk
from tkinter import ttk
from ctypes import windll
from tkinter.messagebox import showinfo
from PIL import Image
from tkcalendar import Calendar

class EmployeeUI:

    def __init__(self):
        self.controller = None

    def set_controller(self, controller):
        """Set controller use for this view"""
        self.controller = controller

    def save_emp(self):
        """Save employee information"""
        showinfo('Click save button', "Hello Hieu Bui")
        return True

    def update_emp(self, event):
        """Update employee information"""
        print(event)
        showinfo('Click update button', "Update employee info")
        return True

    def init_emp_frame(self, container):
        """Create Employee form input form user"""
        employeeFields = {}
        empFrame = ttk.Frame(container)

        empFrame.columnconfigure(0, weight=1)
        empFrame.columnconfigure(1, weight=3)
        empFrame.columnconfigure(2, weight=3)
        empFrame.columnconfigure(3, weight=3)

        # Column 1
        # Avatar
        ttk.Label(empFrame, text="Employee Avatar").grid(row=3, column=0, padx=5, pady=5, sticky="swse")

        # Employee Id
        column1 = ttk.Frame(empFrame)
        column1.columnconfigure(0, weight=1)
        column1.columnconfigure(0, weight=3)
        column1.grid(column=1, row=0)

        employeeFields['empId_lbl'] = ttk.Label(column1, text="Employee ID: ")
        employeeFields['empId_lbl'].grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)

        employeeFields['emp_id'] = ttk.Entry(master=column1)
        employeeFields['emp_id'].grid(column=1, row=0, sticky='we', padx=5, pady=5)

        #First name
        employeeFields['first_name_lbl'] = tk.Label(column1, text='First Name:')
        employeeFields['first_name_lbl'].grid(column=0, row=1, sticky=tk.W, padx=5, pady=5)
        employeeFields['first_name'] = ttk.Entry(master=column1)
        employeeFields['first_name'].grid(column=1, row=1, sticky='we', padx=5, pady=5)

        #Last name
        employeeFields['last_name_lbl'] = tk.Label(column1, text='Last Name:')
        employeeFields['last_name_lbl'].grid(column=0, row=2, sticky=tk.W, padx=5, pady=5)
        employeeFields['last_name'] = ttk.Entry(master=column1)
        employeeFields['last_name'].grid(column=1, row=2, sticky='we', padx=5, pady=5)

        # Birthday
        employeeFields['birthday_lbl'] = tk.Label(column1, text='Birthday:')
        employeeFields['birthday_lbl'].grid(column=0, row=3, sticky=tk.W, padx=5, pady=5)
        employeeFields['birthday'] = Calendar(column1)
        employeeFields['birthday'].grid(column=1, row=3, sticky='we', padx=5, pady=5)


        # Column 2
        column2 = ttk.Frame(empFrame)
        column2.columnconfigure(0, weight=1)
        column2.columnconfigure(0, weight=3)
        column2.grid(column=2, row=0, sticky='nw')

        # Gender
        employeeFields['gender_lbl'] = tk.Label(column2, text='Gender:')
        employeeFields['gender_lbl'].grid(column=0, row=0, sticky='nw', padx=5, pady=5)
        employeeFields['gender'] = tk.StringVar()
        # gender_data = [{"text": 'Male', 'value': '0'}, {"text": 'Female', 'value': '1'}, {"text": 'Other', 'value': '2'}]
        r1 = ttk.Radiobutton(column2, text='Male', value='0', variable=employeeFields['gender'])
        r2 = ttk.Radiobutton(column2, text='Female', value='1', variable=employeeFields['gender'])
        r3 = ttk.Radiobutton(column2, text='Other', value='2', variable=employeeFields['gender'])
        r1.grid(column=1, row=0, sticky=tk.W, padx=5, pady=5)
        r2.grid(column=1, row=1, sticky=tk.W, padx=5, pady=5)
        r3.grid(column=1, row=2, sticky=tk.W, padx=5, pady=5)

        #Phone number
        employeeFields['phone_number_lbl'] = tk.Label(column2, text='Phone Number:')
        employeeFields['phone_number_lbl'].grid(column=0, row=3, sticky=tk.W, padx=5, pady=5)
        employeeFields['phone_number'] = ttk.Entry(master=column2)
        employeeFields['phone_number'].grid(column=1, row=3, sticky='we', padx=5, pady=5)

        # Email
        employeeFields['email_lbl'] = tk.Label(column2, text='Email:')
        employeeFields['email_lbl'].grid(column=0, row=4, sticky=tk.W, padx=5, pady=5)
        employeeFields['email'] = tk.Entry(column2)
        employeeFields['email'].grid(column=1, row=4, sticky='we', padx=5, pady=5)

        # Basic salary
        employeeFields['basic_salary_lbl'] = tk.Label(column2, text='Basic Salary:')
        employeeFields['basic_salary_lbl'].grid(column=0, row=5, sticky=tk.W, padx=5, pady=5)
        employeeFields['basic_salary'] = tk.Entry(column2)
        employeeFields['basic_salary'].grid(column=1, row=5, sticky='we', padx=5, pady=5)

        # Address
        employeeFields['address_lbl'] = ttk.Label(column2, text='Address:')
        employeeFields['address_lbl'].grid(column=0, row=6, sticky=tk.W, padx=5, pady=5)
        employeeFields['address'] = ttk.Entry(column2)
        employeeFields['address'].grid(column=1, row=6, sticky='we', padx=5, pady=5)

        # Material Status
        employeeFields['material_status_lbl'] = ttk.Label(column2, text='Material Status:')
        employeeFields['material_status_lbl'].grid(column=0, row=6, sticky=tk.W, padx=5, pady=5)
        employeeFields['material_status'] = ttk.Combobox(column2)
        employeeFields['material_status']['value'] = ("Alone", "Married", "Other")
        employeeFields['material_status'].grid(column=1, row=6, sticky='we', padx=5, pady=5)


        # Column 3
        column3 = ttk.Frame(empFrame)
        column3.columnconfigure(0, weight=1)
        column3.columnconfigure(1, weight=1)
        column3.grid(column=3, row=0, sticky='nw')

        # Save button
        save_button = tk.Button(column3,
                                text="Save",
                                width=5,
                                height=3,
                                bg='blue',
                                fg="white",
                                command=self.save_emp)
        save_button.grid(column=0, row=2)

        # Update button
        update_btn = tk.Button(master=column3, text='Update', width=5, height=3, bg='orange', fg="black")
        update_btn.bind('<Button>', self.update_emp)
        update_btn.grid(column=1, row=2)
        return empFrame


    def init_employee_grid_data(self, container, empList):
        """Grid data contain employee data"""
        columnTitles = ("employee_id", "first_name", 'last_name', 'birthday', 'gender', 'email', 'phone_number', 'basic_salary', 'address', 'material_status')
        tree = ttk.Treeview(container, columns=columnTitles, show='headings')
        tree.heading('employee_id', text='Employee Id')
        tree.heading('first_name', text='First Name')
        tree.heading('last_name', text='Last Name')
        tree.heading('birthday', text='Birthday')
        tree.heading('gender', text='Gender')
        tree.heading('email', text='Email')
        tree.heading('phone_number', text='Phone number')
        tree.heading('basic_salary', text='Basic salary')
        tree.heading('address', text='Address')
        tree.heading('material_status', text='Material Status')

        # Init sample data
        records = []
        for i in range(1, 100):
            records.append((f'Id{i}', f'first {i}', f'last {i}', f'{i}/{i}/{i}', f'Gender {i}', f'email{i}@gmail.com', f'Phone number: {i}', f'Salary: {i}', f'Address {i}', f'Material status {i}'))
        # Add add to tree
        for r in records:
            tree.insert('', tk.END, values=r)

        return tree


    def create_main_window(self):
        """Create init main windows include employee form and grid data"""
        windll.shcore.SetProcessDpiAwareness(1)     # improve quality on UI
        root = tk.Tk()

        root.iconbitmap(r'D:\$ STUDY\Learn University at UIT\Semester 3\Python\project\QuanLyNhaHang\assets\restaurant.ico')
        root.title("Employee Information")
        window_width = 1920
        window_height = 768

        # Get the screen dimension
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        # find the center point
        center_x = int(screen_width/2 - window_width / 2)
        center_y = int(screen_height/2 - window_height / 2)

        root.resizable(True, True)
        root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

        root.rowconfigure(0, weight=1)
        root.rowconfigure(1, weight=5)

        root['bg'] = 'gray'
        emp_form = self.init_emp_frame(root)
        emp_form.grid(column=0, row=0, sticky='nwse')

        grid_data = self.init_employee_grid_data(root, [])
        grid_data.grid(column=0, row=1, sticky='nwse')

        root.mainloop()

if __name__ == '__main__':
    empApp = EmployeeUI()
    empApp.create_main_window()
