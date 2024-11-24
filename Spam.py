from flask import Flask
from threading import Thread
import telebot
from requests import request

# إعدادات البوت
API_TOKEN = '1737913043:AAFpsmTVhxAqx3QAMqGbC_z-hgKa-Cg1B3k'  # تم استخدام التوكن الذي زودتني به
bot = telebot.TeleBot(API_TOKEN)

# إعداد خادم الويب باستخدام Flask
app = Flask(__name__)

# دالة إرسال الرسائل
def send_messages_asia(phone, count):
    sent = 0
    for _ in range(count):
        try:
            response = request(
                method="POST",
                url="https://vas2.grand-hub.com/api/ludo/asiacell-d/subscribe",
                json={"phone": phone}
            )
            # طباعة الاستجابة للتأكد من صحتها
            print(f"Status Code: {response.status_code}")
            print(f"Response Text: {response.text}")
            if "successfully" in response.json().get("message", ""):
                sent += 1
            else:
                print(f"Failed to send message: {response.json()}")
                break
        except Exception as e:
            print(f"Error: {e}")
            break
    return sent

# رسالة البداية التي تظهر عند المستخدم
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "مرحبًا! أنا بوت إرسال الرسائل لخطوط آسيا.\nأرسل لي رقم الهاتف.")

# استقبال الرقم
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        # الحصول على الرقم وإزالته إذا بدأ بـ 0
        phone = message.text.strip()
        if phone.startswith("0"):
            phone = phone[1:]  # إزالة الصفر من البداية

        # التأكد أن الرقم مكون من أرقام فقط
        if phone.isdigit():
            bot.reply_to(message, f"تم استلام الرقم {phone}.\nالرجاء إدخال عدد الرسائل التي ترغب في إرسالها.")
            bot.register_next_step_handler(message, handle_count, phone)
        else:
            bot.reply_to(message, "الرجاء إدخال رقم صحيح مكون من أرقام فقط.")
    except Exception as e:
        bot.reply_to(message, f"حدث خطأ: {e}")

# استقبال عدد الرسائل
def handle_count(message, phone):
    try:
        count = int(message.text.strip())

        if count > 0:
            bot.reply_to(message, f"تم بدء إرسال {count} رسالة إلى الرقم {phone}...")
            sent = send_messages_asia(phone, count)
            bot.reply_to(message, f"تم إرسال {sent} رسالة بنجاح.")
        else:
            bot.reply_to(message, "الرجاء إدخال عدد رسائل أكبر من صفر.")
    except ValueError:
        bot.reply_to(message, "الرجاء إدخال عدد صحيح من الرسائل.")

# دالة لتشغيل البوت في خيط منفصل
def run_bot():
    bot.polling()

# تشغيل خادم الويب
@app.route('/')
def home():
    return "Telegram bot is running!"

# بدء التطبيق
if __name__ == '__main__':
    # تشغيل البوت في خيط منفصل
    Thread(target=run_bot).start()
    # تشغيل خادم الويب على المنفذ 5000
    app.run(host='0.0.0.0', port=5000)
