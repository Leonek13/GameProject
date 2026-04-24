import pygame as py
from random import randint
py.init()

def randomColor():
    r = randint(0, 255)
    g = randint(0, 255)
    b = randint(0, 255)
    return(r, g, b)

def randomSpeed():
    return randint(1, 15)

sHeight = 600
sWidth = 600
screen = py.display.set_mode((600, 600))
x, y = sWidth/2, sHeight/2
xSquare, ySquare = sWidth/2, sHeight/2
speedX, speedY = 5, 8
speedXSquare, speedYSquare = 11, 17
rgb = randomColor()

running = True
screen.fill("#ffffff")
while running:
    for event in py.event.get():
        if event.type == py.QUIT:
            running = False
    py.draw.circle(screen, rgb, (x, y), 25)
    py.display.flip()
    if x + 50 > 600 or x - 50 < 0:
        speedX = -speedX/abs(speedX)*randomSpeed()
        rgb = randomColor()
    x += speedX
    if y + 50 > 600 or y - 50 < 0:
        speedY = -speedY/abs(speedY)*randomSpeed()
        rgb = randomColor()
    y += speedY
    py.time.delay(10)
py.quit()