def has_enough_money(n, cost, amount):
    return round(cost * 10 * (1.1 ** n - 1), 4) <= amount

def button_rectangle(screen, font, text, font_color, fill_color, coords, f):
    textSurfaceObj = font.render(text, True, font_color, fill_color)
    textRectObj = textSurfaceObj.get_rect()
    if f:
        textRectObj.center = coords
    else:
        textRectObj.topleft = coords
    screen.blit(textSurfaceObj, textRectObj)
    return textRectObj
