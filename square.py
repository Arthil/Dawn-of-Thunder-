'''
Created on 27.4.2015

@author: christian
'''


class Square():
    
    def __init__(self, coordinateX,coordinateY,name,moveable,buildable):
        
        self.set_square_coordinates(coordinateX,coordinateY)
        self.set_square_image(name)
        self.canBuild = buildable
        self.canMove = moveable
        self.hasBuilding = False
        self.building = None
        self.hasTroop = False
        self.troop = None
        
        
    def set_square_graphical_representation(self, graphicalRepresentation):
        self.graphicalRepresentation = graphicalRepresentation
    
    def get_square_graphical_representation(self):
        return self.graphicalRepresentation
    
    def set_square_coordinates(self,coordinateX,coordinateY):
        self.coordinates = [coordinateX,coordinateY]
    
    def get_square_coordinates(self):
        return self.coordinates
    
    def set_square_image(self,name):
        self.square_image = name
        
    def get_square(self):
        return self
    
    def get_square_image(self):
        return self.square_image
    
    def check_if_has_building(self):
        return self.hasBuilding
    
    def add_building(self,building):
        if self.hasBuilding == True:
            print("This tile already has a building")
        else:
            self.building = building
            self.hasBuilding = True
    
    def destroy_square_building(self):
        if self.hasBuilding == True:
            self.building = None
            self.hasBuilding = False
            
        else:
            print("This tile doesn't have a building")
    
    def add_troop(self,troop):
        if self.hasTroop == False:
            self.hasTroop = True
            self.troop = troop
        else:
            print("Already has a troop in this tile")
            
    def remove_troop(self):
        if self.hasTroop == True:
            self.hasTroop = False
            self.troop = None
        else:
            print("Square does not have a troop in it")
            
    def get_troop(self):
        return self.troop
    
    def get_building(self):
        if self.hasBuilding == True:
            return self.building
        else:
            print("This tile doesn't have a building")
            
    def check_if_has_troop(self):
        return self.hasTroop
    
    def check_if_empty(self):
        if self.hasBuilding == False and self.hasTroop == False:
            return True
        else:
            return False
    
    def get_buildable_type(self):
        return self.canBuild
    
    def get_moveable_type(self):
        return self.canMove
    