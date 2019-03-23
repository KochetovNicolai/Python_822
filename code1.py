import pygame


def but_rec(screen, font, text, color1, color2, coords, f):
    textSurfaceObj = font.render(text, True, color1, color2)
    textRectObj = textSurfaceObj.get_rect()
    if f:
        textRectObj.center = coords
    else:
        textRectObj.topleft = coords
    screen.blit(textSurfaceObj, textRectObj)
    return textRectObj
class button:
    count = 0

    def __init__(self, name, namemany, cost, production):
        self.name2 = namemany
        self.name = name
        self.cost = cost
        self.prod = production

    def draw(self, coords):
        global black, gray, cook, light_grey
        if self.cost <= cook:
            self.buy_rec = but_rec(screen, fontObj1, 'Buy {} for {} cookies'.format(self.name, round(self.cost, 2)), black, grey, coords,1)
        else:
            self.buy_rec = but_rec(screen, fontObj1, 'Buy {} for {} cookies'.format(self.name, round(self.cost, 2)), grey,
                                   light_grey, coords, 1)
        if self.cost * 10 * (1.1 ** 10 - 1) <= cook:
            self.buy10_rect = but_rec(screen, fontObj1, 'x10', black, grey, (coords[0] - 20, coords[1] + 35), 1)
        else:
            self.buy10_rect = but_rec(screen, fontObj1, 'x10', grey, light_grey, (coords[0] - 20, coords[1] + 35), 1)
        if self.cost <= cook:
            self.buymax_rect = but_rec(screen, fontObj1, 'Max', black, grey, (coords[0] + 20, coords[1] + 35), 1)
        else:
            self.buymax_rect = but_rec(screen, fontObj1, 'Max', grey, light_grey, (coords[0] + 20, coords[1] + 35), 1)

    def buy(self, n):
        global cook, cook_income
        if round(self.cost * 10 * (1.1 ** n - 1), 4) <= cook:
            for i in range(n):
                cook -= self.cost
                cook_income += self.prod
                self.count += 1
                self.cost *= 1.1
    def point(self, pos):
        but_rec(screen, fontObj2, 'You have {} of {}'.format(self.count, self.name2), black, white, (pos[0], pos[1] + 15), 0)
        but_rec(screen, fontObj2, ' Each produces {} cookies per second'.format(self.prod), black, white, (pos[0], pos[1] + 33), 0)

class cursor(button):
    def buy(self, n):
        global cook, cook_per_click
        if round(self.cost * 10 * (1.1 ** n - 1), 4) <= cook:
            for i in range(n):
                cook -= self.cost
                cook_per_click += self.prod
                self.count += 1
                self.cost *= 1.1
    def point(self, pos):
        but_rec(screen, fontObj2, 'You have {} of {}'.format(self.count, self.name2), black, white, (pos[0], pos[1] + 15), 0)
        but_rec(screen, fontObj2, ' Each produces {} of cookies per click'.format(self.prod), black, white, (pos[0], pos[1] + 33), 0)

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Clicker")
print(pygame.font.get_fonts())
fontObj1 = pygame.font.SysFont('arial', 25)
fontObj2 = pygame.font.SysFont('arial', 15)
white = (255, 255, 255)
light_grey = (200, 200, 200)
grey = (100, 100, 100)
black = (0, 0, 0)
clock = pygame.time.Clock()
FPS = 60
cook = 0
all_cook = 0
clicks = 0
cook_per_click = 1
cook_income = 0
improve_cost = 10
INCOME = pygame.USEREVENT + 1
pygame.time.set_timer(INCOME, 1000)
done = True
oven = button('an oven', 'ovens', 10, 1)
farm = button('a cookie farm', 'cookie farms', 1000, 50)
factory = button('a cookie factory', 'cookie factories', 100000, 2500)
multi_click = cursor('extra hand', 'extra hands', 10, 1)
manipu = cursor('manipulator', 'manipulators', 1000, 50)
robot = cursor('robot', 'robots', 1000000, 2500)
while done:
    screen.fill(white)
    oven.draw((200, 100))
    farm.draw((200, 200))
    factory.draw((200, 300))
    multi_click.draw((600, 100))
    manipu.draw((600, 200))
    robot.draw((600, 300))
    but_rec(screen, fontObj1, 'Press Spacebar to make cookies.'.format(round(cook, 2)), black, white, (600, 400), 1)
    but_rec(screen, fontObj1, 'Press x10 to buy 10 items'.format(round(cook, 2)), black, white, (600, 430), 1)
    but_rec(screen, fontObj1, 'and Max to buy maximum amount of them.'.format(round(cook, 2)), black, white, (600, 460), 1)
    but_rec(screen, fontObj1, 'You have {} of cookies.'.format(round(cook, 2)), black, white, (400, 10), 1)
    but_rec(screen, fontObj1, 'You gain {} of cookies per second'.format(round(cook_income, 2)), black, white, (400, 40), 1)
    but_rec(screen, fontObj1, 'and {} of cookies per click.'.format(round(cook_per_click, 2)), black, white, (400, 70), 1)
    but_rec(screen, fontObj1, 'You made {} clicks'.format(clicks), black, white, (200, 550), 1)
    but_rec(screen, fontObj1, 'and cooked {} cookies.'.format(all_cook), black, white, (200, 575), 1)
    but_rec(screen, fontObj2, 'Made by Sergey Dolgikh for his python project'.format(all_cook), black, white, (600, 570), 1)
    but_rec(screen, fontObj2, 'Dolgoprudny, 2019'.format(all_cook), black, white, (600, 590), 1)
    pos = pygame.mouse.get_pos()
    for j in [oven, farm, factory, multi_click, manipu, robot]:
        if pygame.Rect.collidepoint(j.buy_rec, pos):
            j.point(pos)
    pygame.display.update()
    for i in pygame.event.get():
        print(i)
        if i.type == pygame.QUIT:
            done = False
        elif i.type == pygame.KEYDOWN:
            if i.unicode == ' ':
                cook+=cook_per_click
                clicks+=1
                all_cook+=cook_per_click
        elif i.type == INCOME:
            cook+=cook_income
            all_cook+=cook_income
        elif (i.type == pygame.MOUSEBUTTONUP):
            for j in [oven, farm, factory, multi_click, manipu, robot]:
                if pygame.Rect.collidepoint(j.buy_rec, i.pos):
                    j.buy(1)
                elif pygame.Rect.collidepoint(j.buy10_rect, i.pos):
                    j.buy(10)
                elif pygame.Rect.collidepoint(j.buymax_rect, i.pos):
                    while j.cost <= cook:
                        j.buy(1)
    clock.tick(FPS)
pygame.display.quit()