import asyncio
import json
import sqlite3
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import Command
from time import sleep
import re

# Укажите свой токен Telegram-бота
TOKEN = "7293029886:AAETZZSzlrmTH7uPkz6pdrdeYe8tn9gPBMw"

# Инициализация бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Список для хранения запущенных процессов
running_processes = []

# Хранилище данных от скрипта
latest_data = {}

# Асинхронная функция для запуска скрипта и обновления данных
async def run_script_and_update_data(chat_id: int):
    global latest_data
    try:
        # Запускаем скрипт
        process = await asyncio.create_subprocess_exec(
            "python", "main.py",  # или путь к вашему скрипту
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        running_processes.append(process)

        async for line in process.stdout:
            text = str(line)[2:-3]
            print(text)
            if text:
                try:
                    # Обновляем данные, если строка в формате JSON
                    latest_data = eval(text)

                except:
                    if text.split()[0] not in ["Ultralytics", "0:", "Speed:"] and text is None:
                        await bot.send_message(chat_id, f"Получено некорректное сообщение от скрипта: {text}")



        # Ждём завершения процесса
        return_code = await process.wait()

        # Убираем процесс из списка
        running_processes.remove(process)

        if return_code != 0:
            error = (await process.stderr.read()).decode().strip()
            await bot.send_message(chat_id, f"Скрипт завершился с ошибкой:\n{error}")
        else:
            await bot.send_message(chat_id, "Скрипт успешно завершён!")
    except Exception as e:
        if "list.remove(x)" not in str(e):
            await bot.send_message(chat_id, f"Произошла ошибка:\n{str(e)}")
    finally:
        if process in running_processes:
            running_processes.remove(process)

# Обработчик команды /start
@dp.message(Command("start"))
async def start_command(message: Message):
    await message.answer("Привет! Используй:\n"
                         "/run - запустить скрипт\n"
                         "/stop - остановить все запущенные скрипты\n"
                         "Для получения информации введите ID")

# Обработчик команды /run
@dp.message(Command("run"))
async def run_script_command(message: Message):
    await message.answer("Скрипт запускается. Данные будут обновляться автоматически.")
    asyncio.create_task(run_script_and_update_data(message.chat.id))
    sleep(2)

# Обработчик команды /stop
@dp.message(Command("stop"))
async def stop_script_command(message: Message):
    if not running_processes:
        await message.answer("Нет запущенных скриптов для остановки.")
        return

    for process in running_processes:
        process.terminate()

    running_processes.clear()
    await message.answer("Все запущенные скрипты были остановлены.")

@dp.message(lambda message: re.fullmatch(r"\d+", message.text))
async def handle_digit_message(message: Message):
    await message.answer(f'ФИ: {get_cell_value(row_id=message.text, column="name_surname")}\n'
                         f'Дата рождения: {get_cell_value(row_id=message.text, column="date_of_born")}\n'
                         f'Статус: {get_cell_value(row_id=message.text, column="status")}\n'
                         f'Страна: {get_cell_value(row_id=message.text, column="country")}\n'
                         f'Фотография: {get_cell_value(row_id=message.text, column="path_to_photography")}\n'
                         f'Специальность: {get_cell_value(row_id=message.text, column="speciality")}')

# Основная точка входа
async def main():
    # Запускаем опрос бота
    await dp.start_polling(bot)


def get_cell_value(row_id: int, column: str):
    """
    Получает значение конкретной ячейки из базы данных SQLite.

    :param row_id: Идентификатор строки (значение первичного ключа).
    :param column: Название столбца.
    :return: Значение ячейки или None в случае ошибки.
    """
    db_path = "/home/andrey/tank_AI/neiro_training/campus_id/dataset.db"  # Полный путь к файлу базы данных
    table = "dataset"  # Имя таблицы в базе данных

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        query = f"SELECT {column} FROM {table} WHERE id = ?"
        cursor.execute(query, (row_id,))
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else None
    except sqlite3.Error as e:
        print(f"Ошибка работы с базой данных: {e}")
        return None

if __name__ == "__main__":
    asyncio.run(main())
