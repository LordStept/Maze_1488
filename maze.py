from pygame import *

#Класс:
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (65, 65))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
                
    def reset(self):
        win.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 65:
            self.rect.x += self.speed
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < win_height - 65:
            self.rect.y += self.speed 
        if keys[K_LSHIFT] and keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed + 10     
        if keys[K_LSHIFT] and keys[K_DOWN] and self.rect.y < win_height - 65:
            self.rect.y += self.speed + 10
        if keys[K_LSHIFT] and keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed + 10     
        if keys[K_LSHIFT] and keys[K_RIGHT] and self.rect.x < win_width - 65:
            self.rect.x += self.speed + 10 

class Enemy(GameSprite):
    direction = "left"
    def update(self):
        if self.rect.x <= 470:
            self.direction = 'right'
        if self.rect.x >= win_width - 85:
            self.direction = 'left'
        if self.direction == 'left':
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

class Wall(sprite.Sprite):
    def __init__(self, color_1, color_2, color_3, wall_x, wall_y, wall_width, wall_height):
        super().__init__()
        self.color_1 = color_1
        self.color_2 = color_2
        self.color_3 = color_3
        self.width = wall_width
        self.height = wall_height
        self.image = Surface((self.width, self.height))
        self.image.fill((color_1, color_2, color_3))
        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y

    def draw_wall(self):
        win.blit(self.image, (self.rect.x, self.rect.y))

            
win_width = 700
win_height = 500

#Сцена:
win = display.set_mode((win_width, win_height))
display.set_caption('Лабиринт')
background = transform.scale(image.load('skala.jpg'), (win_width, win_height))

speed = 5

#Музыка:
mixer.init()
mixer.music.load('jungles.ogg')
mixer.music.play()

money = mixer.Sound('money.ogg')
kick = mixer.Sound('kick.ogg')

#Шрифт:
font.init()
font = font.SysFont('Arial', 70)
win_text = font.render("YOU WIN!", True, (255, 215, 0))
lose = font.render("YOU LOSE!", True, (180, 0, 0))

#Персонажи:
player = Player('hero.png', 100, 300, 4)
monster = Enemy('cyborg.png', 525, 300, 2)
final = GameSprite('treasure.png', 525, 400, 0)

wall_1 = Wall(18, 35, 225, 90, 20, 10, 350)
wall_2 = Wall(18, 35, 225, 90, 20, 500, 10)
wall_3 = Wall(18, 35, 225, 590, 20, 10, 250)
wall_4 = Wall(18, 35, 225, 90, 370, 400, 10)

game = True
finish = False
clock = time.Clock()
FPS = 60

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

    if finish != True:
        win.blit(background, (0, 0))
        player.update()
        monster.update()
               
        player.reset()
        monster.reset()
        final.reset()

        wall_1.draw_wall()
        wall_2.draw_wall()
        wall_3.draw_wall()
        wall_4.draw_wall()

        if (
            sprite.collide_rect(player, monster)
            or sprite.collide_rect(player, wall_1)
            or sprite.collide_rect(player, wall_2)
            or sprite.collide_rect(player, wall_3)
            or sprite.collide_rect(player, wall_4)
        ):
            finish = True
            win.blit(lose, (200, 200))
            kick.play()

        if sprite.collide_rect(player, final):
            finish = True
            win.blit(win_text, (200, 200))
            money.play()

    display.update()
    clock.tick(FPS)
