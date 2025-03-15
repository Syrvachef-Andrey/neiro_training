import cv2
import qrcode
from pyzbar import pyzbar
from PIL import Image
import tkinter as tk
from tkinter import messagebox


# Функция для создания QR-кода
def create_qr_code(data: str, filename: str = "qr_code.png"):
    """
    Создаёт QR-код с указанными данными и сохраняет его в файл.

    :param data: Данные для кодирования в QR-код.
    :param filename: Имя файла для сохранения QR-кода.
    """
    qr = qrcode.QRCode(
        version=1,  # Размер QR-кода (1-40, где 1 — самый маленький)
        error_correction=qrcode.constants.ERROR_CORRECT_L,  # Уровень коррекции ошибок
        box_size=10,  # Размер каждого "бокса" QR-кода
        border=4,  # Размер границы (в боксах)
    )
    qr.add_data(data)  # Добавляем данные
    qr.make(fit=True)  # Генерируем QR-код

    img = qr.make_image(fill_color="black", back_color="white")  # Создаём изображение
    img.save(filename)  # Сохраняем QR-код в файл
    print(f"QR-код сохранён в файл: {filename}")


# Функция для проверки видеопотока на наличие QR-кода
def check_qr_in_video_stream(qr_data: str, root: tk.Tk):
    """
    Проверяет видеопоток на наличие QR-кода с указанными данными.

    :param qr_data: Данные, которые должны быть закодированы в QR-коде.
    :param root: Окно tkinter для вывода результата.
    """
    # Открываем видеопоток (0 — это камера по умолчанию)
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Ошибка: Не удалось открыть камеру.")
        return

    print("Ожидание QR-кода...")

    while True:
        # Захватываем кадр
        ret, frame = cap.read()

        if not ret:
            print("Ошибка: Не удалось получить кадр.")
            break

        # Преобразуем кадр в оттенки серого (для лучшего распознавания)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Ищем QR-коды в кадре
        barcodes = pyzbar.decode(gray)

        # Перебираем найденные QR-коды
        for barcode in barcodes:
            # Получаем данные из QR-кода
            barcode_data = barcode.data.decode("utf-8")

            # Если данные совпадают с ожидаемыми
            if barcode_data == qr_data:
                print("Успех: QR-код распознан!")

                # Закрываем видеопоток
                cap.release()
                cv2.destroyAllWindows()

                # Выводим данные в окно tkinter
                result_label = tk.Label(root, text=f"Распознано: {barcode_data}", font=("Arial", 24))
                result_label.pack(pady=20)
                return

            # Рисуем рамку вокруг QR-кода
            (x, y, w, h) = barcode.rect
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Отображаем данные QR-кода на кадре
            cv2.putText(frame, barcode_data, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Отображаем кадр
        cv2.imshow("Video Stream", frame)

        # Выход по нажатию клавиши 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Освобождаем ресурсы
    cap.release()
    cv2.destroyAllWindows()


# Основная функция
def main():
    # Данные для кодирования в QR-код
    qr_data = "Андрей Сырвачев"

    # Создаём QR-код
    create_qr_code(qr_data, "my_qr_code.png")

    # Создаём окно tkinter
    root = tk.Tk()
    root.title("Распознавание QR-кода")
    root.geometry("500x500")

    check_qr_in_video_stream(qr_data, root)

    # Запускаем главный цикл tkinter
    root.mainloop()


if __name__ == "__main__":
    main()