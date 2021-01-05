import pygame
import pymunk
import sqlite3
import time

con = sqlite3.connect('Data_Base.db')
cur = con.cursor()

pygame.init()
display = pygame.display.set_mode((800, 800))
pygame.display.set_caption('BASKETBALL')
clock = pygame.time.Clock()
space = pymunk.Space()
space.gravity = 0, -850
FPS = 80
running = True
# кол-во очков
n = 0

# установка иконки приложения
ICON = pygame.image.load('icon.png')
pygame.display.set_icon(ICON)

# размер и шрифт текста
num = pygame.font.Font('font.ttf', 65)


def convert_coordinates(point):
    return point[0], 800 - point[1]


ball_radius = 30

image_ball = pygame.image.load(cur.execute("SELECT ball_name FROM info").fetchone()[0])
image_ball = pygame.transform.scale(image_ball, (ball_radius * 2, ball_radius * 2))

image = pygame.image.load('basketball.png')
image = pygame.transform.scale(image, (ball_radius * 2, ball_radius * 2))

image_basket = pygame.image.load('basket.png')
image_basket = pygame.transform.scale(image_basket, (100, 100))

image_fon = pygame.image.load('start_fon.jpg')
fon = pygame.transform.scale(image_fon, (800, 800))

image_shop = pygame.image.load('shop_fon.jpg')
image_shop = pygame.transform.scale(image_shop, (800, 800))

image_home_up = pygame.image.load('home_up.png')
image_home_up = pygame.transform.scale(image_home_up, (60, 70))

image_home_down = pygame.image.load('home_down.png')
image_home_down = pygame.transform.scale(image_home_down, (60, 70))

image_button_up = pygame.image.load('button_up.png')
image_button_up = pygame.transform.scale(image_button_up, (280, 100))

image_button_down = pygame.image.load('button_down.png')
image_button_down = pygame.transform.scale(image_button_down, (280, 100))

image_lock = pygame.image.load('lock2.png')
image_lock = pygame.transform.scale(image_lock, (60, 70))

image_volleyball = pygame.image.load('volleyball.png')
image_volleyball = pygame.transform.scale(image_volleyball, (ball_radius * 2, ball_radius * 2))

image_poo = pygame.image.load('poo.png')
image_poo = pygame.transform.scale(image_poo, (ball_radius * 2, ball_radius * 2))

image_smile = pygame.image.load('smile.png')
image_smile = pygame.transform.scale(image_smile, (ball_radius * 2, ball_radius * 2))

image_heart = pygame.image.load('heart.png')
image_heart = pygame.transform.scale(image_heart, (35, 30))

sound_net = pygame.mixer.Sound('sound_net.wav')
sound_ou = pygame.mixer.Sound('sound_ou.wav')


# класс для боковых стен, а также стен, которые мешают
class Walls():
    def __init__(self):
        # display.blit(image_basket, (self.x, 700))
        # space.remove(self.body, self.shape)
        # левая
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.shape = pymunk.Segment(self.body, (10, 0), (10, 800), 5)
        self.shape.elasticity = 1
        space.add(self.body, self.shape)
        # правая
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.shape = pymunk.Segment(self.body, (790, 0), (790, 800), 5)
        self.shape.elasticity = 1
        space.add(self.body, self.shape)
        # нижняя левая
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.shape = pymunk.Segment(self.body, (100, -30), (30, 0), 5)
        self.shape.elasticity = 1
        space.add(self.body, self.shape)

        # нижняя левая
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.shape = pymunk.Segment(self.body, (800, 0), (680, -30), 5)
        self.shape.elasticity = 1
        space.add(self.body, self.shape)

    def draw(self):
        pygame.draw.line(display, (255, 0, 0), (0, -10), (0, 800), 5)
        pygame.draw.line(display, (255, 0, 0), (798, -15), (798, 800), 5)


# класс для мячей
class Ball():
    def __init__(self, pos):
        self.body = pymunk.Body()
        self.body.position = pos[0], 800 - pos[1]
        self.shape = pymunk.Circle(self.body, ball_radius)
        self.shape.density = 1
        self.shape.elasticity = 1
        space.add(self.body, self.shape)

    def draw_update(self, coords_floor):
        try:
            # часть рисования
            x, y = convert_coordinates(self.body.position)
            # pygame.draw.circle(display, (255, 0, 0), (int(x), int(y)), ball_radius)
            display.blit(image_ball, (int(x) - ball_radius, int(y) - ball_radius))
            # print(int(x) - ball_radius, int(y) - ball_radius, coords_floor, ball_radius)
            # удалить тех, кто выпал из мира
            if int(x) - ball_radius > 900 or int(x) - ball_radius < -100 or int(y) - ball_radius > 900:
                space.remove(self.body, self.shape)
                sound_ou.play()
                return 'live'
            # если попал в кольцо, мяч исчезает
            if int(x) - ball_radius > coords_floor[0]:
                # print(coords_floor[0] ,int(x) - ball_radius, int(y)- ball_radius ,ball_radius)
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
        # pygame.draw.line(display, (0, 0, 0), (self.x, 700), (self.y, 700), 5)

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
    text = num.render(f'record: {cur.execute("SELECT record FROM info").fetchone()[0]}', True, (0, 255, 255))
    display.blit(text, (245, 515))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'Stop'
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # print(event.pos)
                if (event.pos[0] >= 252 and event.pos[1] >= 267) and (event.pos[0] <= 520 and event.pos[1] <= 364):
                    return 'Play'
                elif (event.pos[0] >= 252 and event.pos[1] >= 403) and (event.pos[0] <= 520 and event.pos[1] <= 495):
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
        print('УСПЕШНО')
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
                    return 'Home'
                # здесь выбираем скин
                elif event.pos[0] >= 180 and event.pos[1] >= 255 and event.pos[0] <= 275 and event.pos[1] <= 400:
                    pack_choose = [True, False, False, False]
                elif event.pos[0] >= 300 and event.pos[1] >= 250 and event.pos[0] <= 380 and event.pos[1] <= 400:
                    pack_choose = [False, True, False, False]
                elif event.pos[0] >= 400 and event.pos[1] >= 250 and event.pos[0] <= 465 and event.pos[1] <= 400:
                    pack_choose = [False, False, True, False]
                elif event.pos[0] >= 500 and event.pos[1] >= 250 and event.pos[0] <= 570 and event.pos[1] <= 400:
                    pack_choose = [False, False, False, True]
                # нажатие на кнопку 'BUY'
                elif event.pos[0] >= 250 and event.pos[1] >= 600 and event.pos[0] <= 530 and event.pos[1] <= 700:
                    # описать успешная ли покупка или нет
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
sec = 0
walls = Walls()
floor = Floor()
pack_balls = list()
PAUSE = False
START = False
UPDATE_SKIN = True
while running:
    while not START:
        START = start_screen()
    if START == 'Play':
        if UPDATE_SKIN:
            image_ball = pygame.image.load(cur.execute("SELECT ball_name FROM info").fetchone()[0])
            image_ball = pygame.transform.scale(image_ball, (ball_radius * 2, ball_radius * 2))
            UPDATE_SKIN = False
        if not PAUSE:
            display.fill((0, 0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pack_balls.append(Ball(event.pos))
                # pause
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        PAUSE = not PAUSE
            # перемещение кольца
            if pygame.key.get_pressed()[pygame.K_LEFT]:
                floor.move('left')
            if pygame.key.get_pressed()[pygame.K_RIGHT]:
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
                print('die')
            pygame.display.update()
            clock.tick(FPS)
            pygame.event.pump()
            space.step(1 / FPS)
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                # pause
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        PAUSE = not PAUSE
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if (event.pos[0] >= 340 and event.pos[1] >= 350) and (event.pos[0] <= 481 and event.pos[1] <= 410):
                        START = False
                        PAUSE = not PAUSE
                        pack_balls = list()
            text = num.render('PAUSE', True, (255, 255, 255))
            text_home = num.render('  home', True, (0, 255, 255))
            display.blit(text, (290, 300))
            display.blit(text_home, (290, 350))
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
