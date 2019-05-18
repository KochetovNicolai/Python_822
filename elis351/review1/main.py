import tkinter
import random


class Character:
    def __init__(self):
        # Задание интерфейса
        self.root = tkinter.Tk()
        self.root.title("Тамагочи")
        self.root.geometry("800x600")

        self.hunger = 50
        self.health = 50
        self.mood = 50
        self.energy = 50

        self.sleepNow = False
        self.playNow = False

        self.play_img = None

        # Картинки
        self.hungry = tkinter.PhotoImage(file="images/want_eat.png")
        self.normal = tkinter.PhotoImage(file="images/normal.png")
        self.dead = tkinter.PhotoImage(file="images/error.png")
        self.happy = tkinter.PhotoImage(file="images/happy.png")
        self.unhappy = tkinter.PhotoImage(file="images/unhappy.png")
        self.sleeping = tkinter.PhotoImage(file="images/sleep.png")
        self.want_sleep = tkinter.PhotoImage(file="images/want_sleep.png")
        self.fat = tkinter.PhotoImage(file="images/fat.png")
        self.cry = tkinter.PhotoImage(file="images/cry.png")
        self.rock = tkinter.PhotoImage(file="images/rock.png")
        self.guitar = tkinter.PhotoImage(file="images/guitar.png")
        self.music = tkinter.PhotoImage(file="images/music.png")
        self.war = tkinter.PhotoImage(file="images/war.png")

        self.playing = [self.rock, self.guitar, self.music, self.war]

        # Картинка хомяка
        self.pet = tkinter.Label(self.root, image=self.normal)

        # Текстовые поля
        self.startLabel = tkinter.Label(self.root, text="Чтобы начать игру, нажмите Enter", font=('Helvetica', 14))
        self.mainLabel = tkinter.Label(self.root, text="Заботьтесь о Сене, не дайте ему погибнуть!", font=('Helvetica', 14))
        self.hungerLabel = tkinter.Label(self.root, text="Еда: " + str(self.hunger), font=('Helvetica', 10))
        self.healthLabel = tkinter.Label(self.root, text="Здоровье: " + str(self.health), font=('Helvetica', 10))
        self.moodLabel = tkinter.Label(self.root, text="Настроение: " + str(self.mood), font=('Helvetica', 10))
        self.energyLabel = tkinter.Label(self.root, text="Энергия: " + str(self.energy), font=('Helvetica', 10))

        # Кнопки
        self.btnFeed = tkinter.Button(self.root, text="Покормить", width=10, height=1,
                                      font=('Helvetica', 10), command=self.feed)
        self.btnTreat = tkinter.Button(self.root, text="Лечить", width=10, height=1,
                                       font=('Helvetica', 10), command=self.treat)
        self.btnMood = tkinter.Button(self.root, text="Играть", width=10, height=1,
                                      font=('Helvetica', 10), command=self.play)
        self.btnSleep = tkinter.Button(self.root, text="Спать", width=10, height=1,
                                       font=('Helvetica', 10), command=self.sleep)
        self.btnWakeUp = tkinter.Button(self.root, text="Проснуться", width=10, height=1,
                                        font=('Helvetica', 10), command=self.wake_up)
        self.btnStopPlay = tkinter.Button(self.root, text="Прекратить", width=10, height=1,
                                          font=('Helvetica', 10), command=self.stop_play)

        # Закрепление на экране
        self.startLabel.place(x=240, y=570)
        self.hungerLabel.place(x=5, y=5)
        self.healthLabel.place(x=5, y=35)
        self.moodLabel.place(x=5, y=65)
        self.energyLabel.place(x=5, y=95)
        self.pet.place(x=135, y=30)
        self.btnFeed.place(x=700, y=5)
        self.btnTreat.place(x=700, y=35)
        self.btnMood.place(x=700, y=65)
        self.btnSleep.place(x=700, y=95)

    # Запуск
    def start_game(self):
        self.root.bind('<Return>', self.start)
        self.root.resizable(width=False, height=False)
        self.root.mainloop()

    # Функция начала игры
    def start(self):
        is_enter = True

        if is_enter:
            self.startLabel.place_forget()
            self.mainLabel.place(x=200, y=570)
            self.update_hunger()
            self.update_health()
            self.update_mood()
            self.update_energy()

            self.update_display()

            is_enter = False

    # Функция обновления интерфейса
    def update_display(self):
        if self.is_alive():
            self.hungerLabel.config(text="Еда: " + str(self.hunger))
            self.healthLabel.config(text="Здоровье: " + str(self.health))
            self.moodLabel.config(text="Настроение: " + str(self.mood))
            self.energyLabel.config(text="Энергия: " + str(self.energy))

            if self.sleepNow:
                self.pet.config(image=self.sleeping)
                self.btnWakeUp.place(x=700, y=95)
                self.btnFeed.place_forget()
                self.btnTreat.place_forget()
                self.btnMood.place_forget()
            elif self.playNow:
                self.pet.config(image=self.play_img)
                self.btnStopPlay.place(x=700, y=65)
                self.btnFeed.place_forget()
                self.btnTreat.place_forget()
                self.btnSleep.place_forget()
            else:
                if self.energy <= 30:
                    self.pet.config(image=self.want_sleep)
                elif self.hunger <= 30:
                    self.pet.config(image=self.hungry)
                    if self.mood <= 30:
                        self.pet.config(image=self.unhappy)
                elif self.hunger >= 80:
                    self.pet.config(image=self.fat)
                elif self.mood >= 70:
                    self.pet.config(image=self.happy)
                elif self.mood <= 30:
                    self.pet.config(image=self.cry)
                else:
                    self.pet.config(image=self.normal)
        else:
            if self.sleepNow:
                self.btnWakeUp.place_forget()
            self.pet.config(image=self.dead)
            self.hungerLabel.config(text="")
            self.healthLabel.config(text="")
            self.moodLabel.config(text="")
            self.energyLabel.config(text="")
            self.btnSleep.place_forget()
            self.btnMood.place_forget()
            self.btnTreat.place_forget()
            self.btnFeed.place_forget()

        self.pet.after(100, self.update_display)

    # Функции обновления характеристик
    def update_hunger(self):
        if self.hunger > 0:
            self.hunger -= 1
        else:
            self.energy -= 1

        if self.is_alive():
            if self.sleepNow:
                self.hungerLabel.after(4000, self.update_hunger)
            elif self.playNow:
                self.hungerLabel.after(500, self.update_hunger)
            else:
                self.hungerLabel.after(1000, self.update_hunger)

    def update_health(self):
        self.health -= 1

        if self.is_alive():
            if self.sleepNow:
                self.healthLabel.after(4000, self.update_health)
            else:
                self.healthLabel.after(1000, self.update_health)

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
                self.moodLabel.after(8000, self.update_mood)
            elif self.playNow:
                self.moodLabel.after(500, self.update_mood)
            else:
                self.moodLabel.after(1000, self.update_mood)

    def update_energy(self):
        if self.sleepNow and self.energy < 100:
            self.energy += 1
        elif self.energy > 0:
            self.energy -= 1
        else:
            self.health -= 1

        if self.is_alive():
            if self.playNow or self.sleepNow:
                self.energyLabel.after(500, self.update_energy)
            else:
                self.energyLabel.after(1000, self.update_energy)

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
        self.play_img = random.choice(self.playing)

    def stop_play(self):
        self.playNow = False
        self.btnStopPlay.place_forget()
        self.btnFeed.place(x=700, y=5)
        self.btnTreat.place(x=700, y=35)
        self.btnSleep.place(x=700, y=95)

    def sleep(self):
        self.sleepNow = True

    def wake_up(self):
        self.sleepNow = False
        self.btnFeed.place(x=700, y=5)
        self.btnTreat.place(x=700, y=35)
        self.btnMood.place(x=700, y=65)
        self.btnWakeUp.place_forget()

    # проверка на живость
    def is_alive(self):
        if self.health <= 0:
            self.mainLabel.config(text="Ваш питомец умер :c")
            self.mainLabel.place(x=290, y=570)
            return False
        else:
            return True


char = Character()
char.start_game()
