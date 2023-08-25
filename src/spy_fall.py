import json
import os
import random

class spyFall:
    game_host = ""
    players: list = []
    discordserver = ""
    default = {
        "Hospital" : ["Doctor", "Nurse", "spy"],
        "Airplane" : ["Pilot", "Flight Attendant", "spy"]
    }
    currentgamemap : dict = {}
    spy = 0

    chosenmap : str = ""

    def __init__(self, game_host, discordserver):
        self.game_host = game_host
        self.players.append(game_host)
        self.discordserver = discordserver

        absolute_path = os.path.abspath(__file__)
        game_path = os.path.join(os.path.dirname(absolute_path), f"data/spy_fall/{self.discordserver}.json")

        if not os.path.exists(game_path):
            with open(game_path, "w") as json_file:
                self.currentgamemap = self.default
                json_file.write(json.dumps(self.currentgamemap, indent=4))
                
        if os.path.exists(game_path):
            with open(game_path, "r") as json_file:
                self.currentgamemap = json.load(json_file)

    def showplayers(self) -> list:
        return self.players
    
    def write(self):
        absolute_path = os.path.abspath(__file__)
        game_path = os.path.join(os.path.dirname(absolute_path), f"data/spy_fall/{self.discordserver}.json")
        with open(game_path, "w") as json_file:
                json_file.write(json.dumps(self.currentgamemap, indent=4))

    def addmap(self, mapname,  map : list):
        newmap = { mapname : map}
        self.currentgamemap.update(newmap)
        self.write()
        return

    def addplayer(self, userName) -> bool:
        for i in self.players:
            if(i == userName):
                print("Spyfall class: User is already in game.")
                return False
            
        self.players.append(userName)
        print(f"Spyfall class: {userName} is successfully added.")
        return True
    
    def removemap(self, map):
        mapname = self.currentgamemap.pop(map)
        self.write()
        return mapname

    def maps(self):
        return self.currentgamemap
    
    def debug(self):
        return "debug func called properly."
    
    def start(self):
        templist = []
        for keya in self.currentgamemap:
            templist.append(keya)
        self.chosenmap = templist[random.randint(0, len(templist)-1)]
        numberofplayers = len(self.players)
        self.spy = random.randint(0, numberofplayers-1)
        print(f"map is {self.currentgamemap[self.chosenmap]} and the spy is {self.players[self.spy]}")
        return self.players[self.spy]

    def getrole(self, ID):
        if ID == self.players[self.spy]:
            return "spy"
        else:
            roles = self.currentgamemap[self.chosenmap]
            return roles[random.randint(0, len(roles)-2)]
        
    def getmap(self, role):
        if role=="spy":
            return "Guess the location"
        else:
            return self.chosenmap