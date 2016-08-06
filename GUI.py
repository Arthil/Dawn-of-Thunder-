'''
Created on 23.4.2015

@author: christian
'''
import sys
import sqlite3
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import *
from PyQt4.QtCore import *

from functools import partial

from map import Map
from random_map_generator import Random_map_generator
from player import Player 
from building import Building
from extendedqlabel import ExtendedQLabel
from troop import Troop
from computer import Computer
nScreen_x = 1440
nScreen_y = 900




class Example(QtGui.QWidget):
    
    def __init__(self,*args):
        super(Example, self).__init__()
        
        self.initDatabase()
        self.initUI()
        self.actionBarItems = []
        self.actionBarItemNames = []
        self.selectedSquare = None
        self.clicked_tile = None
        self.playing = self.player
        self.allBuildings = [Building("1",None,None),Building("2",None,None),Building("3",None,None),Building("4",None,None),Building("5",None,None),Building("6",None,None),Building("7",None,None)]
        self.allTroops = [Troop("1",None,None),Troop("2",None,None),Troop("3",None,None),Troop("4",None,None),Troop("5",None,None)]
        self.availableBuildings = []
        self.availableTroops = []
        self.inventoryPlus = 0
        self.moving = False
        self.attacking = False
        self.buildQueue = []
        self.troopQueue = []
        
        
   
    def initDatabase(self):
        
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        #cursor.execute("drop table if exists Buildings")
        #conn.commit()
        cursor.execute("""create table if not exists Buildings (
                        name TEXT,
                        buildingID INT,
                        imageName TEXT,
                        era TEXT,
                        type TEXT,
                        goldCost INT,
                        woodCost INT,
                        ironCost INT,
                        foodCost INT,
                        goldGain INT, 
                        woodGain INT,
                        ironGain INT,
                        foodGain INT,
                        sciencePointGain INT,
                        buildTime INT,
                        tileType TEXT,
                        buildingDefence INT
                        )""")
        conn.commit()
        
        cursor.execute("""INSERT INTO Buildings
                        VALUES('Barracks', 1, 'barracks1.png', 'ANCIENT ERA', 'Military', 225, 300, 285, 125, -3,0,0,-2,3,3,'land', 35)""")
        cursor.execute("""INSERT INTO Buildings
                        VALUES('Market', 2, 'market1.png', 'ANCIENT ERA', 'Economy', 300, 200, 150, 125, 10,0,0,-1,2,2,'land', 20)""")
        cursor.execute("""INSERT INTO Buildings
                        VALUES('Capital', 3, 'capital1.png', 'ANCIENT ERA', 'Economy', 550, 440, 450, 200, 10,5,5,5,5,4,'land', 40 )""")
        cursor.execute("""INSERT INTO Buildings
                        VALUES('Capital Building', 4, 'capital_building1.png', 'ANCIENT ERA', 'Economy', 800, 600, 555, 325, 20,10,10,10,10,6,'land', 50)""")
        cursor.execute("""INSERT INTO Buildings
                        VALUES('Lumbermill', 5, 'lumbermill1.png', 'ANCIENT ERA', 'Resources', 250, 300, 225, 115, 5,35,0,-1,1,2,'forest', 20)""")
        cursor.execute("""INSERT INTO Buildings
                        VALUES('Farm', 6, 'farm1.png', 'ANCIENT ERA', 'Resources', 200, 225, 120, 50, 5,0,0,50,1,1,'land',15)""")
        cursor.execute("""INSERT INTO Buildings
                        VALUES('Mines', 7, 'mines.png', 'ANCIENT ERA', 'Resources', 325, 400, 350, 200, 20,0,50,-1,2,3,'mountains',25)""")
        conn.commit()
        
        #cursor.execute("drop table if exists Troops")
        #conn.commit()
        cursor.execute("""create table if not exists Troops (
                        name TEXT,
                        troopID INT,
                        imageName TEXT,
                        era TEXT,
                        type TEXT,
                        goldCost INT,
                        woodCost INT,
                        ironCost INT,
                        foodCost INT,
                        foodConsumption INT,
                        attackPower INT,
                        defenceMelee INT,
                        defenceRanged INT,
                        range INT,
                        movementAmount INT,
                        movementType TEXT,
                        buildTime INT
                        )""")
        conn.commit()
        
        cursor.execute("""INSERT INTO Troops
                        VALUES('Archer', 1, 'archer1.png', 'ANCIENT ERA', 'ranged', 125, 100, 75, 50, -1, 10, 5, 10, 2 , 2 , 'light', 2)""")
        cursor.execute("""INSERT INTO Troops
                        VALUES('Swordman', 2, 'swordman1.png', 'ANCIENT ERA', 'melee', 100, 75, 150, 40, -1, 12, 12, 10, 1 , 1 , 'heavy', 2)""")
        cursor.execute("""INSERT INTO Troops
                        VALUES('Pikeman', 3, 'pikeman1.png', 'ANCIENT ERA', 'melee', 175, 125, 125, 70, -2, 15, 25, 5, 1 , 1, 'light', 2)""")
        cursor.execute("""INSERT INTO Troops
                        VALUES('Knight', 4, 'knight1.png', 'ANCIENT ERA', 'melee', 225, 175, 200, 120, -3, 25, 25, 20, 1 , 4 , 'heavy', 4)""")
        cursor.execute("""INSERT INTO Troops
                        VALUES('Catapult', 5, 'catapult1.png', 'ANCIENT ERA', 'ranged', 300, 300, 250, 50, -4, 30, 5, 20, 3 , 1 , 'heavy', 4)""")
        conn.commit()
        conn.close()
      
 
    def initUI(self):
        
        ''' Setting up the window '''     
        
        self.gameVersion = "Dawn of Thunder Alpha V.0.03"
        
        self.setWindowTitle(self.gameVersion)
        self.setWindowIcon(QtGui.QIcon('dawnofthundericon.png'))
        self.setWindowOpacity(1)
        #self.setWindowFlags(QtCore.Qt.FramelessWindowHint)  #Remove Windowframe
        self.setMinimumSize(1440, 900)
        self.setMaximumSize(1440, 900)
        self.setGeometry(50, 50, 1440, 900) 
        self.backgroundMetal = QtGui.QLabel(self)
        self.backgroundMetal.setPixmap(QtGui.QPixmap("picturewarfare.png"))
        self.backgroundMetal.move(0,20)
        
        randomGenerator = Random_map_generator()
        ''' Create map ''' 
        self.map = Map(15,15,randomGenerator.generate_sequence(15,15))
        
        ''' Draw Palets '''
        self.draw_palets()
        
        
        ''' Draw the map '''
        self.xIncrement = 0
        self.yIncrement = 0
        self.selection = None
        self.draw_map()
        
        
        ''' Create player'''
        self.player = Player("Arthil","EASY","ANCIENT ERA")
        
        
        '''Add player capital building'''
        mapSize = self.map.get_map_size()
        coordinates = randomGenerator.get_random_coordinates()
        square = self.map.get_square(coordinates[0],coordinates[1])
        type = square.get_buildable_type()
        while type != "land":
            coordinates = randomGenerator.get_random_coordinates()
            square = self.map.get_square(coordinates[0],coordinates[1])
            type = square.get_buildable_type()
        square.add_building(Building("4", self.player, (coordinates[0],coordinates[1])))
        square.get_building().set_building_graphical_representation(ExtendedQLabel(self,square.get_building().get_building_image(), square))
        building = square.get_building().get_building_graphical_representation()
        building.setPixmap(QPixmap(square.get_building().get_building_image()))
        self.connect(building, SIGNAL('clicked()'), self.building_options)
        
        if coordinates[0] > 4 and coordinates[0]+5 < mapSize[0]:
            self.xIncrement = coordinates[0]-4
        elif coordinates[0] > 4:
            self.xIncrement = mapSize[0]-8
        if coordinates[1] > 2 and coordinates[1]+3 < mapSize[1]:
            self.yIncrement = coordinates[1]-2
        elif coordinates[1] > 2:
            self.yIncrement = mapSize[1]-5
            
       
        
        
        ''' Create computer'''
        self.computer = Computer("George Washington", "EASY", "ANCIENT ERA")
        
        
        ''' Add computer capital'''
        self.playerCapitalCoordinates = coordinates
        self.comp_moves = 3
        self.comp_attacks = 3
        coordinates = randomGenerator.get_random_coordinates()
        square = self.map.get_square(coordinates[0],coordinates[1])
        type = square.get_buildable_type()
        while type != "land" or self.map.get_distance_between_coordinates(coordinates, self.playerCapitalCoordinates) < 7:
            coordinates = randomGenerator.get_random_coordinates()
            square = self.map.get_square(coordinates[0],coordinates[1])
            type = square.get_buildable_type()
        square.add_building(Building("4", self.computer, (coordinates[0],coordinates[1])))
        square.get_building().set_building_graphical_representation(ExtendedQLabel(self,square.get_building().get_building_image(), square))
        building = square.get_building().get_building_graphical_representation()
        building.setPixmap(QPixmap(square.get_building().get_building_image()))
        self.connect(building, SIGNAL('clicked()'), self.building_options)    
        
        self.update_map()
        
        ''' Display Era on top of the window'''
        
        self.eraText = QtGui.QLabel(self)
        font = QtGui.QFont('Decorative', 18)
        font.setItalic(True)
        self.eraText.setFont(font)
        self.eraText.move(635, 60)
        self.eraText.setText(self.player.get_player_era())
        self.eraText.adjustSize()
   
        
        ''' Display player resources'''
        playerStats = self.player.get_player_resources()  # Gets players resources in a list of 4    Index 0 = Gold | Index 1 = Wood | Index 2 = Iron | Index 3 = Food
        self.resourcesText = QtGui.QLabel(self)
        self.fontResources = QtGui.QFont("Decorative",16)
        self.fontResources.setItalic(True)
        self.resourcesText.setFont(self.fontResources)
        self.resourcesText.move(50,200)
        self.round = 1
        self.resourcesText.setText("\nRound " + str(self.round) + "\n\nGold: " + str(playerStats[0]) + "\nWood: " + str(playerStats[1]) + "\nIron: " + str(playerStats[2]) + "\nFood: " + str(playerStats[3]) + "\n\n\nScience: " + str(self.player.get_player_science_points()))
        self.resourcesText.show()
        
        
        ''' Display player income'''
        playerIncome = self.player.get_player_income()  # Gets players resources in a list of 4    Index 0 = Gold | Index 1 = Wood | Index 2 = Iron | Index 3 = Food
        self.incomeText = QtGui.QLabel(self)
        self.incomeText.setFont(self.fontResources)
        self.incomeText.move(1215,200)
        self.incomeText.setText("\nIncome per round:\n\nGold:\t" + str(playerIncome[0]) + "\nWood:\t" + str(playerIncome[1]) + "\nIron:\t" + str(playerIncome[2]) + "\nFood:\t" + str(playerIncome[3]) + "\n\n\nScience Gain: " + str(self.player.get_player_science_point_income()))
        
        '''Display move and attack counts left'''
        
        self.moves = 3
        self.attacks = 3
        self.moveCountText = QtGui.QLabel(self)
        self.moveCountText.setFont(self.fontResources)
        self.moveCountText.move(50,600)
        self.moveCountText.setText("Moves: " + str(self.moves) + "\nAttacks: " + str(self.attacks))
        self.moveCountText.show()
        
        self.show()    
    
    
    def draw_map(self):
        
        mapSize = self.map.get_map_size()
        x = mapSize[0]
        y = mapSize[1]
        
        ''' Draw the arrows that allows to navigate the map'''
        
        self.rightArrow = ExtendedQLabel(self,"right_arrow.png", None)
        self.rightArrow.setPixmap(QPixmap("right_arrow.png"))
        self.rightArrow.move(1130,375)
        self.rightArrow.show()
        self.connect(self.rightArrow, SIGNAL('clicked()'), self.right_arrow_map)
        
        self.leftArrow = ExtendedQLabel(self,"left_arrow.png", None)
        self.leftArrow.setPixmap(QPixmap("left_arrow.png"))
        self.leftArrow.move(260,375)
        self.leftArrow.show()
        self.connect(self.leftArrow, SIGNAL('clicked()'), self.left_arrow_map)
        
        self.upArrow = ExtendedQLabel(self,"up_arrow.png", None)
        self.upArrow.setPixmap(QPixmap("up_arrow.png"))
        self.upArrow.move(695,120)
        self.upArrow.show()
        self.connect(self.upArrow, SIGNAL('clicked()'), self.up_arrow_map)
        
        self.downArrow = ExtendedQLabel(self,"down_arrow.png", None)
        self.downArrow.setPixmap(QPixmap("down_arrow.png"))
        self.downArrow.move(695,670)
        self.downArrow.show()
        self.connect(self.downArrow, SIGNAL('clicked()'), self.down_arrow_map)
        
        ''' Draw the map tiles and their buttons'''
        
        self.mapTiles = [[0 for x in range(y)] for X in range(x)] 
        
        for j in range(y):
            for i in range(x):
                map = self.map.get_map()
                image = map[i][j].get_square_image()
                self.map.get_square(i,j).set_square_graphical_representation(ExtendedQLabel(self,image, self.map.get_square(i,j)))
                
                self.tile = self.map.get_square(i,j).get_square_graphical_representation()
                self.tile.setPixmap(QPixmap(image))
                self.mapTiles[i][j] = self.tile
                self.connect(self.tile, SIGNAL('clicked()'), self.land_options)
        self.update_map()     
        
        self.map
        

    def draw_palets(self):     
        
        ''' Draw the palets to the screen'''
           
        self.leftPalet = QtGui.QLabel(self)
        self.leftPalet.setPixmap(QtGui.QPixmap("metalboards.png"))
        self.leftPalet.move(5,150)
        self.rightPalet = QtGui.QLabel(self)
        self.rightPalet.setPixmap(QtGui.QPixmap("metalboards.png"))
        self.rightPalet.move(1185,150)
        
        self.bottomPalet = QtGui.QLabel(self)
        self.bottomPalet.setPixmap(QtGui.QPixmap("actionbar.png"))
        self.bottomPalet.move(270,680)
        
        ''' Draw the upper spears and the era '''
        
        self.upperSpear1 = QtGui.QLabel(self)
        self.upperSpear1.setPixmap(QtGui.QPixmap("spearleft.png"))
        self.upperSpear1.move(70,22)
        self.upperSpear2 = QtGui.QLabel(self)
        self.upperSpear2.setPixmap(QtGui.QPixmap("spearright.png"))
        self.upperSpear2.move(850,25)
        self.eraBorder = QtGui.QLabel(self)
        self.eraBorder.setPixmap(QtGui.QPixmap("ageborder.png"))
        self.eraBorder.move(590,25)
        
        ''' Next round button'''
        
        self.nextRound = ExtendedQLabel(self,"nextRound.png",None)
        self.nextRound.setPixmap(QPixmap("nextRound.png"))
        self.nextRound.move(1200,800)
        self.connect(self.nextRound, SIGNAL('clicked()'), self.next_round)
        self.nextRound.show()
                
        
        
    def paintEvent(self, event):
        
        qp = QtGui.QPainter()
        qp.begin(self)

        self.drawUpperbar(qp)
        
        qp.end()
     
  
        
    def drawUpperbar(self,qp):
        
        ''' draw the gray upper bar'''
        pen = QtGui.QPen(QtCore.Qt.blue, 1, QtCore.Qt.SolidLine)
        qp.setPen(pen)
        
        for i in range(20):
            qp.setPen(QtGui.QColor(192-i*3,192-i*3,192-i*3))
            points = [QtCore.QPointF(0,i), QtCore.QPointF(1440,i)]
            qp.drawPolygon(points[0], points[1])

        
        qp.setPen(QtGui.QColor(0,0,0))
        qp.drawRect(0, 20, 1439, 879)

    def barracks_options(self, menus = False):
        
        ''' If player wants to move to this tile'''
        if self.moving == True:
            self.moving = False
            self.display_info("You can't move to a building.")
            return
        
        ''' If player wants to attack to this tile'''
        if self.attacking == True:
            
            self.attacking = False
            troop = self.clicked_troop.get_parent_square().get_troop()
            print(troop)
            coordinates = troop.get_troop_coordinates()
            
            ''' Check if all the conditions are good to attack'''
            attackRange = troop.get_troop_range()
            if self.sender().get_parent_square().check_if_empty() == False and self.map.get_distance_between_coordinates(coordinates,self.sender().get_parent_square().get_square_coordinates()) <= float(attackRange) and troop.get_troop_owner() != self.sender().get_parent_square().get_building().get_building_owner() :
                self.combat_building(self.clicked_troop.get_parent_square().get_troop(), self.sender().get_parent_square().get_building())
                return
            elif self.map.get_distance_between_coordinates(coordinates,self.sender().get_parent_square().get_square_coordinates()) > float(attackRange):
                self.display_info("The tile you are trying to attack to is out of your range.")
                return
            elif self.sender().get_parent_square().check_if_empty() == True:
                self.display_info("There is nothing to attack to.")
                return
            elif troop.get_troop_owner != self.sender().get_parent_square().get_building().get_building_owner():
                self.display_info("You can't attack your own building.")
                return
        
        
        self.destroy_actionbar_items()
        
        ''' Functionality so you can browse with the inventory with the arrows'''
        if menus == False:
            self.inventoryPlus = 0
            self.availableTroops = []
            self.clicked_building = self.sender()
            coordinates = self.clicked_building.get_parent_square().get_square_coordinates()
            self.selection.move((coordinates[0] - self.xIncrement)*100 + 320, (coordinates[1] - self.yIncrement)*100 + 170)
            self.selection.show()
            for i in range(len(self.allTroops)):
                self.availableTroops.append(self.allTroops[i])
        
        ''' Draw the delete button '''
        image = "deletecrossSmall.png"
        self.destroy_actionbar_items()
        print("Clicked building")
        self.tile1 = ExtendedQLabel(self,image,None)
        self.tile1.setPixmap(QPixmap(image))
        self.tile1.move(1060,840)
        self.tile1.show()
        self.actionBarItems.append(self.tile1)

        self.actionBarItemNames.append(QLabel())
        
        self.connect(self.tile1, SIGNAL('clicked()'), self.destroy_building)
        
        ''' Display barracks info'''
        self.actionBarItems.append(QLabel())
        self.Text = QtGui.QLabel(self)
                            
        self.Text.setFont(self.fontResources)
        self.Text.move(370,700)
        self.Text.setText("Barracks\t\tHP: " + str(self.clicked_building.get_parent_square().get_building().get_building_hp()) + "\t\tDefence: " + str(self.clicked_building.get_parent_square().get_building().get_building_defence()))
        self.Text.show()
        self.actionBarItemNames.append(self.Text)       
        
        self.actionBarItems.append(QLabel())
        self.Text = QtGui.QLabel(self)                   
        self.Text.setFont(self.fontResources)
        self.Text.move(330,860)
        self.Text.setText("Owner: " + str(self.clicked_building.get_parent_square().get_building().get_building_owner().get_player_name()))
        self.Text.show()
        self.actionBarItemNames.append(self.Text)
        
        ''' Display all the troops you can train'''  
        if len(self.availableTroops) > 0:
            if len(self.availableTroops) < 4:
                amount = len(self.availableTroops)
            else:
                amount = 4
            for i in range(amount):
                ''' Draw the navigation arrows in the inventory'''
                if (len(self.availableTroops) - self.inventoryPlus) > 4:
                    self.tile = ExtendedQLabel(self,"right_arrow.png", None)
                    self.tile.setPixmap(QPixmap("right_arrow.png"))
                    self.tile.move(1100,740)
                    self.tile.show()
                    self.actionBarItems.append(self.tile)
                    self.actionBarItemNames.append(self.tile)
                    self.connect(self.tile, SIGNAL('clicked()'), self.right_arrow_troop_menu)
                if self.inventoryPlus > 0:
                    self.tile = ExtendedQLabel(self,"left_arrow.png", None)
                    self.tile.setPixmap(QPixmap("left_arrow.png"))
                    self.tile.move(290,740)
                    self.tile.show()
                    self.actionBarItems.append(self.tile)
                    self.actionBarItemNames.append(self.tile)
                    self.connect(self.tile, SIGNAL('clicked()'), self.left_arrow_troop_menu)
                
                ''' then draw the troops you can train '''
                image = self.availableTroops[i+self.inventoryPlus].get_troop_image()
                self.tile = ExtendedQLabel(self,image, self.availableTroops[i+self.inventoryPlus].get_troop_id())
                self.tile.setPixmap(QPixmap(image))
                self.tile.move(400 + i*170,730)
                self.tile.show()
                self.actionBarItems.append(self.tile)
                
                self.Text = QtGui.QLabel(self)
                
                self.Text.setFont(self.fontResources)
                self.Text.move(410 + i*170,830)
                self.Text.setText(self.availableTroops[i+self.inventoryPlus].get_troop_name())
                self.Text.show()
                self.actionBarItemNames.append(self.Text)
                self.connect(self.tile, SIGNAL('clicked()'), self.add_troop_to_queue)
        
    
    
    def add_building_to_queue(self):
        
        ''' Check that the tile is empty and that the player has resources'''
        if self.clicked_tile.get_parent_square().check_if_has_building() == False:
            self.clicked_building = self.sender()
            buildingID = self.clicked_building.get_parent_square()  # to find which building is to be built
            
            coordinates = self.clicked_tile.get_parent_square().get_square_coordinates()
            i = coordinates[0]
            j = coordinates[1]
            self.building = Building(buildingID, self.playing, (i,j))
            cost = self.building.get_building_cost()
            if self.has_resources(cost) == True:
                ''' Reduce the cost from players resources and add the building to queue'''
                self.playing.decrease_player_resources(cost)
                self.buildQueue.append([self.building,self.building.get_building_build_time()])
                
                ''' Set a temporary picture for the building while it's under construction'''
                self.clicked_tile.get_parent_square().add_building(self.building)
                image = "under_construction.png"
                self.clicked_tile.get_parent_square().get_building().set_building_graphical_representation(ExtendedQLabel(self,image,self.clicked_tile.get_parent_square()))
                self.tile = self.clicked_tile.get_parent_square().get_building().get_building_graphical_representation()
                self.tile.setPixmap(QPixmap(image))
                self.connect(self.tile, SIGNAL('clicked()'), self.building_construction_time)
                self.update_texts()
                self.update_map()
                
    def building_construction_time(self):
        ''' Displays the time left until the building is ready'''
        building = self.sender().get_parent_square().get_building()
        
        self.sender()
        coordinates = self.sender().get_parent_square().get_square_coordinates()
        self.selection.move((coordinates[0] - self.xIncrement)*100 + 320, (coordinates[1] - self.yIncrement)*100 + 170)
        self.selection.show()
        
        for i in range(len(self.buildQueue)):
            if building == self.buildQueue[i][0]:
                time = self.buildQueue[i][1]
        self.display_info("Constructing building...\nRemaining rounds: " + str(time))
    
    def construct_building(self,building):
        ''' Constructs the building to the tile and changes the under constrcution image to the real image'''
        self.playing.increase_player_income(building.get_building_gain())
        self.playing.increase_player_science_point_income(building.get_building_science_points())
        building.get_building_graphical_representation().set_new_image(building.get_building_image())
        building.get_building_graphical_representation().setPixmap(QPixmap(building.get_building_image()))
            
        self.disconnect(building.get_building_graphical_representation(), SIGNAL('clicked()'), self.building_construction_time)
        if building.get_building_id() == "1":
            self.connect(building.get_building_graphical_representation(), SIGNAL('clicked()'), self.barracks_options)
        else:
            self.connect(building.get_building_graphical_representation(), SIGNAL('clicked()'), self.building_options)
        self.update_texts()
        self.update_map()
     
    def display_info(self,text,coordinates = [560,830]):
        ''' This method is used to display info in the inventory'''
        self.destroy_actionbar_items()
        self.actionBarItems.append(QLabel())
        self.Text = QtGui.QLabel(self)
                            
        self.Text.setFont(self.fontResources)
        self.Text.move(coordinates[0],coordinates[1])
        self.Text.setText(text)
        self.Text.show()
        self.actionBarItemNames.append(self.Text)       
           
    def add_troop_to_queue(self):
        ''' Check that the tile is empty and that the player has resources'''
        self.destroy_actionbar_items()
        if self.clicked_building.get_parent_square().check_if_has_troop() == False:
            self.clicked_troop = self.sender()
            troopID = self.clicked_troop.get_parent_square()  # to find which building is to be built
            
            coordinates = self.clicked_building.get_parent_square().get_square_coordinates()
            i = coordinates[0]
            j = coordinates[1]
            self.troop = Troop(troopID, self.playing, (i,j))
            cost = self.troop.get_troop_cost()
            if self.has_resources(cost) == True:
                ''' Reduces the troop cost from players resources'''
                self.playing.decrease_player_resources(cost)
                self.troopQueue.append([self.troop,self.troop.get_troop_build_time()])
                
                    
                self.clicked_building.get_parent_square().add_troop(self.troop)
                self.disconnect(self.clicked_building, SIGNAL('clicked()'), self.barracks_options)
                self.connect(self.clicked_building, SIGNAL('clicked()'), self.troop_construction_time)
                self.update_texts()
            else:
                self.display_info("You don't have enough resources.")
        else:
            self.display_info("This tile is occupied.")      
            
    def troop_construction_time(self):
        ''' Displays the remaining time until the troop is ready'''
        troop = self.sender().get_parent_square().get_troop()
        
        coordinates = self.sender().get_parent_square().get_square_coordinates()
        self.selection.move((coordinates[0] - self.xIncrement)*100 + 320, (coordinates[1] - self.yIncrement)*100 + 170)
        self.selection.show()
        
        for i in range(len(self.troopQueue)):
            if troop == self.troopQueue[i][0]:
                time = self.troopQueue[i][1]
                self.display_info("Training " + str(troop.get_troop_name()) + "\nRemaining rounds: " + str(time))
        
    def construct_troop(self,troop):
        ''' Actually constructs the troop '''
        self.playing.increase_player_income([0,0,0,self.troop.get_troop_food_consumption()])
        image = troop.get_troop_image()
        coordinates = troop.get_troop_coordinates()
        
        troop.set_troop_graphical_representation(ExtendedQLabel(self,image, self.map.get_square(coordinates[0],coordinates[1])))
        troop.get_troop_graphical_representation().setPixmap(QPixmap(image))
        self.connect(troop.get_troop_graphical_representation(), SIGNAL('clicked()'), self.troop_options)
        self.connect(troop.get_troop_graphical_representation().get_parent_square().get_building().get_building_graphical_representation(), SIGNAL('clicked()'), self.barracks_options)
        self.update_texts()
        self.update_map()
    
    def troop_options(self):
        ''' Checks if the player wants to move to this tile'''
        if self.moving == True:
            self.moving = False
            self.display_info("There is already a troop in the selected square.")
            return
        
        ''' Checks if the player wants to move to these troops'''
        if self.attacking == True:
            
            self.attacking = False
            troop = self.clicked_troop.get_parent_square().get_troop()
            print(troop)
            coordinates = troop.get_troop_coordinates()
            ''' Checks if all the conditions are ok, for the attack'''
            attackRange = troop.get_troop_range()
            if self.sender().get_parent_square().check_if_empty() == False and self.map.get_distance_between_coordinates(coordinates,self.sender().get_parent_square().get_square_coordinates()) <= float(attackRange) and self.clicked_troop.get_parent_square().get_troop().get_troop_owner() != self.sender().get_parent_square().get_troop().get_troop_owner():
                '''attacks'''
                self.combat_troop(self.clicked_troop.get_parent_square().get_troop(), self.sender().get_parent_square().get_troop())
                return
            elif self.map.get_distance_between_coordinates(coordinates,self.sender().get_parent_square().get_square_coordinates()) > float(attackRange):
                self.display_info("The unit you are trying to attack is out of your range.")
                return
            elif self.sender().get_parent_square().check_if_empty() == True:
                self.display_info("There is nothing to attack to.")
                return
            elif self.clicked_troop.get_parent_square().get_troop().get_troop_owner() == self.sender().get_parent_square().get_troop().get_troop_owner():
                self.display_info("You can't attack your own troops")
                return
        
        
        
        
        self.clicked_troop = self.sender()
        print(self.clicked_troop)
        
        coordinates = self.clicked_troop.get_parent_square().get_square_coordinates()
        self.selection.move((coordinates[0] - self.xIncrement)*100 + 320, (coordinates[1] - self.yIncrement)*100 + 170)
        self.selection.show()
        
        ''' Draws the delete button'''
        image = "deletecrossSmall.png"
        self.destroy_actionbar_items()
        print("Clicked building")
        self.tile1 = ExtendedQLabel(self,image,None)
        self.tile1.setPixmap(QPixmap(image))
        self.tile1.move(1060,840)
        self.tile1.show()
        
        self.actionBarItems.append(self.tile1)
        self.actionBarItemNames.append(QLabel())
        self.connect(self.tile1, SIGNAL('clicked()'), self.destroy_troop)  
        
        '''draws the attack option button'''
        image = "attack.png"
        self.tile1 = ExtendedQLabel(self,image,None)
        self.tile1.setPixmap(QPixmap(image))
        self.tile1.move(400,730)
        self.tile1.show()
        self.actionBarItems.append(self.tile1)
        self.connect(self.tile1, SIGNAL('clicked()'), self.attack)
        
        self.Text = QtGui.QLabel(self)
                
        self.Text.setFont(self.fontResources)
        self.Text.move(410,830)
        self.Text.setText("Attack")
        self.Text.show()
        self.actionBarItemNames.append(self.Text)
        
        '''draws the move option button'''
        image = "moveArrow.png"
        self.tile1 = ExtendedQLabel(self,image,None)
        self.tile1.setPixmap(QPixmap(image))
        self.tile1.move(550,730)
        self.tile1.show()
        self.actionBarItems.append(self.tile1)
        self.connect(self.tile1, SIGNAL('clicked()'), self.move_troop)
        
        self.Text = QtGui.QLabel(self)
                
        self.Text.setFont(self.fontResources)
        self.Text.move(560,830)
        self.Text.setText("Move")
        self.Text.show()
        self.actionBarItemNames.append(self.Text)
        
        ''' Troop information display'''
        self.actionBarItems.append(QLabel())
        self.Text = QtGui.QLabel(self)                 
        self.Text.setFont(self.fontResources)
        self.Text.move(370,710)
        self.Text.setText(str(self.clicked_troop.get_parent_square().get_troop().get_troop_name()) + "\t\tHP: " + str(self.clicked_troop.get_parent_square().get_troop().get_troop_hp()) + "\t\tDefence Melee: " + str(self.clicked_troop.get_parent_square().get_troop().get_troop_defence()[0]) + "  Defence Ranged: " + str(self.clicked_troop.get_parent_square().get_troop().get_troop_defence()[1]))
        self.Text.show()
        self.actionBarItemNames.append(self.Text) 

        
        self.actionBarItems.append(QLabel())
        self.Text = QtGui.QLabel(self)                   
        self.Text.setFont(self.fontResources)
        self.Text.move(330,860)
        self.Text.setText("Owner: " + str(self.clicked_troop.get_parent_square().get_troop().get_troop_owner().get_player_name()))
        self.Text.show()
        self.actionBarItemNames.append(self.Text)
        
            
    def attack(self):
        ''' Checks if the player has any attacks left to attack and displays info about it'''
        if self.attacks > 0:
            self.display_info("Click the tile you want to attack.")
            self.attacking = True   # Next time a tile is clicked this will change back
        else:
            self.display_info("You don't have any attacks left.")
            
    def move_troop(self):
        ''' Checks if the player has any moves left to move and displays info about it'''
        if self.moves > 0:
            self.display_info("Click the tile you want to move the troop to.")
            self.moving = True      # Next time a tile is clicked this will change back
        else:
            self.display_info("You don't have any moves left.")
    
    def destroy_troop(self, troop = None):
        ''' Destroys the troop you clicked or the troop you gave as a parameter'''
        if troop == None:
            square = self.clicked_troop.get_parent_square()
        else:
            square = troop.get_troop_graphical_representation().get_parent_square()
        self.playing.decrease_player_income([0,0,0,square.get_troop().get_troop_food_consumption()])  # delete the income the building gave
        
        square.remove_troop()
        self.clicked_troop.hide()
        self.destroy_actionbar_items()
        self.update_texts()
               
    def building_options(self):
        '''Check If player wants to move to this tile'''
        if self.moving == True:
            self.moving = False
            self.display_info("You can't move to a building.")
            return
        
        '''Check If player wants to attack to this building'''
        if self.attacking == True:
            
            self.attacking = False
            troop = self.clicked_troop.get_parent_square().get_troop()
            print(troop)
            coordinates = troop.get_troop_coordinates()
            
            '''Checks if all the conditions are ok to attack'''
            attackRange = troop.get_troop_range()
            if self.sender().get_parent_square().check_if_empty() == False and self.map.get_distance_between_coordinates(coordinates,self.sender().get_parent_square().get_square_coordinates()) <= float(attackRange) and troop.get_troop_owner != self.sender().get_parent_square().get_building().get_building_owner():
                self.combat_building(self.clicked_troop.get_parent_square().get_troop(), self.sender().get_parent_square().get_building())
                return
            elif self.map.get_distance_between_coordinates(coordinates,self.sender().get_parent_square().get_square_coordinates()) > float(attackRange):
                self.display_info("The tile you are trying to attack to is out of your range.")
                return
            elif self.sender().get_parent_square().check_if_empty() == True:
                self.display_info("There is nothing to attack to.")
                return
            elif troop.get_troop_owner != self.sender().get_parent_square().get_building().get_building_owner():
                self.display_info("You can't attack your own building.")
                return
        
        self.clicked_building = self.sender()
        print(self.clicked_building)
        
        
        
        coordinates = self.clicked_building.get_parent_square().get_square_coordinates()
        self.selection.move((coordinates[0] - self.xIncrement)*100 + 320, (coordinates[1] - self.yIncrement)*100 + 170)
        self.selection.show()
        
        '''Draw the delete button'''
        image = "deletecrossSmall.png"
        self.destroy_actionbar_items()
        print("Clicked building")
        self.tile1 = ExtendedQLabel(self,image,None)
        self.tile1.setPixmap(QPixmap(image))
        self.tile1.move(1060,840)
        self.tile1.show()
        self.actionBarItems.append(self.tile1)
        self.actionBarItemNames.append(QLabel())
        
        ''' Building information display'''
        self.actionBarItems.append(QLabel())
        self.Text = QtGui.QLabel(self)                 
        self.Text.setFont(self.fontResources)
        self.Text.move(370,700)
        self.Text.setText(str(self.clicked_building.get_parent_square().get_building().get_building_name()) + "\t\tHP: " + str(self.clicked_building.get_parent_square().get_building().get_building_hp()) + "\t\tDefence: " + str(self.clicked_building.get_parent_square().get_building().get_building_defence()))
        self.Text.show()
        self.actionBarItemNames.append(self.Text) 
        
        self.actionBarItems.append(QLabel())
        self.Text = QtGui.QLabel(self)                   
        self.Text.setFont(self.fontResources)
        self.Text.move(370,750)
        gain = self.clicked_building.get_parent_square().get_building().get_building_gain()
        self.Text.setText("Resource gain:\n\nGold\t" + str(gain[0]) + "\t\tWood\t" + str(gain[1]) + "\t\tIron\t" + str(gain[2]) + "\nFood\t" + str(gain[3]))
        self.Text.show()
        self.actionBarItemNames.append(self.Text)
        
        self.actionBarItems.append(QLabel())
        self.Text = QtGui.QLabel(self)                   
        self.Text.setFont(self.fontResources)
        self.Text.move(330,860)
        self.Text.setText("Owner: " + str(self.clicked_building.get_parent_square().get_building().get_building_owner().get_player_name()))
        self.Text.show()
        self.actionBarItemNames.append(self.Text)
        
        self.connect(self.tile1, SIGNAL('clicked()'), self.destroy_building)
    
    def destroy_building(self, building = None):
        ''' Destroys the building and refunds 1/3 of the buildings cost'''
        if building == None:
            square = self.clicked_building.get_parent_square()
        else:
            square = building.get_building_graphical_representation().get_parent_square()
        print(square)
        self.playing.decrease_player_income(square.get_building().get_building_gain())  # delete the income the building gave
        cost = square.get_building().get_building_cost()
        
        for i in range(4):                                                              # Refund 1/3 of the building cost to the builder
            cost[i] = int(cost[i]/3)
        self.playing.increase_player_resources(cost)
        self.playing.decrease_player_science_point_income(square.get_building().get_building_science_points())
        
        square.destroy_square_building()
        self.clicked_building.hide()
        self.destroy_actionbar_items()
        self.update_texts()
    
    
    def combat_troop(self,attacker,defender):
        '''This method is called when a player attacks another troop'''
        
        if self.playing == self.player:
            self.attacks -= 1
        else:
            self.comp_attacks -= 1
        '''calculate damage'''
        AP = attacker.get_troop_attack_power()
        attackerType = attacker.get_troop_type()
        if attackerType == "melee":
            DEF = defender.get_troop_defence()[0]
            damageToDefender = int(AP/DEF * 20)
            damageToAttacker = int(DEF/AP * 25)
        elif attackerType == "ranged":
            DEF = defender.get_troop_defence()[1]
            damageToDefender = int(AP/DEF * 20)
            damageToAttacker = 0
        
        ''' apply damage'''
        attacker.damage(damageToAttacker)
        defender.damage(damageToDefender)
     
        self.display_info("Attacker HP: " + str(attacker.get_troop_hp()) +" \\t-" + str(damageToAttacker) + "\nDefender HP: " + str(defender.get_troop_hp()) + " \t\t-" + str(damageToDefender))
        
        self.check_if_dead(attacker)
        self.check_if_dead(defender)
    
    def combat_building(self,attacker,defender):
        '''This method is called when a player attacks a building'''
        if self.playing == self.player:
            self.attacks -= 1
        else:
            self.comp_attacks -= 1
        self.update_texts()
        '''calculate damage'''
        AP = attacker.get_troop_attack_power()
        attackerType = attacker.get_troop_type()
        DEF = defender.get_building_defence()
        if attackerType == "melee":
            damageToDefender = int(AP/DEF * 20)
            damageToAttacker = int(DEF/AP * 5)
        elif attackerType == "ranged":
            damageToDefender = int(AP/DEF * 20)
            damageToAttacker = 0
        
        ''' apply damage'''
        attacker.damage(damageToAttacker)
        defender.damage(damageToDefender)
        
        self.display_info("Attacker HP: " + str(attacker.get_troop_hp()) +" \t\t-" + str(damageToAttacker) + "\nDefender HP: " + str(defender.get_building_hp()) + " \t-" + str(damageToDefender))
        self.check_if_dead(attacker)
        self.check_if_destroyed(defender)
    
    def check_if_dead(self, troop):
        ''' Everytime damage was dealt to a troop this method is called to check if the health is below 0. And if it is, deletes the troop'''
        if troop.get_troop_hp() <= 0:
            troop.get_troop_graphical_representation().hide()
            square = troop.get_troop_graphical_representation().get_parent_square()
            self.destroy_troop(troop)
            square.remove_troop()
            
            self.update_map()
            
    
    def check_if_destroyed(self, building):    
        ''' Everytime damage was dealt to a building this method is called to check if the health is below 0. And if it is, deletes the building'''    
        if building.get_building_hp() <= 0:
            building.get_building_graphical_representation().hide()
            square = building.get_building_graphical_representation().get_parent_square()
            self.destroy_building(building)
            square.destroy_square_building
            
            self.update_map()
    
    ''' These methods are simply for the inventory'''
    ''' They move the inventory to right or left'''
    
    def right_arrow_menu(self):
        self.inventoryPlus += 1
        self.land_options(True)
    def left_arrow_menu(self):
        self.inventoryPlus -= 1
        self.land_options(True)
        
    def right_arrow_troop_menu(self):
        self.inventoryPlus += 1
        self.barracks_options(True)
    def left_arrow_troop_menu(self):
        self.inventoryPlus -= 1
        self.barracks_options(True)
        
    def land_options(self, menus = False):
        '''Check if player wants to attack this tile'''
        if self.attacking == True:
            self.attacking = False
            self.display_info("You can't attack there.")
            return
        
        '''Check if player wants to move to this tile'''
        if self.moving == True:
            
            self.moving = False
            troop = self.clicked_troop.get_parent_square().get_troop()
            print(troop)
            coordinates = troop.get_troop_coordinates()
            previousSquare = self.clicked_troop.get_parent_square()
            movement = troop.get_troop_movement()
            
            '''Check if all the conditions are ok to move the troop'''
            if self.sender().get_parent_square().check_if_empty() == True and self.map.get_distance_between_coordinates(coordinates,self.sender().get_parent_square().get_square_coordinates()) <= float(movement[0]) and self.sender().get_parent_square().get_moveable_type() == True:
                
                '''moves the player from one square to another'''
                troop.set_troop_coordinates(self.sender().get_parent_square().get_square_coordinates())
                previousSquare.remove_troop()
                self.sender().get_parent_square().add_troop(troop)
                self.clicked_troop.set_parent_square(self.sender().get_parent_square())
                if self.playing == self.player:
                    self.moves -= 1
                else:
                    self.comp_moves -= 1
                self.update_map()
                self.update_texts()
            elif self.map.get_distance_between_coordinates(coordinates,self.sender().get_parent_square().get_square_coordinates()) > float(movement[0]):
                self.display_info("The tile you are trying to move to is too far away.")
                return
            elif self.sender().get_parent_square().check_if_empty() == False:
                self.display_info("That tile is already occupied.")
                return
            elif self.sender().get_parent_square().get_moveable_type() == False:
                self.display_info("You can't move to that type of terrain.")
                return
            
        '''Display the red selection shaped like square'''   
        self.selection.show()
        self.destroy_actionbar_items()
        
        hasCapitalNear = False
        
        ''' Functionality so you can browse with the inventory with the arrows'''  
        if menus == False:
            self.inventoryPlus = 0
            self.availableBuildings = []
            self.clicked_tile = self.sender()
            coordinates = self.clicked_tile.get_parent_square().get_square_coordinates()
            self.selection.move((coordinates[0] - self.xIncrement)*100 + 320, (coordinates[1] - self.yIncrement)*100 + 170)
            self.selection.show()
            self.buildType = self.clicked_tile.get_parent_square().get_buildable_type()
            for i in range(len(self.allBuildings)):
                if self.allBuildings[i].get_tile_type() == self.buildType:
                    self.availableBuildings.append(self.allBuildings[i])
        tile_coordinates = self.clicked_tile.get_parent_square().get_square_coordinates()
        
        '''Checks if the square player clicked has a Capital or Capital Building near it otherwise you cannot build there it won't show anything'''
        size = self.map.get_map_size()
        for j in range(size[1]):
            for i in range(size[0]):
                if self.map.get_square(i, j).check_if_has_building() == True:
                    if self.map.get_square(i, j).get_building().get_building_owner() == self.player:
                        if self.map.get_square(i, j).get_building().get_building_name() == "Capital" and self.map.get_distance_between_coordinates([i,j],tile_coordinates) <= 3 :
                            hasCapitalNear = True
                            break
                        elif self.map.get_square(i, j).get_building().get_building_name() == "Capital Building" and self.map.get_distance_between_coordinates([i,j],tile_coordinates) <= 4:
                            hasCapitalNear = True
                            break
        
        '''Draw all the building options to the inventory''' 
        if menus == True:
            hasCapitalNear = True
        if hasCapitalNear == True:
            if len(self.availableBuildings) > 0:
                if len(self.availableBuildings) < 4:
                    amount = len(self.availableBuildings)
                else:
                    amount = 4
                for i in range(amount):
                    if (len(self.availableBuildings) - self.inventoryPlus) > 4:
                        self.tile = ExtendedQLabel(self,"right_arrow.png", None)
                        self.tile.setPixmap(QPixmap("right_arrow.png"))
                        self.tile.move(1100,740)
                        self.tile.show()
                        self.actionBarItems.append(self.tile)
                        self.actionBarItemNames.append(self.tile)
                        self.connect(self.tile, SIGNAL('clicked()'), self.right_arrow_menu)
                    if self.inventoryPlus > 0:
                        self.tile = ExtendedQLabel(self,"left_arrow.png", None)
                        self.tile.setPixmap(QPixmap("left_arrow.png"))
                        self.tile.move(290,740)
                        self.tile.show()
                        self.actionBarItems.append(self.tile)
                        self.actionBarItemNames.append(self.tile)
                        self.connect(self.tile, SIGNAL('clicked()'), self.left_arrow_menu)
                    image = self.availableBuildings[i+self.inventoryPlus].get_building_image()
                    self.tile = ExtendedQLabel(self,image, self.availableBuildings[i+self.inventoryPlus].get_building_id())
                    self.tile.setPixmap(QPixmap(image))
                    self.tile.move(400 + i*170,730)
                    self.tile.show()
                    self.actionBarItems.append(self.tile)
                    
                    self.Text = QtGui.QLabel(self)
                    
                    self.Text.setFont(self.fontResources)
                    self.Text.move(410 + i*170,830)
                    self.Text.setText(self.availableBuildings[i+self.inventoryPlus].get_building_name())
                    self.Text.show()
                    self.actionBarItemNames.append(self.Text)
                    self.connect(self.tile, SIGNAL('clicked()'), self.add_building_to_queue)
        

    
    def destroy_actionbar_items(self):
        '''This method is called to clear the inventory'''
        for i in range(len(self.actionBarItems)):
            self.actionBarItems[i].hide()
            self.actionBarItemNames[i].hide()
            
        self.actionBarItems = []
        self.actionBarItemNames = []
    


  
    def has_resources(self,cost):
        '''This method is called to check if player has enough resources'''
        currentResources = self.playing.get_player_resources()
        if currentResources[0] >= cost[0] and currentResources[1] >= cost[1] and currentResources[2] >= cost[2] and currentResources[3] >= cost[3]:
            return True
        else:
            print("Not enough resources.")
            self.display_info("Not enough resources.")
            return False
    
    ''' These methods are simply to move the map '''
    ''' They move the map to right, left, up or down'''
                
    def right_arrow_map(self):
        self.xIncrement += 1
        self.selection.hide()
        self.update_map()
    
    def left_arrow_map(self):
        self.xIncrement -= 1
        self.selection.hide()
        self.update_map()
    
    def up_arrow_map(self):
        self.yIncrement -= 1
        self.selection.hide()
        self.update_map()
    
    def down_arrow_map(self):
        self.yIncrement += 1
        self.selection.hide()
        self.update_map()
    
    
    def calculate_choice_values(self):
        ''' Initialize valus for different desicions '''
        
        self.build_troops = ["Build_troops",1]
        self.build_buildings = ["Build_buildings",1]
        self.increase_resources = ["Increase_resources",1]
        self.save_resources = ["Save_resources",1]
        self.move_troops = ["Move_troops",1]
        self.attack = ["Attack",1]
        
        self.choices = [self.build_troops,self.build_buildings,self.increase_resources,self.save_resources,self.move_troops,self.attack]
        
        isNear = False
        playerBuildings = []
        computerBuildings = []
        playerTroops = []
        computerTroops = []
        
        buildingOptions = []
        troopOptions = []
        ''' Check the map and count the buildings and troops each player has, check also if there are enemy troops near'''
        
        
        
        for j in range(self.map.get_map_size()[1]):
            for i in range(self.map.get_map_size()[0]):
                square = self.map.get_square(i,j)
                
                ''' Get buildings'''
                if square.check_if_has_building() == True:
                    if square.get_building().get_building_owner() == self.player:
                        playerBuildings.append(square.get_building())
                    elif square.get_building().get_building_owner() == self.computer:
                        computerBuildings.append(square.get_building())
                
                ''' Get troops'''       
                if square.check_if_has_troop() == True:
                    if square.get_troop().get_troop_owner() == self.player:
                        playerTroops.append(square.get_troop())
                    elif square.get_troop().get_troop_owner() == self.computer:
                        computerTroops.append(square.get_troop())
        
        '''Check for incomes'''
        incomeComputer = self.computer.get_player_income()
        
        incomePlayer = self.player.get_player_income()
        
        '''Calculate the averages'''
        incomeComputerAverage = (incomeComputer[0] + incomeComputer[1] + incomeComputer[2] + incomeComputer[3])/4
        incomePlayerAverage = (incomePlayer[0] + incomePlayer[1] + incomePlayer[2] + incomePlayer[3])/4
        
        ''' Check if player has more income '''
        if incomeComputerAverage < incomePlayerAverage and self.resources_constructed == False:
            self.increase_resources[1] += 1
        
        ''' Check if player has more troops '''
        if len(playerTroops) > len(computerTroops) and self.troops_constructed == False:
            self.build_troops[1] += 1
            
        ''' Check if player has troops near computer buildings'''
        for i in range(len(playerTroops)):
            for j in range(len(computerBuildings)):
                if self.map.get_distance_between_coordinates([playerTroops[i].get_troop_coordinates(),computerBuildings[j].get_building_coordinates()]) < 4:
                    self.build_troops[1] += 1
                    self.move_troops[1] += 2
                    if self.map.get_distance_between_coordinates([playerTroops[i].get_troop_coordinates(),computerBuildings[j].get_building_coordinates()]) < 2:
                        self.move_troops[1] += 3
                        self.attack[1] += 5
                        isNear = True
        
        ''' Check for resources '''
        resources = self.computer.get_player_resources()
        
        ''' List all the buildings computer can build'''
        for i in range(len(self.availableBuildings)):
            if self.availableBuildings[i].get_building_cost() < resources:
                buildingOptions.append(self.availableBuildings[i])
        
        ''' List all the troops computer can build'''
        for i in range(len(self.availableTroops)):
            if self.availableTroops[i].get_troop_cost() < resources:
                troopOptions.append(self.availableTroops[i])  
        
        ''' Check if should save resources '''
        if (incomeComputerAverage > incomePlayerAverage and len(playerTroops) < len(computerTroops) and len(playerBuildings) < len(computerBuildings) and isNear == False) or (len(buildingOptions) < 1 and len(troopOptions) < 1):
            self.save_resources[1] += 2
        
        
        ''' Check if can move and attack '''
        if self.comp_attacks < 1:
            self.attack[1] = 0
        if self.comp_moves < 1: 
            self.move_troops[1] = 0
                
                        
    def decide(self):
        
        ''' Check which choice has the biggest value'''
        biggestValue = 0
        for i in range(len(self.choices)):
            if biggestValue < self.choices[i][1]:
                biggestValue = self.choices[i][0]
        
        ''' Do what had the biggest value'''
        
        if biggestValue == "Build_troops":
            return False
        elif biggestValue == "Build_buildings":
            return False
        elif biggestValue == "Increase_resources":
            incomeComputer = self.computer.get_player_income()
            
            return False
        elif biggestValue == "Save_resources":
            return True
        elif biggestValue == "Move_troops":
            return False
        elif biggestValue == "Attack":
            return False
        else:
            return True
    
    
    def computers_turn(self):
        '''This method is called when it's computers turn'''
        nextRound = False
        i = 0
        while(nextRound != True and i < 20):
            self.calculate_choice_values()
            nextRound = self.decide()
            i += 1
    
    def next_round(self):
        '''This method is called when the next round button is pressed'''
        ''' It updates the map, increases resources and gives computer the turn'''
        self.increase_resources(self.computer)
        self.playing = self.computer
        #self.computers_turn()        # NOT READY
        self.update()
        self.playing = self.player
        self.increase_resources(self.player)
        self.update_construction_queue()
        
    def increase_resources(self, who):
        '''Increases the resources with the amount of income the player has'''
        who.increase_player_resources(who.get_player_income())
        who.increase_player_science_points(who.get_player_science_point_income())
    
    def update(self):
        self.destroy_actionbar_items()
        
        ''' Update resources text, round and refresh moves'''
        self.moves = 3
        self.attacks = 3
        self.round += 1
        self.update_texts()
        
        
    
    def update_texts(self):
        ''' Updates the texts on the left and right metal palets'''
        playerStats = self.player.get_player_resources() # Gets players resources in a list of 4    Index 0 = Gold | Index 1 = Wood | Index 2 = Iron | Index 3 = Food
        self.resourcesText.setText("\nRound " + str(self.round) + "\n\nGold :" + str(playerStats[0]) + "\nWood :" + str(playerStats[1]) + "\nIron :" + str(playerStats[2]) + "\nFood :" + str(playerStats[3]) + "\n\n\nScience : " + str(self.player.get_player_science_points()))
        #self.sciencePointText.setText("Science Points: " + str(self.player.get_player_science_points()))
        playerIncome = self.player.get_player_income()  # Gets players income in a list of 4    Index 0 = Gold | Index 1 = Wood | Index 2 = Iron | Index 3 = Food
        self.incomeText.setText("\nIncome per round:\n\nGold:\t" + str(playerIncome[0]) + "\nWood:\t" + str(playerIncome[1]) + "\nIron:\t" + str(playerIncome[2]) + "\nFood:\t" + str(playerIncome[3]) + "\n\n\nScience Gain: " + str(self.player.get_player_science_point_income()))
        
        self.moveCountText.setText("Moves: " + str(self.moves) + "\nAttacks: " + str(self.attacks))
    
    def update_construction_queue(self):
        ''' After each round reduces the construction time of troops and buildings and checks if they have to be built'''
        toBeDeleted = []
        
        for i in range(len(self.buildQueue)):
            self.buildQueue[i][1] -= 1
            if self.buildQueue[i][1] <= 0:
                self.construct_building(self.buildQueue[i][0])
                toBeDeleted.append(i)
        for i in range(len(toBeDeleted)):
            j = toBeDeleted[i]
            del self.buildQueue[j-i]
        
        toBeDeleted = []
                
        for i in range(len(self.troopQueue)):
            self.troopQueue[i][1] -= 1
            if self.troopQueue[i][1] <= 0:
                self.construct_troop(self.troopQueue[i][0])
                toBeDeleted.append(i)
        for i in range(len(toBeDeleted)):
            j = toBeDeleted[i]
            del self.troopQueue[j-i]
    
    def update_map(self):
        '''This method updates the map'''
        
        '''First hide all the map arrows'''
        size = self.map.get_map_size()
        self.rightArrow.hide()
        self.leftArrow.hide()
        self.upArrow.hide()
        self.downArrow.hide()
        
        
        if self.selection == None:
            self.selection = ExtendedQLabel(self,"selection.png", None)
            self.selection.setPixmap(QPixmap("selection.png"))
            self.selection.hide()

        '''Then checks which arrow should be shown'''
        if self.xIncrement + 8 < size[0]:
            self.rightArrow = ExtendedQLabel(self,"right_arrow.png", None)
            self.rightArrow.setPixmap(QPixmap("right_arrow.png"))
            self.rightArrow.move(1130,375)
            self.rightArrow.show()
            self.connect(self.rightArrow, SIGNAL('clicked()'), self.right_arrow_map)
        
        if self.xIncrement > 0:
            self.leftArrow = ExtendedQLabel(self,"left_arrow.png", None)
            self.leftArrow.setPixmap(QPixmap("left_arrow.png"))
            self.leftArrow.move(260,375)
            self.leftArrow.show()
            self.connect(self.leftArrow, SIGNAL('clicked()'), self.left_arrow_map)
        
        if self.yIncrement > 0:
            self.upArrow = ExtendedQLabel(self,"up_arrow.png", None)
            self.upArrow.setPixmap(QPixmap("up_arrow.png"))
            self.upArrow.move(695,120)
            self.upArrow.show()
            self.connect(self.upArrow, SIGNAL('clicked()'), self.up_arrow_map)
        
        if self.yIncrement + 5 < size[1]:
            self.downArrow = ExtendedQLabel(self,"down_arrow.png", None)
            self.downArrow.setPixmap(QPixmap("down_arrow.png"))
            self.downArrow.move(695,670)
            self.downArrow.show()
            self.connect(self.downArrow, SIGNAL('clicked()'), self.down_arrow_map)
        
        '''Hides all the buildings and troops in the map, also the tiles'''
        for j in range(size[1]):
            for i in range(size[0]):
                self.mapTiles[i][j].hide()
                if self.mapTiles[i][j].get_parent_square().check_if_has_building() == True:
                    building = self.mapTiles[i][j].get_parent_square().get_building().get_building_graphical_representation()
                    building.hide()
                if self.mapTiles[i][j].get_parent_square().check_if_has_troop() == True:
                    troop = self.mapTiles[i][j].get_parent_square().get_troop().get_troop_graphical_representation()
                    troop.hide()
        
        ''' Now checks tiles should be shown and shows all the troops and buildings in those tiles'''
        for j in range(5):
            for i in range(8):
                self.mapTiles[i + self.xIncrement][j + self.yIncrement].move(i*100+320,j*100+170)
                self.mapTiles[i + self.xIncrement][j + self.yIncrement].show()
                if self.mapTiles[i + self.xIncrement][j + self.yIncrement].get_parent_square().check_if_has_building() == True:
                    building = self.mapTiles[i + self.xIncrement][j + self.yIncrement].get_parent_square().get_building().get_building_graphical_representation()
                    building.move(i*100+320,j*100+170)
                    building.show()
                if self.mapTiles[i + self.xIncrement][j + self.yIncrement].get_parent_square().check_if_has_troop() == True:
                    troop = self.mapTiles[i + self.xIncrement][j + self.yIncrement].get_parent_square().get_troop().get_troop_graphical_representation()
                    if self.mapTiles[i + self.xIncrement][j + self.yIncrement].get_parent_square().get_troop().get_troop_graphical_representation().get_parent_square() != "Temporary":
                        troop.move(i*100+320,j*100+170)
                        troop.show()
def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()    
    
