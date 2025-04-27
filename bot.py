import telebot
from telebot import types
from config import Config
from player import Player
from game_logic import GameLogic

bot = telebot.TeleBot(Config.TOKEN)
players = {}

def get_player(user_id, name):
    if user_id not in players:
        players[user_id] = Player(user_id, name)
    return players[user_id]

@bot.message_handler(commands=['start'])
def start(message):
    player = get_player(message.from_user.id, message.from_user.first_name)
    
    welcome_text = (
        f"⚔️ Добро пожаловать в мир магии и приключений, {player.name}!\n\n"
        f"Ты - отважный искатель приключений в этом полном опасностей мире.\n"
        f"Сражайся с монстрами, собирай добычу и повышай свой уровень!\n\n"
        f"Используй кнопки ниже для взаимодействия:"
    )
    
    bot.send_message(
        message.chat.id, 
        welcome_text,
        reply_markup=GameLogic.create_main_markup()
    )

@bot.message_handler(func=lambda msg: msg.text == 'Характеристики')
def status(message):
    player = get_player(message.from_user.id, message.from_user.first_name)
    bot.send_message(
        message.chat.id, 
        player.status_text(),
        reply_markup=GameLogic.create_main_markup() if not player.in_battle else GameLogic.create_battle_markup()
    )

@bot.message_handler(func=lambda msg: msg.text == 'Инвентарь')
def inventory(message):
    player = get_player(message.from_user.id, message.from_user.first_name)
    bot.send_message(
        message.chat.id,
        player.inventory_text(),
        reply_markup=GameLogic.create_main_markup() if not player.in_battle else GameLogic.create_battle_markup()
    )

@bot.message_handler(func=lambda msg: msg.text == 'Помощь')
def help(message):
    bot.send_message(
        message.chat.id,
        GameLogic.help_text(),
        reply_markup=GameLogic.create_main_markup()
    )

@bot.message_handler(func=lambda msg: msg.text == 'Охота на монстров')
def hunt(message):
    player = get_player(message.from_user.id, message.from_user.first_name)
    
    if player.in_battle:
        bot.send_message(
            message.chat.id,
            "Ты уже в бою! Используй кнопки боя.",
            reply_markup=GameLogic.create_battle_markup()
        )
        return
    
    if player.hp <= 0:
        bot.send_message(
            message.chat.id,
            "💀 Ты повержен! Тебе нужно исцеление перед новой охотой.",
            reply_markup=GameLogic.create_main_markup()
        )
        return
    
    monster = GameLogic.start_battle(player)
    bot.send_message(
        message.chat.id,
        f"🦖 Ты встретил {monster['name']} с {monster['weapon']}!\n"
        f"❤️ Здоровье: {monster['hp']} HP\n"
        f"⚔️ Атака: {monster['attack']}\n\n"
        "Выбери действие:",
        reply_markup=GameLogic.create_battle_markup()
    )

@bot.message_handler(func=lambda msg: msg.text == 'Атаковать')
def attack(message):
    player = get_player(message.from_user.id, message.from_user.first_name)
    
    if not player.in_battle:
        bot.send_message(
            message.chat.id,
            "Сейчас ты не в бою",
            reply_markup=GameLogic.create_main_markup()
        )
        return
    
    battle_over, result = GameLogic.battle_round(player)
    
    if battle_over:
        bot.send_message(
            message.chat.id,
            result,
            reply_markup=GameLogic.create_main_markup()
        )
    else:
        bot.send_message(
            message.chat.id,
            result,
            reply_markup=GameLogic.create_battle_markup()
        )

@bot.message_handler(func=lambda msg: msg.text == 'Исцеление (30 золота)')
def heal(message):
    player = get_player(message.from_user.id, message.from_user.first_name)
    
    if player.gold >= Config.HEAL_COST:
        player.gold -= Config.HEAL_COST
        player.heal(Config.HEAL_AMOUNT)
        
        if player.hp == Config.HEAL_AMOUNT and player.hp < player.max_hp:
            response = (
                f"✨ {player.name}, ты воскрес за {Config.HEAL_COST} золота!\n"
                f"Теперь у тебя {player.hp}/{player.max_hp} HP и {player.gold} золота."
            )
        else:
            response = (
                f"💚 {player.name}, ты исцелился на {Config.HEAL_AMOUNT} HP.\n"
                f"Теперь у тебя {player.hp}/{player.max_hp} HP и {player.gold} золота."
            )
    else:
        response = f"❌ Недостаточно золота! Нужно {Config.HEAL_COST}, а у тебя {player.gold}."
    
    if player.in_battle:
        markup = GameLogic.create_battle_markup()
    else:
        markup = GameLogic.create_main_markup()
    
    bot.send_message(
        message.chat.id, 
        response,
        reply_markup=markup
    )

@bot.message_handler(func=lambda msg: msg.text == 'Сбежать')
def flee(message):
    player = get_player(message.from_user.id, message.from_user.first_name)
    
    if player.in_battle:
        player.in_battle = False
        player.current_monster = None
        bot.send_message(
            message.chat.id,
            "Ты сбежал из боя! Монстр исчез.",
            reply_markup=GameLogic.create_main_markup()
        )
    else:
        bot.send_message(
            message.chat.id,
            "Сейчас ты не в бою",
            reply_markup=GameLogic.create_main_markup()
        )

@bot.message_handler(func=lambda message: True)
def handle_unknown(message):
    player = get_player(message.from_user.id, message.from_user.first_name)
    bot.send_message(
        message.chat.id,
        "Я не понимаю эту команду. Используй кнопки ниже для игры!",
        reply_markup=GameLogic.create_main_markup() if not player.in_battle else GameLogic.create_battle_markup()
    )

if __name__ == '__main__':
    print("🛡️ RPG-бот запущен!")
    bot.infinity_polling()