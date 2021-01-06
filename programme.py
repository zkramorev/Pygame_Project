import pygame
import pymunk
import sqlite3
import random

con = sqlite3.connect('data/Data_Base.db')
cur = con.cursor()

pygame.init()
display = pygame.display.set_mode((800, 800))
pygame.display.set_caption('BASKETBALL')
clock = pygame.time.Clock()
space = pymunk.Space()
space.gravity = 0, -900
FPS = 80
running = True
# кол-во очков
n = 0

# установка иконки приложения
ICON = pygame.image.load('data/icon.png')
pygame.display.set_icon(ICON)

# размер и шрифт текста
num = pygame.font.Font('data/font.ttf', 65)

ball_radius = 30

image_ball = pygame.image.load('data/' + cur.execute("SELECT ball_name FROM info").fetchone()[0])
image_ball = pygame.transform.scale(image_ball, (ball_radius * 2, ball_radius * 2))

image = pygame.image.load('data/basketball.png')
image = pygame.transform.scale(image, (ball_radius * 2, ball_radius * 2))

image_basket = pygame.image.load('data/basket.png')
image_basket = pygame.transform.scale(image_basket, (100, 100))

image_home_up = pygame.image.load('data/home_up.png')
image_home_up = pygame.transform.scale(image_home_up, (60, 70))

image_home_down = pygame.image.load('data/home_down.png')
image_home_down = pygame.transform.scale(image_home_down, (60, 70))

image_button_up = pygame.image.load('data/button_up.png')
image_button_up = pygame.transform.scale(image_button_up, (280, 100))

image_button_down = pygame.image.load('data/button_down.png')
image_button_down = pygame.transform.scale(image_button_down, (280, 100))

image_lock = pygame.image.load('data/lock2.png')
image_lock = pygame.transform.scale(image_lock, (60, 70))

image_volleyball = pygame.image.load('data/volleyball.png')
image_volleyball = pygame.transform.scale(image_volleyball, (ball_radius * 2, ball_radius * 2))

image_poo = pygame.image.load('data/poo.png')
image_poo = pygame.transform.scale(image_poo, (ball_radius * 2, ball_radius * 2))

image_smile = pygame.image.load('data/smile.png')
image_smile = pygame.transform.scale(image_smile, (ball_radius * 2, ball_radius * 2))

image_heart = pygame.image.load('data/heart.png')
image_heart = pygame.transform.scale(image_heart, (35, 30))

sound_net = pygame.mixer.Sound('data/sound_net.wav')

sound_ou = pygame.mixer.Sound('data/sound_ou.wav')

sound_game_over = pygame.mixer.Sound('data/game_over.wav')
sound_game_over.set_volume(0.2)

sound_buy = pygame.mixer.Sound('data/sound_buy.wav')

sound_click = pygame.mixer.Sound('data/sound_click.wav')


def convert_coordinates(point):
    return point[0], 800 - point[1]


# класс для боковых стен, а также стен, которые мешают
class Walls():
    def __init__(self):
        # левая
        self.add((10, 0), (10, 800), 1)
        # правая
        self.add((790, 0), (790, 800), 1)
        # нижняя левая
        self.add((100, 830), (30, 800), 0.85)
        # нижняя левая
        self.add((800, 800), (680, 830), 0.85)
        # генерация препядствий
        self.x1, self.y1 = random.randint(30, 100), random.randint(85, 215)
        self.x2, self.y2 = random.randint(200, 280), random.randint(200, 280)
        self.add((self.x1, self.y1), (self.x2, self.y2), 0.6)
        self.x3, self.y3 = random.randint(670, 690), random.randint(250, 270)
        self.x4, self.y4 = random.randint(580, 590), random.randint(290, 320)
        self.add((self.x3, self.y3), (self.x4, self.y4), 0.6)
        self.x5, self.y5 = random.randint(325, 450), random.randint(60, 150)
        self.x6, self.y6 = random.randint(320, 450), random.randint(70, 160)
        self.add((self.x5, self.y5), (self.x6, self.y6), 0.6)

    def draw(self):
        pygame.draw.line(display, (5, 200, 130), (self.x1, self.y1), (self.x2, self.y2), 5)
        pygame.draw.line(display, (5, 200, 130), (self.x3, self.y3), (self.x4, self.y4), 5)
        pygame.draw.line(display, (5, 200, 130), (self.x5, self.y5), (self.x6, self.y6), 5)
        pygame.draw.line(display, (255, 0, 0), (0, -10), (0, 800), 5)
        pygame.draw.line(display, (255, 0, 0), (798, -15), (798, 800), 5)

    def add(self, x, y, koef):
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.shape = pymunk.Segment(self.body, (x[0], 800 - x[1]), (y[0], 800 - y[1]), 1)
        self.shape.elasticity = koef
        space.add(self.body, self.shape)


# класс для мячей
class Ball():
    def __init__(self):
        self.body = pymunk.Body()
        self.body.position = random.randint(30, 770), 850
        self.shape = pymunk.Circle(self.body, ball_radius)
        self.shape.density = 1
        self.shape.elasticity = 1
        space.add(self.body, self.shape)

    def draw_update(self, coords_floor):
        try:
            # часть рисования
            x, y = convert_coordinates(self.body.position)
            display.blit(image_ball, (int(x) - ball_radius, int(y) - ball_radius))
            # удалить тех, кто выпал из мира
            if int(x) - ball_radius > 900 or int(x) - ball_radius < -100 or int(y) - ball_radius > 900:
                space.remove(self.body, self.shape)
                sound_ou.play()
                return 'live'
            # если попал в кольцо, мяч исчезает
            if int(x) - ball_radius > coords_floor[0]:
                if int(x) - ball_radius - coords_floor[0] < 50 and int(y) - ball_radius >= 635 \
                        and int(y) - ball_radius <= 650:
                    space.remove(self.body, self.shape)
                    sound_net.play()
                    return None
            else:
                if coords_floor[0] - int(x) + ball_radius < 15 and int(y) - ball_radius >= 635 \
                        and int(y) - ball_radius <= 650:
                    space.remove(self.body, self.shape)
                    sound_net.play()
                    return None
        except BaseException:
            return False
        return True


# класс для кольца
class Floor():
    def __init__(self):
        self.x, self.y = 300, 400
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.shape = pymunk.Segment(self.body, (self.x, 100), (self.y, 100), 5)
        self.shape.elasticity = 1
        space.add(self.body, self.shape)

    def draw(self):
        display.blit(image_basket, (self.x, 700))
        space.remove(self.body, self.shape)
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.shape = pymunk.Segment(self.body, (self.x, 100), (self.y, 100), 5)
        self.shape.elasticity = 1
        space.add(self.body, self.shape)

    def move(self, where):
        if where == 'right':
            if self.x + 9 < 700:
                self.x += 9
                self.y += 9
        else:
            if self.x - 9 > 0:
                self.x -= 9
                self.y -= 9

    def coords(self):
        return self.x, self.y


# стартовый экран
def start_screen():
    display.fill(pygame.Color(85, 85, 85))
    display.blit(image_button_up, (250, 265))
    display.blit(image_button_up, (250, 400))
    text = num.render(f'record: {cur.execute("SELECT record FROM info").fetchone()[0]}', True, (0, 200, 200))
    display.blit(text, (245, 515))
    text = num.render(f'coins: {cur.execute("SELECT coins FROM info").fetchone()[0]}', True, (0, 200, 200))
    display.blit(text, (245, 575))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'Stop'
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # print(event.pos)
                if (event.pos[0] >= 252 and event.pos[1] >= 267) and (event.pos[0] <= 520 and event.pos[1] <= 364):
                    sound_click.play()
                    return 'Play'
                elif (event.pos[0] >= 252 and event.pos[1] >= 403) and (event.pos[0] <= 520 and event.pos[1] <= 495):
                    sound_click.play()
                    return 'Shop'
            elif event.type == pygame.MOUSEMOTION:
                if (event.pos[0] >= 252 and event.pos[1] >= 267) and (event.pos[0] <= 520 and event.pos[1] <= 364):
                    display.blit(image_button_down, (250, 265))
                else:
                    display.blit(image_button_up, (250, 265))

                if (event.pos[0] >= 252 and event.pos[1] >= 403) and (event.pos[0] <= 520 and event.pos[1] <= 495):
                    display.blit(image_button_down, (250, 400))
                else:
                    display.blit(image_button_up, (250, 400))
        text = num.render('PLAY', True, (0, 245, 235))
        display.blit(text, (305, 278))
        text = num.render('SHOP', True, (0, 245, 235))
        display.blit(text, (305, 415))
        pygame.display.flip()
        clock.tick(FPS)


# функция покупки скинов
def shopping(pack_choose):
    idd = pack_choose.index(True)
    coins = cur.execute("SELECT coins FROM info").fetchone()[0]
    price = cur.execute(f"SELECT ball_price FROM balls WHERE id = {idd}").fetchone()[0]
    opened = cur.execute(f"SELECT opened FROM balls WHERE id = {idd}").fetchone()[0]
    if opened == 'no' and int(coins) >= int(price):
        sound_buy.play()
        cur.execute(f"UPDATE info SET coins = {coins - price}")
        cur.execute(f"UPDATE info SET coins = {coins - price}")
        cur.execute(f"UPDATE balls SET opened = 'yes' WHERE id = {idd}")
        con.commit()
        pygame.draw.rect(display, (85, 85, 85), (260, 10, 400, 70))
        text = num.render(f' coins: {cur.execute("SELECT coins FROM info").fetchone()[0]}', True, (0, 255, 255))
        display.blit(text, (260, 10))
        return True
    return False


# функция отрисовки цены скина и замка в магазине
def lock():
    if cur.execute("SELECT opened FROM balls WHERE ball_name == 'volleyball.png'").fetchone()[0] == 'no':
        display.blit(image_lock, (300, 270))
        text = num.render(str(cur.execute("SELECT ball_price FROM balls "
                                          "WHERE ball_name == 'volleyball.png'").fetchone()[0]),
                          True, (0, 255, 255))
        display.blit(text, (310, 420))
    else:
        pygame.draw.rect(display, (85, 85, 85), (300, 270, 75, 75))
        pygame.draw.rect(display, (85, 85, 85), (310, 420, 80, 80))
    if cur.execute("SELECT opened FROM balls WHERE ball_name == 'poo.png'").fetchone()[0] == 'no':
        display.blit(image_lock, (400, 270))
        text = num.render(str(cur.execute("SELECT ball_price FROM balls "
                                          "WHERE ball_name == 'poo.png'").fetchone()[0]),
                          True, (0, 255, 255))
        display.blit(text, (385, 420))
    else:
        pygame.draw.rect(display, (85, 85, 85), (400, 270, 75, 75))
        pygame.draw.rect(display, (85, 85, 85), (385, 420, 80, 80))
    if cur.execute("SELECT opened FROM balls WHERE ball_name == 'smile.png'").fetchone()[0] == 'no':
        display.blit(image_lock, (500, 270))
        text = num.render(str(cur.execute("SELECT ball_price FROM balls "
                                          "WHERE ball_name == 'smile.png'").fetchone()[0]),
                          True, (0, 255, 255))
        display.blit(text, (490, 420))
    else:
        pygame.draw.rect(display, (85, 85, 85), (500, 270, 75, 75))
        pygame.draw.rect(display, (85, 85, 85), (490, 420, 80, 80))


# функция выбора скинов
def choose_skin(pack_choose):
    idd = pack_choose.index(True)
    ball = cur.execute(f"SELECT ball_name FROM balls WHERE id = {idd}").fetchone()[0]
    opened = cur.execute(f"SELECT opened FROM balls WHERE id = {idd}").fetchone()[0]
    if opened == 'yes':
        cur.execute(f"UPDATE info SET ball_name = '{ball}'")
        con.commit()


# экран магазина
def shop_screen():
    display.fill(pygame.Color(85, 85, 85))
    display.blit(image_button_up, (250, 600))
    text_buy = num.render('  buy', True, (0, 255, 255))
    display.blit(image_home_up, (10, 10))
    display.blit(image, (200, 350))
    display.blit(image_volleyball, (300, 350))
    display.blit(image_poo, (400, 350))
    display.blit(image_smile, (500, 350))
    text = num.render(f' coins: {cur.execute("SELECT coins FROM info").fetchone()[0]}', True, (0, 255, 255))
    display.blit(text, (260, 10))
    lock()
    choose = [[180, 250], [282, 250], [382, 250], [482, 250]]
    idd = cur.execute(f"SELECT id FROM balls WHERE ball_name = (SELECT ball_name FROM info)").fetchone()[0]
    pack_choose = list()
    for i in range(4):
        if int(idd) == i:
            pack_choose.append(True)
        else:
            pack_choose.append(False)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'Stop'
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if (event.pos[0] >= 21 and event.pos[1] >= 20) and (event.pos[0] <= 65 and event.pos[1] <= 80):
                    sound_click.play()
                    return 'Home'
                # здесь выбираем скин
                elif event.pos[0] >= 180 and event.pos[1] >= 255 and event.pos[0] <= 275 and event.pos[1] <= 400:
                    pack_choose = [True, False, False, False]
                    sound_click.play()
                elif event.pos[0] >= 300 and event.pos[1] >= 250 and event.pos[0] <= 380 and event.pos[1] <= 400:
                    pack_choose = [False, True, False, False]
                    sound_click.play()
                elif event.pos[0] >= 400 and event.pos[1] >= 250 and event.pos[0] <= 465 and event.pos[1] <= 400:
                    pack_choose = [False, False, True, False]
                    sound_click.play()
                elif event.pos[0] >= 500 and event.pos[1] >= 250 and event.pos[0] <= 570 and event.pos[1] <= 400:
                    pack_choose = [False, False, False, True]
                    sound_click.play()
                # нажатие на кнопку 'BUY'
                elif event.pos[0] >= 250 and event.pos[1] >= 600 and event.pos[0] <= 530 and event.pos[1] <= 700:
                    # описать успешная ли покупка или нет
                    sound_click.play()
                    if shopping(pack_choose):
                        lock()
                    else:
                        pass
            elif event.type == pygame.MOUSEMOTION:
                # кнопка домой
                if (event.pos[0] >= 21 and event.pos[1] >= 20) and (event.pos[0] <= 65 and event.pos[1] <= 80):
                    display.blit(image_home_down, (10, 10))
                else:
                    display.blit(image_home_up, (10, 10))
                # кнопка покупки
                if event.pos[0] >= 250 and event.pos[1] >= 600 and event.pos[0] <= 530 and event.pos[1] <= 700:
                    display.blit(image_button_down, (250, 600))
                else:
                    display.blit(image_button_up, (250, 600))
        # 2 цикла для корректного отображения выбранного элемента(с 1 циклом некрасиво получается)
        for i in range(len(pack_choose)):
            if not pack_choose[i]:
                pygame.draw.rect(display, (85, 85, 85), (choose[i][0], choose[i][1], 100, 175), 3)
        for i in range(len(pack_choose)):
            if pack_choose[i]:
                pygame.draw.rect(display, (0, 255, 255), (choose[i][0], choose[i][1], 100, 175), 3)
        choose_skin(pack_choose)
        display.blit(text_buy, (283, 607))
        pygame.display.flip()
        clock.tick(FPS)


live = 5
walls = Walls()
floor = Floor()
pack_balls = list()
PAUSE = False
START = False
UPDATE_SKIN = True
DIE = False
# Чтобы музыка мосле проигрыша воспроизводилась 1 раз
ONE_TIME = True
# Для корректного отображения заработанных монет
n_UPDATE = True
# Счетчик для генерации мячей, пееменная для ускорения генерации мячей
j, a = 250, 150
coins = 0
r, g, b = 255, 255, 255
R, G, B = True, False, False

while running:
    while not START:
        START = start_screen()
    if START == 'Play':
        if not DIE and not PAUSE:
            # это для того, чтобы мячи появлялись не слишком быстро
            j += 1
            if j - a > 0:
                j = 0
                a += 1
                pack_balls.append(Ball())

            if UPDATE_SKIN:
                image_ball = pygame.image.load('data/' + cur.execute("SELECT ball_name FROM info").fetchone()[0])
                image_ball = pygame.transform.scale(image_ball, (ball_radius * 2, ball_radius * 2))
                UPDATE_SKIN = False
            if not PAUSE:
                # если меньше 15 набранных очков - без усложнения, иначе фон будет менять цвета (это усложняет игру)
                if n < 15:
                    display.fill((0, 0, 0))
                else:
                    display.fill((r, g, b))
                    if R:
                        if r > 0:
                            r -= 1
                        else:
                            R = False
                            G = True
                    else:
                        if r < 254:
                            r += 1
                        else:
                            R = True
                    if G:
                        if g > 0:
                            g -= 1
                        else:
                            G = False
                            B = True
                    else:
                        if g < 254:
                            g += 1
                        else:
                            G = True
                    if B:
                        if b > 0:
                            b -= 1
                        else:
                            B = False
                            R = True
                    else:
                        if b < 254:
                            b += 1
                        else:
                            B = True
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    # pause
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            PAUSE = not PAUSE
                            sound_click.play()
                # перемещение кольца
                if pygame.key.get_pressed()[pygame.K_LEFT] or pygame.key.get_pressed()[pygame.K_a]:
                    floor.move('left')
                if pygame.key.get_pressed()[pygame.K_RIGHT] or pygame.key.get_pressed()[pygame.K_d]:
                    floor.move('right')
                # отрисовываем мячи и удаляем мячи, которые выпали из мира
                for i in range(len(pack_balls)):
                    if pack_balls[i]:
                        s = pack_balls[i].draw_update(floor.coords())
                        if s == 'live':
                            live -= 1
                        elif s is None:
                            n += 1
                        elif not s:
                            pack_balls[i] = False
            # рисуем кольцо
            floor.draw()
            # рисуем стены
            walls.draw()
            # счётчик набранных очков
            text = num.render(f'{n}', True, (200, 0, 0))
            display.blit(text, (670, 50))
            # отображение жизней
            x = 10
            if live > 0:
                for i in range(1, live + 1):
                    display.blit(image_heart, (x, 10))
                    x += 40
            else:
                DIE = True
                ONE_TIME = True
                n_UPDATE = True
            pygame.display.update()
            clock.tick(FPS)
            pygame.event.pump()
            space.step(1 / FPS)
        else:
            if PAUSE:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    # pause
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            PAUSE = not PAUSE
                            sound_click.play()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if (event.pos[0] >= 340 and event.pos[1] >= 350) and (
                                event.pos[0] <= 481 and event.pos[1] <= 410):
                            sound_click.play()
                            START = False
                            PAUSE = not PAUSE
                            n = 0
                            live = 5
                            pack_balls = list()
                text = num.render('PAUSE', True, (255, 255, 255))
                text_home = num.render('  home', True, (0, 255, 255))
                display.blit(text, (290, 300))
                display.blit(text_home, (290, 350))
                pygame.display.update()
            elif DIE:
                if ONE_TIME:
                    sound_game_over.play()
                    ONE_TIME = False
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if (event.pos[0] >= 311 and event.pos[1] >= 360) and (
                                event.pos[0] <= 450 and event.pos[1] <= 400):
                            START = False
                            DIE = False
                            pack_balls = list()
                            live = 5
                            sound_click.play()
                        elif (event.pos[0] >= 265 and event.pos[1] >= 405) and (
                                event.pos[0] <= 530 and event.pos[1] <= 445):
                            DIE = False
                            live = 5
                            pack_balls = list()
                            sound_click.play()
                text = num.render('game over', True, (255, 255, 255))
                text_home = num.render('  home', True, (0, 255, 255))
                text_new_game = num.render('new game', True, (0, 255, 255))
                text_score = num.render('score: ', True, (255, 255, 255))
                # обновление рекорда
                if n_UPDATE:
                    coins = n // 10
                    cur.execute(f"UPDATE info SET coins = coins + {coins}")
                    con.commit()
                    n_UPDATE = False
                record = cur.execute(f"SELECT record FROM info").fetchone()[0]
                if coins < 2:
                    text_plus_coins = num.render(f'+{coins}', True, (255, 255, 0))
                else:
                    text_plus_coins = num.render(f'+{coins}', True, (255, 255, 0))
                if n > record:
                    text_record = num.render(f'NEW RECORD: {n}', True, (0, 255, 0))
                    display.blit(text_record, (180, 180))
                    cur.execute(f"UPDATE info SET record = {n}")
                    con.commit()
                n = 0
                display.blit(text_plus_coins, (320, 445))
                display.blit(text, (260, 285))
                display.blit(text_home, (260, 335))
                display.blit(text_score, (480, 50))
                display.blit(text_new_game, (260, 385))
                pygame.display.update()
    elif START == 'Stop':
        running = False
    elif START == 'Shop':
        SHOP = True
        UPDATE_SKIN = True
        while SHOP:
            shop_do = shop_screen()
            if shop_do == 'Stop':
                SHOP = False
                running = False
            elif shop_do == 'Home':
                SHOP = False
                START = False
