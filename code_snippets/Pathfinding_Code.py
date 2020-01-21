# This snippet of code was written for my bigger project as pathfinding code for enemies

import random as rnd
from time import sleep

game_map = [[0 for x in range(0, 10)] for x in range(0, 10)]

display_map = ""


class A:
    def __init__(self):
        self.x = 8
        self.y = 7
        self.image = 'A'


class B:
    def __init__(self):
        self.x = 2
        self.y = 1
        self.image = 'B'


class Wall:
    def __init__(self, pos_x, pos_y):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.image = 'W'


a = A()
b = B()

# Generate obstacles
generate_walls = rnd.randint(0, 80)
number_of_walls = 0
max_range = len(game_map) - 1
while number_of_walls < generate_walls:
    new_wall = Wall(rnd.randint(0, max_range), rnd.randint(0, max_range))
    if game_map[new_wall.pos_x][new_wall.pos_y] == 0:
        game_map[new_wall.pos_x][new_wall.pos_y] = new_wall
        number_of_walls += 1
    else:

        # Generate new position if the previous one was not empty.
        while game_map[new_wall.pos_x][new_wall.pos_y] != 0:
            new_wall.pos_x = rnd.randint(0, max_range)
            new_wall.pos_y = rnd.randint(0, max_range)
            if game_map[new_wall.pos_x][new_wall.pos_y] == 0:
                game_map[new_wall.pos_x][new_wall.pos_y] = new_wall
                number_of_walls += 1
                break

# Initiate start and finish
game_map[a.x][a.y] = a
game_map[b.x][b.y] = b

initial_x = a.x
initial_y = a.y

# Functions
def pathfinding():
    path = []
    visited = []

# First, find options that are seemingly best:
    while b not in path:
        if a.x < 9 and game_map[a.x + 1][a.y] == b \
                or a.x < 9 and a.x < b.x and game_map[a.x + 1][a.y] == 0:
            a.x += 1
            if game_map[a.x][a.y] == b:
                path.append(game_map[a.x][a.y])
                break
            else:
                game_map[a.x][a.y] = 9
                path.append((a.x, a.y))
        elif a.x > 0 and game_map[a.x - 1][a.y] == b \
                or a.x > 0 and a.x > b.x and game_map[a.x - 1][a.y] == 0:
            a.x -= 1
            if game_map[a.x][a.y] == b:
                path.append(game_map[a.x][a.y])
                break
            else:
                game_map[a.x][a.y] = 9
                path.append((a.x, a.y))
        elif a.y > 0 and game_map[a.x][a.y - 1] == b \
                or a.y > 0 and a.y > b.y and game_map[a.x][a.y - 1] == 0:
            a.y -= 1
            if game_map[a.x][a.y] == b:
                path.append(game_map[a.x][a.y])
                break
            else:
                game_map[a.x][a.y] = 9
                path.append((a.x, a.y))
        elif a.y < 9 and game_map[a.x][a.y - 1] == b \
            or a.y < 9 and a.y < b.y and game_map[a.x][a.y + 1] == 0:
            a.y += 1
            if game_map[a.x][a.y] == b:
                path.append(game_map[a.x][a.y])
                break
            else:
                game_map[a.x][a.y] = 9
                path.append((a.x, a.y))
    ##############################################################

# If there's no direction that obviously take us closer to the target,
# then any step in any direction will be good enough.
        elif a.x < 9 and game_map[a.x + 1][a.y] == b or \
                a.x < 9 and game_map[a.x + 1][a.y] == 0:
            a.x += 1
            if game_map[a.x][a.y] == b:
                path.append(game_map[a.x][a.y])
                break
            else:
                game_map[a.x][a.y] = 9
                path.append((a.x, a.y))
        elif a.x > 0 and game_map[a.x - 1][a.y] == b \
                or a.x > 0 and game_map[a.x - 1][a.y] == 0:
            a.x -= 1
            if game_map[a.x][a.y] == b:
                path.append(game_map[a.x][a.y])
                break
            else:
                game_map[a.x][a.y] = 9
                path.append((a.x, a.y))
        elif a.y > 0 and game_map[a.x][a.y - 1] == b \
                or a.y > 0 and game_map[a.x][a.y - 1] == 0:
            a.y -= 1
            if game_map[a.x][a.y] == b:
                path.append(game_map[a.x][a.y])
                break
            else:
                game_map[a.x][a.y] = 9
                path.append((a.x, a.y))
        elif a.y < 9 and game_map[a.x][a.y + 1] == b \
                or a.y < 9 and game_map[a.x][a.y + 1] == 0:
            a.y += 1
            if game_map[a.x][a.y] == b:
                path.append(game_map[a.x][a.y])
                break
            else:
                game_map[a.x][a.y] = 9
                path.append((a.x, a.y))

# If we cannot move in any direction from the point at where we are, let's go back and
# look for any other route.
        elif len(path) != 0:
            a.x, a.y = path[-1]
            visited.append((a.x, a.y))
            path.pop()

# Else if there was no other route on our previous path, let's try to go back to the start
# to see if we can go anywhere from there.
        elif len(path) == 0:
            # If we can't go anywhere from our starting point, that means that there's no
            # route to our goal. End search.
            if a.x == initial_x and a.y == initial_y and len(path) == 0:
                print(display_path())
                print('No way through')
                break
            a.x = initial_x
            a.y = initial_y

    return path, visited


def display_path():
    display_map = ""
    for x in game_map:
        for y in x:
            if y == 0:
                display_map += ' 0 '
            elif y == 9:
                display_map += ' 9 '
            else:
                display_map += ' ' + y.image + ' '
        display_map += '\n'
    return display_map


path, visited = pathfinding()
a.x, a.y = initial_x, initial_y

# Clear all positions that are not leading to the target.
if len(visited) != 0:
    for position in visited:
        x, y = position
        game_map[x][y] = 0

# Walk the path.
while len(path) != 0:
    if path[0] != b:
        game_map[a.x][a.y] = 0
        a.x, a.y = path[0]
        game_map[a.x][a.y] = a
        path.remove((a.x, a.y))
        sleep(2)
        print(display_path())
