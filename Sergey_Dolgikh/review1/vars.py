from pygame import font, display


screen = display.set_mode((800, 600))
fontObj1 = font.SysFont('arial', 25)
fontObj2 = font.SysFont('arial', 15)

white = (255, 255, 255)
light_grey = (230, 230, 230)
grey = (150, 150, 150)
black = (0, 0, 0)
FPS = 60
class status:
    not_done = True
    cookies = 0
    all_cookies = 0
    clicks = 0
    cookies_per_click = 1
    cookies_income = 0
    improve_cost = 10
accumulative = status()
