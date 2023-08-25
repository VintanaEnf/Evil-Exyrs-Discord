import json
import os

class spyFall:
    game_host = ""
    players: list = []
    discordserver = ""
    default = {
        "Hospital" : ["Doctor", "Nurse"],
        "Airplane" : ["Pilot", "Flight Attendant"],
        "Spy" : ["You are the spy."]
    }
    currentgamemap : dict = {}



    def __init__(self, game_host, discordserver):
        self.game_host = game_host
        self.players.append(game_host)
        self.discordserver = discordserver

        absolute_path = os.path.abspath(__file__)  # Get the absolute path of the current script
        game_path = os.path.join(os.path.dirname(absolute_path), f"data/spy_fall/{self.discordserver}.json")

        if not os.path.exists(game_path):
            with open(game_path, "w") as json_file:
                json_file.write(json.dumps(self.default, indent=4))
                
        if os.path.exists(game_path):
            with open(game_path, "r") as json_file:
                self.currentgamemap = json.load(json_file)

    def showplayers(self) -> list:
        return self.players
    
    def addmap(self, mapname,  map : list):
        newmap = { mapname : map}
        self.currentgamemap.update(newmap)
        return

    def addplayer(self, userName: str) -> bool:
        for i in self.players:
            if(i == userName):
                print("Spyfall class: User is already in game.")
                return False
            
        self.players.append(userName)
        print("Spyfall class: User is successfully added.")
        return True
    
    def maps(self):
        return self.currentgamemap
    
    def debug(self):
        return "debug func called properly."