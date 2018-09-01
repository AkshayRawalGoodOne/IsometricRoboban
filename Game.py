import pygame
import math
import Movables
import Maps
import MapDescription as MD
import IsometricRender as IR
import datetime

Tile = pygame.image.load("TileBig.png")
Box = pygame.image.load("Box2.png")
BoxLit = pygame.image.load("Box2Lit.png")
PlayerUp = pygame.image.load("RoboUp.png")
PlayerDown = pygame.image.load("RoboDown.png")
PlayerRight = pygame.image.load("RoboRight.png")
PlayerLeft = pygame.image.load("RoboLeft.png")
pygame.init()

NumFont = pygame.font.SysFont("Futura", 30)
LevelFont = pygame.font.SysFont("Futura", 40)
LevelNumFont = pygame.font.SysFont("Futura", 70)

clock = pygame.time.Clock()
speed = 4
white = (255, 255, 255)
green = (100, 200, 0)
black = (0, 0, 0)
boxWidth = Tile.get_width()
boxHeight = Tile.get_height()
level = 1
map = Maps.map(level)
rows = len(map)
cols = len(map[0])
windowWidth = 800
windowHeight = 600
gameWidth = boxWidth * rows
gameHeight = boxHeight * cols
gameDisplay = pygame.display.set_mode((windowWidth, windowHeight))
mapImage = pygame.display.set_mode((windowWidth, windowHeight))
pygame.display.set_caption("Isometric Sokoban")
ObjectsList = []
CurrentBoxPositions = []

def clip(val, min, max):
    if val > max:
        return max
    elif val < min:
        return min
    return val

def levelWon():
    for x in range(rows):
        for y in range(cols):
            if map[x][y] == MD.TARGET and not hasBox(x,y):
                    return False

    return True

def hasBox(x, y):
    for object in ObjectsList:
        if object.id == "Box":
             obx, oby = getFlooredTileCoords(object.x, object.y)
             if obx == x and oby == y:
                 return True

    return False

def getRoundedTileCoords(PtX, PtY):
     coordX = (PtX/boxWidth) + (PtY - windowHeight/2)/(boxHeight)
     coordY = ( 2 * (PtX) / boxWidth) - coordX
     x = round(coordX, 0)
     y = round(coordY, 0)
     #print(x,y, "                              ", PtX, PtY)
     return [int(x), int(y)]


def getFlooredTileCoords(PtX, PtY):
    coordX = (PtX / boxWidth) + (PtY - windowHeight / 2) / (boxHeight)
    coordY = (2 * (PtX) / boxWidth) - coordX
    x = math.floor(coordX)
    y = math.floor(coordY)
    # print(x,y, "                              ", PtX, PtY)
    return [x, y]


def getCeiledTileCoords(PtX, PtY):
    coordX = (PtX / boxWidth) + (PtY - windowHeight / 2) / (boxHeight)
    coordY = (2 * (PtX) / boxWidth) - coordX
    x = math.ceil(coordX)
    y = math.ceil(coordY)
    # print(x,y, "                              ", PtX, PtY)
    return [x, y]

def movementAllowed(object, map, direction):
    if(direction == "Up" or direction == "Left"):
        (x, y)  = getCeiledTileCoords(object.x, object.y)
    elif(direction == "Down" or direction == "Right"):
        (x, y)  = getFlooredTileCoords(object.x, object.y)
    else:
         (x, y) = getFlooredTileCoords(object.x, object.y)
    if object.id == "Player":
        if direction == "Up" and (map[x-1][y] == MD.NOTHING or x == 0 or (hasBox(x-1, y) and (map[x-2][y] == MD.NOTHING or x-1 == 0 or hasBox(x-2, y)))):
            return False
        elif direction == "Down" and (x == rows - 1 or map[x+1][y] == MD.NOTHING or (hasBox(x+1, y) and (map[clip(x+2, 0, rows - 1)][y] == MD.NOTHING or x+1 == rows -1 or hasBox(x+2, y)))) :
            return False
        elif direction == "Right" and (y == cols - 1 or map[x][y+1] == MD.NOTHING or (hasBox(x, y+1) and (map[x][clip(y+2, 0, cols-1)] == MD.NOTHING or y+1 == cols -1 or hasBox(x, y+2)))) :
            return False
        elif direction == "Left" and (map[x][y-1] == MD.NOTHING or y == 0 or (hasBox(x, y-1) and (map[x][y-2] == MD.NOTHING or y-1 == 0 or hasBox(x, y-2)))):
            return False
    elif object.id == "Box":
        for obj in ObjectsList:
            if(obj.x != object.x and obj.y != object.y and obj.id != "Player"):
                obx, oby = getRoundedTileCoords(obj.x, obj.y)
                if direction == "Up" and (map[x - 1][y] == MD.NOTHING or x == 0 or (x-1 == obx and y == oby)):
                    return False
                elif direction == "Down" and (x == rows - 1 or map[x + 1][y] == MD.NOTHING or (x+1 == obx and y == oby)):
                    return False
                elif direction == "Right" and (y == cols - 1 or map[x][y + 1] == MD.NOTHING or (x == obx and y+1 == oby)):
                    return False
                elif direction == "Left" and (map[x][y - 1] == MD.NOTHING or y == 0 or (x == obx and y-1 == oby)):
                    return False

    return True


def inPosition(object):
    (x, y) = getRoundedTileCoords(object.x, object.y)
    if(object.id == "Box" and map[x][y] == MD.TARGET):
        object.img = BoxLit
    elif (object.id == "Box"):
        object.img = Box
    point1x = ((x + y) * (boxWidth / 2))
    point1y = windowHeight / 2 + ((x - y) * boxHeight / 2)
    #print(x, y, "                         ", object.x, object.y, "                             ", point1x, point1y)
    if (object.x > point1x):
       while object.x > point1x:
            object.x -= 1
            if(object.y > point1y):
                object.y -= 0.5
            elif(object.y < point1y):
                object.y += 0.5
    elif (object.x < point1x):
       while object.x < point1x:
            object.x += 1
            if(object.y > point1y):
                object.y -= 0.5
            elif(object.y < point1y):
                object.y += 0.5

    #print("Final Pos    ", x, y, "                         ", object.x, object.y, "                             ", point1x, point1y)

def drawMap(level):
    IR.placeTiles(Maps.map(level), gameDisplay, boxWidth, boxHeight, windowHeight, rows, cols)

def makeObjects():
    index = 0
    for y in range(cols-1, -1, -1):
        for x in range(rows):
            point1x = ((x + y) * (boxWidth / 2))
            point1y = windowHeight / 2 + ((x - y) * boxHeight / 2)
            if(map[x][y] == MD.PLAYER):
                object = Movables.Movables()
                object._init_("Player", point1x, (point1y), speed, PlayerDown)
                ObjectsList.append(object)
                print("Player Added at ", object.x, object.y)
                index += 1
            elif(map[x][y] == MD.BOX):
                object = Movables.Movables()
                object._init_("Box", point1x, (point1y), speed, Box)
                ObjectsList.append(object)
                print("Box Added at ", object.x, object.y)
                index += 1
    print("Object List Created")



def Gameloop():

    makeObjects()
    level = 1
    GameExit =  False
    startTime = datetime.datetime.now()


    for object in ObjectsList:
        if object.id == "Player":
            PlayerObject = object

    while not GameExit:

        canMoveUp = movementAllowed(PlayerObject, map, "Up")
        canMoveDown = movementAllowed(PlayerObject, map, "Down")
        canMoveRight = movementAllowed(PlayerObject, map, "Right")
        canMoveLeft = movementAllowed(PlayerObject, map, "Left")
        #print("Right : ", canMoveRight,"         Up : ", canMoveUp, "      Left : ", canMoveLeft, "      Down : ", canMoveDown )

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                GameExit = True
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and canMoveUp:
                    PlayerObject.img = PlayerUp
                    PlayerObject.direction = "Up"
                elif event.key == pygame.K_DOWN and canMoveDown:
                    PlayerObject.img = PlayerDown
                    PlayerObject.direction = "Down"
                elif event.key == pygame.K_RIGHT and canMoveRight:
                    PlayerObject.img = PlayerRight
                    PlayerObject.direction = "Right"
                elif event.key == pygame.K_LEFT and canMoveLeft:
                    PlayerObject.img = PlayerLeft
                    PlayerObject.direction = "Left"

            elif event.type == pygame.KEYUP:
                for object in ObjectsList:
                    inPosition(object)
                    object.direction = None

        for object in ObjectsList:
            if object.id != "Player" or object != None:
                if abs(object.x - PlayerObject.x) < boxWidth/2 and abs(object.y - PlayerObject.y) < boxHeight/2:
                    object.direction = PlayerObject.direction

        drawMap(1)
        #PlayerObject.move()
        for object in ObjectsList:
            object.render(gameDisplay)
            object.move(movementAllowed(object, map, object.direction))

        if PlayerObject.direction == "Right" or PlayerObject.direction == "Left":
            ObjectsList.sort(key = lambda Movables : (IR.Iso_to_2D(Movables.x, Movables.y)[0] * 1000 +  IR.Iso_to_2D(Movables.x, Movables.y)[1]))
        elif PlayerObject.direction == "Up" or PlayerObject.direction == "Down":
            ObjectsList.sort(key = lambda Movables : (IR.Iso_to_2D(Movables.x, Movables.y)[1] * 1000 +  IR.Iso_to_2D(Movables.x, Movables.y)[0]))

        currentTime = datetime.datetime.now()
        elapsedTime = str(currentTime - startTime)
        label= NumFont.render(elapsedTime, 1, white)
        LevelLabel = LevelFont.render("Level : ", 1, white)
        LevelNumLabel = LevelNumFont.render(str(level), 1, white)
        gameDisplay.blit(label, (0, 0))
        gameDisplay.blit(LevelLabel, (windowWidth - 150, 0))
        gameDisplay.blit(LevelNumLabel, (windowWidth-60, 0))
        pygame.display.update()
        gameDisplay.fill(black)
        clock.tick(30)

Gameloop()