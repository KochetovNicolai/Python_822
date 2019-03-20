from tkinter import *

score = 0

def updateScoreSpace(event): #обновление очков при нажатии пробела
    global score
    score += 1
    scoreLabel.config(text="Очки:  {}".format(score))

def updateScore(): #обновлние очков при нажатии на печеньку
    global score
    score += 1
    scoreLabel.config(text="Очки:  {}".format(score))

def get_autoClicker(n): #проверяем хватает ли очков для покупки автоклика
    global score
    if n == 1:
        if score >= 20:
            score -= 20
            autoClicker(n)
        else:
            pass
    elif n == 3:
        if score >= 100:
            score -= 100
            autoClicker(n)
        else:
            pass
    elif n == 5:
        if score >= 500:
            score -= 500
            autoClicker(n)
        else:
            pass
    elif n == 10:
        if score >= 3000:
            score -= 3000
            autoClicker(n)
        else:
            pass
    elif n == 30:
        if score >= 10000:
            score -= 10000
            autoClicker(n)
        else:
            pass

def autoClicker(n): #автокликер
    global score
    score += n
    scoreLabel.config(text="Очки:  {}".format(score))
    root.after(30000, autoClicker, n)

root = Tk()
root.title("Кликер")
root.geometry("1000x600")
root.configure(background='#eafffa')

lowFrame = Frame(root) #создаем контейнер для магазина

canvas = Canvas(lowFrame, width=250, height=400, background='#eafffa')
frame = Frame(canvas)
myscrollbar = Scrollbar(lowFrame, orient = 'vertical', command = canvas.yview) #добаляем скролбар
canvas.configure(yscrollcommand = myscrollbar.set)

canvas.create_window((0,0), window = frame)

def conf(event):
    canvas.configure(scrollregion = canvas.bbox('all'))
frame.bind('<Configure>', conf)

shop = PhotoImage(file="images\shop.png")
shopLabel = Label(root, image=shop,background='#eafffa')

inscription = PhotoImage(file="images\shop1.png")
inscriptionLabel = Label(root, image=inscription, background='#eafffa')

line = PhotoImage(file="images\line.png")
lineLabel = Label(root, image=line)

scoreLabel = Label(root, text="Очки: " + str(score), font=("Helvetica", 12), background='#eafffa')

cookie = PhotoImage(file="images\cookie.png")
cook = Button(root, image=cookie, background='#eafffa', activebackground='#eafffa', bd=0, command = updateScore)


button1 = PhotoImage(file="images\Button1.png")
button2 = PhotoImage(file="images\Button2.png")
button3 = PhotoImage(file="images\Button3.png")
button4 = PhotoImage(file="images\Button4.png")
button5 = PhotoImage(file="images\Button5.png")
#кнопки магазина
cursor1 = Button(frame, image=button1, bd=0, background='#eafffa', command=lambda: get_autoClicker(1))
cursor2 = Button(frame, image=button2, bd=0, background='#eafffa', command=lambda: get_autoClicker(3))
cursor3 = Button(frame, image=button3, bd=0, background='#eafffa', command=lambda: get_autoClicker(5))
cursor4 = Button(frame, image=button4, bd=0, background='#eafffa', command=lambda: get_autoClicker(10))
cursor5 = Button(frame, image=button5, bd=0, background='#eafffa', command=lambda: get_autoClicker(30))

root.bind('<space>', updateScoreSpace) #обновление очков при нажатии на пробел

lowFrame.pack(side = 'right')
myscrollbar.pack(side = 'right', fill = Y)
canvas.pack()

inscriptionLabel.place(x=760, y=505)
scoreLabel.place(x = 265, y = 25)
cook.place(x = 150, y = 120)
shopLabel.place(x = 750, y = 10)
lineLabel.place(x=720)

cursor1.pack()
cursor2.pack()
cursor3.pack()
cursor4.pack()
cursor5.pack()

root.mainloop()