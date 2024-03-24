import tkinter as tk

FONT_FAMILY = ("Roboto", 14)

# Header of page
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

window.resizable(False, False)
# window.iconbitmap('../../assets/restaurant.ico')

window.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')


def save_emp():
    return False

employFrame = tk.Frame(window)
employFrame.pack(padx=5, pady=5, expand=True)


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

# Employee Id
title = tk.Label(text="Employee", justify=tk.LEFT, font=FONT_FAMILY)
title.pack()
empIdTxtBox = tk.Entry(employFrame, textvariable=empId)
empIdTxtBox.pack()

button = tk.Button(
    text="Save",
    width=5,
    height=2,
    bg="blue",
    fg="yellow"
)
button.pack()

window.mainloop()