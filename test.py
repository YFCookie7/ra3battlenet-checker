import tkinter as tk

root = tk.Tk()
root.title("Resizable Grid Example")

# Configure row and column weights
root.grid_rowconfigure(0, weight=1)  # 1st row takes 100% height
root.grid_rowconfigure(1, weight=1)  # 2nd row takes 100% height
root.grid_columnconfigure(0, weight=1)  # 1st column takes 50% width
root.grid_columnconfigure(1, weight=1)  # 2nd column takes 30% width
root.grid_columnconfigure(2, weight=1)  # 3rd column takes 20% width

# Create and place widgets
label1 = tk.Label(root, text="Widget 1")
label1.grid(row=0, column=0, sticky="nsew")  # Sticky ensures widget expands with cell

label2 = tk.Label(root, text="Widget 2")
label2.grid(row=0, column=1, sticky="nsew")

label3 = tk.Label(root, text="Widget 3")
label3.grid(row=0, column=2, sticky="nsew")

label4 = tk.Label(root, text="Widget 4")
label4.grid(row=1, column=0, columnspan=3, sticky="nsew")  # Spanning all columns

root.mainloop()
