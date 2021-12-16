import time

outList = [[3,0],[3,3],[3,2],[0,3],[1,3],[2,3],[0,4],[0,5],[0,6],[0,7],[1,7],[2,7],[3,7],[4,7],[5,7],[6,7],[6,6],[6,5],[6,4],[6,3],[6,2],[6,1],[6,0],[4,0],[5,0],[3,1]]
wholeMap = [[0 for col in range(8)] for row in range(7)]
# wholeMap[6][5] = 2

# outList = [[0,0],[0,1],[0,2],[0,3],[0,5],[0,6],[0,7],[1,0],[1,3],[1,5],[1,7],[2,0],[2,3],[2,5],[2,7],[3,0],[3,3],[3,4],[3,5],[3,7],[4,0],[4,7],[5,0],[5,1],[5,2],[5,3],[5,4],[5,5],[5,6],[5,7]]
# wholeMap = [[0 for col in range(8)] for row in range(6)]

for item in outList:
    wholeMap[item[0]][item[1]] = 1


print('--------------------매핑 예제-------------------------')
for item in wholeMap:
    print(item)
print('----------------------------------------------------')
time.sleep(1)
x = 1
y = 1
# currentLoc = [x,y]


# #north
# while wholeMap[x][y] != 1:
#     break
#     moveForward()
#     if wholeMap[x][y] == 0:
#         pass

# print(wholeMap[1][1])
# wholeMap[1][1] = 1
# print(wholeMap[5][1])

dirIndex = 1
#방향이 북쪽으로 이 함수 시작
def searchNonClean(currentX, currentY):
    # west
    dirIndex = 3
    # MoveLeft()
    tempX = currentX - 1
    tempY = currentY
    cntDist = 1
    while wholeMap[tempX][tempY] != 1:
        if wholeMap[tempX][tempY] == 0:
            wholeMap[tempX][tempY] = 2
            for i in range(cntDist):
                # MoveFront()
                pass
            print('')  
            for item in wholeMap:
                print(item)    
            return 'again', tempX, tempY
        tempX = tempX - 1
        cntDist = cntDist + 1
        
    # south
    dirIndex = 2
    # MoveLeft()
    tempX = currentX
    tempY = currentY - 1
    cntDist = 1
    while wholeMap[tempX][tempY] != 1:
        if wholeMap[tempX][tempY] == 0:
            wholeMap[tempX][tempY] = 2
            for i in range(cntDist):
                # MoveFront()
                pass
            print('')  
            for item in wholeMap:
                print(item)            
            return 'again', tempX, tempY
        tempY = tempY - 1
        cntDist = cntDist + 1

    # north
    dirIndex = 0
    # MoveLeft()
    tempX = currentX
    tempY = currentY + 1
    cntDist = 1
    while wholeMap[tempX][tempY] != 1:
        if wholeMap[tempX][tempY] == 0:
            wholeMap[tempX][tempY] = 2
            for i in range(cntDist):
                # MoveFront()
                pass
            print('')  
            for item in wholeMap:
                print(item)    
            return 'again', tempX, tempY
        tempY = tempY + 1
        cntDist = cntDist + 1

    # east
    dirIndex = 1
    # MoveLeft()
    tempX = currentX + 1
    tempY = currentY
    cntDist = 1
    while wholeMap[tempX][tempY] != 1:
        if wholeMap[tempX][tempY] == 0:
            wholeMap[tempX][tempY] = 2
            for i in range(cntDist):
                # MoveFront()
                pass
            print('')  
            for item in wholeMap:
                print(item)    
            return 'again', tempX, tempY
        tempX = tempX + 1
        cntDist = cntDist + 1
    

    return 'done', tempX, tempY

A = 6
B = 5
testChar = 'again'
while (testChar != 'done'):
    testChar, A, B = searchNonClean(A, B)
    time.sleep(1.5)
    # print(dirIndex)
# print(testChar)