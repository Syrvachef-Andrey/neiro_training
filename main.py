import cv2
from ultralytics import YOLO
from ultralytics import solutions
import torch
import datetime
import logging
import time

logging.basicConfig(
    level=logging.DEBUG,  # Уровень логирования (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format='%(asctime)s - %(message)s',  # Формат сообщения
    handlers=[
        logging.FileHandler("botlogger.log"),  # Логирование в файл
        logging.StreamHandler()  # Логирование в консоль
    ]
)

logger = logging.getLogger("BotLogger")


class ObjectDetection:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        assert self.cap.isOpened(), "Error reading video file"
        self.cap.set(3, 800)
        w, h, fps = (int(self.cap.get(x)) for x in (cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT, cv2.CAP_PROP_FPS))

        self.model = YOLO("yolo11n.pt")
        self.count_of_people = 0
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
        self.s = ''
        # Initialize temperature, ventilation, and lighting parameters
        self.start_temp = 0
        self.start_square = 0
        self.data_of_bright = 0
        self.get_data_of_start_temperature()
        self.get_start_temp()
        self.get_start_brightness()

    def get_data_of_start_temperature(self):
        while True:
            print("Введите начальную температуру помещения в градусах цельсия: ", end='')
            self.start_temp = int(input())
            if self.start_temp < -50:
                print("Неправильно введены данные, попробуйте снова")
            else:
                break

    def get_start_temp(self):
        while True:
            print("Введите начальную площадь помещения в метрах квадратных: ", end='')
            self.start_square = int(input())
            if self.start_square <= 0:
                print("Неверно указаны данные, введите снова")
            else:
                break

    def get_start_brightness(self):
        while True:
            print("Введите начальную освещенность помещения в люксах: ", end='')
            self.data_of_bright = int(input())
            if self.data_of_bright < 0 or self.data_of_bright > 1000:
                print("Неправильно введены данные, попробуйте снова")
            else:
                break

    def get_season(self):
        month = datetime.datetime.now().month
        if month == 1 or month == 2 or month == 12:
            return 'зима'
        elif month == 3 or month == 4 or month == 5:
            return 'весна'
        elif month == 6 or month == 7 or month == 8:
            return 'лето'
        else:
            return 'осень'

    def calculate_temperature(self):
        season = self.get_season()
        if season == 'зима':
            if self.start_temp < 24:
                self.temper = 24
                print(f"Темпераратура на батареях: +{self.temper}")
                s = f"b{self.temper}"
            else:
                print("Не нужно запускать повышение темппературы на батареях")
                s = f"b-"
        elif season == 'осень' or season == 'весна':
            if self.start_temp < 15:
                self.temper = 24
                print(f"Темпераратура на батареях: +{self.temper}")
                s = f"b{self.temper}"
            elif self.start_temp > 24:
                self.temper = 21
                print(f"Темпераратура на кондиционере: +{self.temper}")
                s = f"c{self.temper}"
            else:
                print("Ни батареи, ни кондиционер не нужно включать")
                s = f"bc-"
        else:
            if self.start_temp > 24:
                self.temper = 24
                print(f"Темпераратура на кондиционере: +{self.temper}")
                s = f"c {self.temper}"
            else:
                print("Не нужно запускать понижение темппературы на кондиционере")
                s = f"c-"
        return s

    def counting_power_of_vent(self):
        power = 2 * self.count_of_people
        if power > 100:
            power = 100
        s = str(power)
        print(f"Мощность вентиляции: {power}%")
        return s

    def calculate_lights(self):
        if self.count_of_people > 0:
            if 0 < self.data_of_bright < 500:
                bright = (500 - self.data_of_bright)
                s = str(bright)
                print(f"Освещенность - {bright} Люкс, так как в аудитории есть {self.count_of_people} человек и освещенность в аудитории {self.data_of_bright} недостаточна")
        else:
            s = str(0)
            print("Освещенность - 0%, так как в аудитории никого нет")
        return s

    def exit_image(self):
        while self.cap.isOpened():
            self.s = ''
            success, im0 = self.cap.read()
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            if not success:
                print("Video frame is empty or video processing has been successfully completed.")
                break

            try:
                im0 = self.region.count(im0)
                results = self.model(im0)
                self.count_of_people = self.process_results(results)
                print(f"Количество людей: {self.count_of_people}")

                time.sleep(0.05)
                # Calculate temperature, ventilation, and lighting
                self.s += self.calculate_temperature() + " "
                self.s += self.counting_power_of_vent() + " "
                self.s += self.calculate_lights()
                print(self.s)

                logger.info(self.s)

            except Exception as e:
                print(f"Ошибка при обработке кадра: {e}")
                break

        self.cap.release()
        cv2.destroyAllWindows()
        return 1

    def process_results(self, results):
        person_count = 0
        for result in results:
            boxes = result.boxes
            for box in boxes:
                class_id = box.cls.item()
                if class_id == 0:  # Предполагаем, что класс "person" имеет ID 0
                    person_count += 1

        return person_count

detection = ObjectDetection()
detection.exit_image()