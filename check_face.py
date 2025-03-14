import cv2
import face_recognition
# Инициализация видеозахвата (0 — индекс камеры по умолчанию)
cap = cv2.VideoCapture(0)

# Проверка, удалось ли открыть камеру
if not cap.isOpened():
    print("Ошибка: Не удалось открыть камеру.")
    exit()

# Бесконечный цикл для захвата и отображения кадров
while True:
    # Считывание кадра
    ret, frame = cap.read()

    # Если кадр не считан, выходим из цикла
    if not ret:
        print("Ошибка: Не удалось получить кадр.")
        break

    # Отображение кадра в окне с именем "Webcam Stream"
    cv2.imshow('Webcam Stream', frame)

    # Выход из цикла по нажатию клавиши 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Освобождение ресурсов камеры и закрытие окон
cap.release()
cv2.destroyAllWindows()