'''
Created on 28.4.2015

@author: christian
'''
from building import Building

class Player():
    
    def __init__(self,name,difficulty,startingEra):
        self.name = name 
        self.difficulty = difficulty
        self.initialize_resources()
        self.playerEra = startingEra
        self.sciencePoints = 0
        self.ownedBuildings = None
        self.sciencePointIncome = 0
    def initialize_resources(self):
        if self.difficulty == "EASY":
            self.gold = 1250
            self.wood = 750
            self.iron = 750
            self.food = 1000
        elif self.difficulty == "NORMAL":
            self.gold = 1000
            self.wood = 650
            self.iron = 650
            self.food = 800
        elif self.difficulty == "HARD":
            self.gold = 750
            self.wood = 500
            self.iron = 500
            self.food = 600
        else:
            print("Invalid value for difficulty")
            
        self.goldIncome = 20
        self.woodIncome = 15
        self.ironIncome = 15
        self.foodIncome = 15
        
    def set_player_era(self,era):
        self.playerEra = era
        
    def get_player_era(self):
        return self.playerEra
        
    def get_player(self):
        return self
    
    def get_player_name(self):
        return self.name
    
    def increase_player_resources(self,resources):
        self.gold += resources[0]
        self.wood += resources[1]
        self.iron += resources[2]
        self.food += resources[3]
    
    def decrease_player_resources(self,resources):
        self.gold -= resources[0]
        self.wood -= resources[1]
        self.iron -= resources[2]
        self.food -= resources[3]
    
    def get_player_resources(self):
        
        ''' 
        Index 0 = gold
        Index 1 = wood
        Index 2 = iron
        Index 3 = food
        '''
        
        return [self.gold, self.wood, self.iron, self.food] 
    
    def increase_player_science_points(self,increasedAmount):
        self.sciencePoints += increasedAmount
    
    def decrease_player_science_points(self,increasedAmount):
        self.sciencePoints -= increasedAmount
    
    def get_player_science_points(self):
        return self.sciencePoints
    
    def get_player_science_point_income(self):
        return self.sciencePointIncome
        
    def increase_player_science_point_income(self,amount):
        self.sciencePointIncome += amount
    
    def decrease_player_science_point_income(self,amount):
        self.sciencePointIncome -= amount
    
    def get_player_buildings(self):
        return self.ownedBuildings
    
    def add_player_building(self,building):
        self.ownedBuildings.append(building)
        
    def increase_player_income(self,income):
        self.goldIncome += income[0]
        self.woodIncome += income[1]
        self.ironIncome += income[2]
        self.foodIncome += income[3]
    
    def decrease_player_income(self,income):
        self.goldIncome -= income[0]
        self.woodIncome -= income[1]
        self.ironIncome -= income[2]
        self.foodIncome -= income[3]
        
    def get_player_income(self):
        return [self.goldIncome, self.woodIncome, self.ironIncome, self.foodIncome]
        
        
        
        
    