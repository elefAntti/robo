import sys

import rx
from rx.subjects import BehaviorSubject
from rx.concurrency import QtScheduler
from PyQt5 import QtCore
from PyQt5.QtCore import QObject, QUrl, pyqtSignal, pyqtSlot, pyqtProperty
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtWidgets import QApplication

from vec2 import Transform, Vec2
import kinematics as kine

class Backend(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.robot = None
        self._commandSubject = BehaviorSubject(kine.Command(0, 0))

    @pyqtSlot()
    def forward(self):
        self._commandSubject.on_next(kine.Command(0.5, 0.0))

    @pyqtSlot()
    def backward(self):
        self._commandSubject.on_next(kine.Command(-0.5, 0.0))

    @pyqtSlot()
    def left(self):
        self._commandSubject.on_next(kine.Command(0.5, 0.5))

    @pyqtSlot()
    def right(self):
        self._commandSubject.on_next(kine.Command(0.5, -0.5))

    @pyqtSlot()
    def stop(self):
        self._commandSubject.on_next(kine.Command(0.0, 0.0))

    @pyqtSlot()
    def pivotLeft(self):
        self._commandSubject.on_next(kine.PivotCommand(0.3))

    @pyqtSlot()
    def pivotRight(self):
        self._commandSubject.on_next(kine.PivotCommand(-0.3))

    @property
    def commands(self):
        return self._commandSubject


class GuiRobot(QObject):
    _xChanged = pyqtSignal()
    _yChanged = pyqtSignal()
    _headingChanged = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._x = 0
        self._y = 0
        self._heading = 0

    @pyqtProperty('QVariant', notify=_xChanged)
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value
        self._xChanged.emit()

    @pyqtProperty('QVariant', notify=_yChanged)
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value
        self._yChanged.emit()

    @pyqtProperty('QVariant', notify=_headingChanged)
    def heading(self):
        return self._heading

    @heading.setter
    def heading(self, value):
        self._heading = value
        self._headingChanged.emit()

    def setPose(self, pose):
        self.x = pose.x
        self.y = pose.y
        self.heading = pose.heading
        self._headingChanged.emit()


def simulateRobot(commands):
    dt = 30
    return rx.Observable.interval(dt, scheduler=scheduler)\
        .with_latest_from(commands, lambda idx, command: command)\
        .scan(
            lambda pose, command: kine.predictPose(pose, command, dt/1000),
            Transform(heading = 0, offset=Vec2(0, 0))
        )

scheduler = QtScheduler(QtCore)
app = QApplication(sys.argv)
backend = Backend()
robot = GuiRobot()
robot.heading = 0.5
backend.robot = robot

backend.commands.subscribe(lambda command: print("Received "+str(command)))

simulateRobot(backend.commands) \
    .subscribe(robot.setPose)

engine = QQmlApplicationEngine()
engine.rootContext().setContextProperty("backend", backend)
engine.rootContext().setContextProperty("robot", robot)
engine.load('main.qml')

win = engine.rootObjects()[0]
win.show()

app.exec_()
