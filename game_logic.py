import random
from config import Config
from telebot import types

class GameLogic:
    @staticmethod
    def create_main_markup():
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        btn_status = types.KeyboardButton('Характеристики')
        btn_hunt = types.KeyboardButton('Охота на монстров')
        btn_inventory = types.KeyboardButton('Инвентарь')
        btn_shop = types.KeyboardButton('🛒 Магазин')
        btn_help = types.KeyboardButton('Помощь')
        markup.add(btn_status, btn_hunt, btn_inventory, btn_shop, btn_help)
        return markup

    @staticmethod
    def create_battle_markup():
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        btn_attack = types.KeyboardButton('Атаковать')
        btn_heal = types.KeyboardButton('Исцеление (30 золота)')
        btn_flee = types.KeyboardButton('Сбежать')
        markup.add(btn_attack, btn_heal, btn_flee)
        return markup

    @staticmethod
    def generate_monster(player_level):
        base_hp = Config.BASE_MONSTER_HP + player_level * 5
        base_attack = Config.BASE_MONSTER_ATTACK + player_level * 2
        
        monster_hp = random.randint(base_hp, base_hp + 10)
        monster_attack = random.randint(base_attack, base_attack + 3)
        gold_reward = random.randint(*Config.HUNT_REWARD_RANGE) + player_level * 2
        exp_reward = random.randint(*Config.HUNT_EXP_RANGE) + player_level
        
        monster_types = [
            ('Гоблин', 'ржавый кинжал', 'Гоблиньи уши'),
            ('Орк', 'топор', 'Клык орка'),
            ('Тролль', 'дубина', 'Кровь тролля'), 
            ('Скелет', 'костяной меч', 'Магическая пыль'),
            ('Демон', 'огненный посох', 'Сердце демона'),
            ('Вампир', 'кровавые когти', 'Зуб вампира'),
            ('Элементаль', 'стихийная энергия', 'Ядро элементаля')
        ]
        name, weapon, loot = random.choice(monster_types)
        
        # 50% шанс получить дополнительный лут
        additional_loot = None
        if random.random() < 0.5:
            additional_loot_items = [
                'Золотой слиток',
                'Редкий гриб',
                'Магический кристалл',
                'Древний свиток',
                'Руна силы'
            ]
            additional_loot = random.choice(additional_loot_items)
        
        return {
            'hp': monster_hp,
            'max_hp': monster_hp,
            'attack': monster_attack,
            'gold': gold_reward,
            'exp': exp_reward,
            'name': name,
            'weapon': weapon,
            'loot': loot,
            'additional_loot': additional_loot
        }

    @staticmethod
    def start_battle(player):
        player.in_battle = True
        player.current_monster = GameLogic.generate_monster(player.level)
        monster = player.current_monster
        
        battle_stickers = {
            'Гоблин': 'CAACAgIAAxkBAAEL3m1mE53JZ5xV6V4AAbKQJ1QzXzKv5AACaQsAAnDUuUqFJgABJQABNwXDNA',
            'Орк': 'CAACAgIAAxkBAAEL3m9mE53Y5v8AAU9T9wABQ5M3vJ2VXQACagsAAnDUuUqXy5J3XgABXzQ0',
            'Тролль': 'CAACAgIAAxkBAAEL3nFmE53m5V1QY7YAAbQ3GQABnz3e1gACbQsAAnDUuUoAAXZQ0h1y5jQ0',
            'Скелет': 'CAACAgIAAxkBAAEL3nNmE53zO5Y1eW4AAXmQ0QABnz3e1gACbwsAAnDUuUoAAXZQ0h1y5jQ0',
            'Демон': 'CAACAgIAAxkBAAEL3nVmE5375V1QY7YAAbQ3GQABnz3e1gACcQsAAnDUuUoAAXZQ0h1y5jQ0'
        }
        
        sticker_id = battle_stickers.get(monster['name'], 'CAACAgIAAxkBAAEL3ndmE54J5V1QY7YAAbQ3GQABnz3e1gACcgsAAnDUuUoAAXZQ0h1y5jQ0')
        
        return {
            'sticker': sticker_id,
            'text': (
                f"🦖 *Ты встретил {monster['name']} с {monster['weapon']}!*\n\n"
                f"❤️ Здоровье: {monster['hp']} HP\n"
                f"⚔️ Атака: {monster['attack']}\n\n"
                "*Выбери действие:*"
            )
        }

    @staticmethod
    def battle_round(player):
        if not player.in_battle or not player.current_monster:
            return None, "Бой не начат"
            
        monster = player.current_monster
        
        # Игрок атакует
        player_damage = max(1, player.attack + player.attack_bonus + random.randint(-2, 2))
        monster['hp'] -= player_damage
        
        if monster['hp'] <= 0:
            # Победа
            gold_reward = int(monster['gold'] * (1 + player.gold_bonus))
            exp_reward = int(monster['exp'] * (1 + player.exp_bonus))
            
            player.gold += gold_reward
            leveled_up = player.add_exp(exp_reward)
            
            loot = monster['loot']
            if monster['additional_loot']:
                loot += f", {monster['additional_loot']}"
            got_loot = player.add_to_inventory(loot)
            
            reward_text = (
                f"🎯 Ты победил {monster['name']}!\n"
                f"💰 Получено: {gold_reward} золота\n"
                f"🔮 Опыт: +{exp_reward}\n"
            )
            if got_loot:
                reward_text += f"🎒 Получен предмет: {loot}\n"
            if leveled_up:
                reward_text += f"\n🌟 Уровень повышен до {player.level}!"
            
            player.in_battle = False
            player.current_monster = None
            return True, reward_text
        
        # Монстр атакует
        monster_damage = max(1, monster['attack'] + random.randint(-1, 1))
        player.take_damage(monster_damage)
        
        result = (
            f"⚔️ Ты нанес {player_damage} урона {monster['name']}\n"
            f"👹 {monster['name']} атакует и наносит {monster_damage} урона\n\n"
            f"❤️ Твое здоровье: {player.hp}/{player.max_hp}\n"
            f"💀 {monster['name']}: {monster['hp']}/{monster['max_hp']} HP"
        )
        
        if player.hp <= 0:
            result += "\n\n💀 Ты повержен! Используй исцеление."
            player.in_battle = False
            player.current_monster = None
            return True, result
        
        return False, result

    @staticmethod
    def help_text():
        return (
            "📖 Помощь по игре:\n\n"
            "• Характеристики - показывает твои параметры\n"
            "• Охота на монстров - начать битву с монстром\n"
            "• Инвентарь - показать собранные предметы\n"
            "• 🛒 Магазин - купить оружие, броню или питомца\n\n"
            "В бою:\n"
            "• Атаковать - нанести урон монстру\n"
            "• Исцеление - восстановить здоровье за 30 золота\n"
            "• Сбежать - выйти из боя (монстр исчезнет)\n\n"
            "Чем выше уровень, тем сильнее монстры!"
        )