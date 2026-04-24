import pygame as py
from player import Player

py.init()
w, h = 600, 600
screen = py.display.set_mode((w, h))
py.display.set_caption("Creating player object")

p1 = Player(w/2, h/2, 50, 50)
p2 = Player(500, 500, 50, 50)
print(screen.get_width())   

run = True
clock = py.time.Clock()
while run:
    for event in py.event.get():
        if event.type == py.QUIT:
            run = False
    clock.tick(60) 
    screen.fill("#ACA5A5")

    p1.draw(screen)
    p2.draw(screen)
    p1.move(screen)
    p1.collision(p2)
    
    py.display.flip()

py.quit()