import tkinter
import random

okToPressEnter = True

hunger = 50
health = 50
mood = 50
energy = 50

sleepNow = False
playNow = False


# Функция начала игры
def start(event):
    global okToPressEnter

    if okToPressEnter:
        startLabel.place_forget()
        mainLabel.place(x=200, y=570)
        update_hunger()
        update_health()
        update_mood()
        update_energy()

        update_display()

        okToPressEnter = False
    else:
        pass


# Функция обновления интерфейса
def update_display():
    global hunger
    global health

    if is_alive():
        hungerLabel.config(text="Еда: " + str(hunger))
        healthLabel.config(text="Здоровье: " + str(health))
        moodLabel.config(text="Настроение: " + str(mood))
        energyLabel.config(text="Энергия: " + str(energy))

        if sleepNow:
            pet.config(image=sleeping)
            btnWakeUp.place(x=700, y=95)
            btnFeed.place_forget()
            btnTreat.place_forget()
            btnMood.place_forget()
        elif playNow:
            pet.config(image=img)
            btnStopPlay.place(x=700, y=65)
            btnFeed.place_forget()
            btnTreat.place_forget()
            btnSleep.place_forget()
        else:
            if energy <= 30:
                pet.config(image=want_sleep)
            elif hunger <= 30:
                pet.config(image=hungry)
                if mood <= 30:
                    pet.config(image=unhappy)
            elif hunger >= 80:
                pet.config(image=fat)
            elif mood >= 70:
                pet.config(image=happy)
            elif mood <= 30:
                pet.config(image=cry)
            else:
                pet.config(image=normal)
    else:
        if sleepNow:
            btnWakeUp.place_forget()
        pet.config(image=dead)
        hungerLabel.config(text="")
        healthLabel.config(text="")
        moodLabel.config(text="")
        energyLabel.config(text="")
        btnSleep.place_forget()
        btnMood.place_forget()
        btnTreat.place_forget()
        btnFeed.place_forget()

    pet.after(100, update_display)


# Функции обновления характеристик
def update_hunger():
    global hunger
    global energy
    if hunger > 0:
        hunger -= 1
    else:
        energy -= 1

    if is_alive():
        if sleepNow:
            hungerLabel.after(4000, update_hunger)
        elif playNow:
            hungerLabel.after(500, update_hunger)
        else:
            hungerLabel.after(1000, update_hunger)


def update_health():
    global health
    health -= 1

    if is_alive():
        if sleepNow:
            healthLabel.after(4000, update_health)
        else:
            healthLabel.after(1000, update_health)


def update_mood():
    global mood
    if playNow and mood < 100:
        mood += 1
    elif mood > 0:
        mood -= 1
    else:
        hunger -= 1

    if is_alive():
        if sleepNow:
            mood += 2
            moodLabel.after(8000, update_mood)
        elif playNow:
            moodLabel.after(500, update_mood)
        else:
            moodLabel.after(1000, update_mood)


def update_energy():
    global energy
    global health

    if sleepNow and energy < 100:
        energy += 1
    elif energy > 0:
        energy -= 1
    else:
        health -= 1

    if is_alive():
        if playNow or sleepNow:
            energyLabel.after(500, update_energy)
        else:
            energyLabel.after(1000, update_energy)


# Функции восполнения характеристик
def feed():
    global hunger

    if is_alive():
        if hunger <= 90:
            hunger += 10
        else:
            hunger -= 30


def treat():
    global health

    if is_alive():
        if health <= 90:
            health += 10
        else:
            health -= 30


def play():
    global mood
    global playNow
    global img
    playNow = True
    img = random.choice(playing)


def stop_play():
    global playNow
    playNow = False
    btnStopPlay.place_forget()
    btnFeed.place(x=700, y=5)
    btnTreat.place(x=700, y=35)
    btnSleep.place(x=700, y=95)


def sleep():
    global sleepNow
    sleepNow = True


def wake_up():
    global sleepNow
    sleepNow = False
    btnFeed.place(x=700, y=5)
    btnTreat.place(x=700, y=35)
    btnMood.place(x=700, y=65)
    btnWakeUp.place_forget()


# проверка на живость
def is_alive():
    global health

    if health <= 0:
        mainLabel.config(text="Ваш питомец умер :c")
        mainLabel.place(x=290, y=570)
        return False
    else:
        return True


# Задание интерфейса
root = tkinter.Tk()
root.title("Тамагочи")
root.geometry("800x600")

# Картинки
hungry = tkinter.PhotoImage(file="images/want_eat.png")
normal = tkinter.PhotoImage(file="images/normal.png")
dead = tkinter.PhotoImage(file="images/error.png")
happy = tkinter.PhotoImage(file="images/happy.png")
unhappy = tkinter.PhotoImage(file="images/unhappy.png")
sleeping = tkinter.PhotoImage(file="images/sleep.png")
want_sleep = tkinter.PhotoImage(file="images/want_sleep.png")
fat = tkinter.PhotoImage(file="images/fat.png")
cry = tkinter.PhotoImage(file="images/cry.png")
rock = tkinter.PhotoImage(file="images/rock.png")
guitar = tkinter.PhotoImage(file="images/guitar.png")
music = tkinter.PhotoImage(file="images/music.png")
war = tkinter.PhotoImage(file="images/war.png")

playing = [rock, guitar, music, war]

# Картинка хомяка
pet = tkinter.Label(root, image=normal)

# Текстовые поля
startLabel = tkinter.Label(root, text="Чтобы начать игру, нажмите Enter", font=('Helvetica', 14))
mainLabel = tkinter.Label(root, text="Заботьтесь о Сене, не дайте ему погибнуть!", font=('Helvetica', 14))
hungerLabel = tkinter.Label(root, text="Еда: " + str(hunger), font=('Helvetica', 10))
healthLabel = tkinter.Label(root, text="Здоровье: " + str(health), font=('Helvetica', 10))
moodLabel = tkinter.Label(root, text="Настроение: " + str(mood), font=('Helvetica', 10))
energyLabel = tkinter.Label(root, text="Энергия: " + str(energy), font=('Helvetica', 10))

# Кнопки
btnFeed = tkinter.Button(root, text="Покормить", width=10, height=1, font=('Helvetica', 10), command=feed)
btnTreat = tkinter.Button(root, text="Лечить", width=10, height=1, font=('Helvetica', 10), command=treat)
btnMood = tkinter.Button(root, text="Играть", width=10, height=1, font=('Helvetica', 10), command=play)
btnSleep = tkinter.Button(root, text="Спать", width=10, height=1, font=('Helvetica', 10), command=sleep)
btnWakeUp = tkinter.Button(root, text="Проснуться", width=10, height=1, font=('Helvetica', 10), command=wake_up)
btnStopPlay = tkinter.Button(root, text="Прекратить", width=10, height=1, font=('Helvetica', 10), command=stop_play)

# Закрепление на экране
startLabel.place(x=240, y=570)
hungerLabel.place(x=5, y=5)
healthLabel.place(x=5, y=35)
moodLabel.place(x=5, y=65)
energyLabel.place(x=5, y=95)
pet.place(x=135, y=30)
btnFeed.place(x=700, y=5)
btnTreat.place(x=700, y=35)
btnMood.place(x=700, y=65)
btnSleep.place(x=700, y=95)

# Запуск
root.bind('<Return>', start)
root.resizable(width=False, height=False)
root.mainloop()
