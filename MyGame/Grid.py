import pygame as py
from pygame import mixer
from random import randint
from player import Player, Obstacle
py.mixer.init()

cell_w, cell_h = 60, 60
row, col = 9, 9
screen_w, screen_h = col * cell_w, row*cell_h
panel_w = 3 * cell_w
screen = py.display.set_mode((screen_w + panel_w, screen_h))
py.display.set_caption("Character Select")

grid = [[randint(0,4) for i in range(col)] for j in range(row)]
grid[0][0], grid[0][1], grid[1][0] = 1, 1, 1
for r in grid:
    print(r)


wizard = py.image.load("C:\\Users\\01Solec\\PreDP2-LeonT\\MyGame\\Wizard.png.png")
wizard = py.transform.scale(wizard, (60, 60))
knight = py.image.load("C:\\Users\\01Solec\\PreDP2-LeonT\\MyGame\\Knight-removebg-preview.png")
knight = py.transform.scale(knight, (60, 60))    
spikes = py.image.load("C:\\Users\\01Solec\\PreDP2-LeonT\\MyGame\\Spikes-removebg-preview.png")
spikes = py.transform.scale(spikes, (60, 60))
coin_sound = py.mixer.Sound("C:\\Users\\01Solec\\PreDP2-LeonT\\MyGame\\ribhavagrawal-coin-recieved-230517.mp3")
coin_img = py.image.load("C:\\Users\\01Solec\\PreDP2-LeonT\\MyGame\\Gold-Coin.png")
coin_img = py.transform.scale(coin_img, (60, 60))
background = py.image.load("C:\\Users\\01Solec\\PreDP2-LeonT\\MyGame\\Desert.webp")
background = py.transform.scale(background, (600, 600))

p1 = Player(0, 0, 60, 60, knight)
obstacleList = []
for r in range(row):
    for c in range(col):
        if grid[r][c] == 0:
            obstacleList.append(Obstacle(c*cell_w, r*cell_h, spikes))

clock = py.time.Clock()
py.init()
screen = py.display.set_mode((screen_w + panel_w,screen_h))
py.display.set_caption("Generating random grid")


def drawGrid(grid:list[list]):
    index = 0
    for r in range(row):
        for c in range(col):
            if grid[r][c] == 0:
                obstacleList[index].draw(screen)
                index += 1
            if grid[r][c] == 6:
                screen.blit(coin_img, (c * cell_w, r * cell_h))

coin = 0
def draw_panel(screen):
    font = py.font.SysFont(None, 30)
    py.draw.rect(screen, "#8BD0CA", (screen_w, 0, panel_w, screen_h))
    textSurface = font.render(f"Coins: {coin}", True, "#ffffff")
    screen.blit(textSurface, (screen_w + 20, 40))

def find(coin):
    r = p1.y // 60
    c = p1.x // 60  
    if event.type == py.KEYDOWN:
        if event.key == py.K_SPACE and grid[r][c] == 3:
            coin += 1
            grid[r][c] = 6
            coin_sound.play() 
    return coin     

run = True
while run:
    for event in py.event.get():
        if event.type == py.QUIT:
            run = False
        p1.move(screen, grid, event)
        coin = find(coin)
    clock.tick(15)
    screen.blit(background, (0,0))
    drawGrid(grid)
    draw_panel(screen)
    p1.draw(screen)
    py.display.flip()
py.quit()

