import cv2
import time
import face_recognition
import os
from pathlib import Path

# Функция для захвата изображения с камеры
def capture_image():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Ошибка: Не удалось открыть камеру.")
        exit()

    start_time = time.time()
    last_frame = None

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Ошибка: Не удалось получить кадр.")
            break

        cv2.imshow('Webcam Stream', frame)
        last_frame = frame

        if time.time() - start_time >= 3:  # Ждём 3 секунды
            break

        if cv2.waitKey(1) & 0xFF == ord('q'):  # Выход по нажатию 'q'
            break

    cap.release()
    cv2.destroyAllWindows()

    if last_frame is not None:
        save_path = "/home/andrey/tank_AI/neiro_training/database/some_photo.jpg"
        cv2.imwrite(save_path, last_frame, [cv2.IMWRITE_JPEG_QUALITY, 100])
        print(f"Фото сохранено по пути: {save_path}")
        return save_path
    else:
        print("Ошибка: Не удалось захватить кадр.")
        return None

# Функция для сравнения лиц
def compare_faces(image1_path, image2_path):
    image1 = face_recognition.load_image_file(image1_path)
    image2 = face_recognition.load_image_file(image2_path)

    face_locations = face_recognition.face_locations(image2)
    if len(face_locations) == 0:
        print(f"Лицо не найдено на изображении: {image2_path}")
        return False

    face_encoding1 = face_recognition.face_encodings(image1)[0]
    face_encoding2 = face_recognition.face_encodings(image2)[0]

    results = face_recognition.compare_faces([face_encoding1], face_encoding2)

    if results[0]:
        print(f"Совпадение найдено! Это один и тот же человек.")
        return True
    else:
        print(f"Совпадение не найдено")
        return False

# Основной код
def main():
    # Захватываем изображение с камеры
    captured_image_path = capture_image()

    if captured_image_path is None:
        return

    # Путь к директории с базой данных изображений
    database_dir = Path("/home/andrey/tank_AI/neiro_training/database")

    # Перебираем все изображения в директории
    for image_path in database_dir.glob("*.jpg"):
        if image_path.name == "some_photo.jpg":  # Пропускаем только что сохранённое изображение
            continue

        print(f"Сравниваю с изображением: {image_path}")
        if compare_faces(image_path, captured_image_path):
            print(f"Найдено совпадение с изображением: {image_path}")
            break
    else:
        print("Совпадений не найдено.")

if __name__ == "__main__":
    main()