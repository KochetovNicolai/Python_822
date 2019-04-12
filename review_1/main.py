from tkinter import *
import os
from functools import partial

class Window:
    def __init__(self, root, update):
        self.root = root
        self.update = update
        self.root.configure(background='#eafffa')

        self.lowFrame = Frame(root)
        self.canvas = Canvas(self.lowFrame, width=250, height=400, background='#eafffa')
        self.frame = Frame(self.canvas)
        self.myscrollbar = Scrollbar(self.lowFrame, orient='vertical', command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.myscrollbar.set)
        self.canvas.create_window((0,0), window = self.frame)
        def conf(event):
            self.canvas.configure(scrollregion=self.canvas.bbox('all'))
        self.frame.bind('<Configure>', conf)
        self.lowFrame.pack(side='right')
        self.myscrollbar.pack(side='right', fill=Y)
        self.canvas.pack()

        self.shop = PhotoImage(file=os.path.join('images', 'shop.png'))
        self.shopLabel = Label(root, image=self.shop, background='#eafffa')
        self.shopLabel.place(relx=0.75)

        self.inscription = PhotoImage(file=os.path.join('images', 'shop1.png'))
        self.inscriptionLabel = Label(root, image=self.inscription, background='#eafffa')
        self.inscriptionLabel.place(relx=0.75, rely=0.85)

        self.line = PhotoImage(file=os.path.join('images', 'line.png'))
        self.lineLabel = Label(root, image=self.line)
        self.lineLabel.place(relx=0.7)

        self.scoreLabel = Label(root, text="Очки: 0", font=("Helvetica", 12), background='#eafffa')
        self.scoreLabel.place(relx=0.3, rely=0.05)

        self.cookie = PhotoImage(file=os.path.join('images', 'cookie.png'))
        self.updateScore = partial(update.updateScore, self)
        self.cook = Button(root, image=self.cookie, background='#eafffa', activebackground='#eafffa', bd=0, command=self.updateScore)
        self.cook.place(relx=0.2, rely=0.2)

        self.buttons = [PhotoImage(file=os.path.join('images', 'Button1.png')),
                        PhotoImage(file=os.path.join('images', 'Button2.png')),
                        PhotoImage(file=os.path.join('images', 'Button3.png')),
                        PhotoImage(file=os.path.join('images', 'Button4.png')),
                        PhotoImage(file=os.path.join('images', 'Button5.png'))]
        self.cursors = [ Button(self.frame, image=i, bd=0, background='#eafffa') for i in self.buttons ]


        self.price = [[1,20], [3,100], [5,500], [10,3000], [30,10000]]
        self.k = 0 #для итерации по price
        for i in self.cursors:
            self.buy = partial(update.buy, self, self.price[self.k][1], self.price[self.k][0])
            self.k += 1
            i.configure(command=self.buy)
        for i in self.cursors:
            i.pack()


class Update:
    def __init__(self):
        self.score = 0

    def updateScore(self, object):
        self.score += 1
        object.scoreLabel.config(text="Очки: {}".format(self.score))

    def buy(self, object, cost, amount_click):
        if self.score >= cost:
            self.score -= cost
            self.autoClicker(object, amount_click)

    def autoClicker(self, object, n):
        self.score += n
        object.scoreLabel.config(text="Очки: {}".format(self.score))
        root.after(1000, self.autoClicker, object, n) #30 игровых секунд = 1 секунде (чтобы быстрее проверять работоспособность функции)



root = Tk()
root.title("Кликер")
root.geometry("1000x600")
root.resizable(False, False)
update = Update()
Window(root, update)
root.mainloop()
