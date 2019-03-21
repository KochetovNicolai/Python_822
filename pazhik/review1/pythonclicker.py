#!/usr/bin/python3
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
from functools import partial
import time

money = 0
money_per_sec = 0
money_per_click = 1
price_for_upgrade = 3
autoclickers = {'shop': 0, 'casino': 0, 'oilcompany': 0, 'weapon': 0, 'town': 0}


def showmoney():
    global money
    if money < 1000:
        moneylab.config(text="Money: {}$".format(money))
    elif money < 1000000:
        moneylab.config(text="Money: {}K$".format(money // 1000))
    elif money < 1000000000:
        moneylab.config(text="Money: {}B$".format(money // 1000000))
    elif money < 1000000000000:
        moneylab.config(text="Money: {}T$".format(money // 1000000000))
    else:
        moneylab.config(text="Money: {}Q$".format(money // 1000000000000))


def showlabelmoney(where, text, place):
    global autoclickers
    if autoclickers[place] < 1000:
        where.config(text=text+": {}".format(autoclickers[place]))
    elif autoclickers[place] < 1000000:
        where.config(text=text+": {}K".format(autoclickers[place] // 1000))
    elif autoclickers[place] < 1000000000:
        where.config(text=text+": {}B".format(autoclickers[place] // 1000000))
    elif autoclickers[place] < 1000000000000:
        where.config(text=text+": {}T".format(autoclickers[place] // 1000000000))
    else:
        where.config(text=text+": {}Q".format(autoclickers[place] // 1000000000000))


def Refresher():
    global money_per_sec, money
    money += money_per_sec
    showmoney()
    root.after(1000, Refresher)# every second...

################################################################
def buy(place, money_cost, money_plus, where_put, text):
    global autoclickers, money, money_per_sec
    if money >= money_cost:
        autoclickers[place] += 1
        money -= money_cost
        money_per_sec += money_plus
        showlabelmoney(where_put, text, place)
        showmoney()


def sell(place, money_cost, money_plus, where_put, text):
    global autoclickers, money, money_per_sec
    if autoclickers[place] > 0:
        autoclickers[place] -= 1
        money += money_cost
        money_per_sec -= money_plus
        showlabelmoney(where_put, text, place)
        showmoney()


def buyEARTH():
    global money
    if money >= 3000000000000:
        money -= 3000000000000
        showmoney()
        messagebox.showinfo("!!!!!!!!!!!!!!!!!", "YOU WIN!")

###############################################################


def click_button():
    global money, money_per_click
    money += money_per_click
    showmoney()


def upgrade():
    global money_per_click, money, price_for_upgrade
    if money >= price_for_upgrade:
        money -= price_for_upgrade
        money_per_click *= 3
        price_for_upgrade *= 5
        showmoney()
        if price_for_upgrade < 1000:
            btnupgrade.config(text="Upgrade: {}$".format(price_for_upgrade))
        elif price_for_upgrade < 1000000:
            btnupgrade.config(text="Upgrade: {}K$".format(price_for_upgrade // 1000))
        elif price_for_upgrade < 1000000000:
            btnupgrade.config(text="Upgrade: {}B$".format(price_for_upgrade // 1000000))
        elif price_for_upgrade < 1000000000000:
            btnupgrade.config(text="Upgrade: {}T$".format(price_for_upgrade // 1000000000))
        else:
            btnupgrade.config(text="Upgrade: {}Q$".format(price_for_upgrade // 1000000000000))


root = Tk()
root.title("Idle Clicker")
root.geometry("1200x800")


# background
im = Image.open('bitcoin.jpg')
im = im.resize((1200, 800), Image.ANTIALIAS)
im = ImageTk.PhotoImage(im)
backgr = Label(root, image=im)
backgr.place(relx=.5, rely=.5, anchor="c")

# label money
moneylab = Label(root, text="Money: 0", bg='gold', font="Arial 20")
moneylab.place(relx=.01, rely=.02, width="180", height="30")

# clickbutton
image = Image.open("4.gif")
image = image.resize((250, 200), Image.ANTIALIAS)
newimage = ImageTk.PhotoImage(image)
clickbtn = Button(root, text="Click", background="#555", foreground="#ccc",
                  padx="20", pady="8", font="16", image=newimage, command=click_button)
clickbtn.place(relx=.45, rely=.87, anchor="c", height=200, width=250, bordermode=OUTSIDE)

# button upgrade click
btnupgrade = Button(root, text="Upgrade 3$", background='OliveDrab4', foreground="deep sky blue",
                  padx="20", pady="8", font="Arial 20", command=upgrade)
btnupgrade.place(relx=.1, rely=.5, anchor="c", height=100, width=200, bordermode=OUTSIDE)

# label upgrade
moneyupg = Label(root, text="Increase money per click", bg='gold', font="Arial 10")


moneyupg.place(relx=.1, rely=.4, anchor="c", width="180", height="30", bordermode=OUTSIDE)

############################################
# label shop
shoplab = Label(root, text="SHOP: 0", bg='blue4', foreground="green2", font="Arial 20", justify=LEFT)
shoplab.place(x=1100, y=50, anchor="c",  width=180, height=50)

# button buyshop
shopbuy = partial(buy, 'shop', 100, 10, shoplab, 'SHOP')
btnshopbuy = Button(root, text="Buy", background='OliveDrab4', foreground="deep sky blue",
                  padx="20", pady="8", font="16", command=shopbuy)
btnshopbuy.place(x=820, y=50, anchor="c", height=50, width=50, bordermode=OUTSIDE)

# button sellshop
shopsell = partial(sell, 'shop', 100, 10, shoplab, 'SHOP')
btnshopsell = Button(root, text="Sell", background='OliveDrab4', foreground="deep sky blue",
                  padx="20", pady="8", font="16", command=shopsell)
btnshopsell.place(x=870, y=50, anchor="c", height=50, width=50, bordermode=OUTSIDE)


# label shop price
shopprice = Label(root, text="100$", bg='chocolate3', foreground="gold", font="Arial 20")
shopprice.place(x=950, y=50, anchor="c",  width=100, height=50)

############################################
# label casino
casinolab = Label(root, text="CASINO: 0", bg='blue4', foreground="green2", font="Arial 20", justify=LEFT)
casinolab.place(x=1100, y=150, anchor="c",  width=180, height=50)

# button buycasino
casinobuy = partial(buy, 'casino', 10000, 300, casinolab, 'CASINO')
btncasinobuy = Button(root, text="Buy", background='OliveDrab4', foreground="deep sky blue",
                  padx="20", pady="8", font="16", command=casinobuy)
btncasinobuy.place(x=820, y=150, anchor="c", height=50, width=50, bordermode=OUTSIDE)

# button sellcasino
casinosell = partial(sell, 'casino', 10000, 300, casinolab, 'CASINO')
btncasinosell = Button(root, text="Sell", background='OliveDrab4', foreground="deep sky blue",
                  padx="20", pady="8", font="16", command=casinosell)
btncasinosell.place(x=870, y=150, anchor="c", height=50, width=50, bordermode=OUTSIDE)


# label casino price
casinoprice = Label(root, text="10K$", bg='chocolate3', foreground="gold", font="Arial 20")
casinoprice.place(x=950, y=150, anchor="c",  width=100, height=50)

############################################
# label casino
oillab = Label(root, text="OIL: 0", bg='blue4', foreground="green2", font="Arial 20", justify=LEFT)
oillab.place(x=1100, y=250, anchor="c",  width=180, height=50)

# button buyoil
oilbuy = partial(buy, 'oilcompany', 1000000, 8000, oillab, 'OIL')
btnoilbuy = Button(root, text="Buy", background='OliveDrab4', foreground="deep sky blue",
                  padx="20", pady="8", font="16", command=oilbuy)
btnoilbuy.place(x=820, y=250, anchor="c", height=50, width=50, bordermode=OUTSIDE)

# button selloil
oilsell = partial(sell, 'oilcompany', 1000000, 8000, oillab, 'OIL')
btnoilsell = Button(root, text="Sell", background='OliveDrab4', foreground="deep sky blue",
                  padx="20", pady="8", font="16", command=oilsell)
btnoilsell.place(x=870, y=250, anchor="c", height=50, width=50, bordermode=OUTSIDE)


# label oil price
oilprice = Label(root, text="1B$", bg='chocolate3', foreground="gold", font="Arial 20")
oilprice.place(x=950, y=250, anchor="c",  width=100, height=50)
############################################

# label weapon
weaponlab = Label(root, text="ARMY: 0", bg='blue4', foreground="green2", font="Arial 20", justify=LEFT)
weaponlab.place(x=1100, y=350, anchor="c",  width=180, height=50)

# button buyweapon
weaponbuy = partial(buy, 'weapon', 100000000, 100000, weaponlab, 'ARMY')
btnweaponbuy = Button(root, text="Buy", background='OliveDrab4', foreground="deep sky blue",
                  padx="20", pady="8", font="16", command=weaponbuy)
btnweaponbuy.place(x=820, y=350, anchor="c", height=50, width=50, bordermode=OUTSIDE)

# button sellweapon
weaponsell = partial(sell, 'weapon', 100000000, 100000, weaponlab, 'ARMY')
btnweaponsell = Button(root, text="Sell", background='OliveDrab4', foreground="deep sky blue",
                  padx="20", pady="8", font="16", command=weaponsell)
btnweaponsell.place(x=870, y=350, anchor="c", height=50, width=50, bordermode=OUTSIDE)

# label weapon price
weaponprice = Label(root, text="100B$", bg='chocolate3', foreground="gold", font="Arial 20")
weaponprice.place(x=950, y=350, anchor="c",  width=100, height=50)

############################################
# label town
townlab = Label(root, text="TOWN: 0", bg='blue4', foreground="green2", font="Arial 20")
townlab.place(x=1100, y=450, anchor="c",  width=180, height=50)

# button buyoil
townbuy = partial(buy, 'town', 10000000000, 3000000, townlab, 'TOWN')
btntownbuy = Button(root, text="Buy", background='OliveDrab4', foreground="deep sky blue",
                  padx="20", pady="8", font="16", command=townbuy)
btntownbuy.place(x=820, y=450, anchor="c", height=50, width=50, bordermode=OUTSIDE)

# button selltown
townsell = partial(sell, 'town', 10000000000, 3000000, townlab, 'TOWN')
btntownsell = Button(root, text="Sell", background='OliveDrab4', foreground="deep sky blue",
                  padx="20", pady="8", font="16", command=townsell)
btntownsell.place(x=870, y=450, anchor="c", height=50, width=50, bordermode=OUTSIDE)


# label oil price
townprice = Label(root, text="10T$", bg='chocolate3', foreground="gold", font="Arial 20")
townprice.place(x=950, y=450, anchor="c",  width=100, height=50)

##############################################################

# label EARTH
EARTHlab = Label(root, text="3Q$", bg='chocolate3', foreground="gold", font="Arial 20")
EARTHlab.place(x=950, y=550, anchor="c",  width=100, height=50)
# button buyEARTH
imearth = Image.open("earth.jpg")
imearth = imearth.resize((350, 230), Image.ANTIALIAS)
newimearth = ImageTk.PhotoImage(imearth)
btntownbuy = Button(root, background='black', padx="20", pady="8", font="16", image=newimearth, command=buyEARTH)
btntownbuy.place(x=950, y=700, anchor="c", height=230, width=350)
################################################################
messagebox.showinfo("!!!!!!!!!!!!!!!!!", "Perpose of the game - buy EARTH")
Refresher()
root.mainloop()
