from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
from functools import partial
import time


class Update:
    def __init__(self):
        self.money_per_sec = 0
        self.money = 0
        self.money_per_click = 1
        self.price_for_upgrade = 3
        self.autoclickers = {'shop': 0, 'casino': 0, 'oilcompany': 0, 'weapon': 0, 'town': 0}
        self.constants = [1, 1000, 1000000, 1000000000, 1000000000000, 1000000000000000, 1000000000000000000, 1000000000000000000000]
        self.letters = ['', 'K', 'B', 'T', 'Qi', 'Qa', 'Sq', 'Sp']

    def showmoney(self, changed):
        for i in range(len(self.constants)-1):
            if self.money < self.constants[i+1]:
                changed.moneylab.config(text="Money: {}${}".format(self.money // self.constants[i], self.letters[i]))
                return 0

    def showlabelmoney(self, where, text, place):
        for i in range(len(self.constants)-1):
            if self.autoclickers[place] < self.constants[i+1]:
                where.config(text=text+": {}{}".format(self.autoclickers[place] // self.constants[i], self.letters[i]))
                return 0

    def buy(self, changed, place, money_cost, money_plus, where_put, text):
        if self.money >= money_cost:
            self.autoclickers[place] += 1
            self.money -= money_cost
            self.money_per_sec += money_plus
            self.showlabelmoney(where_put, text, place)
            self.showmoney(changed)

    ################################################################
    def sell(self, changed, place, money_cost, money_plus, where_put, text):
        if self.autoclickers[place] > 0:
            self.autoclickers[place] -= 1
            self.money += money_cost
            self.money_per_sec -= money_plus
            self.showlabelmoney(where_put, text, place)
            self.showmoney(changed)

    def buyEARTH(self, changed):
        if self.money >= 3000000000000:
            self.money -= 3000000000000
            self.showmoney(changed)
            messagebox.showinfo("!!!!!!!!!!!!!!!!!", "YOU WIN!")

    def click_button(self, changed):
        self.money += self.money_per_click
        self.showmoney(changed)

    ###############################################################

    def upgrade(self, changed):
        if self.money >= self.price_for_upgrade:
            self.money -= self.price_for_upgrade
            self.money_per_click *= 3
            self.price_for_upgrade *= 5
            self.showmoney(changed)
            for i in range(len(self.constants) - 1):
                if self.price_for_upgrade < self.constants[i+1]:
                    changed.btnupgrade.config(text="Upgrade: {}${}".format(self.price_for_upgrade // self.constants[i], self.letters[i]))
                    return 0

class Window:
    def __init__(self, update, root):
        self.update = update
        self.root = root
        # background
        self.im = Image.open('bitcoin.jpg')
        self.im = self.im.resize((1200, 800), Image.ANTIALIAS)
        self.im = ImageTk.PhotoImage(self.im)
        self.backgr = Label(root, image=self.im)
        self.backgr.place(relx=.5, rely=.5, anchor="c")

        # label money
        self.moneylab = Label(root, text="Money: 0", bg='gold', font="Arial 20")
        self.moneylab.place(relx=.01, rely=.02, width="180", height="30")

        # clickbutton
        self.image = Image.open("4.gif")
        self.image = self.image.resize((250, 200), Image.ANTIALIAS)
        self.newimage = ImageTk.PhotoImage(self.image)
        self.click_button = partial(update.click_button, self)
        self.clickbtn = Button(root, text="Click", background="#555", foreground="#ccc",
                          padx="20", pady="8", font="16",
                          image=self.newimage, command=self.click_button)
        self.clickbtn.place(relx=.45, rely=.87, anchor="c", height=200, width=250, bordermode=OUTSIDE)

        # button upgrade click
        self.upgrade = partial(update.upgrade, self)
        self.btnupgrade = Button(root, text="Upgrade 3$", background='OliveDrab4', foreground="deep sky blue",
                                 padx="20", pady="8", font="Arial 20", command=self.upgrade)
        self.btnupgrade.place(relx=.1, rely=.5, anchor="c", height=100, width=200, bordermode=OUTSIDE)

        # label upgrade
        self.moneyupg = Label(root, text="Increase money per click", bg='gold', font="Arial 10")
        self.moneyupg.place(relx=.1, rely=.4, anchor="c", width="180", height="30", bordermode=OUTSIDE)

        ############################################
        # label shop
        self.shoplab = Label(root, text="SHOP: 0", bg='blue4', foreground="green2", font="Arial 20", justify=LEFT)
        self.shoplab.place(x=1100, y=50, anchor="c",  width=180, height=50)

        # button buyshop
        self.shopbuy = partial(update.buy, self, 'shop', 100, 10, self.shoplab, 'SHOP')
        self.btnshopbuy = Button(root, text="Buy", background='OliveDrab4', foreground="deep sky blue",
                          padx="20", pady="8", font="16", command=self.shopbuy)
        self.btnshopbuy.place(x=820, y=50, anchor="c", height=50, width=50, bordermode=OUTSIDE)

        # button sellshop
        self.shopsell = partial(update.sell, self, 'shop', 100, 10, self.shoplab, 'SHOP')
        self.btnshopsell = Button(root, text="Sell", background='OliveDrab4', foreground="deep sky blue",
                          padx="20", pady="8", font="16", command=self.shopsell)
        self.btnshopsell.place(x=870, y=50, anchor="c", height=50, width=50, bordermode=OUTSIDE)


        # label shop price
        self.shopprice = Label(root, text="100$", bg='chocolate3', foreground="gold", font="Arial 20")
        self.shopprice.place(x=950, y=50, anchor="c",  width=100, height=50)

        ############################################
        # label casino
        self.casinolab = Label(root, text="CASINO: 0", bg='blue4', foreground="green2", font="Arial 20", justify=LEFT)
        self.casinolab.place(x=1100, y=150, anchor="c",  width=180, height=50)

        # button buycasino
        self.casinobuy = partial(update.buy, self, 'casino', 10000, 300, self.casinolab, 'CASINO')
        self.btncasinobuy = Button(root, text="Buy", background='OliveDrab4', foreground="deep sky blue",
                                   padx="20", pady="8", font="16", command=self.casinobuy)
        self.btncasinobuy.place(x=820, y=150, anchor="c", height=50, width=50, bordermode=OUTSIDE)

        # button sellcasino
        self.casinosell = partial(update.sell, self, 'casino', 10000, 300, self.casinolab, 'CASINO')
        self.btncasinosell = Button(root, text="Sell", background='OliveDrab4', foreground="deep sky blue",
                               padx="20", pady="8", font="16", command=self.casinosell)
        self.btncasinosell.place(x=870, y=150, anchor="c", height=50, width=50, bordermode=OUTSIDE)


        # label casino price
        self.casinoprice = Label(root, text="10K$", bg='chocolate3', foreground="gold", font="Arial 20")
        self.casinoprice.place(x=950, y=150, anchor="c",  width=100, height=50)

        ############################################
        # label casino
        self.oillab = Label(root, text="OIL: 0", bg='blue4', foreground="green2", font="Arial 20", justify=LEFT)
        self.oillab.place(x=1100, y=250, anchor="c",  width=180, height=50)

        # button buyoil
        self.oilbuy = partial(update.buy, self, 'oilcompany', 1000000, 8000, self.oillab, 'OIL')
        self.btnoilbuy = Button(root, text="Buy", background='OliveDrab4', foreground="deep sky blue",
                           padx="20", pady="8", font="16", command=self.oilbuy)
        self.btnoilbuy.place(x=820, y=250, anchor="c", height=50, width=50, bordermode=OUTSIDE)

        # button selloil
        self.oilsell = partial(update.sell, self, 'oilcompany', 1000000, 8000, self.oillab, 'OIL')
        self.btnoilsell = Button(root, text="Sell", background='OliveDrab4', foreground="deep sky blue",
                            padx="20", pady="8", font="16", command=self.oilsell)
        self.btnoilsell.place(x=870, y=250, anchor="c", height=50, width=50, bordermode=OUTSIDE)


        # label oil price
        self.oilprice = Label(root, text="1B$", bg='chocolate3', foreground="gold", font="Arial 20")
        self.oilprice.place(x=950, y=250, anchor="c",  width=100, height=50)
        ############################################

        # label weapon
        self.weaponlab = Label(root, text="ARMY: 0", bg='blue4', foreground="green2", font="Arial 20", justify=LEFT)
        self.weaponlab.place(x=1100, y=350, anchor="c",  width=180, height=50)

        # button buyweapon
        self.weaponbuy = partial(update.buy, self, 'weapon', 100000000, 100000, self.weaponlab, 'ARMY')
        self.btnweaponbuy = Button(root, text="Buy", background='OliveDrab4', foreground="deep sky blue",
                                   padx="20", pady="8", font="16", command=self.weaponbuy)
        self.btnweaponbuy.place(x=820, y=350, anchor="c", height=50, width=50, bordermode=OUTSIDE)

        # button sellweapon
        self.weaponsell = partial(update.sell, self, 'weapon', 100000000, 100000, self.weaponlab, 'ARMY')
        self.btnweaponsell = Button(root, text="Sell", background='OliveDrab4', foreground="deep sky blue",
                                    padx="20", pady="8", font="16", command=self.weaponsell)
        self.btnweaponsell.place(x=870, y=350, anchor="c", height=50, width=50, bordermode=OUTSIDE)

        # label weapon price
        self.weaponprice = Label(root, text="100B$", bg='chocolate3', foreground="gold", font="Arial 20")
        self.weaponprice.place(x=950, y=350, anchor="c",  width=100, height=50)

        ############################################
        # label town
        self.townlab = Label(root, text="TOWN: 0", bg='blue4', foreground="green2", font="Arial 20")
        self.townlab.place(x=1100, y=450, anchor="c",  width=180, height=50)

        # button buyoil
        self.townbuy = partial(update.buy, self, 'town', 10000000000, 3000000, self.townlab, 'TOWN')
        self.btntownbuy = Button(root, text="Buy", background='OliveDrab4', foreground="deep sky blue",
                                 padx="20", pady="8", font="16", command=self.townbuy)
        self.btntownbuy.place(x=820, y=450, anchor="c", height=50, width=50, bordermode=OUTSIDE)

        # button selltown
        self.townsell = partial(update.sell, self, 'town', 10000000000, 3000000, self.townlab, 'TOWN')
        self.btntownsell = Button(root, text="Sell", background='OliveDrab4', foreground="deep sky blue",
                             padx="20", pady="8", font="16", command=self.townsell)
        self.btntownsell.place(x=870, y=450, anchor="c", height=50, width=50, bordermode=OUTSIDE)


        # label oil price
        self.townprice = Label(root, text="10T$", bg='chocolate3', foreground="gold", font="Arial 20")
        self.townprice.place(x=950, y=450, anchor="c",  width=100, height=50)

        ##############################################################

        # label EARTH
        self.EARTHlab = Label(root, text="3Q$", bg='chocolate3', foreground="gold", font="Arial 20")
        self.EARTHlab.place(x=950, y=550, anchor="c",  width=100, height=50)
        # button buyEARTH
        self.imearth = Image.open("earth.jpg")
        self.imearth = self.imearth.resize((350, 230), Image.ANTIALIAS)
        self.newimearth = ImageTk.PhotoImage(self.imearth)
        self.buyEARTH = partial(update.buyEARTH, self)
        self.btntownbuy = Button(root, background='black', padx="20", pady="8", font="16",
                                 image=self.newimearth, command=self.buyEARTH)
        self.btntownbuy.place(x=950, y=700, anchor="c", height=230, width=350)
        ################################################################
        messagebox.showinfo("!!!!!!!!!!!!!!!!!", "Perpose of the game - buy EARTH")
        self.Refresher()

    def Refresher(self):
        self.update.money += self.update.money_per_sec
        self.update.showmoney(self)
        self.root.after(1000, self.Refresher)# every second...


root = Tk()
root.title("Idle Clicker")
root.geometry("1200x800")
x = Update()
Window(x, root)
root.mainloop()
