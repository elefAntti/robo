import sys
from PyQt5 import QtCore
from PyQt5.QtCore import QObject, QUrl, pyqtSignal, pyqtSlot, pyqtProperty
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtWidgets import QApplication

class Backend(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)

    @pyqtSlot(str, bool)
    def forward(self, pressed, down):
        print("Forward {} is {}".format(pressed, 'down' if down else 'up') )

app = QApplication(sys.argv)
backend = Backend()

engine = QQmlApplicationEngine()
engine.rootContext().setContextProperty("backend", backend)
engine.load('examples/keys.qml')

win = engine.rootObjects()[0]
win.show()

app.exec_()