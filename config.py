import os

class Config:
    TOKEN = '8053007733:AAFsAsCMhweQqnhPuf-xM1A9lslRn457hdM'
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    
    # Игровые константы
    BASE_EXP_REQUIREMENT = 50
    HEAL_COST = 30
    HEAL_AMOUNT = 30
    HUNT_REWARD_RANGE = (10, 20)
    HUNT_EXP_RANGE = (5, 15)
    BASE_MONSTER_HP = 30
    BASE_MONSTER_ATTACK = 5
    INVENTORY_SIZE = 10

    # Добавить в Config class
    SHOP_ITEMS = {
        "оружие": {
            "Деревянный меч": {"price": 50, "attack": 5},
            "Железный меч": {"price": 150, "attack": 10},
            "Стальной меч": {"price": 300, "attack": 15},
            "Мифриловый меч": {"price": 600, "attack": 25}
        },
        "броня": {
            "Кожаная броня": {"price": 40, "hp": 20},
            "Кольчуга": {"price": 120, "hp": 40},
            "Латная броня": {"price": 250, "hp": 60},
            "Мифриловая броня": {"price": 500, "hp": 100}
        },
        "питомцы": {
            "Кот": {"price": 200, "exp_bonus": 0.1, "gold_bonus": 0.1},
            "Сова": {"price": 400, "exp_bonus": 0.2, "gold_bonus": 0.15},
            "Дракончик": {"price": 800, "exp_bonus": 0.3, "gold_bonus": 0.25}
        }
    }
