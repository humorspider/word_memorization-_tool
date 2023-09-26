import tkinter as tk
from tkinter import font

# 获取字体系列列表
font_families = font.families()

# 打印所有字体系列名称
for family in font_families:
    print(family)
