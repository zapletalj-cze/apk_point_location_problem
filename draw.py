from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtGui import QMouseEvent, QPaintEvent
from PyQt6.QtWidgets import *
from osgeo import ogr
from os.path import *
from osgeo import ogr
import time
import sys



class Draw(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.q = QPointF(-100, -100)
        self.pol = QPolygonF()
        self.add_vertex = True

    def polygon_to_polygon(geometry):
        """
        Converts geometry to QPolygonF
        :return: list of polygons
        """
        if geometry.GetGeometryName() == 'POLYGON':
            polygon = QPolygonF()
            for point in geometry.GetGeometryRef(0):
                polygon.append(QPointF(point[0], point[1]))
            return polygon
        elif geometry.GetGeometryName() == 'MULTIPOLYGON':
            polygons = []
            for i in range(geometry.GetGeometryCount()):
                polygon = QPolygonF()
                for point in geometry.GetGeometryRef(i).GetGeometryRef(0):
                    polygon.append(QPointF(point[0], point[1]))
                polygons.append(polygon)
            return polygons
        else:
            return None


    def gis_to_polygon(self, path: str):
        """
        Converts geodata to list of QPolygonF objects using OGR
        :param path: path to file, receiving from self
        :return: list of QPolygonF objects returning to self
        """
        if exists(path) and splitext(path)[1] in ['.shp', '.gpkg', '.geojson']:
            ds = ogr.Open(path)
            layer = ds.GetLayer()
            for feature in layer:
                geometry = feature.GetGeometryRef()
                if geometry.GetGeometryType() not in (ogr.wkbPolygon, ogr.wkbMultiPolygon):
                    print("Not all geometries are polygons.")

            # Convert geometries to QPolygonF
            self.polygons = []
            for feature in layer:
                geom = feature.GetGeometryRef()
                qgeom = polygon_to_polygon(geom)
                if qgeom is not None:
                    self.polygons.append(qgeom)
        else:
            mb_error = QtWidgets.QMessageBox()
            mb_error.setWindowTitle('Error')
            mb_error.setText("File not found.")
            time.sleep(30)
            sys.exit()



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

