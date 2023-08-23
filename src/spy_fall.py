import json
import os

class spyFall:

    game_host = ""
    players: list = []
    discordserver = ""
    default = {
        "Hospital" : ["Doctor", "Nurse"],
        "Airplane" : ["Pilot", "Flight Attendant"]
    }
    currentgame = {}
    def __init__(self, game_host, discordserver):
        self.game_host = game_host
        self.players.append(game_host)
        self.discordserver = discordserver
        if not os.path.exists(f"data\spy_fall\{self.discordserver}.json"):
            with open(f"{self.discordserver}.json", "w") as json_file:
                json_file.write(json.dumps(self.default, indent=4))
        if os.path.exists(f"data\spy_fall\{self.discordserver}.json"):
            with open("data.json", "r") as json_file:
                self.currentgame = json.load(json_file)

    def showplayers(self) -> list:
        return self.players
    
    def addmap(self, map : list):
        newmap = {map: list}
        self.currentgame.update(newmap)