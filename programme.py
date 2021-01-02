import pygame
import pymunk

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

image = pygame.image.load('basketball.png')
image = pygame.transform.scale(image, (ball_radius * 2, ball_radius * 2))
image_basket = pygame.image.load('basket.png')
image_basket = pygame.transform.scale(image_basket, (100, 100))
image_fon = pygame.image.load('start_fon.jpg')
fon = pygame.transform.scale(image_fon, (800, 800))
image_shop = pygame.image.load('shop_fon.jpg')
image_shop = pygame.transform.scale(image_shop, (800, 800))


# класс для боковых и верхней стены, а также стен, которые мешают
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
            display.blit(image, (int(x) - ball_radius, int(y) - ball_radius))
            # print(int(x) - ball_radius, int(y) - ball_radius, coords_floor, ball_radius)
            # удалить тех, кто выпал из мира
            if int(x) - ball_radius > 900 or int(x) - ball_radius < -100 or int(y) - ball_radius > 900:
                space.remove(self.body, self.shape)
            # если попал в кольцо, мяч исчезает
            if int(x) - ball_radius > coords_floor[0]:
                if int(x) - ball_radius - coords_floor[0] < 30 and int(y) - ball_radius >= 635:
                    space.remove(self.body, self.shape)
                    return None
            else:
                if coords_floor[0] - int(x) < 15 and int(y) - ball_radius >= 635:
                    space.remove(self.body, self.shape)
                    return None
                    # print(coords_floor[0] ,int(x), int(y) ,ball_radius)
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


# завершение игры
def terminate():
    pygame.quit()


# стартовый экран
def start_screen():
    display.blit(fon, (0, 0))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'Stop'
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # print(event.pos)
                if (event.pos[0] >= 151 and event.pos[1] >= 221) and (event.pos[0] <= 649 and event.pos[1] <= 320):
                    return 'Play'
                elif (event.pos[0] >= 151 and event.pos[1] >= 432) and (event.pos[0] <= 649 and event.pos[1] <= 533):
                    return 'Shop'

        pygame.display.flip()
        clock.tick(FPS)


def shop_screen():
    display.blit(image_shop, (0, 0))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'Stop'
            elif event.type == pygame.MOUSEBUTTONDOWN:
                print(event.pos)
                if (event.pos[0] >= 30 and event.pos[1] >= 25) and (event.pos[0] <= 162 and event.pos[1] <= 80):
                    return 'Home'

        pygame.display.flip()
        clock.tick(FPS)


walls = Walls()
floor = Floor()
pack_balls = list()
PAUSE = False
START = False
while running:
    while not START:
        START = start_screen()
    if START == 'Play':
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
                    if s is None:
                        n += 1
                    if not s:
                        pack_balls[i] = False
            # рисуем кольцо
            floor.draw()
            # рисуем стены
            walls.draw()
            # счётчик набранных очков
            text = num.render(f'{n}', True,
                              (200, 0, 0))
            display.blit(text, (700, 50))
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
                    print(event.pos)
                    if (event.pos[0] >= 290 and event.pos[1] >= 350) and (event.pos[0] <= 420 and event.pos[1] <= 410):
                        START = False
                        PAUSE = not PAUSE
            text = num.render('PAUSE', True,
                              (255, 255, 255))
            text_home = num.render('home', True,
                                   (0, 255, 255))
            display.blit(text, (290, 300))
            display.blit(text_home, (290, 350))
            pygame.display.update()
    elif START == 'Stop':
        running = False
    elif START == 'Shop':
        SHOP = True
        while SHOP:
            shop_do = shop_screen()
            if shop_do == 'Stop':
                SHOP = False
                running = False
            elif shop_do == 'Home':
                SHOP = False
                START = False
