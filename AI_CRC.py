import RPi.GPIO as GPIO
import time

#version 9.0

#GPIO setting
MOTER_A1 = 5
MOTER_A2 = 6
MOTER_B1 = 20
MOTER_B2 = 21
CLEAN_MOTER = 13
GPIO.setmode(GPIO.BCM)
GPIO.setup(MOTER_A1,GPIO.OUT)
GPIO.setup(MOTER_A2,GPIO.OUT)
GPIO.setup(MOTER_B1,GPIO.OUT)
GPIO.setup(MOTER_B2,GPIO.OUT)
GPIO.setup(CLEAN_MOTER, GPIO.OUT) # GPIO Assign mode

#RightBack
RB = GPIO.PWM(MOTER_A1, 50)
#RightFront
RF = GPIO.PWM(MOTER_A2, 50)
#LeftBack
LB = GPIO.PWM(MOTER_B1, 50)
#LeftFront
LF = GPIO.PWM(MOTER_B2, 50)

def MoveForward():
   LF.start(0)
   RF.start(0)
   LF.ChangeDutyCycle(25)
   RF.ChangeDutyCycle(25)
   time.sleep(2)
   LF.stop()
   RF.stop()

def MoveBackWard():
   RB.start(0)
   LB.start(0)
   LB.ChangeDutyCycle(23)
   RB.ChangeDutyCycle(28)
   time.sleep(2)
   LB.stop()
   RB.stop()

def MoveRight():
   LF.start(0)
   RB.start(0)
   LF.ChangeDutyCycle(24)
   RB.ChangeDutyCycle(25)
   time.sleep(1)
   LF.stop()
   RB.stop()

def MoveLeft():
   LB.start(0)
   RF.start(0)
   LB.ChangeDutyCycle(24)
   RF.ChangeDutyCycle(25)
   time.sleep(1)
   LB.stop()
   RF.stop()

GPIO.cleanup()

#===========================SLAM============================

wholeMap = []
directionList = ['north','east','south','west']

nsList = [0]
ewList = [0]

#x,y coordinate
outerList = []
innerList = []


#analyzing the whole map
def FindBoundary(dir,prevSt,x,y):
    if dir == 'north':
        x = x + 1
        if (prevSt == 'L'):
            innerList = [x,y-1]
        elif (prevSt == 'R'):
            innerList = [x,y+1]
    elif dir == 'south':
        x = x - 1
        if (prevSt == 'L'):
            innerList = [x,y+1]
        elif (prevSt == 'R'):
            innerList = [x,y-1]
    elif dir == 'east':
        y = y + 1
        if (prevSt == 'L'):
            innerList = [x+1,y]
        elif (prevSt == 'R'):
            innerList = [x-1,y]
    elif dir == 'west':
        y = y - 1
        if (prevSt == 'L'):
            innerList = [x-1,y]
        elif (prevSt == 'R'):
            innerList = [x+1,y]
    return x,y,innerList


def CntXY(dir,xCnt,yCnt):
    if dir == 'north':
        xCnt = xCnt + 1
        nsList.append(xCnt)
    elif dir == 'south':
        xCnt = xCnt - 1
        nsList.append(xCnt)
    elif dir == 'east':
        yCnt = yCnt + 1
        ewList.append(yCnt)
    elif dir == 'west':
        yCnt = yCnt - 1
        ewList.append(yCnt)
    return xCnt, yCnt

def CntMapSize():
    maxNS = max(nsList)
    minNS = min(nsList)
    maxEW = max(nsList)
    minEW = min(nsList)

    xSize = maxNS - minNS + 1
    ySize = maxEW - minEW + 1

    matrix = [[0 for col in range(xSize+1)] for row in range(ySize+1)]
    return matrix

def dirChange(dirIndex):
    if (dirIndex == 4):
        dirIndex = 0
    elif (dirIndex == -1):
        dirIndex = 3
    return dirIndex








#CM(control mode), CA(control auto)
MODE = 'CM'

def main():
    #AUTO Mode
    dirIndex = 0
    dir = directionList[dirIndex]
    xCnt = 0
    yCnt = 0
    x = 1
    y = 1
    prevSt = 'None'
    while (MODE is 'CA'):
        GPIO.output(CLEAN_MOTER, 1) # on
        while (bottom is True):
            if (Left is True):
                prevSt = 'L'
                MoveForward()
                dir = directionList[dirIndex]
                xCnt, yCnt = CntXY(dir, xCnt, yCnt)
                x, y, innerList = FindBoundary(dir, prevSt, x, y)
                outerList.append(innerList)
            elif (Right is True):
                prevSt = 'R'
                MoveForward()
                dir = directionList[dirIndex]
                xCnt, yCnt = CntXY(dir, xCnt, yCnt)
                x, y, innerList = FindBoundary(dir, prevSt, x, y)
                outerList.append(innerList)
            elif (Left is True and Front is True):
                MoveRight()
                dirIndex = dirChange(dirIndex+1)
                dir = directionList[dirIndex]
            elif (Right is True and Front is True):
                MoveLeft()
                dirIndex = dirChange(dirIndex-1)
                dir = directionList[dirIndex]
            elif (Left is False and Right is False and Front is False):
                if (prevSt == 'L'):
                    MoveLeft()
                    dirIndex = dirChange(dirIndex-1)
                    dir = directionList[dirIndex]                    
                    MoveForward()
                elif (prevSt == 'R'):
                    MoveRight()
                    dirIndex = dirChange(dirIndex+1)
                    dir = directionList[dirIndex]                    
                    MoveForward()
            
            if (innerList == [1,1]):
                break
        wholeMap = CntMapSize()
        for item in outerList:
            wholeMap[item[0]][item[1]] = 1


        



    #CONTROL Mode
    while (MODE is 'CM'):
        if (CLEANER == 'P1'):
            GPIO.output(CLEAN_MOTER, 1) # on
        elif(CLEANER == 'P0'):
            GPIO.output(CLEAN_MOTER, 0) # off
        break
       #get motor speed from the device
       



