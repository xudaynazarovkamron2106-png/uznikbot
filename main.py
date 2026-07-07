import telebot
from telebot import types
from google import genai
import time
import os

# ------- 1. SOZLAMALAR (KALITLAR) -------
TELEGRAM_TOKEN = "8911290591:AAFYH6WS5JjQkfGSVUpHBje2iMHFxzpBo0A"
GEMINI_KEY = "AIzaSyDV6n7ZUsWoqZGd4WZ4xsXSGeuhR8S4Wxw"

# Bot va AI konfiguratsiyasi
bot = telebot.TeleBot(TELEGRAM_TOKEN)
ai_client = genai.Client(api_key=GEMINI_KEY)

# AI xarakteri va konteksti (System Instruction)
tizim_korsatmasi = (
    "Sen Kamronbek Xudaynazarov (Uznik) tomonidan yaratilgan Uznik AI assistentisan. "
    "Foydalanuvchilarga doim o'zbek tilida, aniq, aqlli va quvnoq javob berasan. "
    "Hech qachon 'bilmayman' deb aytma, har doim yechim topishga harakat qil. "
    "Sening yaratuvching haqida so'rashsa, quyidagilarni bilasan:\n"
    "- Ismi: Kamronbek Xudaynazarov\n"
    "- Roblox username: @chmadara02 (Uznik)\n"
    "- YouTube: UznikBlox\n"
    "- Sayt: uznik.netlify.app\n"
    "- Telegram: @uznik21"
)

# ------- 2. TUGMALAR (KEYBOARD) -------
def asosiy_menyuni_yarat():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    tugma1 = types.KeyboardButton("🌐 Bizning Sayt")
    tugma2 = types.KeyboardButton("📺 YouTube Kanal")
    tugma3 = types.KeyboardButton("🎮 Roblox Profil")
    tugma4 = types.KeyboardButton("👨‍💻 Admin (Kamronbek)")
    markup.add(tugma1, tugma2, tugma3, tugma4)
    return markup

# ------- 3. BOT FUNKSIYALARI -------

# /start buyrug'i
@bot.message_handler(commands=['start'])
def start_command(message):
    salom = (
        f"Salom, {message.from_user.first_name}! 🤖\n"
        "Men **Uznik AI** botiman. Menga xohlagan savolingizni berishingiz, "
        "matn yoki dasturlash bo'yicha yordam so'rashingiz mumkin. Men hamma narsani bilaman!\n\n"
        "Quyidagi tugmalar orqali asoschimiz Kamronbekning ijtimoiy tarmoqlariga o'tishingiz mumkin 👇"
    )
    try:
        bot.send_message(message.chat.id, salom, reply_markup=asosiy_menyuni_yarat(), parse_mode="Markdown")
    except Exception as e:
        print(f"Start yuborishda xato: {e}")

# Tugmalar bosilganda ishlaydigan qism
@bot.message_handler(func=lambda message: message.text in ["🌐 Bizning Sayt", "📺 YouTube Kanal", "🎮 Roblox Profil", "👨‍💻 Admin (Kamronbek)"])
def tugmalar_boshqaruvi(message):
    try:
        if message.text == "🌐 Bizning Sayt":
            bot.send_message(message.chat.id, "🔗 Bizning rasmiy sayt: uznik.netlify.app")
        elif message.text == "📺 YouTube Kanal":
            bot.send_message(message.chat.id, "🔗 Bizning YouTube kanal: UznikBlox-ni tomosha qiling!")
        elif message.text == "🎮 Roblox Profil":
            bot.send_message(message.chat.id, "🎮 Roblox Username: @chmadara02 (Nik: Uznik)")
        elif message.text == "👨‍💻 Admin (Kamronbek)":
            bot.send_message(message.chat.id, "👨‍💻 Aloqa uchun lichka: @uznik21 (Kamronbek Xudaynazarov)")
    except Exception as e:
        print(f"Tugma ishlashida xato: {e}")

# AI bilan gaplashish qismi (Hamma matnli xabarlar uchun)
@bot.message_handler(content_types=['text'])
def ai_bilan_suhbat(message):
    try:
        # Bot yozmoqda... effektini ko'rsatish
        bot.send_chat_action(message.chat.id, 'typing')
        
        # Yangi google-genai kutubxonasi buyrug'i
        response = ai_client.models.generate_content(
            model='gemini-1.5-flash',
            contents=message.text,
            config=genai.types.GenerateContentConfig(
                system_instruction=tizim_korsatmasi
            )
        )
        bot.reply_to(message, response.text)
    except Exception as e:
        print(f"AI javob berishda xato: {e}")
        try:
            bot.reply_to(message, "⚠️ Hozircha so'rovni qayta ishlashda muammo bo'ldi. Birozdan so'ng urinib ko'ring.")
        except:
            pass

# Botni uzluksiz va xavfsiz ishga tushirish (Render uchun optimizatsiya qilingan)
if __name__ == "__main__":
    print("🤖 Uznik AI bot Render platformasida ishga tushmoqda...")
    while True:
        try:
            # Ulanish vaqtlari tarmoq uzilishlariga chidamli qilib sozlandi
            bot.infinity_polling(timeout=90, long_polling_timeout=60)
        except Exception as e:
            print(f"Ulanish uzildi, 5 soniyadan keyin qayta harakat qilinadi: {e}")
            time.sleep(5)
