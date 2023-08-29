import json
import os
import random

class spyFall:
    
    game_host = ""
    players = []
    discordserver = ""
    default = {
        "Hospital" : ["Doctor", "Nurse", "spy"],
        "Airplane" : ["Pilot", "Flight Attendant", "spy"]
    }
    currentgamemap : dict = {}
    spy = 0
    config : dict
    chosenmap : str = ""
    profile : str
    current_profile_dir : str = ""
    config_path :str = ""
    guild_save_path : str

    def showplayers(self) -> list:
        return self.players
    

    ## update will: UPDATE the profile.
    def update(self):
        absolute_path = os.path.abspath(__file__)
        self.read_config()
        self.profile = self.config[self.discordserver.name]
        self.current_profile_dir = os.path.join(os.path.dirname(absolute_path), f"../data/spy_fall/{self.discordserver}/{self.profile[0]}.json")

    #Todo PROFILE MANIPULATION
    
    def changeprofile(self, name : str) -> bool:
        self.update()
        self.config[self.discordserver.name] = [name]
        self.write_config()
        self.read_profile()
        print(self.profile)
        return True
    
    def newprofile(self, name : str) -> bool:
        try:
            absolute_path = os.path.abspath(__file__)
            self.guild_save_path = os.path.join(os.path.dirname(absolute_path), f"../data/spy_fall/{self.discordserver}/{name}.json")
            with open(self.guild_save_path, "w") as json_file:
                json_file.write(json.dumps(self.default, indent=4))
            return True
        except:
            return False
    
    def deleteprofile(self, name : str) -> bool:
        if self.config[self.discordserver.name] == [name]:
            return False
        
        if not self.config[self.discordserver.name] == [name]:
            absolute_path = os.path.abspath(__file__)
            removethis = os.path.join(os.path.dirname(absolute_path), f"../data/spy_fall/{self.discordserver}/{name}.json")
            try:
                os.remove(removethis)
                return True
            except:
                return False
    
    def showprofile(self) -> list:
        temp = os.listdir(self.guild_save_path)
        profile_list : list = []
        for i in temp:
            profile_list.append(i.split(".")[0])
        return profile_list
    
    #READ AND WRITE DATA

    def read_config(self):
        with open(self.config_path, "r") as json_file:
            self.config = json.load(json_file)
        return
    
    def write_config(self):
        with open(self.config_path, "w") as json_file:
                json_file.write(json.dumps(self.config, indent=4))
        return
    
    def read_profile(self):
        self.update()
        with open(self.current_profile_dir, "r") as json_file:
            self.currentgamemap = json.load(json_file)

    def write_profile(self):
        self.update()
        with open(self.current_profile_dir, "w") as json_file:
                json_file.write(json.dumps(self.currentgamemap, indent=4))

    def addmap(self, mapname,  map : list):
        newmap = { mapname : map}
        self.currentgamemap.update(newmap)
        self.write_profile()
        return

    def addplayer(self, userName) -> bool:
        for i in self.players:
            if(i == userName):
                print("Spyfall class: Player already in game.")
                return False
            
        self.players.append(userName)
        print(f"Spyfall class: {userName} is successfully added.")
        return True

    def removemap(self, map):
        mapname = self.currentgamemap.pop(map)
        self.write_profile()
        return mapname

    def maps(self):
        return self.currentgamemap
    
    def debug(self):
        return "debug func called properly."
    
    #GAME START METHODS

    def start(self):
        templist = []
        for keya in self.currentgamemap:
            templist.append(keya)
        self.chosenmap = templist[random.randint(0, len(templist)-1)]
        numberofplayers = len(self.players)
        self.spy = random.randint(0, numberofplayers-1)
        print(f"map is {self.currentgamemap[self.chosenmap]} and the spy is {self.players[self.spy]}")
        return self.players[random.randint(0, numberofplayers-1)]

    def getrole(self, ID):
        if ID == self.players[self.spy]:
            return "spy"
        else:
            roles = self.currentgamemap[self.chosenmap]
            return roles[random.randint(0, len(roles)-2)]
        
    def getmap(self, role):
        if role=="spy":
            return "unknown"
        else:
            return self.chosenmap
        
    def clearplayers(self):
        self.players.clear()
        return
    
    def removeplayer(self, user):
        if user in self.players:
            self.players.remove(user)
            return True
        return False
    
    def __init__(self, game_host, discordserver):
        
        self.game_host = game_host
        self.players = []
        self.discordserver = discordserver

        self.players.append(game_host)

        absolute_path = os.path.abspath(__file__)
        self.config_path = os.path.join(os.path.dirname(absolute_path), f"../data/spy_fall/config.json")
        self.read_config()
        try:
            self.profile = self.config[discordserver.name]
        except:
            self.newprofile("default")
            self.config[discordserver.name] = ['default']
            self.write_config()
            self.profile = self.config[discordserver.name]
        self.guild_save_path = os.path.join(os.path.dirname(absolute_path), f"../data/spy_fall/{self.discordserver}")

        if not os.path.exists(self.guild_save_path):
            tempath = os.path.join(os.path.dirname(absolute_path), f"../data/spy_fall")
            os.chdir(tempath)
            os.mkdir(self.discordserver.name)

        self.current_profile_dir = os.path.join(os.path.dirname(absolute_path), f"../data/spy_fall/{self.discordserver}/{self.profile[0]}.json")

        if not os.path.exists(self.current_profile_dir):
            with open(self.current_profile_dir, "w") as json_file:
                self.currentgamemap = self.default
                json_file.write(json.dumps(self.currentgamemap, indent=4))

        if os.path.exists(self.current_profile_dir):
            with open(self.current_profile_dir, "r") as json_file:
                self.currentgamemap = json.load(json_file)


    def __del__(self):
        return "The game of spyfall has been destroyed."