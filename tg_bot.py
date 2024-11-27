import asyncio
import json
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import Command
from time import sleep

# Укажите свой токен Telegram-бота
TOKEN = "7591931468:AAEtJGnP7rc2U4zpTTM1aMm6dpq3X4x3gI4"

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

        # Читаем вывод скрипта построчно
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
                         "/data - получить текущие данные\n"
                         "/people - узнать количество людей\n"
                         "/temperature - узнать температуру\n"
                         "/ac_power - узнать мощность кондиционера\n"
                         "/light_power - узнать силу освещения")

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

# Обработчик команды /data
@dp.message(Command("data"))
async def get_data_command(message: Message):
    if latest_data is None:
        await message.answer("Нет данных от скрипта.")
    else:
        await message.answer(f"Текущие данные:\nТемпература: {latest_data['temperature']}°C\nМощность кондиционера: {latest_data['ventilation']}%\nСила освещения: {latest_data['lighting']}%\nКоличество людей: {latest_data['people']}")

# Команды для получения конкретных данных
@dp.message(Command("people"))
async def get_people_command(message: Message):
    people = latest_data.get("people", "Нет данных")
    await message.answer(f"Количество людей: {people}")

@dp.message(Command("temperature"))
async def get_temperature_command(message: Message):
    temperature = latest_data.get("temperature", "Нет данных")
    await message.answer(f"Температура: {temperature}°C")

@dp.message(Command("ac_power"))
async def get_ac_power_command(message: Message):
    ac_power = latest_data.get("ventilation", "Нет данных")
    await message.answer(f"Мощность кондиционера: {ac_power}%")

@dp.message(Command("heater_power"))
async def get_heater_power_command(message: Message):
    heater_power = latest_data.get("heater_power", "Нет данных")
    await message.answer(f"Мощность обогревателя: {heater_power}%")

@dp.message(Command("light_power"))
async def get_light_power_command(message: Message):
    light_power = latest_data.get("lighting", "Нет данных")
    await message.answer(f"Сила освещения: {light_power}%")

# Основная точка входа
async def main():
    # Запускаем опрос бота
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())