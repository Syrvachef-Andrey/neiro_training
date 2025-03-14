import cv2
import tkinter as tk
from tkinter import messagebox

# Функция для захвата и сохранения изображения
def capture_and_save_image(filename):
    if not filename:
        messagebox.showwarning("Ошибка", "Название файла не введено!")
        return

    filename = filename.split()
    filename = filename[0] + "_" + filename[1] + "_" + filename[2] + ".jpg"

    # Захват изображения с камеры
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        messagebox.showerror("Ошибка", "Не удалось открыть камеру!")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            messagebox.showerror("Ошибка", "Не удалось захватить изображение!")
            return

        cv2.imshow('Video', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.imwrite(f"./dataset/{filename}", frame)
            messagebox.showinfo("Успех", f"Изображение сохранено как {filename}")
            break

    cap.release()
    cv2.destroyAllWindows()

# Функция для обработки ввода и вызова захвата изображения
def on_submit(entry):
    filename = entry.get()  # Получаем название файла из поля ввода
    capture_and_save_image(filename)

def save_image_global():
    # Создаем графический интерфейс
    root = tk.Tk()
    root.title("Сохранение изображения с камеры")

    # Поле ввода для названия файла
    label = tk.Label(root, text="Введите название свое ФИО:")
    label.pack(pady=10)

    entry = tk.Entry(root, width=40)
    entry.pack(pady=10)

    # Кнопка для запуска захвата и сохранения
    submit_button = tk.Button(
        root,
        text="Для сохранения изображение введите имя и фамилию, нажмите на эту кнопку, а когда вам подойдет изображение нажмите q",
        command=lambda: on_submit(entry)  # Передаем entry в on_submit
    )
    submit_button.pack(pady=10)

    root.mainloop()

# Если этот файл запущен как основной, вызываем функцию
if __name__ == "__main__":
    save_image_global()