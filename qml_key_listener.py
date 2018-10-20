import sys
import rx

from rx.concurrency import QtScheduler
from PyQt5 import QtCore
from PyQt5.QtCore import QObject, QUrl, pyqtSignal, pyqtSlot, pyqtProperty
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtWidgets import QApplication
from collections import defaultdict

import socket

manual = False
release = False

ip = '192.168.43.21'
scheduler = QtScheduler(QtCore)

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
address = (ip, 8000)

sock.setblocking(0)

#sock.sendto(bytes("0,0,0", "UTF-8"),address)

class Backend(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.keys = defaultdict(lambda:False)
        self.seq_no = 0
        self.robot_state = 0

    @pyqtSlot(str, bool)
    def forward(self, pressed, down):
        self.keys[pressed] = down
        print("Forward {} is {}".format(pressed, 'down' if down else 'up') )
    
    @pyqtSlot(int)
    def releaseManual(self, challenge_id):
        print("Go to challenge %d"%challenge_id)
        self.robot_state = challenge_id

    def get_command(self):
        leftMotorSpeed = 0
        rightMotorSpeed = 0
        forward = self.keys['w'] and not self.keys['s']
        backward = self.keys['s'] and not self.keys['w']
        right = self.keys['d'] and not self.keys['a']
        left  = self.keys['a'] and not self.keys['d']
        if forward:
            leftMotorSpeed += 500
            rightMotorSpeed += 500
        if backward:
            leftMotorSpeed -= 500
            rightMotorSpeed -= 500
        if right:
            rightMotorSpeed -= 250
            leftMotorSpeed += 250
        if left:
            rightMotorSpeed += 250
            leftMotorSpeed -= 250
        return leftMotorSpeed, rightMotorSpeed
    def send_packet(self, _):
        command = self.get_command()
        print("sending %f %f %d"%(command[0], command[1], self.robot_state))
        try:
            sock.sendto(bytes("%d, %f, %f, %f, %d" % \
            (self.seq_no, command[0], command[1], 0, self.robot_state), \
            "UTF-8"), address)
            self.seq_no += 1
        except:
            print("error")

app = QApplication(sys.argv)
backend = Backend()

engine = QQmlApplicationEngine()
engine.rootContext().setContextProperty("backend", backend)
engine.load('qml/keys.qml')

win = engine.rootObjects()[0]
win.show()

rx.Observable.interval(1000/30, scheduler=scheduler).subscribe(backend.send_packet)

app.exec_()