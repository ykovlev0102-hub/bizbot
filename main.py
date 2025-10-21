jimport telebot
import openai
import os

# === 🔑 Настройки ===
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

bot = telebot.TeleBot(8345133648:AAHEH-H4mcBkXd8TTUQnh-dbFbtbeQATZOk)
openai.api_key = OPENAI_API_KEYsk-proj-li8P2_Y1MWOuUAH_r4IynIgHFFbdRYgf6BKGqvwzoL1-dDRVTIyWyfexbXn79NHPpaywrSvoWeT3BlbkFJQ3UZksccuSyO8A-mb3W6j-Bgi8xfKALI1l3dCMKNBWYkK7TYnWMdEmrh4hmSNb4-vc4uSjRIcA

# === 🌍 Языковая поддержка ===
LANG = {}  # словарь для хранения языка пользователя

# === 💬 Главное меню ===
MAIN_MENU_RU = (
    "📋 Главное меню:\n"
    "1️⃣ Создать пост\n"
    "2️⃣ Придумать идею\n"
    "3️⃣ Коммерческое предложение\n"
    "4️⃣ Улучшить текст\n"
    "5️⃣ Обучение ChatGPT\n\n"
    "🌐 Для смены языка напиши /lang"
)
MAIN_MENU_EN = (
    "📋 Main menu:\n"
    "1️⃣ Create post\n"
    "2️⃣ Business idea\n"
    "3️⃣ Commercial offer\n"
    "4️⃣ Improve text\n"
    "5️⃣ ChatGPT training\n\n"
    "🌐 Type /lang to switch language"
)

# === ⚙️ Системные промты для BizBot ===
SYSTEM_PROMPT_RU = "Ты — BizBot, умный помощник для малого бизнеса. Пиши кратко, по делу и дружелюбно. Помогай предпринимателям с идеями, текстами и контентом."
SYSTEM_PROMPT_EN = "You are BizBot, an intelligent AI assistant for entrepreneurs. Write clearly, concisely, and in a friendly tone. Help users with ideas, content, and marketing texts."

# === Команда /start ===
@bot.message_handler(commands=["start"])
def start_message(message):
    LANG[message.chat.id] = "ru"
    bot.send_message(
        message.chat.id,
        "👋 Привет! Я BizBot — твой AI-помощник для бизнеса.\n"
        "I can also work in English.\n\n"
        + MAIN_MENU_RU,
    )

# === Команда /lang ===
@bot.message_handler(commands=["lang"])
def change_language(message):
    if LANG.get(message.chat.id) == "ru":
        LANG[message.chat.id] = "en"
        bot.send_message(message.chat.id, "✅ Language switched to English.\n\n" + MAIN_MENU_EN)
    else:
        LANG[message.chat.id] = "ru"
        bot.send_message(message.chat.id, "✅ Язык переключён на русский.\n\n" + MAIN_MENU_RU)

# === Обработка текстовых сообщений ===
@bot.message_handler(func=lambda msg: True)
def handle_message(message):
    lang = LANG.get(message.chat.id, "ru")

    # Определяем задачу по выбору пользователя
    text = message.text.lower()
    if lang == "ru":
        if "1" in text or "пост" in text:
            task = "Создай продающий пост для бизнеса: "
        elif "2" in text or "иде" in text:
            task = "Придумай бизнес-идею или рекламную идею: "
        elif "3" in text or "коммер" in text:
            task = "Сделай коммерческое предложение для клиента: "
        elif "4" in text or "улуч" in text:
            task = "Улучшить этот текст, чтобы он звучал профессионально и продающе: "
        elif "5" in text or "обуч" in text:
            bot.reply_to(message, "🎓 Урок 1. Что такое ChatGPT и как он помогает бизнесу...\n(ты можешь добавить сюда свой контент)")
            return
        else:
            bot.reply_to(message, MAIN_MENU_RU)
            return
        prompt = SYSTEM_PROMPT_RU
    else:
        if "1" in text or "post" in text:
            task = "Write a marketing post for business: "
        elif "2" in text or "idea" in text:
            task = "Suggest a business or advertising idea: "
        elif "3" in text or "offer" in text:
            task = "Write a commercial offer for a client: "
        elif "4" in text or "improve" in text:
            task = "Improve this text to sound professional and persuasive: "
        elif "5" in text or "train" in text:
            bot.reply_to(message, "🎓 Lesson 1. What is ChatGPT and how it helps business...\n(you can add your own text here)")
            return
        else:
            bot.reply_to(message, MAIN_MENU_EN)
            return
        prompt = SYSTEM_PROMPT_EN

    user_input = message.text
    bot.send_chat_action(message.chat.id, "typing")

    # === GPT-ответ ===
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": task + user_input},
            ],
        )
        reply = completion.choices[0].message["content"]
        bot.reply_to(message, reply)
    except Exception as e:
        bot.reply_to(message, f"⚠️ Ошибка: {e}")

# === Запуск ===
if __name__ == "__main__":
    bot.polling(non_stop=True)
