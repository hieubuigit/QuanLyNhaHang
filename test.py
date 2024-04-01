
import tkinter as tk
from tkinter import ttk
from ctypes import windll

root = tk.Tk()
windll.shcore.SetProcessDpiAwareness(1)     # improve quality on UI
root.title('Tkinter Pack Layout')
root.geometry('600x400')

# 1. Learn pack()
# label1 = tk.Label(master=root, text='Tkinter',bg='red',fg='white')
# label2 = tk.Label(master=root,text='Pack Layout',bg='green', fg='white')
# label3 = tk.Label(master=root, text='Demo',bg='blue', fg='white')
# label4 = tk.Label(master=root, text='Demo',bg='blue', fg='white')

# label1.pack(side=tk.TOP, expand=True, fill=tk.X)
# label4.pack(side=tk.TOP, expand=True, fill=tk.Y)
# label2.pack(side=tk.TOP, expand=True, fill=tk.NONE, ipadx=55, ipady=10, pady=100)
# label3.pack(side=tk.TOP, expand=True, fill=tk.BOTH)

## Ancor
# box1 = tk.Label(root, text="Box 1", bg="green", fg="white")
# box1.pack(ipadx=20, ipady=20, anchor=tk.E,  expand=True)
# box2 = tk.Label(root, text="Box 2", bg="red", fg="white")
# box2.pack(ipadx=20, ipady=20, anchor=tk.W, expand=True)



# 2. Learn TKinter Grid
# root.columnconfigure(0, weight=50)
# root.rowconfigure(1, weight=50)



# 3. Learn Tkinter place
# label1 = tk.Label(master=root, text='Box 1',bg='yellow',fg='black', width=10, height=2)
# label1.place(x=10, y=10, width=50, height=50, anchor='center')

# label2 = tk.Label(master=root, text='Box 2',bg='red',fg='white', width=10, height=2)
# label2.place(relx=0.5, rely=0.5, relwidth=0.5, relheight=0.5, anchor='center')


# 4. Learn Frame
# frame = ttk.Frame(root, borderwidth=5, relief='solid', padding=(5, 4, 3, 2), height=100, width=200)


root.mainloop()