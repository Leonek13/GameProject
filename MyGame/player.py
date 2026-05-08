import pygame as py
from random import randint
py.mixer.init()
class Player:
    '''
    Player is a rectangle object of pygame
    So it must take x, y, width and height
    '''

    dig = py.mixer.Sound("C:\\Users\\01Solec\\PreDP2-LeonT\\GameProject\\Pig_idle2.oga")
    def __init__(self, x, y, w, h, img, class_name: str = "Knight"):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.img = img
        self.rect = (self.x, self.y, self.w, self.h)
        self.collide = False
        self.max_hp = 100
        self.hp = self.max_hp
        self.xp = 0
        self.lvl = 1
        self.dmg = 10
        self.class_name = class_name
        self.has_weapon = False
        self.has_key = False
        self.iframes = 0
        self.iframes_max = 45



    
    def draw(self, screen):
         screen.blit(self.img, (self.x, self.y))
         bar_w = self.w 
         filled = int(bar_w * self.hp / self.max_hp)
         py.draw.rect(screen, "#fffb00", (self.x, self.y + self.h + 2, bar_w, 5))
    
    def move(self, screen:any, grid:list[list], event):
        r = self.y // 60
        c = self.x // 60   
        if event.type == py.KEYDOWN:
            if event.key == py.K_LEFT and c - 1 >= 0 and grid[r][c-1] != 0:
                self.x -= 60
            if event.key == py.K_RIGHT and c + 1 < len(grid[0]) and grid[r][c+1] != 0:
                self.x += 60
            if event.key == py.K_UP and r - 1 >= 0 and grid[r-1][c] != 0:
                self.y -= 60
            if event.key == py.K_DOWN and r + 1 < len(grid) and grid[r+1][c] != 0:
                self.y += 60

    def collision(self, enemy):
        if abs(self.x - enemy.x) <= self.w and abs(self.y - enemy.y) <= self.h:
            if self.collide == False:
                print("collision")
                self.collide = True
        elif self.collide == True:
            self.collide = False


class Obstacle:
    '''
    This is an obstacle class which will have fixed size for now
    and we only need to store (x, y) coordinates.
    '''

    def __init__(self, x:int, y:int, img):
        self.x = x
        self.y = y
        self.img = img

    def draw(self, screen):
        screen.blit(self.img, (self.x, self.y))

class Enemy: 
    '''
    This is an enemy class which will be destroyed by the player
    '''

    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.max_hp = 40
        self.hp = self.max_hp
        self.dmg = 10
        self.alive = True

    def draw(self, screen):
        if self.alive:
            screen.blit(self.img, (self.x, self.y))
            py.draw.rect(screen, "#de1414", (self.x, self.y - 10, 60, 5))
            green = int(60 * self.hp / self.max_hp)
            py.draw.rect(screen, "#16d927", (self.x, self.y, -10, green, 5))

    def take_damage(self, amount):
        self.hp -= amount
        if self.hp <= 0:
            self.alive = False
            