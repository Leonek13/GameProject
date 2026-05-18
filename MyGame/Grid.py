import pygame as py
from pygame import mixer
from random import randint
from player import Player, Obstacle, Enemy
py.init()
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

archer = py.image.load("C:\\Users\\01Solec\\Documents\\PygameProjectRepo\\GameProject\\MyGame\\Archer.png")
archer = py.transform.scale(archer, (60, 60))
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
enemy_img = py.image.load("C:\\Users\\01Solec\\Documents\\PygameProjectRepo\\GameProject\\MyGame\\zombie.webp")
enemy_img = py.transform.scale(enemy_img, (60, 60))

def character_select():
    '''
    Shows a selection screen with three characters.
    '''
    font_title = py.font.SysFont(None, 60)
    font_label = py.font.SysFont(None, 32)
    font_hint = py.font.SysFont(None, 24)

    characters = [
        {"name": "Knight", "img": knight},
        {"name": "Wizard", "img": wizard},
        {"name": "Archer", "img": archer},
    ]

    preview_size = 120
    previews = [py.transform.scale(c["img"], (preview_size, preview_size)) for c in characters]

    spacing = (screen_w + panel_w) // (len(characters) + 1)
    card_w, card_h = preview_size + 20, preview_size + 50
    rects = []
    for i in range(len(characters)):
        cx = spacing * (i + 1) - card_w // 2
        cy = screen_h // 2 - card_h // 2
        rects.append(py.Rect(cx, cy, card_w, card_h))

    selected = None
    hovered = None

    while selected is None:
        screen.fill("#1e1428")

        title_surf = font_title.render("Choose Your Character", True, "#ffdc64")
        screen.blit(title_surf, ((screen_w + panel_w) // 2 - title_surf.get_width() // 2, 60))
        hint_surf = font_hint.render("Click to Select", True, "#b4b4b4")
        screen.blit(hint_surf, ((screen_w + panel_w) // 2 - hint_surf.get_width() // 2, 130))
        mouse_pos = py.mouse.get_pos()
        hovered = None
        for i, rect in enumerate(rects):
            if rect.collidepoint(mouse_pos):
                hovered = i
        for i, (char, rect) in enumerate(zip(characters, rects)):
            color = "#503c6e" if hovered == i else "#322846"
            border_color = "#ffdc64" if hovered == i else "#645082"
            py.draw.rect(screen, color, rect, border_radius = 12)
            py.draw.rect(screen, border_color, rect, width = 3, border_radius = 12)
            img_x = rect.x + (card_w - preview_size) // 2
            img_y = rect.y + 10
            screen.blit(previews[i], (img_x, img_y))
            label = font_label.render(char["name"], True, "#ffffff")
            screen.blit(label, (rect.x + card_w // 2 - label.get_width() // 2, rect.y + preview_size + 18))
        
        py.display.flip()

        for event in py.event.get():
            if event.type == py.QUIT:
                py.quit()
                exit()
            if event.type == py.MOUSEBUTTONDOWN and event.button == 1:
                for i, rect in enumerate(rects):
                    if rect.collidepoint(event.pos):
                        selected = characters[i]
    return selected


chosen_character = character_select()
py.display.set_caption("Generating random grid")

enemyList = []
for r in range(row):
    for c in range(col):
        if grid[r][c] == 2:
            enemyList.append(Enemy(c * 60, r * 60, enemy_img))

p1 = Player(0, 0, 60, 60, chosen_character["img"], chosen_character["name"])
obstacleList = []
for r in range(row):
    for c in range(col):
        if grid[r][c] == 0:
            obstacleList.append(Obstacle(c*cell_w, r*cell_h, spikes))

clock = py.time.Clock()
screen = py.display.set_mode((screen_w + panel_w,screen_h))



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
        if event.type == py.MOUSEBUTTONDOWN:
            if event.button == 1:
                p1.attack(enemyList)
        for enemy in enemyList:
            enemy.attack_player(p1)
    if p1.iframes > 0:
        p1.iframes -= 1
    p1.check_lvl_up()
    clock.tick(15)
    screen.blit(background, (0,0))
    drawGrid(grid)
    draw_panel(screen)
    p1.draw(screen)
    py.display.flip()
py.quit()

