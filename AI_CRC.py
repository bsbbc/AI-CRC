import RPi.GPIO as GPIO
import time
import socket
import time
import os, sys

#version f

#socket setting
HOST = '172.20.10.12'
PORT = 9999
crc = ''

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((HOST, PORT))

server_socket.listen()

client_socket, addr=server_socket.accept()

print('Connected by', addr)

# restart preparation
executable = sys.executable
args = sys.argv[:]
args.insert(0, executable)

#GPIO setting
MOTER_A1 = 5
MOTER_A2 = 13
MOTER_B1 = 14
MOTER_B2 = 15
CLEAN_MOTER = 6
LEFT_SENSOR = 11
RIGHT_SENSOR = 9
FRONT_SENSOR = 10
GPIO.setmode(GPIO.BCM)
GPIO.setup(MOTER_A1,GPIO.OUT)
GPIO.setup(MOTER_A2,GPIO.OUT)
GPIO.setup(MOTER_B1,GPIO.OUT)
GPIO.setup(MOTER_B2,GPIO.OUT)
GPIO.setup(CLEAN_MOTER, GPIO.OUT) # GPIO Assign mode
GPIO.setup(LEFT_SENSOR, GPIO.IN)
GPIO.setup(RIGHT_SENSOR, GPIO.IN)
GPIO.setup(FRONT_SENSOR, GPIO.IN)

#RightBack
RB = GPIO.PWM(MOTER_A1, 50)
#RightFront
RF = GPIO.PWM(MOTER_A2, 50)
#LeftBack
LB = GPIO.PWM(MOTER_B1, 50)
#LeftFront
LF = GPIO.PWM(MOTER_B2, 50)



def MoveForward():
    GPIO.output(MOTER_A2, True)
    GPIO.output(MOTER_B2, True)
    time.sleep(0.3)
    GPIO.output(MOTER_A2, False)
    GPIO.output(MOTER_B2, False)
    time.sleep(1)

def MoveBackWard():
    GPIO.output(MOTER_A1, True)
    GPIO.output(MOTER_B1, True)
    time.sleep(0.3)
    GPIO.output(MOTER_A1, False)
    GPIO.output(MOTER_B1, False)
    time.sleep(1)
    
def MoveRight():
    GPIO.output(MOTER_A1, True)
    GPIO.output(MOTER_B2, True)
    time.sleep(0.3)
    GPIO.output(MOTER_A1, False)
    GPIO.output(MOTER_B2, False)
    time.sleep(1)
    
def MoveLeft():
    GPIO.output(MOTER_A2, True)
    GPIO.output(MOTER_B1, True)
    time.sleep(0.3)
    GPIO.output(MOTER_A2, False)
    GPIO.output(MOTER_B1, False)
    time.sleep(1)
#GPIO.cleanup()

#========================================SLAM===============================================

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

#direction must be north at first
def searchNonClean(currentX, currentY):
    # west
    dirIndex = 3
    MoveLeft()
    tempX = currentX - 1
    tempY = currentY
    cntDist = 1
    while wholeMap[tempX][tempY] != 1:
        if wholeMap[tempX][tempY] == 0:
            wholeMap[tempX][tempY] = 2
            for i in range(cntDist):
                MoveForward()
            print('')  
            for item in wholeMap:
                print(item)    
            return 'again', tempX, tempY, dirIndex
        tempX = tempX - 1
        cntDist = cntDist + 1
        
    # south
    dirIndex = 2
    MoveLeft()
    tempX = currentX
    tempY = currentY - 1
    cntDist = 1
    while wholeMap[tempX][tempY] != 1:
        if wholeMap[tempX][tempY] == 0:
            wholeMap[tempX][tempY] = 2
            for i in range(cntDist):
                MoveForward()
            print('')  
            for item in wholeMap:
                print(item)            
            return 'again', tempX, tempY, dirIndex
        tempY = tempY - 1
        cntDist = cntDist + 1

    # north
    dirIndex = 0
    MoveLeft()
    MoveLeft()
    tempX = currentX
    tempY = currentY + 1
    cntDist = 1
    while wholeMap[tempX][tempY] != 1:
        if wholeMap[tempX][tempY] == 0:
            wholeMap[tempX][tempY] = 2
            for i in range(cntDist):
                MoveForward()
            print('')  
            for item in wholeMap:
                print(item)    
            return 'again', tempX, tempY, dirIndex
        tempY = tempY + 1
        cntDist = cntDist + 1

    # east
    dirIndex = 1
    MoveRight()
    tempX = currentX + 1
    tempY = currentY
    cntDist = 1
    while wholeMap[tempX][tempY] != 1:
        if wholeMap[tempX][tempY] == 0:
            wholeMap[tempX][tempY] = 2
            for i in range(cntDist):
                MoveForward()
            print('')  
            for item in wholeMap:
                print(item)    
            return 'again', tempX, tempY, dirIndex
        tempX = tempX + 1
        cntDist = cntDist + 1
    

    return 'done', tempX, tempY


#AUTO Mode
def auto(crc):


    dirIndex = 0
    dir = directionList[dirIndex]
    xCnt = 0
    yCnt = 0
    x = 1
    y = 1
    prevSt = 'None'

    while (crc == 'CA'):
        GPIO.output(CLEAN_MOTER, 1) # on
        while (True):

            Left = False
            Right = False
            Front = False

            if GPIO.input(LEFT_SENSOR):
                print("left something")
                Left = True
            elif GPIO.input(RIGHT_SENSOR):
                print("right something")
                Right = True
            elif GPIO.input(FRONT_SENSOR):
                print("right something")
                Front = True
            else:
                print("unknown")
            time.sleep(0.2)

            #detect obstacle & slam
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

        #direction to north
        if (dirIndex == 1):
            MoveLeft()
        elif (dirIndex == 2):
            MoveLeft()
            MoveLeft()
        elif (dirIndex == 3):
            MoveRight()
        
        #SLAM FINISHED
        wholeMap = CntMapSize()
        for item in outerList:
            wholeMap[item[0]][item[1]] = 1
        
        #start cleaning
        continueYn = 'again'
        while (continueYn != 'done'):
            continueYn, A, B, dirIndex = searchNonClean(A, B)
            if (dirIndex == 1):
                MoveLeft()
            elif (dirIndex == 2):
                MoveLeft()
                MoveLeft()
            elif (dirIndex == 3):
                MoveRight()        

#===========================MODE SELECTION=============================================

while True:
    data = None
    data = client_socket.recv(1024)

    if not data :
        break
    
    print('Recived from', addr)
    print('Data : ', data.decode())

    crc = data.decode()
    #client_socket.sendall(data)
    
    #청소기 동작/취소 명령어 실행

    if crc == 'P0':
        print('come')
        GPIO.output(CLEAN_MOTER, 1)
        os.execvp(executable, args) # 재실행
    elif crc == 'P1' :
        GPIO.output(CLEAN_MOTER, 0)
        os.execvp(executable, args)
    elif crc == "GO" :
        print("1")
        MoveForward()
    elif crc == "BACK" :
        MoveBackWard()
    elif crc == "L" :
        MoveLeft()
    elif crc == "R" :
        MoveRight()
    elif crc == 'CA':
        auto(crc)
    elif crc == 'CM':
        GPIO.cleanup()
        os.execvp(executable, args)
    os.execvp(executable, args)






