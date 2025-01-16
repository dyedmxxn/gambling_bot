import random
from dotenv import load_dotenv
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import os
import telebot
import time

load_dotenv()
API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise ValueError("API_KEY environment is not set!")
bot = telebot.TeleBot(API_KEY)

spins = 0
wins = 0
losses = 0
winrate = 0
money = 0
status_user = None
status = {
    0: "Gambling newbie",
    100: "Gambling student",
    300: "Gambling enjoyer",
    500: "Gambling addict",
    1000: "Gambling monk",
    1500: "Gambling king",
    2000: "Gambling emperor",
    2500: "Gambling god",
    3000: "Unemployed"
}

def menu():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    btn_gamble = KeyboardButton("🎰Gamble🎰")
    btn_stats = KeyboardButton("📄Statistics📄")
    keyboard.add(btn_gamble)
    keyboard.add(btn_stats)
    return keyboard

@bot.message_handler(commands=["start"])
def welcome(message):
    keyboard = menu()

    add_path = r"adds"
    add_name = r"nav_ta_gav.jpg"
    addvert = os.path.join(add_path, add_name)
    with open(addvert, "rb") as image_add:
        bot.send_photo(message.chat.id, photo=image_add)

    bot.send_message(message.chat.id, "Заходь, реєструйся та отримуй знижку! \nhttps://zoo-tovary.com/")

    time.sleep(1.5)

    bot.send_message(message.chat.id, "Enough of that, let's go gambling!", reply_markup=keyboard)

@bot.message_handler(func=lambda message: message.text in ["🎰Gamble🎰"])
def gamble(message):
    global spins, wins, losses, winrate, money, status_user
    items = []
    items_list = ["C", "P", "L", "D"]
    for x in range(3):
        indx = random.randint(0, 3)
        item_x = items_list[indx]
        items.append(item_x)

    ticket = random.randint(1, 5)
    spins = spins + 1

    def status_calculator():
        
        sorted_key_list = sorted(status.keys())

        closest_key = 0

        for key in sorted_key_list:
            if spins >= key:
                closest_key = key
            else:
                break
        
        return status[closest_key]
    
    if spins % 100 == 0:
        bot.send_message(message.chat.id, "Hey there! It seems like you found a liking in this bot. \nTherefore, maybe you want to support the creator? \nIf so, then here is my credit card: 4441111031181856. Thanks :D")
        time.sleep(3)
    else:
        pass

    money = money + ticket

    if items[0] == items[1] == items[2]:
        wins = wins + 1
    else:
        losses = losses + 1

    winrate = round((wins / spins) * 100, 2)

    status_user = status_calculator()
        
    def slot_machine_image():
        path = r"TG stickerpack_CR"
        file_name = f"{items[0]}{items[1]}{items[2]}.png"
        return os.path.join(path, file_name)
    
    image_path = slot_machine_image()
    with open(image_path, "rb") as image: 
        bot.send_photo(message.chat.id, photo=image)

    items.clear()


@bot.message_handler(func=lambda message: message.text in ["📄Statistics📄"])
def stats_calculation(message):

    def show_stats():
        stats = (
            f"Spins: {spins} \n"
            f"Wins: {wins} \n"
            f"Losses {losses} \n"
            f"Winrate: {winrate}% \n"
            f"Money spent gambling: {money}$ \n"
            f"Your status: {status_user} \n"
        )
        return stats
    
    bot.send_message(message.chat.id, show_stats())

bot.polling()