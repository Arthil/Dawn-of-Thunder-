'''
Created on 30.4.2015

@author: christian
'''

import sqlite3

class Building():
    
    def __init__(self,buildingID,owner,coordinates):
        
        self.buildingID = buildingID
        self.owner = owner
        
        
        self.buildingName = ""
        self.buildingImage = ""
        self.buildingEra = ""
        self.buildingType = ""
        self.buildingCost = [0,0,0,0]
        self.buildingGain = [0,0,0,0]
        self.sciencePointGain = 0
        self.buildTime = 0
        self.buildingHP = 100
        self.buildingDefence = 0
        self.tileType = ""
        
        self.coordinates = coordinates
        
        
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Buildings WHERE buildingID = " + str(self.buildingID))
        
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
        
        self.buildingName = row[0]
        self.buildingImage = row[2]
        self.buildingEra = row[3]
        self.buildingType = row[4]
        self.buildingCost = [int(row[5]), int(row[6]), int(row[7]), int(row[8])]
        self.buildingGain = [int(row[9]), int(row[10]), int(row[11]), int(row[12])]
        self.sciencePointGain = int(row[13])
        self.buildTime = int(row[14])
        self.tileType = row[15]
        self.buildingDefence = int(row[16])
        
    def get_building_name(self):
        return self.buildingName
    
    def set_building_graphical_representation(self, graphicalRepresentation):
        self.graphicalRepresentation = graphicalRepresentation
    
    def get_building_graphical_representation(self):
        return self.graphicalRepresentation

    def get_building_owner(self):
        return self.owner
    
    def get_building_gain(self):
        return self.buildingGain
    
    def get_building_science_points(self):
        return self.sciencePointGain
    
    def get_building_build_time(self):
        return self.buildTime
    
    def get_building_cost(self):
        return self.buildingCost
    
    def get_building_image(self):
        return self.buildingImage
    
    def get_building_type(self):
        return self.buildingType
    
    def get_building_hp(self):
        return self.buildingHP
    
    def get_building_coordinates(self):
        return self.coordinates
    
    def get_building_id(self):
        return self.buildingID
    
    def get_tile_type(self):
        return self.tileType
    
    def get_building_defence(self):
        return self.buildingDefence
    
    def damage(self,amount):
        self.buildingHP -= amount