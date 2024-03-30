from pygame import *
from random import *


screen = display.set_mode((1500, 850), FULLSCREEN    )
display.set_caption("Космический корабль")

mixer.init()
mixer.music.load("zobmi.ogg")
mixer.music.play()
life = 10

fire_sound = mixer.Sound('fire.ogg')
lose = 0
score = 0
max_lose = 20
max_score = 50
font.init()
font1 = font.SysFont('Arial', 36)

font2 = font.SysFont('Arial', 45)
win = font2.render('Ура, ты зачистил зону, фраерок =) ', True,(60, 255, 129))
lost = font2.render('Эх ты, фраерок =( ', True, (212, 1, 1))

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, size_w, size_h):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_w, size_h))
        self.speed = player_speed    
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.rect.w = size_w
        self.rect.h = size_h
    
    def reset(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 10:
            self.rect.x -= 20
        if keys[K_d] and self.rect.x < width - 80:
            self.rect.x += 20
        if keys[K_w]:
            self.rect.y -= 20
        if keys[K_s]:
            self.rect.y += 20
        if keys[K_ESCAPE]:
            QUIT()
        if keys[K_r]:
            mixer.music.load("pistoll.ogg")
            mixer.music.play()
            
    def attack(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 80, 25, 30)
        bullets.add(bullet)
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lose
        if self.rect.y > height:
            self.rect.x = randint(80, width-80)
            self.rect.y = 0
            lose += 1
            

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < -25:
            self.kill()
            

width = 1500
height = 850
background = transform.scale(image.load("doroga2.png"), (width, height))
hero = Player('chel.png', 350, height-100, 10, 100, 110)
monsters = sprite.Group()
for i in range(1, 8):
    enemy = Enemy('zombi2.png', randint(80, width-80),-40, randint(1,7), 95,100)
    monsters.add(enemy)

asteroids = sprite.Group()
for i in range(1,7):
    asteroid = Enemy('tank.png', randint(80, width-80),-40, randint(1,7), 100,150)
    asteroids.add(asteroid)

bullets = sprite.Group()
running = True
finish = False

clock = time.Clock()
while running:
    for e in event.get():
        if e.type == QUIT:
            running = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                hero.attack()
            if e.key == K_V:
                fire_sound.play()
                hero.attack()

    if not finish:
        screen.blit(background, (0,0))
        text_lose = font1.render('Попущено^_^'+str(lose), True,(234, 56, 123))
        text_win = font1.render('Запущено^_^'+str(score), True,(234, 56, 123))

        screen.blit(text_win,(10,20))
        screen.blit(text_lose,(10,60))
        
        monsters.update()
        monsters.draw(screen)
        bullets.update()
        bullets.draw(screen)
        asteroids.update()
        asteroids.draw(screen)
        hero.reset()
        hero.update()

        collides = sprite.groupcollide(monsters, bullets, True, True)
        collides1 = sprite.groupcollide(asteroids, bullets, True, True)
        for c in collides:
            score += 1
            enemy = Enemy('zombi2.png', randint(80, width-80),-40, randint(1,7), 95,150)
            monsters.add(enemy)
        if sprite.spritecollide(hero, monsters, False) or sprite.spritecollide(hero, asteroids, False):
            sprite.spritecollide(hero, monsters, True)
            sprite.spritecollide(hero, asteroids, True)
            life -= 1
        if life == 0 or lose>max_lose:
            finish = True 
            screen.blit(lost,(725, 400))        
        if score >= max_score:
            finish = True
            screen.blit(win,(725, 400))

        if life > 7:
            life_color = (0, 234, 14)
        if life >= 4 and life <=7:
            life_color = (255, 252, 0)
        if life <= 3:
            life_color = (255, 31, 100)

        text_life = font1.render("Life: " + str(life), True, life_color)
        life_x = (width - text_life.get_width()) // 2
        life_y = height - text_life.get_height() - 10
        screen.blit(text_life, (life_x, life_y))

        display.update()
    else:
        finish = False
        score = 0
        lose = 0
        life = 10 

        for b  in bullets:
            b.kill()
        for m in monsters:
            b.kill()
        for a in asteroids:
            a.kill()
        time.delay(3000)
        for i in range(1, 10):
            enemy = Enemy('zombi2.png', randint(80, width-80),-40, randint(1,7), 95,100)
            monsters.add(enemy)

        for i in range(1,5):
            asteroid = Enemy('tank.png', randint(80, width-80),-40, randint(1,7), 100,150)
            asteroids.add(asteroid)


    time.delay(50)