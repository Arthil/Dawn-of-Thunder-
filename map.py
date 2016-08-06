'''
Created on 27.4.2015

@author: christian
'''

from square import Square
import math

class Map():
    
    def __init__(self,mapSizeX,mapSizeY,generationSequence):
        
        ''' Creating maximum coordinates for the map generation'''
        
        self.mapSizeX = mapSizeX
        self.mapSizeY = mapSizeY
        self.construct_map(generationSequence)
        
        
    def construct_map(self,generationSequence):
        ''' First we construct a 2 dimentional matrix and fill it with zeros'''
        
        self.map = [[0 for x in range(self.mapSizeY)] for x in range(self.mapSizeX)] 
        
       
        
        
        ''' Then according to the generation sequence we start adding different types of tiles, and we construct squares for each index of the map'''
        
        for j in range(self.mapSizeY):
            for i in range(self.mapSizeX):
                if generationSequence[i][j] == 0:
                    name = "land1.png"
                    moveable = True
                    buildable = "land"
                elif generationSequence[i][j] == 1:
                    name = "land2.png"
                    moveable = True
                    buildable = "land"
                elif generationSequence[i][j] == 2:
                    name = "land3.png"
                    moveable = True
                    buildable = "land"
                elif generationSequence[i][j] == 3:
                    name = "land4.png"
                    moveable = True
                    buildable = "land"
                elif generationSequence[i][j] == 4:
                    name = "land1.png"
                    moveable = True
                    buildable = "land"
                elif generationSequence[i][j] == 5:
                    name = "forest1.png"
                    moveable = True
                    buildable = "forest"
                elif generationSequence[i][j] == 6:
                    name = "mountains1.png"
                    moveable = False
                    buildable = "mountains"
                elif generationSequence[i][j] == 7:
                    name = "forest1.png"
                    moveable = True
                    buildable = "forest"
                else:
                    name = "waterland5.png"
                    moveable = False
                    buildable = "water"
                
                self.map[i][j] = Square(i,j,name,moveable,buildable)

        #print(self.map) 
        
    def modify_map(self,coordinateX, coordinateY, value):
        self.map[coordinateX][coordinateY] = value
        #print("({:d},{:d}) = {:d}".format(coordinateX,coordinateY,value))
        
    def get_map(self):
        return self.map
    
    def get_map_size(self):
        return (self.mapSizeX,self.mapSizeY)
    
    def get_square(self,x,y):
        return self.map[x][y]
        
    def get_distance_between_coordinates(self,coordinates1,coordinates2):
        return math.sqrt((coordinates2[0]-coordinates1[0])**2 + (coordinates2[1]-coordinates1[1])**2)
        
'''      
def main():
    
    map = Map(4,4,[0,1,1,1,1,1,0,0,0,1,1,0,0,0,1,0])  
    print(map.get_map())
    
            
    
    
main()
'''