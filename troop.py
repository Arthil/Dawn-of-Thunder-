'''
Created on 16.5.2015

@author: christian
'''

import sqlite3
from extendedqlabel import ExtendedQLabel

class Troop():
    
    def __init__(self,troopID,owner,coordinates):
        
        self.troopID = troopID
        self.owner = owner
        
        
        self.troopName = ""
        self.troopImage = ""
        self.troopEra = ""
        self.troopType = ""
        self.troopCost = [0,0,0,0]
        self.troopGain = [0,0,0,0]
        self.sciencePointGain = 0
        self.buildTime = 0
        self.troopHP = 100
        self.tileType = ""
        
        self.coordinates = coordinates
        self.graphicalRepresentation = ExtendedQLabel(None,None,"Temporary")
        
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Troops WHERE troopID = " + str(self.troopID))
        
        while True:
            rows = cursor.fetchone()
            if rows == None:
                break
            else:
                for i in range(17):
                    rows = str(rows)
                    row = rows.split(",")
                    row[i] = str(row[i])
                    
        for i in range(17):
            row[i] = row[i].strip("(")
            row[i] = row[i].strip(")")
            row[i] = row[i].strip(",")
            row[i] = row[i].strip(" ")
            row[i] = row[i].strip("'")
            #print(row[i])
            
        
        conn.close()
        
        self.troopName = row[0]
        self.troopImage = row[2]
        self.troopEra = row[3]
        self.troopType = row[4]
        self.troopCost = [int(row[5]), int(row[6]), int(row[7]), int(row[8])]
        self.foodConsuption = int(row[9])
        self.attackPower = int(row[10])
        self.defenceStats = [int(row[11]),int(row[12])]
        self.range = int(row[13])
        self.movement = [int(row[14]), row[15]]
        self.buildTime = int(row[16])

        
    def get_troop_name(self):
        return self.troopName
    
    def set_troop_graphical_representation(self, graphicalRepresentation):
        self.graphicalRepresentation = graphicalRepresentation
    
    def get_troop_graphical_representation(self):
        return self.graphicalRepresentation
    
    def get_troop_owner(self):
        return self.owner
    
    def get_troop_range(self):
        return self.range
    
    def get_troop_movement(self):
        return self.movement
    
    def get_troop_build_time(self):
        return self.buildTime
    
    def get_troop_cost(self):
        return self.troopCost
    
    def get_troop_image(self):
        return self.troopImage
    
    def get_troop_type(self):
        return self.troopType
    
    def get_troop_hp(self):
        return self.troopHP
    
    def get_troop_coordinates(self):
        return self.coordinates
    
    def set_troop_coordinates(self,coordinates):
        self.coordinates = coordinates
    
    def get_troop_id(self):
        return self.troopID
    
    def get_troop_attack_power(self):
        return self.attackPower
    
    def get_troop_defence(self):
        return self.defenceStats

    def get_troop_food_consumption(self):
        return self.foodConsuption

    def damage(self,amount):
        self.troopHP -= amount