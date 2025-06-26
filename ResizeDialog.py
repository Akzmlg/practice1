import tkinter as tk
from tkinter import simpledialog

# Диалог ввода данных для изменения размера изображения
class ResizeDialog(tk.simpledialog.Dialog):
    def __init__(self, parent, current_width, current_height):
        self.current_width = current_width
        self.current_height = current_height
        super().__init__(parent, "Изменить размер изображения")

    def body(self, master):
        tk.Label(master, text="Ширина:").grid(row=0, sticky=tk.W)
        tk.Label(master, text="Высота:").grid(row=1, sticky=tk.W)

        self.width_entry = tk.Entry(master)
        self.height_entry = tk.Entry(master)

        self.width_entry.grid(row=0, column=1)
        self.height_entry.grid(row=1, column=1)

        # Установка текущих размеров по умолчанию
        self.width_entry.insert(0, str(self.current_width))
        self.height_entry.insert(0, str(self.current_height))

        return self.width_entry

    def validate(self):
        try:
            width = int(self.width_entry.get())
            height = int(self.height_entry.get())
            if width <= 0 or height <= 0:
                raise ValueError
            self.result = (width, height)
            return True
        except ValueError:
            tk.messagebox.showerror("Ошибка", "Некорректный ввод!")
            return False