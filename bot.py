import telebot
import time

# Создание объекта бота
bot = telebot.TeleBot("API_TOKEN")

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
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    user = message.from_user.username
    message_text = message.text.lower()
    message_time = time.time()
    messages.setdefault(user_id, []).append((message_text, message_time))
    messages[user_id] = [(m, t) for (m, t) in messages[user_id] if time.time() - t < 60]
    count_messages = count_words(messages[user_id])
    if int(max(count_messages[1::2])) > 4:
        # Отправка сообщения пользователю о муте на час
        try:
            bot.restrict_chat_member(chat_id, user_id, until_date=time.time() + 3600)
        except telebot.apihelper.ApiTelegramException:
            print("Ошибка, я не могу замутить администратора.")
        bot.send_message(chat_id, "Пользователь @" + user + " был замучен на 1 час за спам, старайтесь больше не нарушать правила.")
        bot.send_message(chat_id, "Первый мут на час, следующий мут будет на день")
        # Отправка сообщения администратору о количестве сообщений пользователя
        try:
            bot.send_message(693188597, 'У пользователя с ником @' + user + " больше 4 сообщений '" + str(count_messages[count_messages.index(max(count_messages[1::2]))-1]) + "' за минуту, он был замучен.")
        except telebot.apihelper.ApiTelegramException:
            print("Не удалось отправить сообщение вам в ЛС, убедитесь что уже писали данному боту в личку.")

# Запуск бота
bot.polling(none_stop=True)
