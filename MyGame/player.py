import pygame as py
from random import randint
py.mixer.init()
enemy_death = py.mixer.Sound("C:\\Users\\01Solec\\Documents\\PygameProjectRepo\\GameProject\\MyGame\\Zombie_death.ogg")
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
        self.weapon = "Fists"
        self.atk_dmg = 10
        self.potions = 0
        self.atk_cooldown = 0
        self.atk_cooldown_max = 15

    def attack(self, enemies):
        if self.atk_cooldown > 0:
            return
        self.atk_cooldown = self.atk_cooldown_max
        player_r = self.y // 40
        player_c = self.x // 40
        for enemy in enemies:
            if not enemy.alive:
                continue
            enemy_r = enemy.y // 40
            enemy_c = enemy.x // 40
            delta_x = abs(player_c - enemy_c)
            delta_y = abs(player_r - enemy_r)

            if self.class_name == "Knight":
                if delta_x <= 1 and delta_y <= 1:
                    enemy.take_damage(self.atk_dmg)
                    if not enemy.alive:
                        self.xp += 20
            elif self.class_name == "Archer":
                if delta_x <= 3 and delta_y <= 4:
                    crit = randint(1, 5) == 1
                    damage = self.atk_dmg
                    if crit:
                        damage *= 2
                    enemy.take_damage(damage)
                    if not enemy.alive:
                        self.xp += 20

            elif self.class_name == "Wizard":
                if delta_x <= 3 and delta_y <= 3:
                    center_r = enemy_r
                    center_c = enemy_c

                    for other_enemy in enemies:
                        if not other_enemy.alive:
                            continue
                        other_r = other_enemy.y // 40
                        other_c = other_enemy.x // 40
                        if center_r <= other_r < center_r + 2 and center_c <= other_c < center_c + 2:
                            other_enemy.take_damage(self.atk_dmg)
                            if not enemy.alive:
                                self.xp += 20


    
    def draw(self, screen):
         screen.blit(self.img, (self.x, self.y))
         bar_w = self.w 
         filled = int(bar_w * self.hp / self.max_hp)
         py.draw.rect(screen, "#ff0000", (self.x, self.y + self.h + 2, bar_w, 5))
         py.draw.rect(screen, "#00ff1e", (self.x, self.y + self.h + 2, filled, 5))
    
    def move(self, screen:any, grid:list[list], event):
        r = self.y // 40
        c = self.x // 40   
        if event.type == py.KEYDOWN:
            if event.key == py.K_LEFT and c - 1 >= 0 and grid[r][c-1] != 0:
                self.x -= 40
            if event.key == py.K_RIGHT and c + 1 < len(grid[0]) and grid[r][c+1] != 0:
                self.x += 40
            if event.key == py.K_UP and r - 1 >= 0 and grid[r-1][c] != 0:
                self.y -= 40
            if event.key == py.K_DOWN and r + 1 < len(grid) and grid[r+1][c] != 0:
                self.y += 40

    def collision(self, enemy):
        if abs(self.x - enemy.x) <= self.w and abs(self.y - enemy.y) <= self.h:
            if self.collide == False:
                print("collision")
                self.collide = True
        elif self.collide == True:
            self.collide = False
    
    def check_lvl_up(self):
        if self.xp >= 100 and self.has_weapon == False:
            self.has_weapon = True
            if self.class_name == "Knight":
                self.weapon = "Sword"
                self.atk_dmg = 30
            if self.class_name == "Wizard":
                self.weapon = "Staff"
                self.atk_dmg = 15
            if self.class_name == "Archer":
                self.weapon = "Bow"
                self.atk_dmg = 25

    def use_potion(self):
        if self.potions > 0 and self.hp < self.max_hp:
                    self.potions -= 1
                    self.hp += 30
                    if self.hp > self.max_hp:
                        self.hp = self.max_hp


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
        self.move_timer = 0
        self.move_delay = 30

    def draw(self, screen):
        if self.alive:
            screen.blit(self.img, (self.x, self.y))
            py.draw.rect(screen, "#de1414", (self.x, self.y - 10, 60, 5))
            green = int(60 * self.hp / self.max_hp)
            py.draw.rect(screen, "#16d927", (self.x, self.y -10, green, 5))

    def take_damage(self, amount):
        self.hp -= amount
        if self.hp <= 0:
            self.alive = False
            enemy_death.play()

    def attack_player(self, player):
        if self.alive:
            if abs(self.x - player.x) <= 40 and abs(self.y - player.y) <= 40:
                if player.iframes == 0:
                    player.hp -= self.dmg
                    player.iframes = player.iframes_max

    def move_towards_player(self, player, grid):
        if not self.alive:
            return
        self.move_timer += 1
        if self.move_timer < self.move_delay:
            return
        self.move_timer = 0
        enemy_r = self.y // 40
        enemy_c = self.x // 40
        player_r = player.y // 40
        player_c = player.x // 40
        if abs(player_r - enemy_r) + abs(player_c - enemy_c) <= 5:
            if player_r > enemy_r:
                new_r = enemy_r + 1
                if grid[new_r][enemy_c] != 0:
                    self.y += 40
            elif player_r < enemy_r:
                new_r = enemy_r - 1
                if grid[new_r][enemy_c] != 0:
                    self.y -= 40
            elif player_c > enemy_c:
                new_c = enemy_c + 1
                if grid[enemy_r][new_c] != 0:
                    self.x += 40
            elif player_c < enemy_c:
                new_c = enemy_c - 1
                if grid[enemy_r][new_c] != 0:
                    self.x -= 40             