import time
import string
import asyncio
from aiogram import Bot, Dispatcher, types

# Создание объекта бота
bot = Bot(token="6106244196:AAH7abNC05562iga8Hf0nT4lcUBo3qddJpI")
dp = Dispatcher(bot)

# Создание словаря для хранения сообщений
messages = {}

# Функция для подсчета количества сообщений
def count_words(lst):
    counts = []
    for i in lst:
        if i[0] not in counts:
            counts.append(i[0])
            counts.append(1)
        else:
            counts[counts.index(i[0])+1] += 1
    return counts

# Обработчик всех сообщений
@dp.message_handler()
async def echo_all(message: types.Message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    user = message.from_user.username
    message_text = message.text.lower().translate(str.maketrans("", "", string.punctuation))
    message_time = time.time()
    messages.setdefault(user_id, []).append((message_text, message_time))
    messages[user_id] = [(m, t) for (m, t) in messages[user_id] if time.time() - t < 60]
    count_messages = count_words(messages[user_id])
    if int(max(count_messages[1::2])) > 4:
        # Отправка сообщения пользователю о муте на час
        try:
            await bot.restrict_chat_member(chat_id, user_id, until_date=time.time() + 3600)
            await bot.send_message(chat_id, "Пользователь @" + user + " был замучен на 1 час за спам, старайтесь больше не нарушать правила.")
            await bot.send_message(chat_id, "Первый мут на час, следующий мут будет на день")
        except Exception as e:
            print("Ошибка, я не могу замутить администратора.")
        # Отправка сообщения администратору о количестве сообщений пользователя
        try:
            await bot.send_message(693188597, 'У пользователя с ником @' + user + " больше 4 сообщений '" + str(count_messages[count_messages.index(max(count_messages[1::2]))-1]) + "' за минуту, он был замучен.")
        except Exception as e:
            print("Не удалось отправить сообщение вам в ЛС, убедитесь что уже писали данному боту в личку.")

# Запуск бота
if __name__ == '__main__':
    asyncio.run(dp.start_polling(dp))
