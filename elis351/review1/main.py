import tkinter
import random


class Character:
    hunger = 50
    health = 50
    mood = 50
    energy = 50

    sleepNow = False
    playNow = False

    play_img = None

    # Функция обновления интерфейса
    def update_display(self):
        if self.is_alive():
            hungerLabel.config(text="Еда: " + str(self.hunger))
            healthLabel.config(text="Здоровье: " + str(self.health))
            moodLabel.config(text="Настроение: " + str(self.mood))
            energyLabel.config(text="Энергия: " + str(self.energy))

            if self.sleepNow:
                pet.config(image=sleeping)
                btnWakeUp.place(x=700, y=95)
                btnFeed.place_forget()
                btnTreat.place_forget()
                btnMood.place_forget()
            elif self.playNow:
                pet.config(image=self.play_img)
                btnStopPlay.place(x=700, y=65)
                btnFeed.place_forget()
                btnTreat.place_forget()
                btnSleep.place_forget()
            else:
                if self.energy <= 30:
                    pet.config(image=want_sleep)
                elif self.hunger <= 30:
                    pet.config(image=hungry)
                    if self.mood <= 30:
                        pet.config(image=unhappy)
                elif self.hunger >= 80:
                    pet.config(image=fat)
                elif self.mood >= 70:
                    pet.config(image=happy)
                elif self.mood <= 30:
                    pet.config(image=cry)
                else:
                    pet.config(image=normal)
        else:
            if self.sleepNow:
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

        pet.after(100, self.update_display)

    # Функции обновления характеристик
    def update_hunger(self):
        if self.hunger > 0:
            self.hunger -= 1
        else:
            self.energy -= 1

        if self.is_alive():
            if self.sleepNow:
                hungerLabel.after(4000, self.update_hunger)
            elif self.playNow:
                hungerLabel.after(500, self.update_hunger)
            else:
                hungerLabel.after(1000, self.update_hunger)

    def update_health(self):
        self.health -= 1

        if self.is_alive():
            if self.sleepNow:
                healthLabel.after(4000, self.update_health)
            else:
                healthLabel.after(1000, self.update_health)

    def update_mood(self):
        if self.playNow and self.mood < 100:
            self.mood += 1
        elif self.mood > 0:
            self.mood -= 1
        else:
            self.hunger -= 1

        if self.is_alive():
            if self.sleepNow:
                self.mood += 2
                moodLabel.after(8000, self.update_mood)
            elif self.playNow:
                moodLabel.after(500, self.update_mood)
            else:
                moodLabel.after(1000, self.update_mood)

    def update_energy(self):
        if self.sleepNow and self.energy < 100:
            self.energy += 1
        elif self.energy > 0:
            self.energy -= 1
        else:
            self.health -= 1

        if self.is_alive():
            if self.playNow or self.sleepNow:
                energyLabel.after(500, self.update_energy)
            else:
                energyLabel.after(1000, self.update_energy)

    # Функции восполнения характеристик
    def feed(self):
        if self.is_alive():
            if self.hunger <= 90:
                self.hunger += 10
            else:
                self.hunger -= 30

    def treat(self):
        if self.is_alive():
            if self.health <= 90:
                self.health += 10
            else:
                self.health -= 30

    def play(self):
        self.playNow = True
        self.play_img = random.choice(playing)

    def stop_play(self):
        self.playNow = False
        btnStopPlay.place_forget()
        btnFeed.place(x=700, y=5)
        btnTreat.place(x=700, y=35)
        btnSleep.place(x=700, y=95)

    def sleep(self):
        self.sleepNow = True

    def wake_up(self):
        self.sleepNow = False
        btnFeed.place(x=700, y=5)
        btnTreat.place(x=700, y=35)
        btnMood.place(x=700, y=65)
        btnWakeUp.place_forget()

    # проверка на живость
    def is_alive(self):
        if self.health <= 0:
            mainLabel.config(text="Ваш питомец умер :c")
            mainLabel.place(x=290, y=570)
            return False
        else:
            return True


char = Character()


# Функция начала игры
def start(event):
    is_enter = True

    if is_enter:
        startLabel.place_forget()
        mainLabel.place(x=200, y=570)
        char.update_hunger()
        char.update_health()
        char.update_mood()
        char.update_energy()

        char.update_display()

        is_enter = False


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
hungerLabel = tkinter.Label(root, text="Еда: " + str(char.hunger), font=('Helvetica', 10))
healthLabel = tkinter.Label(root, text="Здоровье: " + str(char.health), font=('Helvetica', 10))
moodLabel = tkinter.Label(root, text="Настроение: " + str(char.mood), font=('Helvetica', 10))
energyLabel = tkinter.Label(root, text="Энергия: " + str(char.energy), font=('Helvetica', 10))

# Кнопки
btnFeed = tkinter.Button(root, text="Покормить", width=10, height=1, font=('Helvetica', 10), command=char.feed)
btnTreat = tkinter.Button(root, text="Лечить", width=10, height=1, font=('Helvetica', 10), command=char.treat)
btnMood = tkinter.Button(root, text="Играть", width=10, height=1, font=('Helvetica', 10), command=char.play)
btnSleep = tkinter.Button(root, text="Спать", width=10, height=1, font=('Helvetica', 10), command=char.sleep)
btnWakeUp = tkinter.Button(root, text="Проснуться", width=10, height=1, font=('Helvetica', 10), command=char.wake_up)
btnStopPlay = tkinter.Button(root, text="Прекратить", width=10, height=1, font=('Helvetica', 10), command=char.stop_play)

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
