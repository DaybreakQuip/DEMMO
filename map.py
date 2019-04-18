import sqlite3
import datetime
import pickle
import json

class Monster:
    def __str__(self):
        return "M"

class NPC:
    def __str__(self):
        return "N"
class Player:
    def __str__(self):
        return "P"
class Map:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = {(x,y): ["&nbsp&nbsp"] for x in range(self.width) for y in range(self.height)}

    def __str__(self):
        map = ""
        for i in range(self.width):
            map += "<br/>-------------------------------<br/>|&nbsp&nbsp"
            for j in range(self.height):
                map += "" + [x.__str__() for x in self.grid[(i,j)]].__str__()[1:-1] + "&nbsp&nbsp|&nbsp&nbsp"
        map += "<br/>-------------------------------<br/>"
        return map

    def addToMap(self,x, y, npc):
        if self.grid[(x,y)][0] == "&nbsp&nbsp":
            self.grid[(x,y)] = [npc]
        else:
            self.grid[(x,y)].append(npc)


def request_handler(request=None):
    with open("__HOME__/demmo/map.JSON") as map_file:
        map_data = json.load(map_file)
        width = map_data['width']
        height = map_data['height']
        monsters = map_data['monsters']
        shops = map_data['shops']

        game_map = Map(width, height)
        for x, y in monsters:
            game_map.addToMap(x, y, Monster())
        for x, y in shops:
            game_map.addToMap(x, y, NPC())
        game_map.addToMap(0, 1, Player())

        return str(game_map)


