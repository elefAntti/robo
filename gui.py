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

scheduler = QtScheduler(QtCore)

#kommentti

class Backend(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._commandSubject = BehaviorSubject(kine.Command.arc(0, 0))

    @pyqtSlot()
    def forward(self):
        self._commandSubject.on_next(kine.Command.arc(0.5, 0.0))

    @pyqtSlot()
    def backward(self):
        self._commandSubject.on_next(kine.Command.arc(-0.5, 0.0))

    @pyqtSlot()
    def left(self):
        self._commandSubject.on_next(kine.Command.arc(0.5, 0.5))

    @pyqtSlot()
    def right(self):
        self._commandSubject.on_next(kine.Command.arc(0.5, -0.5))

    @pyqtSlot()
    def stop(self):
        self._commandSubject.on_next(kine.Command.arc(0.0, 0.0))

    @pyqtSlot()
    def pivotLeft(self):
        self._commandSubject.on_next(kine.Command(
            velocity = 0,
            angularVelocity=0.3))

    @pyqtSlot()
    def pivotRight(self):
        self._commandSubject.on_next(kine.Command(
            velocity = 0,
            angularVelocity=-0.3))

    @pyqtSlot()
    def toOrigin(self):
        self._commandSubject.on_next(
            kine.Command.arc_to(self.robot.pose, Vec2.zero(), 0.5))

    @property
    def commands(self):
        return self._commandSubject


class GuiRobot(QObject):
    _xChanged = pyqtSignal()
    _yChanged = pyqtSignal()
    _headingChanged = pyqtSignal()
    _leftVelChanged = pyqtSignal()
    _rightVelChanged = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._x = 0
        self._y = 0
        self._heading = 0
        self._left_wheel_vel = 0
        self._right_wheel_vel = 0

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

    @pyqtProperty('QVariant', notify=_leftVelChanged)
    def leftWheelVel(self):
        return self._left_wheel_vel

    @pyqtProperty('QVariant', notify=_rightVelChanged)
    def rightWheelVel(self):
        return self._right_wheel_vel

    @property
    def pose(self):
        return Transform(self.heading, Vec2(self.x, self.y))
    
    def setPose(self, pose):
        self.x = pose.x
        self.y = pose.y
        self.heading = pose.heading
        self._headingChanged.emit()
    

    def setWheelCommand(self, command):
        self._left_wheel_vel = command.left_angular_vel
        self._right_wheel_vel = command.right_angular_vel
        self._leftVelChanged.emit()
        self._rightVelChanged.emit()

def simulateRobot(initial_pose, commands, timestep_ms=30, scheduler=scheduler):
    return rx.Observable.interval(timestep_ms, scheduler=scheduler)\
        .with_latest_from(commands, lambda idx, command: command)\
        .scan(
            lambda pose, command: kine.predictPose(pose, command, timestep_ms/1000),
            initial_pose)

app = QApplication(sys.argv)
backend = Backend()
robot = GuiRobot()
backend.robot = robot

backend.commands.subscribe(lambda command: print("Received "+str(command)))

simulation = simulateRobot(Transform.identity(), backend.commands)
simulation.subscribe(robot.setPose)

kinematics = kine.KinematicModel(axel_width = 0.2, left_wheel_r = 0.03, right_wheel_r = 0.03)
backend.commands.map(kinematics.computeWheelCommand)\
    .subscribe(robot.setWheelCommand)

engine = QQmlApplicationEngine()
engine.rootContext().setContextProperty("backend", backend)
engine.rootContext().setContextProperty("robot", robot)
engine.load('main.qml')

win = engine.rootObjects()[0]
win.show()

app.exec_()
