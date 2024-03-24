from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtGui import QMouseEvent, QPaintEvent
from PyQt6.QtWidgets import *


class Draw(QWidget):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.q = QPointF(-100, -100)
        self.pol = QPolygonF()
        self.add_vertex = True
        
        
    def mousePressEvent(self, e: QMouseEvent):
        
        #Get coordinates of q
        x = e.position().x()
        y = e.position().y()
        
        #Add new vertex
        if self.add_vertex:
                
            #Create temporary point
            p = QPointF(x, y)
            
            #Add p to polygon
            self.pol.append(p)
            
        #Move q
        else:
            self.q.setX(x)
            self.q.setY(y)
            
        #Repaint screen
        self.repaint()
        
        
    def paintEvent(self, e: QPaintEvent):
        #Draw situation
        
        #Create new graphic object
        qp = QPainter(self)
        
        #Start drawing
        qp.begin(self)
        
        #Set graphical attributes
        qp.setPen(Qt.GlobalColor.black)
        qp.setBrush(Qt.GlobalColor.yellow)
        
        #Draw polygon
        qp.drawPolygon(self.pol)
        
        #Set graphical attributes
        qp.setBrush(Qt.GlobalColor.red)
        
        #Draw point
        r = 10
        qp.drawEllipse(int(self.q.x()-r), int(self.q.y()-r), 2*r, 2*r)
        
        #End drawing
        qp.end()
        
        
    def switchDrawing(self):
        #Change what will be drawn
        self.add_vertex = not(self.add_vertex)
            
            
    def getQ(self):
        #Return analyzed point
        return self.q
    
    
    def getPol(self):
        # Return analyzed polygon
        return self.pol
    
    
    def clearData(self):
        #Clear polygon
        self.pol.clear()
        
        #Shift point
        self.q.setX(-100)
        self.q.setY(-100)
        
        #Repaint screen
        self.repaint()
        