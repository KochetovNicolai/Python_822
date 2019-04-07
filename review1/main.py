import pygame

pygame.init()

from classes import items
import text, vars


def event_processing(i):
    print(i)
    if i.type == pygame.QUIT:
        vars.not_done = False
    elif i.type == pygame.KEYDOWN:
        if i.unicode == ' ':
            print(vars.cookies)
            vars.cookies+= vars.cookies_per_click
            vars.clicks+=1
            vars.all_cookies+= vars.cookies_per_click
    elif i.type == Income:
        vars.cookies+= vars.cookies_income
        vars.all_cookies+= vars.cookies_income
    elif (i.type == pygame.MOUSEBUTTONUP):
        for j in items:
            if pygame.Rect.collidepoint(j.buy_rec, i.pos):
                j.buy(1)
            elif pygame.Rect.collidepoint(j.buy10_rect, i.pos):
                j.buy(10)
            elif pygame.Rect.collidepoint(j.buymax_rect, i.pos):
                while j.cost <= vars.cookies:
                    j.buy(1)

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Clicker")
print(pygame.font.get_fonts())
clock = pygame.time.Clock()
Income = pygame.USEREVENT + 1
pygame.time.set_timer(Income, 1000)
while vars.not_done:
    text.screen_update(screen,0)
    pos = pygame.mouse.get_pos()
    for j in items:
        if pygame.Rect.collidepoint(j.buy_rec, pos):
            j.is_pointed(pos)
    pygame.display.update()
    for i in pygame.event.get():
        event_processing(i)
    clock.tick(vars.FPS)
pygame.display.quit()
