import tkinter as tk
from tkinter import simpledialog

# Диалог ввода данных для вывода круга на изображении
class DrawRedCircleDialog(tk.simpledialog.Dialog):
    def __init__(self, parent, max_height, max_width):
        self.max_height = max_height
        self.max_width = max_width
        super().__init__(parent, "Нарисовать красный круг")

    def body(self, master):
        tk.Label(master, text="Отступ слева (X):").grid(row=0, sticky=tk.W)
        tk.Label(master, text="Отступ сверху (Y):").grid(row=1, sticky=tk.W)
        tk.Label(master, text="Радиус:").grid(row=2, sticky=tk.W)

        self.x_entry = tk.Entry(master)
        self.y_entry = tk.Entry(master)
        self.radius_entry = tk.Entry(master)

        self.x_entry.grid(row=0, column=1)
        self.y_entry.grid(row=1, column=1)
        self.radius_entry.grid(row=2, column=1)

        return self.x_entry

    def validate(self):
        try:
            x_value = int(self.x_entry.get())
            y_value = int(self.y_entry.get())
            radius_value = int(self.radius_entry.get())
            if radius_value <= 0 or x_value < 0 or y_value < 0\
                    or x_value > self.max_height or y_value > self.max_width:
                raise ValueError
            self.result = (x_value, y_value, radius_value)
            return True
        except ValueError:
            tk.messagebox.showerror("Ошибка", "Некорректный ввод!")
            return False