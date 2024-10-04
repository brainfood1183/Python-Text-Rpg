import random
import lists
import dungeon

level = 2
monster_list = []

location_one = random.choice(dungeon.game_rooms)
location = random.choice(location_one)

room_type = random.choice(list(dungeon.game_room_types.keys()))

location['room_name'] = room_type
location['start'] = True
if random.randint(0, 10) <= 6:
    location['entity'] = "Monster"
if location['entity'] == "Monster":
    for i in lists.game_monsters:
        if lists.game_monsters[i]["difficulty"] <= level:
            monster_list.append(lists.game_monsters[i]['name'])
    location['monster'] = random.choice(monster_list)
dungeons = dungeon.game_rooms

for i in range(len(dungeons)):
    for j in range(len(dungeons[i])):
        if dungeons[i][j]['start']:
            north = "type 'n' to go North!"
            south = "type 's' to go South!"
            east = "type 'e' to go East!"
            west = "type 'w' to go West"
            input(f"{len(dungeons[i])}")
            input(len(dungeons))
            input(f"{len(dungeons[i][j])} id: {dungeons[i][j]['id']}")
            if j + 1 <= len(dungeons[i]):
                print(north)
            if j - 1 >= 0:
                print(south)
            if i + 1 <= len(dungeons):
                print(east)
            if i - 1 >= 0:
                print(west)


loot_list = []
loot_type_list = []
if random.randint(0, 3) <= 2:
    for i in list(dungeon.game_room_types.keys()):
        if i == location['room_name']:
            loot_type_list = dungeon.game_room_types[i]
            break

    item = random.choice(list(loot_type_list))
    for j in list(lists.game_items.keys()):
        if lists.game_items[j]['type'] == item:
            loot_list += (list(lists.game_items.keys()))

    if len(loot_list) > 0:
        location['loot'] = random.choice(loot_list)

print(loot_list)
print(location)
