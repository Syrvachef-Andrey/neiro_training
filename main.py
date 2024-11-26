import cv2
from ultralytics import YOLO
from ultralytics import solutions
import torch
import datetime

global count_of_people

class ObjectDetection:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        assert self.cap.isOpened(), "Error reading video file"
        self.cap.set(3, 800)
        w, h, fps = (int(self.cap.get(x)) for x in (cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT, cv2.CAP_PROP_FPS))

        self.model = YOLO("yolo11n.pt")

        # Define region points
        self.region_points = {
            "region-01": [(0, 0), (650, 0), (650, 500), (0, 500)],
        }
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        # Video writer
        self.frame, self.video_writer = self.cap.read()

        # Init Object Counter
        self.region = solutions.RegionCounter(
            show=True,
            region=self.region_points,
            model="yolo11n.pt",
        )
        if self.region.model is None:
            print("Модель не загружена. Проверьте путь к модели.")
            exit(1)

    def exit_image(self):
        while self.cap.isOpened():
            success, im0 = self.cap.read()
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            if not success:
                print("Video frame is empty or video processing has been successfully completed.")
                break

            try:
                im0 = self.region.count(im0)
                results = self.model(im0)
                count_of_people = self.process_results(results)
                print(count_of_people)
            except Exception as e:
                print(f"Ошибка при обработке кадра: {e}")
                break

        self.cap.release()
        cv2.destroyAllWindows()

    def process_results(self, results):
        for result in results:
            boxes = result.boxes
            person_count = 0
            for box in boxes:
                class_id = box.cls.item()
                if class_id == 0:  # Предполагаем, что класс "person" имеет ID 0
                    person_count += 1

            return person_count

class Ventilation:
    def __init__(self):
        self.square_flag = 1
        while self.square_flag:
            print("Введите начальную площадь помещения в метрах квадратных: ", end='')
            self.start_square = int(input())
            if self.start_square <= 0:
                self.square_flag = 1
            else:
                self.square_flag = 0
            self.count_of_people_in_room = count_of_people
            self.start_power = self.count_of_people_in_room * 2
            self.power = 0

    def counting_power(self):
        self.power = 5 * self.count_of_people_in_room
        if self.power > 100:
            self.power = 100
            print(f"Мощность вентиляции: {self.power}%")
        else:
            print(f"Мощность вентиляции: {self.power}%")

class QualityOfLight:
    def __init__(self):
        self.data_of_bright = 0
        self.count_of_people_in_room = count_of_people
        self.bright = 0

    def lights(self):
        if self.count_of_people_in_room > 0:
            if 0 < self.data_of_bright < 300:
                self.bright = 3 * self.data_of_bright
                print(f"Освещенность - {self.data_of_bright}%, так как в аудитории никого нет")
        else:
            print("Освещенность - 0%, так как в аудитории никого нет")

class Temperature:
    def __init__(self):
        self.square_flag = 1
        while self.square_flag:
            print("Введите начальную температуру помещения в градусах цельсия: ", end='')
            self.start_temp = int(input())
            self.month = 0
            # self.

    def get_season(self):
        self.month = datetime.datetime.now().month
        if self.month == 1 or self.month == 2 or self.month == 11:
            return 'зима'
        elif self.month == 3 or self.month == 4 or self.month == 5:
            return 'весна'
        elif self.month == 6 or self.month == 7 or self.month == 8:
            return 'лето'
        else:
            return 'осень'


first_cap = ObjectDetection()
first_cap.exit_image()