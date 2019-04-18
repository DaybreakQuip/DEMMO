import sqlite3
import datetime
import pickle


class Monster:
    def __str__(self):
        return "M"

class NPC:
    def __str__(self):
        return "N"

class Map:
    def __init__(self):
        self.width = 5
        self.height = 5
        self.grid = {(x,y): "&nbsp&nbsp" for x in range(self.width) for y in range(self.height)}

    def __str__(self):
        map = ""
        for i in range(self.width):
            map += "<br/>-------------------------------<br/>|&nbsp&nbsp"
            for j in range(self.height):
                map += "" + self.grid[(i,j)].__str__() + "&nbsp&nbsp|&nbsp&nbsp"
        map += "<br/>-------------------------------<br/>"
        return map

    def addToMap(self,x, y, npc):
        self.grid[(x,y)] = npc

def request_handler(request=None):
    mapper = Map()
    monster = pickle.load(open( "__HOME__/monster.p", "rb" ))
    npc = pickle.load(open( "__HOME__/npc.p", "rb" ))
    for i in range(len(monster["x"])):
        mapper.addToMap(monster["x"][i], monster["y"][i], Monster())
    for i in range(len(npc["x"])):
        mapper.addToMap(npc["x"][i], npc["y"][i], NPC())
    return mapper.__str__()