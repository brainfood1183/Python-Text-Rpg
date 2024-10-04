import random
import lists


class Character:
    def __init__(self, strength=0, dexterity=0, intelligence=0, wisdom=0, charisma=0, name=""):
        self.name = name
        self.character_class = ""
        self.strength = strength
        self.dexterity = dexterity
        self.intelligence = intelligence
        self.wisdom = wisdom
        self.charisma = charisma
        self.max_mana = 0
        self.mana = 0
        self.damage = 0
        self.max_health = 0
        self.health = 0
        self.accuracy = 0
        self.speed = 0
        self.items = []
        self.spells = []
        self.head = "Empty"
        self.neck = "Empty"
        self.body = "Empty"
        self.left = "Empty"
        self.right = "Empty"
        self.explored = 0
        self.gold = 0

    def __str__(self):
        return (
            f"Name: {self.get_name}\nClass: {self.character_class}\nStrength: {self.strength}\nDexterity: {self.dexterity}\nIntelligence: "
            f"{self.intelligence}\nWisdom: {self.wisdom}\nCharisma: {self.charisma}\nHealth: {self.health}/"
            f"{self.max_health}\nMana: {self.mana}/{self.max_mana}\nItems: {self.get_items}\nSpells: {self.get_spells}")

    def sort_items(self):
        for item in self.items:
            if item in lists.game_items:
                if lists.game_items[item]["equipment"] == "head" and self.head == "Empty":
                    self.head = item
                elif lists.game_items[item]["equipment"] == "neck" and self.neck == "Empty":
                    self.neck = item
                elif lists.game_items[item]["equipment"] == "body" and self.neck == "Empty":
                    self.body = item
                elif lists.game_items[item][
                    "equipment"] == "b_hands" and self.left == "Empty" and self.right == "Empty":
                    self.right = item
                    self.left = f"Second Hand {item}"
                elif lists.game_items[item]["equipment"] == "left" and self.left == "Empty":
                    self.left = item
                elif lists.game_items[item]["equipment"] == "right" and self.right == "Empty":
                    self.right = item
                elif lists.game_items[item]["equipment"] == "left" and self.left != "Empty" and self.right == "Empty":
                    self.right = item

    def add_spell(self, spell):
        self.spells.append(spell)

    def add_item(self, item):
        self.items.append(item)
        if lists.game_items[item]["equipment"] == "none":
            return
        if lists.game_items[item]["equipment"] == "head" and self.head == "Empty":
            self.head = item
        elif lists.game_items[item]["equipment"] == "head":
            if input(f"Replace {self.head} with {item}?"):
                self.head = item
        if lists.game_items[item]["equipment"] == "neck" and self.neck == "Empty":
            self.neck = item
        elif lists.game_items[item]["equipment"] == "neck":
            if input(f"Replace {self.neck} with {item}?"):
                self.neck = item
        if lists.game_items[item]["equipment"] == "body" and self.body == "Empty":
            self.body = item
        elif lists.game_items[item]["equipment"] == "body":
            if input(f"Replace {self.body} with {item}?"):
                self.body = item
        if lists.game_items[item]["equipment"] == "body" and self.body == "Empty":
            self.body = item
        elif lists.game_items[item]["equipment"] == "body":
            if input(f"Replace {self.body} with {item}?"):
                self.body = item

    def alter_health(self, amount):
        self.health += amount

    def alter_mana(self, amount):
        self.mana += amount

    def alter_stat(self, stat, amount):
        match stat:
            case "strength":
                self.strength += amount
            case "dexterity":
                self.dexterity += amount
                self.accuracy = self.dexterity * self.intelligence
            case "intelligence":
                self.intelligence += amount
                self.accuracy = self.dexterity * self.intelligence
        if stat == "dexterity" or stat == "strength":
            self.max_health = self.strength * self.dexterity
            if self.health > self.max_health:
                self.health = self.max_health
            self.speed = self.dexterity + (self.strength / 2)
        elif stat == "intelligence" or stat == "wisdom":
            self.max_mana = self.intelligence * self.wisdom
            if self.mana > self.max_mana:
                self.mana = self.max_mana

    @property
    def get_name(self):
        return self.name

    @property
    def strength_stat(self):
        return self.strength

    @property
    def health_stat(self):
        return self.health

    @property
    def dexterity_stat(self):
        return self.dexterity

    @property
    def intelligence_stat(self):
        return self.intelligence

    @property
    def wisdom_stat(self):
        return self.wisdom

    @property
    def charisma_stat(self):
        return self.charisma

    @property
    def get_items(self):
        return f"{", ".join(self.items)}"

    @property
    def get_items_stat(self):
        return self.items

    @property
    def damage_stat(self):
        return self.damage

    @property
    def mana_stat(self):
        return self.mana

    @property
    def accuracy_stat(self):
        return self.accuracy

    @property
    def max_health_stat(self):
        return self.max_health

    @property
    def get_spells(self):
        return f"{", ".join(self.spells)}"

    @property
    def get_spells_stat(self):
        return self.spells

    def generate_class_stats(self, response):
        rand_stat = random.randint(1, 4)
        c = lists.classes

        for i in c:
            if response == i:
                self.character_class = c[response]['name']
                self.strength += c[response]['strength']
                self.dexterity += c[response]['dexterity']
                self.intelligence += c[response]['intelligence']
                self.wisdom += c[response]['wisdom']
                self.charisma += c[response]['charisma']
                for s in c[response]['spells']:
                    self.add_spell(s)
                for i in c[response]['items']:
                    self.add_item(i)
        self.accuracy = (self.dexterity / 2) + rand_stat
        self.max_health = self.health
        self.max_mana = self.intelligence + self.wisdom
        self.mana = self.max_mana
        self.damage = round(self.strength / 3, 2) + rand_stat
        self.max_health = self.strength + round(self.dexterity / 2) + rand_stat
        self.health = self.max_health


##################################################################################

class Monster:
    def __init__(self, name="", strength=0, max_health=0, max_mana=0, miss="", hit="", special="", gold=0):
        self.name = name
        self.strength = strength
        self.max_health = max_health
        self.health = self.max_health
        self.max_mana = max_mana
        self.mana = max_mana
        self.rewards = []
        self.spells = []
        self.special = special
        self.miss = miss
        self.hit = hit
        self.gold = gold

    def wound_monster(self, damage):
        self.health -= damage

    @property
    def get_spells(self):
        return f"{", ".join(self.spells)}"

    @property
    def get_max_health(self):
        return self.max_health

    @property
    def get_health(self):
        return self.health

    @property
    def get_max_mana(self):
        return self.max_mana

    @property
    def get_mana(self):
        return self.mana

    @property
    def get_strength(self):
        return self.strength

    @property
    def get_special(self):
        return self.special

    @property
    def get_miss(self):
        return self.miss

    @property
    def get_hit(self):
        return self.hit
