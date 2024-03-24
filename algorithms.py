from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *


#Processing data
class Algorithms:
    
    def __init__(self):
        pass
    
    
    def analyzePointPolygonPosition(self, q:QPointF, pol:QPolygonF):
        
        #Inicialize amount of intersections
        k = 0
        
        #Amount of vertices
        n = len(pol)
        
        #Process all segments
        for i in range(n):
            #Reduce coordinates
            xir = pol[i].x() - q.x()
            yir = pol[i].y() - q.y()
            
            xi1r = pol[(i+1)%n].x() - q.x()
            yi1r = pol[(i+1)%n].y() - q.y()
            
            #Suitable segment?
            if ((yi1r > 0) and (yir <= 0)) or ((yir > 0) and (yi1r <= 0)):
               
               #Compute intersection
               xm = (xi1r * yir - xir * yi1r)/(yi1r - yir)
               
               #Right half plane
               if xm > 0:       
                   k += 1  
                   
        #Point q inside polygon?
        if (k%2 == 1):
            return 1
        
        #Point q outside polygon
        return 0
          
                   
                   