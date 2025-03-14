import sqlite3
from faker import Faker
import random
import tkinter as tk
from tkinter import messagebox
import save_files_for_dataset_of_images

# Инициализация Faker
fake = Faker()

# Создание базы данных и таблицы
def create_database():
    conn = sqlite3.connect('dataset.db')
    cursor = conn.cursor()

    # Создаем таблицу dataset
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS dataset (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name_surname TEXT NOT NULL,
            date_of_born TEXT NOT NULL,
            status TEXT NOT NULL,
            country TEXT NOT NULL,
            path_to_photography TEXT NOT NULL,
            speciality TEXT NOT NULL 
        )
    ''')
    conn.commit()
    conn.close()

# Добавление записи в таблицу
def add_record(name_surname, date_of_born, status, country, path_to_photography, speciality):
    conn = sqlite3.connect('dataset.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO dataset (name_surname, date_of_born, status, country, path_to_photography, speciality)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (name_surname, date_of_born, status, country, path_to_photography, speciality))
    conn.commit()
    conn.close()

# Заполнение базы данных случайными данными
def fill_random_data(num_records=50):
    statuses = ["Student", "Teacher", "Admin", "Guest"]
    code_of_specialities = ["13.06.05", "15.03.06", "08.05.04", "17.06.06", "18.07.03"]
    countries = ["Russia", "Germany", "USA", "Ghana", "UK", "China"]

    for _ in range(num_records):
        name_surname = fake.name()  # Генерация случайного ФИО
        date_of_born = fake.date_of_birth(minimum_age=18, maximum_age=65).strftime("%Y-%m-%d")  # Дата рождения
        status = random.choice(statuses)  # Случайный статус
        if status == "Admin":
            country = "Russia"
        else:
            country = random.choice(countries)  # Случайная страна
        path_to_photography = f"/dataset/{name_surname.replace(' ', '_')}.jpg"  # Случайный путь к фото
        speciality = random.choice(code_of_specialities)  # Случайная специальность

        # Добавляем запись в базу данных
        add_record(name_surname, date_of_born, status, country, path_to_photography, speciality)

# Получение всех данных из таблицы
def get_all_records():
    conn = sqlite3.connect('dataset.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM dataset")
    rows = cursor.fetchall()
    conn.close()
    return rows

# Функция для добавления записи через GUI
def add_record_gui():
    def on_submit():
        # Получаем данные из полей ввода
        name_surname = entry_name_surname.get()
        date_of_born = entry_date_of_born.get()
        status = entry_status.get()
        country = entry_country.get()
        speciality = entry_speciality.get()

        # Проверяем, что все поля заполнены
        if not all([name_surname, date_of_born, status, country, speciality]):
            messagebox.showwarning("Ошибка", "Все поля должны быть заполнены!")
            return

        # Генерируем путь к фото на основе ФИО
        path_to_photography = f"/dataset/{name_surname.replace(' ', '_')}.jpg"

        # Добавляем запись в базу данных
        add_record(name_surname, date_of_born, status, country, path_to_photography, speciality)
        messagebox.showinfo("Успех", f"Запись успешно добавлена!\nПуть к фото: {path_to_photography}")
        root.destroy()  # Закрываем окно после добавления

    # Создаем графический интерфейс
    root = tk.Tk()
    root.title("Добавление записи")

    # Поля ввода
    tk.Label(root, text="Имя Фамилия:").grid(row=0, column=0, padx=10, pady=5)
    entry_name_surname = tk.Entry(root, width=30)
    entry_name_surname.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(root, text="Дата рождения (ГГГГ-ММ-ДД):").grid(row=1, column=0, padx=10, pady=5)
    entry_date_of_born = tk.Entry(root, width=30)
    entry_date_of_born.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(root, text="Статус:").grid(row=2, column=0, padx=10, pady=5)
    entry_status = tk.Entry(root, width=30)
    entry_status.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(root, text="Страна:").grid(row=3, column=0, padx=10, pady=5)
    entry_country = tk.Entry(root, width=30)
    entry_country.grid(row=3, column=1, padx=10, pady=5)

    tk.Label(root, text="Специальность:").grid(row=4, column=0, padx=10, pady=5)
    entry_speciality = tk.Entry(root, width=30)
    entry_speciality.grid(row=4, column=1, padx=10, pady=5)

    # Сообщение о пути к фото
    tk.Label(root, text="Путь к фото будет сгенерирован автоматически.").grid(row=5, column=0, columnspan=2, pady=5)

    # Кнопка для добавления записи
    submit_button = tk.Button(root, text="Добавить запись", command=on_submit)
    submit_button.grid(row=6, column=0, columnspan=2, pady=10)

    root.mainloop()

def read_all_database():
    print("Все записи в базе данных:")
    records = get_all_records()
    for record in records:
        print(record)

def read_database_by_index(ind):
    return ind[1]

# Основная функция
if __name__ == "__main__":
    # create_database()
    # # Заполняем базу данных случайными данными (опционально)
    # fill_random_data(num_records=50)
    #
    # # Запускаем графический интерфейс для добавления записи
    # add_record_gui()
    # #
    # save_files_for_dataset_of_images.save_image_global()

    read_all_database()
