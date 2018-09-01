import pygame
import MapDescription as MD

Tile = pygame.image.load("Tile0.png")
Target = pygame.image.load("Tile3.png")
Box = pygame.image.load("Box2.png")

def twoD_to_Iso(ptX, ptY):
    isoX =  ptX - ptY
    isoY = (ptX + ptY)/2
    return (isoX, isoY)

def Iso_to_2D(isoX, isoY):
    ptX = (2 * isoY + isoX) / 2
    ptY = (2 * isoY - isoX) / 2
    return (ptX, ptY)

def placeTiles(map, gameDisplay, tileWidth, tileHeight, windowHeight, rows, cols):

    for y in range(cols-1, -1, -1):
        for x in range(rows):
            point1x = ((x + y) * (tileWidth / 2))
            point1y = windowHeight/2 + ((x - y) * tileHeight/2)
            if(map[x][y] != MD.NOTHING and map[x][y] != MD.TARGET):
                point1 = (point1x, int(point1y))
                gameDisplay.blit(Tile, point1)
            elif (map[x][y] == MD.TARGET):
                point1 = (point1x, int(point1y))
                gameDisplay.blit(Target, point1)


