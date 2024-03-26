import tkinter as tk
from ctypes import windll
from tkinter.messagebox import showinfo

FONT_FAMILY = ("Roboto", 14)


# Set up root windows
windll.shcore.SetProcessDpiAwareness(1)     # improve quality on UI
window = tk.Tk()
window.title("Employee Information")
window_width = 1368
window_height = 768

# Get the screen dimension
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

# find the center point
center_x = int(screen_width/2 - window_width / 2)
center_y = int(screen_height/2 - window_height / 2)

# window.resizable(False, False)
# window.iconbitmap('../../assets/restaurant.ico')
window.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')


# Model
empId = tk.StringVar();
firstName = tk.StringVar();
lastName = tk.StringVar();
birthDate = tk.StringVar();
gender = tk.BooleanVar();
phoneNumber = tk.StringVar();
email = tk.StringVar();
basicSalary = tk.DoubleVar();
address = tk.StringVar();
materialStatus = tk.IntVar();
avatarUrl = tk.IntVar();
createdDate = tk.StringVar();
createdDate = tk.StringVar();

employeeFields = {}


# Functions use on this page
def save_emp():
    showinfo('Click save button', "Hello Hieu Bui")


# Employee frame
empFrame = tk.Frame(window, width=350, height=200)


# Avatar
# material_status_lbl = tk.Label(window, text='Avatar:')
# material_status_lbl.pack()
# material_status_entry = tk.Entry(window)
# material_status_entry.pack()

# Employee Id
employeeFields['empId_lbl'] = tk.Label(text="Employee ID: ")
employeeFields['emp_id'] = tk.Entry(window)

#First name
employeeFields['first_name_lbl'] = tk.Label(text='First Name:')
employeeFields['fist_name'] = tk.Entry(window)

#Last name
employeeFields['last_name_lbl'] = tk.Label(text='Last Name:')
employeeFields['last_name'] = tk.Entry(window)

# Birthday
employeeFields['birthday_lbl'] = tk.Label(text='Birthday:')
employeeFields['birthday'] = tk.Entry()

# Gender
employeeFields['gender_lbl'] = tk.Label(text='Gender:')
employeeFields['gender'] = tk.Entry()

#Phone number
employeeFields['phone_number_lbl'] = tk.Label(text='Phone Number:')
employeeFields['phone_number'] = tk.Entry()

# Email
employeeFields['email_lbl'] = tk.Label(text='Email:')
employeeFields['email_lbl'] = tk.Entry()

# Basic salary
employeeFields['basic_salary_lbl'] = tk.Label(text='Basic Salary:')
employeeFields['basic_salary'] = tk.Entry()

# Address
employeeFields['address_lbl'] = tk.Label(text='Address:')
employeeFields['address'] = tk.Entry()

# Material Status
employeeFields['material_status_lbl'] = tk.Label(text='Material Status:')
employeeFields['material_status'] = tk.Entry()

for field in employeeFields.values():
    field.pack(anchor=tk.W, padx=2, pady=3, fill=tk.X)

save_button = tk.Button(empFrame,
                        text="Save",
                        width='20',
                        height='10',
                        bg='red',
                        command=save_emp)
save_button.pack(expand=True, pady=10)
save_button.pack()


# Grid data





window.mainloop()