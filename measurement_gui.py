import sys
from PyQt5 import QtCore
from PyQt5.QtCore import QObject, QUrl, pyqtSignal, pyqtSlot, pyqtProperty
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtWidgets import QApplication
from lib import obj_pipe
from time import sleep


server = obj_pipe.listen(("", 8001)) 
#scheduler = ThreadPoolScheduler()

class Backend(QObject):
    _measurementChanged = pyqtSignal()
    def __init__(self, parent=None):
        super().__init__(parent)
        self._measurement = 0

    def new_measurement(self, measurement):
        measurement = measurement

    @pyqtProperty('QVariant', notify=_measurementChanged)
    def measurement(self):
        return self._measurement

    @measurement.setter
    def measurement(self, value):
        self._measurement = value
        self._measurementChanged.emit()

app = QApplication(sys.argv)
backend = Backend()

engine = QQmlApplicationEngine()
engine.rootContext().setContextProperty("backend", backend)
engine.load('qml/measurement_main.qml')

win = engine.rootObjects()[0]
win.show()
server.subscribe(backend.new_measurement)

app.exec_()