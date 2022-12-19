import sys

from PyQt5.QtWidgets import (
    QApplication, QDialog, QMainWindow, QMessageBox
)
from PyQt5.uic import loadUi

from Probablistic_Window import Ui_Probablistic_Window

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QWidget
from PyQt5.QtGui import QPixmap
import pandas as pd
import geopandas
import matplotlib.pyplot as plt

path_to_data = geopandas.datasets.get_path("nybb")
gdf = geopandas.read_file(path_to_data)
gdf.to_file("my_file.geojson", driver="GeoJSON")
gdf = gdf.set_index("BoroName")
gdf["area"] = gdf.area
gdf['centroid'] = gdf.centroid
gdf.plot("area", legend=True)
plt.axis('off')
plt.savefig('testmap.png')
gdf = gdf.set_geometry("centroid")
gdf.plot("area", legend=True)
plt.savefig('testplot.png')

graph = []
for x in gdf:
    print(x)
    xstr=str(x)
    graph.append(x)
    plt.close("all")
    for y in gdf:
        ystr=str(y)
        try:
            fig, ax = plt.subplots(figsize=(12,5))
            ax2 = ax.twinx()
            ax.plot(gdf[x], color='green', marker='x')
            ax2.plot(gdf[y], color='red', marker='o')
            ax.yaxis.grid(color='lightgray', linestyle='dashed')
            plt.tight_layout()
            plt.savefig(x + '_' + y + '_plot.png')
        except AttributeError as e:
            pass
        except TypeError as e:
            pass
        except ValueError as e:
            pass

class Window(QMainWindow, Ui_Probablistic_Window):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.drapdown.addItems(['Map','Plot'])
        self.drapdown_Primary.addItems(graph)
        self.drapdown_Secondary.addItems(graph)

        qpixmap = QPixmap('testmap.png')
        self.imglabel.setPixmap(qpixmap)
        self.imglabel.setScaledContents(True)

        qpixgraph = QPixmap(graph[0] + '_' + graph[0] + '_plot.png')
        self.graph_label.setPixmap(qpixgraph)
        self.graph_label.setScaledContents(True)

        self.connectSignalsSlots()

    def connectSignalsSlots(self):
        self.drapdown.currentIndexChanged.connect(self.addimage)
        self.drapdown_Primary.currentIndexChanged.connect(self.addgraph1)
        self.drapdown_Secondary.currentIndexChanged.connect(self.addgraph2)

    def addimage(self,index1):
        print("Index changed", index1)
        if index1 == 0:
            qpixmap = QPixmap('testmap.png')
            self.imglabel.setPixmap(qpixmap)
            self.imglabel.setScaledContents(True)
        if index1 == 1:
            qpixmap = QPixmap('testplot.png')
            self.imglabel.setPixmap(qpixmap)
            self.imglabel.setScaledContents(True)

    def addgraph1(self, index2):
        print(str(self.drapdown_Secondary.currentText()))
        for x in graph:
            if index2 == graph.index(x):
                qpixgraph = QPixmap(x + '_' + str(self.drapdown_Secondary.currentText()) + '_plot.png')
                self.graph_label.setPixmap(qpixgraph)
                self.graph_label.setScaledContents(True)

    def addgraph2(self, index3):
        for y in graph:
            if index3 == graph.index(y):
                qpixgraph = QPixmap(str(self.drapdown_Primary.currentText()) + '_' + y + '_plot.png')
                self.graph_label.setPixmap(qpixgraph)
                self.graph_label.setScaledContents(True)

        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec())