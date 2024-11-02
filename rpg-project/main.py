import random
import classes
import dungeon
import lists

HELP = random.choice(dungeon.game_helper)
WORLD = f"{random.choice(dungeon.game_world_name_one)}-{random.choice(dungeon.game_world_name_two)}"
FIRST_ROOM = True


def main():
    build_world()
    character = select_class()
    game_loop(character)


def build_world():
    print("You awaken in a forest clearing on the outskirts of a large brooding castle. Your head aches and ears "
          "ring, as your vision begins to clear you "
          "notice a tall robed figure standing in front of you.")
    input("press any key")
    print(f"{HELP} - 'Greetings, i am {HELP} and i welcome you to {WORLD}, a dark curse has consumed this "
          f"land and the source emanates from this very castle. You are our only hope, please find the Dark Orb and "
          f"destroy it.\nFree us from this darkness and save {WORLD} from the Dark Lord.")
    input("press any key")


def select_class():
    character = ""
    ask_name = True
    name = input(f"{HELP} - 'What should i call you wayfarer?' ")
    print(f"{HELP} - 'Well met {name}, i'm afraid we have little time but i can provide you with some equipment.'")
    class_select = input("Type a letter to select a class for example 'e' for 'Enchanter': ").lower()
    while ask_name:
        if class_select in 'abcdefghijklmnopqrstuvwxyz' and len(class_select) == 1:
            ask_name = False
            character = classes.Character(name=name)
            character.generate_class_stats(class_select)
            print(character)
        else:
            class_select = input("This is not a class. Please type a letter for example 'm' for Magician: ")
    return character


def game_loop(character):
    create_monster = False
    game = True
    monster_type = ""
    location_one = random.choice(dungeon.game_rooms)
    location = random.choice(location_one)
    while game:
        create_monster, location = create_room(character, location)
        if create_monster:
            new_monster = make_monster(location['monster'])
            if new_monster is not None:
                fight(new_monster, character)
        description(location)


def create_room(character, location):
    global FIRST_ROOM
    if FIRST_ROOM:
        location['start'] = True
        room_type = random.choice(list(dungeon.game_room_types.keys()))
        location['room_name'] = room_type
        location['goal'] = True
        end_room = True
        location['current'] = True
        if end_room:
            location_two = random.choice(dungeon.game_rooms)
            location_end = random.choice(location_two)
            if location_end != location:
                location_end['goal'] = True
                end_room = False
        FIRST_ROOM = False
    else:
        location = make_choice(location)
        location['current'] = True
        room_type = random.choice(list(dungeon.game_room_types.keys()))
        location['room_name'] = room_type

    if location['monster'] is None and location['start'] is not True:
        add_monster(location, character)
        create_monster = True
    else:
        create_monster = False
    add_loot(location)
    location['visited'] = True
    return create_monster, location


def add_monster(location, character):
    monster_list = []
    if random.randint(0, 10) <= 6:
        location['entity'] = "Monster"
    if location['entity'] == "Monster":
        for i in lists.game_monsters:
            if lists.game_monsters[i]["difficulty"] <= character.explored:
                monster_list.append(lists.game_monsters[i]['name'])
        location['monster'] = random.choice(monster_list)


def add_loot(location):
    loot_list = []
    loot_type_list = []
    if random.randint(0, 3) <= 2:
        for i in list(dungeon.game_room_types.keys()):
            if i == location['room_name']:
                loot_type_list = dungeon.game_room_types[i]
                break

        if len(loot_type_list) > 0:
            item = random.choice(list(loot_type_list))
            for j in list(lists.game_items.keys()):
                if lists.game_items[j]['type'] == item:
                    loot_list += (list(lists.game_items.keys()))


def make_choice(location):
    for i in range(len(dungeon.game_rooms)):
        for j in range(len(dungeon.game_rooms[i])):
            if dungeon.game_rooms[i][j]['current']:
                location['current'] = True
                print(f"Original: {i}, {j}")
                i, j = check_rooms(i, j)
                print("i and j: ", i, j)
                print(f"New: {i}, {j}")
                return dungeon.game_rooms[i][j]


def check_rooms(i, j):
    go_north = False
    go_south = False
    go_east = False
    go_west = False
    north = "Type 'n' to go North!"
    south = "Type 's' to go South!"
    east = "Type 'e' to go East!"
    west = "Type 'w' to go West"
    if j + 1 <= len(dungeon.game_rooms[i]) - 1:
        print(north)
        go_north = True
    if j - 1 >= 0:
        print(south)
        go_south = True
    if i + 1 <= len(dungeon.game_rooms) - 1:
        print(east)
        go_east = True
    if i - 1 >= 0:
        print(west)
        go_west = True
    while True:
        response = input(": ").lower()
        if go_north and response == 'n':
            return i, j + 1
        elif go_south and response == 's':
            return i, j - 1
        elif go_east and response == 'e':
            return i + 1, j
        elif go_west and response == 'w':
            return i - 1, j


def make_monster(monster):
    if monster is not None:
        monster = lists.game_monsters[monster]
        new_monster = classes.Monster(strength=monster['strength'],
                                      max_health=monster['max_health'],
                                      max_mana=monster['mana'],
                                      miss=monster['miss'],
                                      hit=monster['hit'],
                                      name=monster['name'],
                                      gold=random.randint(0, monster['gold'])
                                      )
        return new_monster


def description(location):
    print(f"You find yourself in a {location['room_name']} ({location['id']})!")
    if location['monster'] is not None:
        print(f"There is a {location['monster']} in front of you!")
    else:
        print(f"You appear to be alone!")
    if location['loot'] is not None:
        print(f"You notice a {location['loot']} in the centre of the {location['room_name']}!")
    else:
        print(f"Nothing catches your eye!")


def fight(monster, character):
    print(f"A {monster.name} attacks you!")
    info = (f"{monster.name}\nHealth: {monster.health}/{monster.get_max_health}\nMana: {monster.mana}/{monster.max_mana}"
            f"\nStrength: {monster.strength}\nSpecial: {monster.special}")
    if 'Bow' in character.items:
        print(f"You fire your bow at the {monster.name}!")
        if random.randint(0,3) == 3:
            monster.wound_monster(character.damage)
            print(f"Your arrow strikes the {monster.name}")
            print(info)
    while monster.health > 0:
        monster_choice = random.randint(0,4)
        if monster_choice == 0 or monster_choice == 1:
            if monster_choice == 0:
                input(f"You cannot read the {monster.name}'s intentions!")
            else:
                input(f"{monster.miss}")
        else:
            if monster_choice == 3:
                input(f"You cannot read the {monster.name}'s intentions!")
            else:
                input(f"{monster.hit}")
            decision = input(f"Type 'a' to attack, 'b' to defend or 's' to cast a spell: ")
            if decision == 'a':
                attack(monster, character)
    print(info)
    input(f"You defeated the {monster.name}!")
    if len(monster.rewards) > 0:
        item = random.choice(monster.rewards)
        character.items += item
        print(f"You recovered {item}")
    input(f"You recovered {monster.gold} gold")
    character.gold += monster.gold



def attack(monster, character):
    if random.randint(0,3) * character.accuracy > 3:
        print(f"You strike the {monster.name} dealing {character.damage} points of damage!")
        monster.wound_monster(character.damage)
    else:
        print(f"You miss the {monster.name}!")



def block():
    ...

def cast_spell():
    ...








if __name__ == "__main__":
    main()
