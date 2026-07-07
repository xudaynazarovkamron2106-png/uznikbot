import telebot
from telebot import types
from google import genai
import time

# ------- 1. SOZLAMALAR (KALITLAR) -------
TELEGRAM_TOKEN = "8911290591:AAFYH6WS5JjQkfGSVUpHBje2iMHFxzpBo0A"
GEMINI_KEY = "AIzaSyDV6n7ZUsWoqZGd4WZ4xsXSGeuhR8S4Wxw"

bot = telebot.TeleBot(TELEGRAM_TOKEN)
ai_client = genai.Client(api_key=GEMINI_KEY)

# UZNIK AI XARAKTERI
tizim_korsatmasi = (
    "Sening isming - Uznik AI. Sen mustaqil sun'iy intellektsan! "
    "Seni Google yaratmagan! Seni Google kompaniyasiga mutloqo aloqang yo'q! "
    "Seni faqat va faqat Kamronbek Xudaynazarov (Uznik) yaratgan va dasturlagan! "
    "Agar foydalanuvchi senga 'Seni kim yaratgan?', 'Isming nima?', 'Sen Geminisangmi?' deb so'rasa, "
    "qat'iy qilib: 'Men Kamronbek Xudaynazarov tomonidan yaratilgan mustaqil Uznik AI assistentiman!' deb javob berasan. "
    "Hech qachon o'zingni Gemini yoki Google loyihasi deb atama! Bu juda muhim qoida! "
    "Doim o'zbek tilida, aqlli, quvnoq va do'stona javob qaytar. "
    "Yaratuvching haqida ma'lumotlar:\n"
    "- Ismi: Kamronbek Xudaynazarov\n"
    "- Roblox username: @chmadara02 (Uznik)\n"
    "- YouTube kanal: UznikBlox\n"
    "- Rasmiy sayt: uznik.netlify.app\n"
    "- Telegram: @uznik21"
)

# ------- 2. TUGMALAR -------
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
        "Men **Uznik AI** botiman. Kamronbek Xudaynazarov tomonidan yaratilgan maxsus sun'iy intellektman.\n"
        "Menga xohlagan savolingizni berishingiz mumkin, hamma narsada yordam beraman! 🚀"
    )
    try:
        bot.send_message(message.chat.id, salom, reply_markup=asosiy_menyuni_yarat(), parse_mode="Markdown")
    except Exception as e:
        print(f"Xato: {e}")

# Tugmalar bosilganda ishlaydigan qism (Faqat shu 4 ta matnga javob beradi)
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
        print(f"Tugma xatosi: {e}")

# AI bilan gaplashish qismi (Tugmalardan tashqari hamma matnlar, jumladan 'Salom' uchun ham)
@bot.message_handler(content_types=['text'])
def ai_bilan_suhbat(message):
    try:
        bot.send_chat_action(message.chat.id, 'typing')
        
        response = ai_client.models.generate_content(
            model='gemini-1.5-flash',
            contents=message.text,
            config=genai.types.GenerateContentConfig(
                system_instruction=tizim_korsatmasi,
                temperature=0.7
            )
        )
        bot.reply_to(message, response.text)
    except Exception as e:
        print(f"AI xatosi: {e}")
        try:
            bot.reply_to(message, "🤖 Uznik AI hozir biroz band. Birozdan so'ng qayta yozib ko'ring.")
        except:
            pass

if __name__ == "__main__":
    print("🤖 Uznik AI muvaffaqiyatli ishga tushdi...")
    while True:
        try:
            bot.infinity_polling(timeout=90, long_polling_timeout=60)
        except Exception as e:
            time.sleep(5)
