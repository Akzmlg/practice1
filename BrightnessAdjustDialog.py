import tkinter as tk
from tkinter import simpledialog

# Диалог ввода данных для изменения яркости изображения
class BrightnessAdjustDialog(tk.simpledialog.Dialog):
    def __init__(self, parent):
        super().__init__(parent, "Понизить яркость")

    def body(self, master):
        tk.Label(master, text="Изменение яркости:").grid(row=0, sticky=tk.W)

        self.brightness_entry = tk.Entry(master)
        self.brightness_entry.grid(row=0, column=1)

        return self.brightness_entry

    def validate(self):
        try:
            brightness = int(self.brightness_entry.get())
            if brightness <= 0 or brightness > 255:
                raise ValueError
            self.result = brightness
            return True
        except ValueError:
            tk.messagebox.showerror("Ошибка", "Некорректный ввод!")
            return False