import pygame as py
py.init()

w, h = 600, 600
screen = py.display.set_mode((w, h))
py.display.set_caption("Working with Images in Pygame")
img = py.image.load("C:\\Users\\01Solec\\PreDP2-LeonT\\GameProject\\dino.png")
img = py.transform.scale(img, (60, 60))
x, y = 0, 0
clock = py.time.Clock()
run = True
while run:
    clock.tick(25)
    for event in py.event.get():
        if event.type == py.QUIT:
            run = False
    screen.fill("#ffffff")
    screen.blit(img, (x, y))
    x, y = x+1, y +1
    
    py.display.flip()

py.quit()
