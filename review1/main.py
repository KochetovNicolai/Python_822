import pygame

pygame.init()

from classes import items
import text, vars


def event_processing(event):
    print(event)
    if event.type == pygame.QUIT:
        vars.accumulative.not_done = False
    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE:
            print(vars.accumulative.cookies)
            vars.accumulative.cookies+= vars.accumulative.cookies_per_click
            vars.accumulative.clicks+=1
            vars.accumulative.all_cookies+= vars.accumulative.cookies_per_click
    elif event.type == Income:
        vars.accumulative.cookies+= vars.accumulative.cookies_income
        vars.accumulative.all_cookies+= vars.accumulative.cookies_income
    elif (event.type == pygame.MOUSEBUTTONUP):
        for i in items:
            if pygame.Rect.collidepoint(i.buy_rec, event.pos):
                i.buy(1)
            elif pygame.Rect.collidepoint(i.buy10_rect, event.pos):
                i.buy(10)
            elif pygame.Rect.collidepoint(i.buymax_rect, event.pos):
                while i.cost <= vars.accumulative.cookies:
                    i.buy(1)

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Clicker")
print(pygame.font.get_fonts())
clock = pygame.time.Clock()
Income = pygame.USEREVENT + 1
pygame.time.set_timer(Income, 1000)
while vars.accumulative.not_done:
    text.screen_update(screen,0)
    pos = pygame.mouse.get_pos()
    for j in items:
        if pygame.Rect.collidepoint(j.buy_rec, pos):
            j.on_point(pos)
    pygame.display.update()
    for i in pygame.event.get():
        event_processing(i)
    clock.tick(vars.FPS)
pygame.display.quit()
