import tkinter as tk

#Tkinter Test
root = tk.Tk()
root.title("Tkinter Test")
root.geometry("700x500")
label = tk.Label(root, text="Hello Tkinter!")
label.pack()
root.mainloop()