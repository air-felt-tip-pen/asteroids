from pygame import *
from random import *

w, h = 700, 500
window = display.set_mode((w, h))
display.set_caption('Аня')

game = True
finish = False
clock = time.Clock()
FPS = 40
background = transform.scale(image.load("galaxy.jpg"), (w, h))

class GameSprite(sprite.Sprite):
    def __init__(self, pImage, px, py, sizeX, sizeY, pSpeed):
        super().__init__()
        self.image = transform.scale(image.load(pImage), (sizeX, sizeY))
        self.speed = pSpeed
        self.rect = self.image.get_rect()
        self.rect.x = px
        self.rect.y = py
    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a]:
            self.rect.x -= self.speed
        if keys[K_d]:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet("bullet.png", self.rect.centerx-15//2, self.rect.top, 15, 30, 15)
        bullets.add(bullet)

ship = Player("rocket.png", 10, h-100, 65, 95, 4)

lost = 0
class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        # -------------------------------------------------------------------------------------------------------------------------------------------------------
        global hearts
        if self.rect.y > h:
            try:
                hearts.pop(-1)
            except:
                pass
            self.rect.y = 0
            self.rect.x = randint(0, w-50)
            lost += 1

asteroids = sprite.Group()

for i in range(6):
    pics = ["asteroid.png", "ufo.png"]
    asteroids.add(Enemy(choice(pics), randint(0, w-50), -40, 50, 50, randint(1, 2)))
score = 0

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= 0:
            self.kill()

bullets = sprite.Group()

mixer.init()
mixer.music.load("space.ogg")
mixer.music.set_volume(0.05)
mixer.music.play()

fire_sound = mixer.Sound('fire.ogg')
fire_sound.set_volume(0.01)

font.init()
mainfont = font.Font(None, 40)


from time import time as timer
num_fire = 0
reload_time = False
#-------------------------------------------------------------------------------------------------------------------------------------------------------
hearts = []
lives = 10
hx = 170
for i in range(lives):
    heart = GameSprite("health.png", hx, 10, 40, 37, 0)
    hearts.append(heart)
    hx += 40

restart = GameSprite("restart.jpg", 240, 200, 222, 150, 0)

start = GameSprite("start.png", 240, 250, 222, 100, 0)
exit = GameSprite("exit.png", 5, 5, 60, 60, 0)
finish = True

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and reload_time == False:
                    num_fire += 1
                    ship.fire()
                    fire_sound.play()
                if num_fire >= 5 and reload_time == False:
                    reload_time = True
                    reload_start = timer()

            if e.key == K_r and finish:
                for a in asteroids:
                    a.rect.y = -100
                    a.rect.x = randint(0, w-100)
                score, lost, finish = 0, 0, 0
                # -------------------------------------------------------------------------------------------------------------------------------------------------------
                hearts = []
                lives = 10
                hx = 170
                for i in range(lives):
                    heart = GameSprite("health.png", hx, 10, 40, 37, 0)
                    hearts.append(heart)
                    hx += 40

        if e.type == MOUSEBUTTONDOWN:
            if e.button == 1:
                x, y = e.pos
                if restart.rect.collidepoint(x, y) and finish:
                    for a in asteroids:
                        a.rect.y = -100
                        a.rect.x = randint(0, w - 100)
                    score, lost, finish = 0, 0, 0
                    # -------------------------------------------------------------------------------------------------------------------------------------------------------
                    hearts = []
                    lives = 10
                    hx = 170
                    for i in range(lives):
                        heart = GameSprite("health.png", hx, 10, 40, 37, 0)
                        hearts.append(heart)
                        hx += 40
                if start.rect.collidepoint(x, y):
                    finish = False

                if exit.rect.collidepoint(x, y):
                    game = False


    if finish:
        window.blit(background, (0, 0))
        start.draw()
        exit.draw()

    if not finish:
        window.blit(background, (0, 0))
        score_text = mainfont.render("SCORE: "+str(score), True, (0, 255, 0))
        lose_text = mainfont.render("MISSED: "+str(lost), True, (0, 255, 0))
        window.blit(score_text, (5, 10))
        window.blit(lose_text, (5, 50))

        if reload_time:
            reload_end = timer()
            if reload_end - reload_start < 3:
                reload_text = mainfont.render("RELOADING...", True, (0, 255, 0))
                window.blit(reload_text, (5, 90))
            else:
                num_fire = 0
                reload_time = False

        ship.draw()
        ship.update()
        asteroids.update()
        asteroids.draw(window)
        bullets.draw(window)
        bullets.update()

        if sprite.spritecollide(ship, asteroids, False):
            lose_text = mainfont.render("YOU LOSE", True, (0, 255, 0))
            window.blit(lose_text, (270, 220))
            restart.draw()
            finish = True
        collides = sprite.groupcollide(bullets, asteroids, True, True)
        for c in collides:
            score += 1
            asteroids.add(Enemy(choice(pics), randint(0, w-50), -40, 50, 50, randint(1, 2)))

        # -------------------------------------------------------------------------------------------------------------------------------------------------------
        if len(hearts) <= 0:
            lose_text = mainfont.render("YOU LOSE", True, (0, 255, 0))
            restart.draw()
            window.blit(lose_text, (270, 220))
            finish = True
        # -------------------------------------------------------------------------------------------------------------------------------------------------------
        for heart in hearts:
            heart.draw()

    display.update()
    clock.tick(120)
