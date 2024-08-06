import sys
import numpy as np
import random
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QGraphicsView, QGraphicsEllipseItem, \
    QGraphicsLineItem, QFrame, QVBoxLayout, QHBoxLayout, QWidget, QCheckBox
from PyQt5.QtGui import QMouseEvent, QPen, QColor, QPolygonF
from PyQt5.QtCore import Qt, QEvent, QPointF

# import your script to generate the Voronoi diagram and Delaunay triangulation
import voronoi as vo
from voronoi_packages import Point
from shapely import MultiPolygon


class MainWindow(QMainWindow):
    def __init__(self, geometry=(100, 100, 800, 800)):
        super().__init__()

        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.view.setMouseTracking(True)
        self.view.setCursor(Qt.CrossCursor)
        self.view.viewport().installEventFilter(self)

        self.point_items = []
        self.points = []
        self.voronoi_edges = []
        self.voronoi_polygons = []
        self.polygon_colors = []
        self.delaunay_edges = []
        self.current_point_index = None

        self.show_voronoi = True
        self.show_delaunay = True

        # create a frame to hold the checkboxes
        frame = QFrame(self)
        frame.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
        frame.setLineWidth(1)
        vbox = QVBoxLayout(frame)

        # create the checkboxes
        self.voronoi_checkbox = QCheckBox('Show Voronoi Diagram', self)
        self.voronoi_checkbox.setChecked(True)
        self.voronoi_checkbox.stateChanged.connect(self.toggle_voronoi)

        self.delaunay_checkbox = QCheckBox('Show Delaunay Triangulation', self)
        self.delaunay_checkbox.setChecked(True)
        self.delaunay_checkbox.stateChanged.connect(self.toggle_delaunay)

        vbox.addWidget(self.voronoi_checkbox)
        vbox.addWidget(self.delaunay_checkbox)

        # create a horizontal box layout to hold the view and the checkboxes
        hbox = QHBoxLayout()
        hbox.addWidget(self.view)
        hbox.addWidget(frame)

        # create a widget to hold the horizontal layout
        widget = QWidget()
        widget.setLayout(hbox)

        self.setCentralWidget(widget)

        # set the initial size of the window
        self.bound = (geometry[0], geometry[2])
        self.setGeometry(geometry[0], geometry[1], geometry[2]+200, geometry[3])
    
    def eventFilter(self, source, event):
        if event.type() == QEvent.MouseButtonPress:
            source.mousePressEvent(event)
        if event.type() == QEvent.MouseMove:
            if event.buttons() == Qt.RightButton and self.current_point_index is not None:
                new_point = Point(event.pos().x()+44.5, event.pos().y()+49.5)

                # update the position of the point in the scene
                item = self.point_items[self.current_point_index]
                item.setRect(new_point.x - 5, new_point.y - 5, 10, 10)

                # update the corresponding Point object in the self.points list
                self.points[self.current_point_index] = new_point

                # generate the new Voronoi and Delaunay edges
                self.voronoi_edges, voronoi_cells = vo.compute_voronoi(self.points, self.bound)
                self.delaunay_edges, self.voronoi_polygons = vo.compute_delaunay(self.points, voronoi_cells)

                # redraw the edges
                self.draw_edges()
        
        return super(QMainWindow, self).eventFilter(source, event)
    
    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.LeftButton:
            point = Point(event.pos().x()+44.5, event.pos().y()+49.5)
            self.add_point(point)
        elif event.button() == Qt.RightButton:
            self.current_point_index = None
            point = Point(event.pos().x()+44.5, event.pos().y()+49.5)
            for index, item in enumerate(self.points):
                if self.points[index].eq(point,50):
                    self.current_point_index = index
                    break
                
    def add_point(self, point: Point):
        # add the point to the scene as an ellipse
        pen = QPen(Qt.black)
        brush = QColor(255, 255, 255, 50)
        item = QGraphicsEllipseItem(point.x-5, point.y-5, 10, 10)
        item.setPen(pen)
        item.setBrush(brush)
        self.scene.addItem(item)
        self.points.append(point)
        self.point_items.append(item)

        # generate the new Voronoi and Delaunay edges
        points = [Point(item.x, item.y) for item in self.points]
        self.voronoi_edges, voronoi_cells = vo.compute_voronoi(points, self.bound)
        self.delaunay_edges, self.voronoi_polygons = vo.compute_delaunay(points, voronoi_cells)
        for i in range(len(self.voronoi_polygons) - len(self.polygon_colors)):
            self.polygon_colors.append([random.randint(0, 255) for i in range(3)])

        # redraw the edges
        self.draw_edges()

    
    def toggle_voronoi(self, state):
        self.show_voronoi = state == Qt.Checked
        self.draw_edges()

    def toggle_delaunay(self, state):
        self.show_delaunay = state == Qt.Checked
        self.draw_edges()
    
    def draw_edges(self):
        for item in self.scene.items():
            if not isinstance(item, QGraphicsEllipseItem):
                self.scene.removeItem(item)

        # draw the Voronoi edges
        if self.show_voronoi:
            pen = QPen(Qt.black)
            for edge in self.voronoi_edges:
                line = QGraphicsLineItem(edge[0].x, edge[0].y, edge[1].x, edge[1].y)
                line.setPen(pen)
                self.scene.addItem(line)
        
            for poly in range(len(self.voronoi_polygons)):
                # create a QPolygonF from the shapely polygon and add it to the scene
                qpolygonf = QPolygonF([QPointF(coord[0], coord[1]) for coord in self.voronoi_polygons[poly].exterior.coords])
                pen = QPen(QColor(*self.polygon_colors[poly]))
                polygon_item = self.scene.addPolygon(qpolygonf, pen)
                polygon_item.setBrush(QColor(*self.polygon_colors[poly]+[85]))

        # draw the Delaunay edges
        if self.show_delaunay:
            pen = QPen(QColor(255, 0, 0))
            for edge in self.delaunay_edges:
                line = QGraphicsLineItem(edge[0].x, edge[0].y, edge[1].x, edge[1].y)
                line.setPen(pen)
                self.scene.addItem(line)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())