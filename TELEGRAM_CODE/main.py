import os
import threading
import time
from asyncio import sleep

from aiogram import Bot, Dispatcher, executor
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup

from config import TELEGRAM_TOKEN, TIME_WAIT_PHOTO
from mqtt_worker import client

keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.add(
    KeyboardButton(text="Включи светодиод"),
    KeyboardButton("Выключи светодиод"),
    KeyboardButton("Сделай фото")
)

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(bot)

tr = threading.Thread(target=client.loop_forever)
tr.start()


@dp.message_handler(lambda message: message.text == "Включи светодиод")
async def enable_led(message: Message):
    client.publish("command", "enable_led")
    await message.answer("Команда на включение светодиода отправлена", reply_markup=keyboard)


@dp.message_handler(lambda message: message.text == "Выключи светодиод")
async def disable_led(message: Message):
    client.publish("command", "disable_led")
    await message.answer("Команда на выключение светодиода отправлена", reply_markup=keyboard)


@dp.message_handler(lambda message: message.text == "Сделай фото")
async def take_photo(message: Message):
    client.publish("image", "None")
    client.publish("command", "take_screenshot")
    start = time.time()
    while not os.listdir("images"):
        if time.time() - start < TIME_WAIT_PHOTO:
            await sleep(1)
        else:
            await message.answer("Что-то пошло не так - повторите попозже!", reply_markup=keyboard)
            return
    with open("images/photo.jpeg", "rb") as new_image:
        await message.answer_photo(photo=new_image, reply_markup=keyboard)


@dp.message_handler()
async def any_text_message(message: Message):
    await message.answer(
        "Привет! Я умею включать и выключать светодиод и делать фотографии. Нажми на нужную кнопку!",
        reply_markup=keyboard
    )


if __name__ == "__main__":
    # Запуск бота
    executor.start_polling(dp, skip_updates=True)
