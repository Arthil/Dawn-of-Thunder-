'''
Created on 27.4.2015

@author: christian
'''

from random import randint

class Random_map_generator():
    
    def generate_sequence(self,dimensionX,dimensionY):
        
        ''' This generates a sequence of 0 and 8 with the given dimensions''' 
        self.dimensionX = dimensionX
        self.dimensionY = dimensionY
        self.mapGenerationSequence = [[randint(0,8) for x in range(dimensionY)] for x in range(dimensionX)] 
        return self.mapGenerationSequence



    def get_random_coordinates(self):
        return [randint(0,(self.dimensionX-1)), randint(0,(self.dimensionY-1))]
    



    
'''
    ---more advanced map generation algorithm but it was never finished---
    
    def generate_advanced_random_map(self,dimensionX,dimensionY):
        self.dimensionX = dimensionX
        self.dimensionY = dimensionY
        self.mapSequence = [[ 0 for x in range(dimensionY)] for x in range(dimensionX)]     #first create an empty map
        
        self.mapSequence[0][0] = randint(0,19)
        
        for j in range(dimensionX):
            for i in range(dimensionY):
                if i == 0 and j == 0:
                    pass
                else:
                    pass
    
        
        tile = [0 for x in range(20)] 
        
        tile[0] = ["water1.png", ["water1.png","waterland1.png", "waterland9.png","waterland8.png"], ["water1.png","waterland8.png"],["water1.png","waterland2.png","waterland10.png","waterland8.png"],
                                 ["water1.png","waterland9.png"], ["water1.png","waterland10.png"],
                                 ["water1.png","waterland9.png", "waterland6.png","waterland11.png"], ["water1.png","waterland8.png"],["water1.png","waterland10.png","waterland7.png","waterland11.png"]]
        
        tile[1] = ["land1.png",  ["land1.png","waterland4.png", "waterland3.png","waterland6.png","waterland7.png","waterland11.png","waterland10.png","waterland6.png"], ["land1.png","waterland4.png","waterland3.png","waterland5.png","waterland6.png","waterland7.png","waterland11.png"],["land1.png",],
                                 ["land1.png","waterland9.png"], ["land1.png","waterland10.png"],
                                 ["land1.png","waterland9.png", "waterland6.png","waterland11.png"], ["land1.png","waterland8.png"],["land1.png","waterland10.png","waterland7.png","waterland11.png"]]
        
        tile[0] = ["water1.png",]
        tile[1] = ["land1.png",]
        tile[2] = ["waterland5.png",]
'''       
        
