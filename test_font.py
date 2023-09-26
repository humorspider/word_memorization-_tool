import tkinter as tk

# 创建根窗口
root = tk.Tk()

# 创建向左布局的组件
left_label = tk.Label(root, text="Left Label")
left_label.pack(side="left")
left_text = tk.Text(root, height=4, width=20)
left_text.insert("end", "This is left text.")
left_text.pack(side="left")

# 创建向右布局的组件
right_label = tk.Label(root, text="Right Label")
right_label.pack(side="right")
right_text = tk.Text(root, height=4, width=20)
right_text.insert("end", "This is right text.")
right_text.pack(side="right")

# 启动主循环
root.mainloop()
