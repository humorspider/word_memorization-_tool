import tkinter as tk

root = tk.Tk()

# 上左部分
label1 = tk.Label(root, text="角色A")
label1.grid(row=0, column=0)

# 上右部分
label2 = tk.Label(root, text="角色B")
label2.grid(row=0, column=1)

# 中间部分
label3 = tk.Label(root, text="事件")
label3.grid(row=1, column=0, columnspan=2)

# 下部分
label4 = tk.Label(root, text="结果")
label4.grid(row=2, column=0, columnspan=2)

root.mainloop()
