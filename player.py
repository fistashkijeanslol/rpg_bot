from config import Config

class Player:
    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name
        self.level = 1
        self.hp = 100
        self.max_hp = 100
        self.gold = 50
        self.exp = 0
        self.attack = 10
        self.total_exp = 0
        self.inventory = []
        self.in_battle = False
        self.current_monster = None
        self.equipped_weapon = None
        self.equipped_armor = None
        self.pet = None
        self.attack_bonus = 0
        self.hp_bonus = 0
        self.exp_bonus = 0
        self.gold_bonus = 0
        
    def add_exp(self, amount):
        self.exp += amount
        self.total_exp += amount
        if self.exp >= self.level * Config.BASE_EXP_REQUIREMENT:
            return self.level_up()
        return False
    
    def level_up(self):
        self.level += 1
        self.max_hp += 20
        self.hp = self.max_hp
        self.attack += 5
        self.exp = 0
        return True
        
    def heal(self, amount):
        self.hp = min(self.max_hp, self.hp + amount)
        
    def take_damage(self, amount):
        self.hp = max(0, self.hp - amount)
        return self.hp > 0
        
    def equip_weapon(self, weapon_name):
        weapon = Config.SHOP_ITEMS["weapons"][weapon_name]
        self.equipped_weapon = weapon_name
        self.attack_bonus = weapon["attack"]
        
    def equip_armor(self, armor_name):
        armor = Config.SHOP_ITEMS["armor"][armor_name]
        self.equipped_armor = armor_name
        self.hp_bonus = armor["hp"]
        self.max_hp = 100 + self.hp_bonus
        self.hp = min(self.hp, self.max_hp)
        
    def set_pet(self, pet_name):
        pet = Config.SHOP_ITEMS["pets"][pet_name]
        self.pet = pet_name
        self.exp_bonus = pet["exp_bonus"]
        self.gold_bonus = pet["gold_bonus"]
        
    def status_text(self):
        exp_needed = self.level * Config.BASE_EXP_REQUIREMENT
        equipped_items = []
        if self.equipped_weapon:
            equipped_items.append(f"⚔️ Оружие: {self.equipped_weapon}")
        if self.equipped_armor:
            equipped_items.append(f"🛡️ Броня: {self.equipped_armor}")
        if self.pet:
            equipped_items.append(f"🐾 Питомец: {self.pet}")
            
        equipped_text = "\n".join(equipped_items) if equipped_items else "Нет экипировки"
        
        return (
            f"🧙‍♂️ {self.name}, вот твои характеристики:\n\n"
            f"🔹 Уровень: {self.level}\n"
            f"❤️ Здоровье: {self.hp}/{self.max_hp}\n"
            f"💰 Золото: {self.gold}\n"
            f"🔮 Опыт: {self.exp}/{exp_needed}\n"
            f"⚔️ Атака: {self.attack + self.attack_bonus}\n"
            f"🌟 Всего опыта: {self.total_exp}\n\n"
            f"🎒 Экипировка:\n{equipped_text}"
        )
    
    def sell_item(self, item_index):
        if 0 <= item_index < len(self.inventory):
            item = self.inventory.pop(item_index)
            # Простая логика продажи - все предметы продаются за 20 золота
            self.gold += 20
            return f"✅ Предмет '{item}' продан за 20 золота"
        return "❌ Неверный номер предмета"
    
    def inventory_text(self):
        if not self.inventory:
            return "🎒 Твой инвентарь пуст"
        items = "\n".join(f"• {item}" for item in self.inventory)
        return f"🎒 Инвентарь ({len(self.inventory)}/{Config.INVENTORY_SIZE}):\n{items}"
    
    def add_to_inventory(self, item):
        if len(self.inventory) < Config.INVENTORY_SIZE:
            self.inventory.append(item)
            return True
        return False