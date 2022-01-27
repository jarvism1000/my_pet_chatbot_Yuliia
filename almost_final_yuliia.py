import telebot

from telebot import types

# Підключення API
bot = telebot.TeleBot('Your_token')


class IncrementCounter:
    """Лічильник."""

    def __init__(self):
        self._value = 0

    def new_value(self):
        """Установити нове значення +1."""
        self._value += 1
        return self._value

    def reset_value(self):
        """Обнулити значення."""
        self._value = 0

    def get_value(self):
        """Отримати поточне значення."""
        return self._value


# Створюємо екземпляр лічильника.
ic = IncrementCounter()

# Створюємо список для збереження відповідей.
report = []

# Відкриття і запис файла у список.
with open('questions.txt', 'r', encoding='utf-8') as f:
    file = f.read().split('\n')
    list_question = []
    for question in file:
        list_question.append(question)

# Відкриття і запис файла у список.
with open('answears.txt', 'r',  encoding='utf-8') as f:
    file = f.read().split('\n')
    list_answears = []
    for answear in file:
        list_answears.append(answear)


# Опитування
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    """Опитування."""

    # Запис відповідей у файл.
    if message.text in str(list_answears[ic.get_value()].split(',')):
        new_data = {
            "question" :list_question[ic.get_value()],
            "answer" :message.text
        }
        report.append(new_data)
        with open('report.txt', 'w', encoding='utf-8') as f:
            f.write(str(report))
        ic.new_value()

    # Готуємо кнопки.
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    try:
        for answear in list_answears[ic.get_value()].split(','):
            key = types.KeyboardButton(text=str(answear))
            keyboard.add(key)
    except IndexError:
        bot.send_message(message.from_user.id, text="Опитування закінчено")

        # Обнулити лічильник коли опитування закінчено.
        ic.reset_value()

    # Показуємо всі кнопки і пишемо повідомлення про вибір.
    try:
        bot.send_message(message.from_user.id, text=list_question[ic.get_value()], reply_markup=keyboard)
    except IndexError:
        bot.send_message(message.from_user.id, text="Опитування закінчено")

        # Обнулити лічильник коли опитування закінчено.
        ic.reset_value()


# Запускаємо постійне опитування.
bot.polling(none_stop=True, interval=0)
