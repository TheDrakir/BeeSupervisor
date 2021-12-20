from Focuser import Focuser
from time import sleep
from math import atan, degrees


class Laser:
    zeroAngleX = 80
    servoOffsetX = 0
    zeroAngleY = 35
    def __init__(self, laserHeight=13.5, boardWidth=37.5, boardLength=8): 
        self.laserHeight = laserHeight
        self.boardWidth = boardWidth
        self.boardLength = boardLength
        self.focuser = Focuser(1)

    def calculateAngle(self, distanceToMiddle):
        tanAngle = distanceToMiddle / self.laserHeight
        return int(degrees(atan(tanAngle)))

    def pointAt(self, x, y):
        distY = y - self.boardLength / 2.
        angleY = self.calculateAngle(distY) + Laser.zeroAngleY
        self.setY(angleY)
        distX = x - self.boardWidth / 2.
        # distX = (distX**2 + distY ** 2) ** 0.5
        angleX = self.calculateAngle(distX) + Laser.zeroAngleX
        self.setX(angleX)

	
    def toggle(self):
        pass

    def setX(self, angle):
        if angle < 10 or angle > 150: return
        sleep(.02)
        self.focuser.set(Focuser.OPT_MOTOR_X, angle)

    def setY(self, angle):
        if angle < 10 or angle > 60: return
        sleep(.02)
        self.focuser.set(Focuser.OPT_MOTOR_Y, angle)
    
    def resetPosition(self):
        self.setX(Laser.zeroAngleX)
        self.setY(Laser.zeroAngleY)
        
    

if __name__ == "__main__":
    laser = Laser()

    for _ in range(10):
        laser.pointAt(40, 2.)
        sleep(.1)
        laser.pointAt(40, 4.)
        sleep(.1)
        laser.pointAt(40, 6.)
        sleep(.1)

    laser.resetPosition()
    sleep(1)

    for _ in range(10):
        laser.pointAt(40, 2.)
        sleep(.05)
        laser.pointAt(40, 4.)
        sleep(.05)
        laser.pointAt(40, 6.)
        sleep(.05)

    laser.resetPosition()
    sleep(1)

    for _ in range(10):
        laser.pointAt(40, 2.)
        sleep(.3)
        laser.pointAt(40, 4.)
        sleep(.3)
        laser.pointAt(-5, 6.)
        sleep(.3)
        laser.pointAt(-5, 2.)
        sleep(.3)

    laser.resetPosition()