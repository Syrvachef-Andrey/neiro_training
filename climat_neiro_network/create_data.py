import csv
import random

# Функция для генерации случайных данных
def generate_random_data():
    humidity = round(random.uniform(30, 70), 2)  # Влажность в помещении (30-70%)
    temperature = round(random.uniform(18, 30), 2)  # Температура (18-30°C)
    light_level = round(random.uniform(0, 100), 2)  # Уровень освещенности (0-100%)
    pressure = round(random.uniform(950, 1050), 2)  # Давление (950-1050 гПа)
    co2 = random.randint(300, 2000)  # Количество CO2 (300-2000 ppm)
    indoor_temperature = round(random.uniform(18, 25), 2)  # Температура в помещении (18-25°C)
    return [humidity, temperature, light_level, pressure, co2, indoor_temperature]

# Создание CSV-файла
def create_csv(filename, rows=5000):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        # Записываем заголовки столбцов
        writer.writerow(["Влажность (%)", "Температура (°C)", "Освещенность (%)", "Давление (гПа)", "CO2 (ppm)", "Температура в помещении (°C)"])
        # Заполняем файл случайными данными
        for _ in range(rows):
            writer.writerow(generate_random_data())

# Основная программа
if __name__ == "__main__":
    filename = "dataset.csv"
    create_csv(filename, rows=5000)  # Создаем файл с 100 строками данных
    print(f"Файл '{filename}' успешно создан и заполнен случайными данными.")