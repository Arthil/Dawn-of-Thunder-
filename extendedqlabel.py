'''
Created on 1.5.2015

@author: christian
'''



from PyQt4.QtGui import *
from PyQt4.QtCore import *

from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import pyqtSignal
class ExtendedQLabel(QLabel):
 
    def __init__(self, parent,image,parent_square):
        QLabel.__init__(self, parent)
        self.setMouseTracking(True)
        self.hoverImage = "H" + str(image)
        self.image = image
        self.parent_square = parent_square
    
    def enterEvent(self,event):
        self.setPixmap(QPixmap(self.hoverImage))

    def leaveEvent(self,event):
        self.setPixmap(QPixmap(self.image))
      
    def mousePressEvent(self, ev):
        self.emit(SIGNAL('clicked()'))
    
    def get_parent_square(self):
        return self.parent_square
    def set_parent_square(self,newParent):
        self.parent_square = newParent
        
    def set_new_image(self,image):
        self.hoverImage = "H" + image
        self.image = image
        
        