import random as rnd
from time import sleep


class Player:
    def __init__(self, x, y):
        self.x = 4
        self.y = 4


class Skill:
    def __init__(self, name, shape, skill_range):
        self.name = name
        self.shape = shape
        self.skill_range = skill_range

    def k6(self):
        dmg = rnd.randint(1, 6)
        return dmg


def display_map():
    display_map = ''

    for x in game_map:
        for y in x:
            if y == 0:
                display_map += ' 0 '
            elif y == player1:
                display_map += ' P '
            else:
                display_map += ' ' + str(y) + ' '

        display_map += '\n'
    return display_map


fire_ray = Skill('Ray', 'Line', 6)
fire_ball = Skill('Ball', 'Line Circle', 2)

player1 = Player(2, 4)

game_map = [[0 for x in range(0, 10)] for x in range(0, 10)]

game_map[player1.x][player1.y] = player1

use_skill = input('Please choose -FR or -FB: ')
if use_skill == '-FR':
    direction = input('Please choose direction -W, -E, -N, -S: ')
    if direction == '-W':
        counter = 0
        while counter < fire_ray.skill_range:
            counter += 1
            if player1.y - counter >= 0:
                game_map[player1.x][player1.y - counter] = 'F'
            print(display_map())
            sleep(0.2)

    if direction == '-E':
        counter = 0
        while counter < fire_ray.skill_range:
            counter += 1
            if player1.y + counter <= 9:
                game_map[player1.x][player1.y + counter] = 'F'
            print(display_map())
            sleep(0.2)

    if direction == '-N':
        counter = 0
        while counter < fire_ray.skill_range:
            counter += 1
            if player1.x - counter >= 0:
                game_map[player1.x - counter][player1.y] = 'F'
            print(display_map())
            sleep(0.2)

    if direction == '-S':
        counter = 0
        while counter < fire_ray.skill_range:
            counter += 1
            if player1.x + counter <= 9:
                game_map[player1.x + counter][player1.y] = 'F'
            print(display_map())
            sleep(0.2)

if use_skill == '-FB':
    direction = input('Choose direction -W, -E, -N, -S: ')
    if direction == '-N':
        counter = 0
        while counter < fire_ball.skill_range:
            counter += 1
            if player1.x - counter >= 0:
                game_map[player1.x - counter][player1.y] = 'F'
            print(display_map())
            sleep(0.2)
        posx = player1.x - fire_ball.skill_range
        y = 1
        while y < 2:
            for x in range(0, 2):
                if posx - x >= 0:
                    game_map[posx - x][player1.y] = 'F'
                if posx + x <= 9 and player1.y - y >= 0:
                    game_map[posx + x][player1.y - y] = 'F'
                if posx + x <= 9 and player1.y + y <= 9:
                    game_map[posx + x][player1.y + y] = 'F'
                if posx - x >= 0 and player1.y - y >= 0:
                    game_map[posx - x][player1.y - y] = 'F'
                if posx - x >= 0 and player1.y + y <= 9:
                    game_map[posx - x][player1.y + y] = 'F'
                print(display_map())
                sleep(0.2)
            y += 1



