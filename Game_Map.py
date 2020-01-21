import random as rnd
import string

game_map = [[0 for x in range(0, 10)] for x in range(0, 10)]


class Player:
    def __init__(self, name, pos_x, pos_y, game_repr):
        self.name = name
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.game_repr = game_repr

# Separate class for Monsters, mainly for isinstance() check.


class Monster(Player):
    pass


class Wall:
    def __init__(self, pos_x, pos_y):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.game_repr = 'W'


list_of_players = []
list_of_monsters = []
list_of_walls = []

monster_dictionary = {}

player1 = Player('Player1', 0, 0, 'P1')
player2 = Player('Player2', 0, 0, 'P2')
goblin = Monster('Goblin', 0, 0, 'G')
monster_dictionary['Goblin'] = goblin
orc = Monster('Orc', 0, 0, 'O')
monster_dictionary['Orc'] = orc
wall = Wall(0, 0)

list_of_players.append(player1)
list_of_players.append(player2)
list_of_monsters.append(goblin)
list_of_monsters.append(orc)
list_of_walls.append(wall)


def create_map(*objects):
    players = None
    monsters = None
    walls = None

# Split *objects:
    if len(objects) >= 0:
        players = objects[0]
    if len(objects) >= 1:
        monsters = objects[1]
    if len(objects) >= 2:
        walls = objects[2]

    # Initiate player's starting point

    player_x = 9
    player_y = 4

    # Place all the objects on the map / grid:

    for player in players:
        if game_map[player_x][player_y] == 0:
            player.pos_x = player_x
            player.pos_y = player_y
            game_map[player.pos_x][player.pos_y] = player
        else:
            player_y += 1
            player.pos_x = player_x
            player.pos_y = player_y
            if game_map[player_x][player_y] == 0:
                game_map[player.pos_x][player.pos_y] = player

    if walls:
        for wall in walls:
            pattern = rnd.randint(1, 3)
            number_of_tiles = rnd.randint(1, 4)

            # Pattern = 1: Horizontal Wall
            # Pattern = 2: Vertical Wall
            # Pattern = 3: House

            if pattern == 1:
                wall.pos_x = rnd.randint(0, 9)
                wall.pos_y = rnd.randint(4, 5)
                if wall.pos_y == 4 and game_map[wall.pos_x][wall.pos_y] == 0 \
                        or wall.pos_y == 5 and game_map[wall.pos_x][wall.pos_y] == 0:
                    game_map[wall.pos_x][wall.pos_y] = wall
                    while number_of_tiles > 0:
                        if game_map[wall.pos_x][wall.pos_y - 1] == 0:
                            number_of_tiles -= 1
                            wall.pos_y -= 1
                            game_map[wall.pos_x][wall.pos_y] = wall
                        elif game_map[wall.pos_x][wall.pos_y + 1] == 0:
                            number_of_tiles -= 1
                            wall.pos_y += 1
                            game_map[wall.pos_x][wall.pos_y] = wall
                        else:
                            break
            elif pattern == 2:
                wall.pos_x = rnd.randint(4, 5)
                wall.pos_y = rnd.randint(0, 9)
                if wall.pos_x == 4 and game_map[wall.pos_x][wall.pos_y] == 0 \
                        or wall.pos_x == 5 and game_map[wall.pos_x][wall.pos_y] == 0:
                    game_map[wall.pos_x][wall.pos_y] = wall
                    while number_of_tiles > 0:
                        if game_map[wall.pos_x - 1][wall.pos_y] == 0:
                            number_of_tiles -= 1
                            wall.pos_x -= 1
                            game_map[wall.pos_x][wall.pos_y] = wall
                        elif game_map[wall.pos_x + 1][wall.pos_y] == 0:
                            number_of_tiles -= 1
                            wall.pos_x += 1
                            game_map[wall.pos_x][wall.pos_y] = wall
                        else:
                            break
            elif pattern == 3:
                wall.pos_x = rnd.randint(4, 5)
                wall.pos_y = rnd.randint(4, 5)
                left_front_tiles = 1
                while left_front_tiles >= 0:
                    left_front_tiles -= 1
                    wall.pos_y -= 1
                    game_map[wall.pos_x][wall.pos_y] = wall
                left_side_tiles = 2
                while left_side_tiles >= 0:
                    left_side_tiles -= 1
                    wall.pos_x -= 1
                    game_map[wall.pos_x][wall.pos_y] = wall
                back_tiles = 3
                while back_tiles >= 0:
                    back_tiles -= 1
                    wall.pos_y += 1
                    game_map[wall.pos_x][wall.pos_y] = wall
                left_side_tiles = 2
                while left_side_tiles >= 0:
                    left_side_tiles -= 1
                    wall.pos_x += 1
                    game_map[wall.pos_x][wall.pos_y] = wall
                right_front_tiles = 0
                while right_front_tiles >= 0:
                    right_front_tiles -= 1
                    wall.pos_y -= 1
                    game_map[wall.pos_x][wall.pos_y] = wall
        if monsters:
            # Choose what monster type to spawn can be improved to selection
            # of more than one type of monsters. Ex: passing list of input
            # to the function
            choose_monster = input('Please choose, orc or goblin: ')
            # Let's make sure that the monster name is always in the same
            # format.

            def convert_name(name_to_convert):
                converted_name = ""
                if name_to_convert[0].islower():
                    converted_name += name_to_convert[0].upper()
                for letter in name_to_convert[1:]:
                    if letter.isupper():
                        converted_name += letter.lower()
                    else:
                        converted_name += letter
                return converted_name
            monster_name = convert_name(choose_monster)

            def spawn_creatures(type_of_monster):
                number_of_creatures = rnd.randint(1, 3)
                while number_of_creatures > 0:
                    number_of_creatures -= 1
                    new_creature = Monster(type_of_monster.name, 0, 0, type_of_monster.game_repr)
                    new_creature.pos_x = rnd.randint(0, 9)
                    new_creature.pos_y = rnd.randint(0, 9)
                    if game_map[new_creature.pos_x][new_creature.pos_y] == 0:
                        game_map[new_creature.pos_x][new_creature.pos_y] = new_creature
                    else:
                        while game_map[new_creature.pos_x][new_creature.pos_y] != 0:
                            new_creature.pos_x = rnd.randint(0, 9)
                            new_creature.pos_y = rnd.randint(0, 9)
                            if game_map[new_creature.pos_x][new_creature.pos_y] == 0:
                                game_map[new_creature.pos_x][new_creature.pos_y] = new_creature
                                break

            # Once we have all set, we can spawn creatures:
            if monster_name in monster_dictionary:
                spawn_creatures(monster_dictionary[monster_name])
            else:
                print('Invalid input!')
            '''
            
            # An option with list of monsters. Otherwise dictionary seems more elegant.
            
            for creature_type in monsters:
                if monster_name == 'Orc' and creature_type.name == monster_name:
                    spawn_creatures(monster_name, creature_type)
                elif monster_name == 'Goblin' and creature_type.name == monster_name:
                    spawn_creatures(monster_name, creature_type)
            '''

create_map(list_of_players, list_of_monsters, list_of_walls)

display_map = ""

for x in game_map:
    for y in x:
        if y == 0:
            display_map += '  0  '
        else:
            display_map += '  ' + y.game_repr + '  '
    display_map += '\n'

print(display_map)