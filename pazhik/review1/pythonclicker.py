from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
from functools import partial
import time


class Update:
    def showmoney(self, changed):
        if changed.money < 1000:
            changed.moneylab.config(text="Money: {}$".format(changed.money))
        elif changed.money < 1000000:
            changed.moneylab.config(text="Money: {}K$".format(changed.money // 1000))
        elif changed.money < 1000000000:
            changed.moneylab.config(text="Money: {}B$".format(changed.money // 1000000))
        elif changed.money < 1000000000000:
            changed.moneylab.config(text="Money: {}T$".format(changed.money // 1000000000))
        else:
            changed.moneylab.config(text="Money: {}Q$".format(changed.money // 1000000000000))

    def showlabelmoney(self, where, text, place, autoclickers):
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


    def buy(self, changed, place, money_cost, money_plus, where_put, text):
        if changed.money >= money_cost:
            changed.autoclickers[place] += 1
            changed.money -= money_cost
            changed.money_per_sec += money_plus
            self.showlabelmoney(where_put, text, place, changed.autoclickers)
            self.showmoney(changed)

    ################################################################
    def sell(self, changed, place, money_cost, money_plus, where_put, text):
        if changed.autoclickers[place] > 0:
            changed.autoclickers[place] -= 1
            changed.money += money_cost
            changed.money_per_sec -= money_plus
            self.showlabelmoney(where_put, text, place, changed.autoclickers)
            self.showmoney(changed)

    def buyEARTH(self, changed):
        if changed.money >= 3000000000000:
            changed.money -= 3000000000000
            self.showmoney(changed)
            messagebox.showinfo("!!!!!!!!!!!!!!!!!", "YOU WIN!")

    def click_button(self, changed):
        changed.money += changed.money_per_click
        self.showmoney(changed)

    ###############################################################

    def upgrade(self, changed):
        if changed.money >= changed.price_for_upgrade:
            changed.money -= changed.price_for_upgrade
            changed.money_per_click *= 3
            changed.price_for_upgrade *= 5
            self.showmoney(changed)
            if changed.price_for_upgrade < 1000:
                changed.btnupgrade.config(text="Upgrade: {}$".format(changed.price_for_upgrade))
            elif changed.price_for_upgrade < 1000000:
                changed.btnupgrade.config(text="Upgrade: {}K$".format(changed.price_for_upgrade // 1000))
            elif changed.price_for_upgrade < 1000000000:
                changed.btnupgrade.config(text="Upgrade: {}B$".format(changed.price_for_upgrade // 1000000))
            elif changed.price_for_upgrade < 1000000000000:
                changed.btnupgrade.config(text="Upgrade: {}T$".format(changed.price_for_upgrade // 1000000000))
            else:
                changed.btnupgrade.config(text="Upgrade: {}Q$".format(changed.price_for_upgrade // 1000000000000))


class Window:
    def __init__(self, update):
        self.money_per_sec = 0
        self.updat = update
        self.money = 0
        self.money_per_click = 1
        self.price_for_upgrade = 3
        self.autoclickers = {'shop': 0, 'casino': 0, 'oilcompany': 0, 'weapon': 0, 'town': 0}

        self.root = Tk()
        self.root.title("Idle Clicker")
        self.root.geometry("1200x800")

        # background
        im = Image.open('bitcoin.jpg')
        im = im.resize((1200, 800), Image.ANTIALIAS)
        im = ImageTk.PhotoImage(im)
        backgr = Label(self.root, image=im)
        backgr.place(relx=.5, rely=.5, anchor="c")

        # label money
        self.moneylab = Label(self.root, text="Money: 0", bg='gold', font="Arial 20")
        self.moneylab.place(relx=.01, rely=.02, width="180", height="30")

        # clickbutton
        image = Image.open("4.gif")
        image = image.resize((250, 200), Image.ANTIALIAS)
        newimage = ImageTk.PhotoImage(image)
        click_button = partial(update.click_button, self)
        clickbtn = Button(self.root, text="Click", background="#555", foreground="#ccc",
                          padx="20", pady="8", font="16",
                          image=newimage, command=click_button)
        clickbtn.place(relx=.45, rely=.87, anchor="c", height=200, width=250, bordermode=OUTSIDE)

        # button upgrade click
        upgrade = partial(update.upgrade, self)
        self.btnupgrade = Button(self.root, text="Upgrade 3$", background='OliveDrab4', foreground="deep sky blue",
                            padx="20", pady="8", font="Arial 20", command=upgrade)
        self.btnupgrade.place(relx=.1, rely=.5, anchor="c", height=100, width=200, bordermode=OUTSIDE)

        # label upgrade
        self.moneyupg = Label(self.root, text="Increase money per click", bg='gold', font="Arial 10")
        self.moneyupg.place(relx=.1, rely=.4, anchor="c", width="180", height="30", bordermode=OUTSIDE)

        ############################################
        # label shop
        shoplab = Label(self.root, text="SHOP: 0", bg='blue4', foreground="green2", font="Arial 20", justify=LEFT)
        shoplab.place(x=1100, y=50, anchor="c",  width=180, height=50)

        # button buyshop
        shopbuy = partial(update.buy, self, 'shop', 100, 10, shoplab, 'SHOP')
        btnshopbuy = Button(self.root, text="Buy", background='OliveDrab4', foreground="deep sky blue",
                          padx="20", pady="8", font="16", command=shopbuy)
        btnshopbuy.place(x=820, y=50, anchor="c", height=50, width=50, bordermode=OUTSIDE)

        # button sellshop
        shopsell = partial(update.sell, self, 'shop', 100, 10, shoplab, 'SHOP')
        btnshopsell = Button(self.root, text="Sell", background='OliveDrab4', foreground="deep sky blue",
                          padx="20", pady="8", font="16", command=shopsell)
        btnshopsell.place(x=870, y=50, anchor="c", height=50, width=50, bordermode=OUTSIDE)


        # label shop price
        shopprice = Label(self.root, text="100$", bg='chocolate3', foreground="gold", font="Arial 20")
        shopprice.place(x=950, y=50, anchor="c",  width=100, height=50)

        ############################################
        # label casino
        casinolab = Label(self.root, text="CASINO: 0", bg='blue4', foreground="green2", font="Arial 20", justify=LEFT)
        casinolab.place(x=1100, y=150, anchor="c",  width=180, height=50)

        # button buycasino
        casinobuy = partial(update.buy, self, 'casino', 10000, 300, casinolab, 'CASINO')
        btncasinobuy = Button(self.root, text="Buy", background='OliveDrab4', foreground="deep sky blue",
                          padx="20", pady="8", font="16", command=casinobuy)
        btncasinobuy.place(x=820, y=150, anchor="c", height=50, width=50, bordermode=OUTSIDE)

        # button sellcasino
        casinosell = partial(update.sell, self, 'casino', 10000, 300, casinolab, 'CASINO')
        btncasinosell = Button(self.root, text="Sell", background='OliveDrab4', foreground="deep sky blue",
                          padx="20", pady="8", font="16", command=casinosell)
        btncasinosell.place(x=870, y=150, anchor="c", height=50, width=50, bordermode=OUTSIDE)


        # label casino price
        casinoprice = Label(self.root, text="10K$", bg='chocolate3', foreground="gold", font="Arial 20")
        casinoprice.place(x=950, y=150, anchor="c",  width=100, height=50)

        ############################################
        # label casino
        oillab = Label(self.root, text="OIL: 0", bg='blue4', foreground="green2", font="Arial 20", justify=LEFT)
        oillab.place(x=1100, y=250, anchor="c",  width=180, height=50)

        # button buyoil
        oilbuy = partial(update.buy, self, 'oilcompany', 1000000, 8000, oillab, 'OIL')
        btnoilbuy = Button(self.root, text="Buy", background='OliveDrab4', foreground="deep sky blue",
                          padx="20", pady="8", font="16", command=oilbuy)
        btnoilbuy.place(x=820, y=250, anchor="c", height=50, width=50, bordermode=OUTSIDE)

        # button selloil
        oilsell = partial(update.sell, self, 'oilcompany', 1000000, 8000, oillab, 'OIL')
        btnoilsell = Button(self.root, text="Sell", background='OliveDrab4', foreground="deep sky blue",
                          padx="20", pady="8", font="16", command=oilsell)
        btnoilsell.place(x=870, y=250, anchor="c", height=50, width=50, bordermode=OUTSIDE)


        # label oil price
        oilprice = Label(self.root, text="1B$", bg='chocolate3', foreground="gold", font="Arial 20")
        oilprice.place(x=950, y=250, anchor="c",  width=100, height=50)
        ############################################

        # label weapon
        weaponlab = Label(self.root, text="ARMY: 0", bg='blue4', foreground="green2", font="Arial 20", justify=LEFT)
        weaponlab.place(x=1100, y=350, anchor="c",  width=180, height=50)

        # button buyweapon
        weaponbuy = partial(update.buy, self, 'weapon', 100000000, 100000, weaponlab, 'ARMY')
        btnweaponbuy = Button(self.root, text="Buy", background='OliveDrab4', foreground="deep sky blue",
                          padx="20", pady="8", font="16", command=weaponbuy)
        btnweaponbuy.place(x=820, y=350, anchor="c", height=50, width=50, bordermode=OUTSIDE)

        # button sellweapon
        weaponsell = partial(update.sell, self, 'weapon', 100000000, 100000, weaponlab, 'ARMY')
        btnweaponsell = Button(self.root, text="Sell", background='OliveDrab4', foreground="deep sky blue",
                          padx="20", pady="8", font="16", command=weaponsell)
        btnweaponsell.place(x=870, y=350, anchor="c", height=50, width=50, bordermode=OUTSIDE)

        # label weapon price
        weaponprice = Label(self.root, text="100B$", bg='chocolate3', foreground="gold", font="Arial 20")
        weaponprice.place(x=950, y=350, anchor="c",  width=100, height=50)

        ############################################
        # label town
        townlab = Label(self.root, text="TOWN: 0", bg='blue4', foreground="green2", font="Arial 20")
        townlab.place(x=1100, y=450, anchor="c",  width=180, height=50)

        # button buyoil
        townbuy = partial(update.buy, self, 'town', 10000000000, 3000000, townlab, 'TOWN')
        btntownbuy = Button(self.root, text="Buy", background='OliveDrab4', foreground="deep sky blue",
                          padx="20", pady="8", font="16", command=townbuy)
        btntownbuy.place(x=820, y=450, anchor="c", height=50, width=50, bordermode=OUTSIDE)

        # button selltown
        townsell = partial(update.sell, self, 'town', 10000000000, 3000000, townlab, 'TOWN')
        btntownsell = Button(self.root, text="Sell", background='OliveDrab4', foreground="deep sky blue",
                          padx="20", pady="8", font="16", command=townsell)
        btntownsell.place(x=870, y=450, anchor="c", height=50, width=50, bordermode=OUTSIDE)


        # label oil price
        townprice = Label(self.root, text="10T$", bg='chocolate3', foreground="gold", font="Arial 20")
        townprice.place(x=950, y=450, anchor="c",  width=100, height=50)

        ##############################################################

        # label EARTH
        EARTHlab = Label(self.root, text="3Q$", bg='chocolate3', foreground="gold", font="Arial 20")
        EARTHlab.place(x=950, y=550, anchor="c",  width=100, height=50)
        # button buyEARTH
        imearth = Image.open("earth.jpg")
        imearth = imearth.resize((350, 230), Image.ANTIALIAS)
        newimearth = ImageTk.PhotoImage(imearth)
        buyEARTH = partial(update.buyEARTH, self)
        btntownbuy = Button(self.root, background='black', padx="20", pady="8", font="16",
                            image=newimearth, command=buyEARTH)
        btntownbuy.place(x=950, y=700, anchor="c", height=230, width=350)
        ################################################################
        messagebox.showinfo("!!!!!!!!!!!!!!!!!", "Perpose of the game - buy EARTH")
        self.Refresher()
        self.root.mainloop()

    def Refresher(self):
        self.money += self.money_per_sec
        self.updat.showmoney(self)
        self.root.after(1000, self.Refresher)# every second...

def main():
    x = Update()
    Window(x)

main()
