import cv2
import numpy as np

# Реализует основные функции работы с приложением
class ImageProcessor:

    # Получение изображения из файла
    def load_image(self, file_path):

        image = cv2.imread(file_path)
        if image is None:
            raise ValueError("Не удалось прочитать файл.")
        return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Получение изображения с веб-камеры
    def get_image_from_webcam(self):

        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            raise RuntimeError("Не удалось открыть веб-камеру.")

        ret, frame = cap.read()
        cap.release()

        if not ret:
            raise RuntimeError("Не удалось получить изображение с веб-камеры.")

        return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Оставляет в изображении только нужный канал
    def extract_channel(self, image, channel):

        channel_img = np.zeros_like(image)

        if channel == 'red':
            channel_img[:, :, 0] = image[:, :, 0]
        elif channel == 'green':
            channel_img[:, :, 1] = image[:, :, 1]
        elif channel == 'blue':
            channel_img[:, :, 2] = image[:, :, 2]

        return channel_img

    # Изменяет размер изображения
    def resize(self, image, width, height):
        return cv2.resize(image, (width, height), interpolation=cv2.INTER_AREA)

    # Добавляем яркость к каждому пикселю. Смешивание с пустым изображением
    def adjust_brightness(self, image, value):
        return cv2.addWeighted(image, 1, np.zeros(image.shape, image.dtype), 0, -value)

    # Рисует красный круг на изображении
    def draw_red_circle(self, image, x, y, radius):
        return cv2.circle(image, center = (x, y), radius=radius, color=(255, 0, 0), thickness=2)