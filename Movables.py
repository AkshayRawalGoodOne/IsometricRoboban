import pygame

class Movables():

    def _init_(self, id, x, y, speed, img):
        self.id = id
        self.x = x
        self.y = y
        self.speed = speed
        self.img = img
        self.direction = None

    def move(self, condition):
        if condition:
            if(self.direction == "Up"):
                self.x -= self.speed
                self.y -= self.speed/2
            elif (self.direction == "Down"):
                self.x += self.speed
                self.y += self.speed / 2
            elif (self.direction == "Right"):
                self.x += self.speed
                self.y -= self.speed / 2
            elif (self.direction == "Left"):
                self.x -= self.speed
                self.y += self.speed / 2



    def getXY_(self):
        return (self.x, self.y)

    def render(self, Surface):
        boundy = self.y - self.img.get_height() / 2
        Surface.blit(self.img, (self.x, boundy))
        #pygame.display.update((self.x, self.y, self.img.get_width(), self.img.get_height()))





