import json
import os

class spyFall:

    game_host = ""
    players: list = []
    discordserver = ""
    default = {
        1 : ["Hospital", "Doctor", "Nurse"],
        2 : ["Airplane", "Pilot", "Flight Attendant"]
    }
    def __init__(self, game_host, discordserver):
        self.game_host = game_host
        self.players.append(game_host)
        self.discordserver = discordserver
        if not os.path.exists(f"data\spy_fall\{self.discordserver}.json"):
            with open(f"{self.discordserver}.json", "w") as json_file:
            json_file.write(json.dumps(self.default, indent=4))

    def showplayers(self) -> list:
        return self.players
    
    def addmap(self, map : list):
        newmap = {number: list}