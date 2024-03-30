from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtGui import QMouseEvent, QPaintEvent
from PyQt6.QtWidgets import *
import algorithms
from shapely.geometry import Polygon
import geopandas as gpd
from os import path

class Draw(QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Inicialize features
        self.q = QPointF(-100, -100)
        self.add_vertex = False
        self.polygons = []
        self.features = [None]
        self.results = []
        self.extent = 4*[0]


    def shapely_to_qpolygonf(shape_polygon):
        """
        Converts a Shapely polygon object to a Qt QPolygonF object.
        :param Shapely polygon object.
        :return: A Qt QPolygonF object representing the converted polygon
        """
        qpolygon = QPolygonF()
        for point in shape_polygon.exterior.coords:
            qpolygon.append(QPointF(point[0], point[1]))
        return qpolygon

    def resize_polygons_to_widget(self, padding=50):
        """
        Resizes all QPolygons in self.polygons to fit proportionally within the widget with padding.
        :param padding: padding in pixels
        :type padding int
        :return: list of QPolygons
        """
        # Get widget geometry,
        x_win = int(self.widget_size.x() + padding)
        y_win = int(self.widget_size.y() + padding)
        width_win = int(self.widget_size.width() - padding)
        height_win = int(self.widget_size.height() - padding)
        x_min_dat = self.extent[0]
        x_max_dat = self.extent[2]
        y_min_dat = self.extent[1]
        y_max_dat = self.extent[3]
        resized_polygons = []
        for feature in self.features:
            scaled_point_list = []
            for point in feature:
                scaled_x = int(((point.x() - x_min_dat) / (x_max_dat - x_min_dat) * width_win))
                scaled_y = int((height_win - (point.y() - y_min_dat) / (y_max_dat - y_min_dat) * height_win))
                scaled_point = QPointF(scaled_x, scaled_y)
                scaled_point_list.append(scaled_point)
            resized_polygon = QPolygonF(scaled_point_list)
            resized_polygons.append(resized_polygon)
        return resized_polygons

    def gis_to_qt_polygons(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open file", "", "")
        if path.splitext(filename)[1] in ['.gpkg', '.shp', '.geojson']:
            # Load shapefile using GeoPandas
            gdf = gpd.read_file(filename)
            self.extent = [item for item in (gdf.total_bounds)]
            # Convert Shapely polygons to QPolygonF and store them in self.features
            self.features = []
            for shapely_geometry in gdf.geometry:
                if isinstance(shapely_geometry, Polygon):
                    self.features.append(Draw.shapely_to_qpolygonf(shapely_geometry))
                else:
                    for polygon in shapely_geometry:
                        self.features.append(Draw.shapely_to_qpolygonf(polygon))
            self.polygons = Draw.resize_polygons_to_widget(self)
            self.results = [0] * len(self.polygons)

        else:
            warning_box = QMessageBox()
            warning_box.setText("Unsupported format")
            warning_box.setIcon(QMessageBox.Icon.Warning)
            warning_box.setInformativeText(
                f"The selected file '{path.basename(filename)}' could not be loaded. It might be an unsupported format")
            warning_box.exec()

    def mousePressEvent(self, e: QMouseEvent):
        # get cursor position
        x = e.position().x()
        y = e.position().y()

        # add vertex
        self.q.setX(x)
        self.q.setY(y)

        # repaint
        self.repaint()

    #  function that sets colors
    def paintEvent(self, e: QPaintEvent):
        # create new object
        qp = QPainter(self)
        # start drawing
        qp.begin(self)
        # set graphical attributes
        for (result, polygon) in zip(self.results, self.polygons):
            # set graphical attributes
            qp.setPen(QPen(Qt.GlobalColor.lightGray))
            qp.setBrush(Qt.GlobalColor.transparent)
            if result == 1:
                qp.setBrush(Qt.GlobalColor.yellow)
                qp.setPen(Qt.GlobalColor.black)
            # draw polygon
            qp.drawPolygon(polygon)

        if self.add_vertex:
            # draw vertex
            pen = QPen(Qt.GlobalColor.red)
            qp.setPen(pen)

            brush = QBrush(Qt.GlobalColor.magenta)
            brush.setStyle(Qt.BrushStyle.SolidPattern)
            # Ensure solid brush for transparency
            qp.setBrush(brush)
            r = 10

            qp.drawEllipse(int(self.q.x() - r), int(self.q.y() - r), 2 * r, 2 * r)

        qp.end()

    # function that sets the result
    def setResults(self, results):
        """
        Updates self results obtained by algorithm and widget windows.
        :param results: list of results [int like]
        """
        self.results = results
        self.repaint()

    # function that adds a point or removes a point
    def switchDrawing(self):
        self.add_vertex = not self.add_vertex
        self.repaint()

    # function that returns analyzed point
    def getQ(self):
        # return analyzed point
        return self.q

    # function that returns analyzed polygons
    def getPolygons(self):
        return self.polygons

    def getResults(self):
        return self.results

    # clear dynamic variables
    def clearData(self):
        # clear data
        self.polygons.clear()
        self.results.clear()
        self.q.setX(-100)
        self.q.setY(-100)
        self.repaint()