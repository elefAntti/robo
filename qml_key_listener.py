import sys
from PyQt5 import QtCore
from PyQt5.QtCore import QObject, QUrl, pyqtSignal, pyqtSlot, pyqtProperty
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtWidgets import QApplication
from collections import defaultdict

import socket

manual = False
release = False

ip = '192.168.43.21'

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
address = (ip, 8000)

#sock.sendto(bytes("0,0,0", "UTF-8"),address)

class Backend(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.keys = defaultdict(lambda:False)

    @pyqtSlot(str, bool)
    def forward(self, pressed, down):
        self.keys[pressed] = down
        print("Forward {} is {}".format(pressed, 'down' if down else 'up') )
        command = self.get_command()
        print("sending %f %f"%command)
        sock.sendto(bytes("%f, %f, %f" % \
        (command[0], command[1], 0), \
        "UTF-8"), address)

    def get_command(self):
        leftMotorSpeed = 0
        rightMotorSpeed = 0
        forward = self.keys['w'] and not self.keys['s']
        backward = self.keys['s'] and not self.keys['w']
        right = self.keys['d'] and not self.keys['a']
        left  = self.keys['a'] and not self.keys['d']
        if forward:
            leftMotorSpeed += 100
            rightMotorSpeed += 100
        if backward:
            leftMotorSpeed -= 100
            rightMotorSpeed -= 100
        if right:
            rightMotorSpeed -= 50
            leftMotorSpeed += 50
        if left:
            rightMotorSpeed += 50
            leftMotorSpeed -= 50
        return leftMotorSpeed, rightMotorSpeed

app = QApplication(sys.argv)
backend = Backend()

engine = QQmlApplicationEngine()
engine.rootContext().setContextProperty("backend", backend)
engine.load('qml/keys.qml')

win = engine.rootObjects()[0]
win.show()

app.exec_()