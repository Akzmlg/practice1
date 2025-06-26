import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from ImageProcessor import ImageProcessor
from ResizeDialog import ResizeDialog
from BrightnessAdjustDialog import BrightnessAdjustDialog
from DrawRedCircleDialog import DrawRedCircleDialog

# Класс предназначен для отображения пользовательского интерфейса
class UserApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Работа с изображениями. Практика 1")
        self.image_processor = ImageProcessor()
        self.image = None
        self.photo = None
        self.current_channel = None

        self.create_interface()

    # Создает основной интерфейс
    def create_interface(self):

        # Загрузка изображения
        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(pady=5)

        # Загрузка из файла
        tk.Button(
            self.button_frame,
            text="Загрузить изображение",
            command=self.load_image
        ).pack(side=tk.LEFT, padx=3)

        # Загрузка из камеры
        tk.Button(
            self.button_frame,
            text="Получить изображение с веб-камеры",
            command=self.get_image_from_webcam
        ).pack(side=tk.LEFT, padx=3)

        # Кнопки каналов
        self.channel_frame = tk.Frame(self.root)
        self.channel_frame.pack(pady=3)

        self.channel_buttons = {
            'all': tk.Button(self.channel_frame, text="Все каналы",
                             command=self.show_all_channels),
            'red': tk.Button(self.channel_frame, text="Красный канал",
                             command=lambda: self.show_channel('red')),
            'green': tk.Button(self.channel_frame, text="Зеленый канал",
                               command=lambda: self.show_channel('green')),
            'blue': tk.Button(self.channel_frame, text="Синий канал",
                              command=lambda: self.show_channel('blue'))

        }

        for btn in self.channel_buttons.values():
            btn.pack(side=tk.LEFT, padx=5)
            btn.config(state=tk.DISABLED)

        # Кнопки варианта
        self.variant_frame = tk.Frame(self.root)
        self.variant_frame.pack(pady=10)

        self.variant_buttons = {
            'resize': tk.Button(self.variant_frame, text="Изменить размер", command=self.resize),
            'reduce_brightness': tk.Button(self.variant_frame, text="Уменьшить яркость",
                                           command=self.reduce_brightness),
            'draw_red_circle': tk.Button(self.variant_frame, text="Нарисовать красный круг",
                                         command=self.draw_red_circle)
        }

        for btn in self.variant_buttons.values():
            btn.pack(side=tk.LEFT, padx=5)
            btn.config(state=tk.DISABLED)

        # Отображение изображения
        self.image_label = tk.Label(self.root)
        self.image_label.pack(pady=10)

    # Загрузка изображения из файла
    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Изображения", "*.jpg *.jpeg *.png")])
        if file_path:
            try:
                self.image = self.image_processor.load_image(file_path)
                self.show_all_channels()
                self.toggle_buttons(True)
            except Exception as e:
                messagebox.showerror("Error", f"Не удалось загрузить изображение. "
                                              f"Возможно файла не существует,"
                                              f" или его следует переименовать"
                                              f" на латинские буквы: {str(e)}")

    # Получение изображения с веб-камеры
    def get_image_from_webcam(self):
        try:
            self.image = self.image_processor.get_image_from_webcam()
            self.show_all_channels()
            self.toggle_buttons(True)
        except Exception as e:
            messagebox.showerror("Ошибка",
                                 f"Ошибка работы с камерой: {str(e)}")

    # Переключение доступности кнопок
    def toggle_buttons(self, state):
        for btn in self.channel_buttons.values():
            btn.config(state=tk.NORMAL if state else tk.DISABLED)
        for btn in self.variant_buttons.values():
            btn.config(state=tk.NORMAL if state else tk.DISABLED)

    # Переключение на канал - красный, зеленый, синий
    def show_channel(self, channel):
        if self.image is None:
            messagebox.showerror("Ошибка", "Изображение не загружено!")
            return
        self.current_channel = channel
        channel_img = self.image_processor.extract_channel(self.image, channel)
        self.display_image(channel_img)

    # Переключение на нормальное отображение
    def show_all_channels(self):
        if self.image is None:
            messagebox.showerror("Ошибка", "Изображение не загружено!")
            return
        self.current_channel = None
        self.display_image(self.image)

    # Изменение размера изображения
    def resize(self):
        if self.image is None:
            messagebox.showerror("Ошибка", "Изображение не загружено!")
            return
        current_height, current_width = self.image.shape[:2]
        dialog = ResizeDialog(self.root, current_width, current_height)

        if hasattr(dialog, 'result') and dialog.result is not None:
            new_width, new_height = dialog.result
            try:
                self.image = self.image_processor.resize(
                    self.image,
                    new_width,
                    new_height
                )

                if self.current_channel == None:
                    self.show_all_channels()
                else:
                    self.show_channel(self.current_channel)

            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось "
                                               f"изменить размер изображения: {str(e)}")

    # Снижение яркости изображения
    def reduce_brightness(self):
        if self.image is None:
            messagebox.showerror("Ошибка", "Изображение не загружено!")
            return

        dialog = BrightnessAdjustDialog(self.root)
        if hasattr(dialog, 'result') and dialog.result is not None:
            brightness_adjust_value = dialog.result
            try:
                self.image = self.image_processor.adjust_brightness(
                    self.image,
                    brightness_adjust_value
                )

                if self.current_channel == None:
                    self.show_all_channels()
                else:
                    self.show_channel(self.current_channel)

            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось "
                                               f"изменить яркость изображения: {str(e)}")

    # Рисует красный круг по введенным данным
    def draw_red_circle(self):
        if self.image is None:
            messagebox.showerror("Ошибка", "Изображение не загружено!")
            return

        current_height, current_width = self.image.shape[:2]
        dialog = DrawRedCircleDialog(self.root, current_height, current_width)
        if hasattr(dialog, 'result') and dialog.result is not None:
            circle_x, circle_y, radius = dialog.result;
            try:
                self.image = self.image_processor.draw_red_circle(
                    self.image,
                    circle_x,
                    circle_y,
                    radius)

                if self.current_channel == None:
                    self.show_all_channels()
                else:
                    self.show_channel(self.current_channel)

            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось "
                                   f"изменить размер изображения: {str(e)}")

    # Отображение картинки
    def display_image(self, img):
        img_pil = Image.fromarray(img)

        self.photo = ImageTk.PhotoImage(img_pil)
        self.image_label.config(image=self.photo)
        self.image_label.image = self.photo


if __name__ == "__main__":
    root = tk.Tk()
    app = UserApp(root)
    root.mainloop()
