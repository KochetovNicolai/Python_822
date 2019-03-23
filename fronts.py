import tkinter as tk
from PIL import Image, ImageTk
import elements

class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.game = elements.Game()
        self.W = 300
        self.H = 200
        self.title('Мастер без Маргариты')

        self.text_frame = tk.Label(self, text="", font='Arial 13')
        self.panel_frame = None

        self._load_fonts()

    def _load_fonts(self):
        self._update_text(self.game.get_text())
        self._update_choose()
        self.text_frame.pack(side='top')
        self.panel_frame.pack(side='bottom')

    def _update_text(self, text):
        self.text_frame.config(text=text)

    def _update_choose(self):
        if self.panel_frame is not None:
            self.panel_frame.destroy()

        self.panel_frame = tk.Frame(self, height=200, bg='gray')

        quest_type = self.game.get_quest_type()
        if quest_type == 0:
            self.place_next()

        if quest_type == 1:
            self.place_buttons()

        if quest_type == 2:
            self.place_entry()

    def _make_step(self, text):
        if self.game.pick_ans(text):
            self._load_fonts()

    def place_next(self):
        f = lambda: self._make_step("skip")
        btn = tk.Button(self.panel_frame, text="Далее",
                        command=f)
        btn.pack()

    def place_buttons(self):
        for ans in self.game.get_answers():
            text = ans.text
            f = lambda: self._make_step(text)
            btn = tk.Button(self.panel_frame, text=ans.text,
                            command=f)
            btn.pack()

    def place_entry(self):
        my_entry = tk.Entry(self.panel_frame)
        my_entry.pack()
        ret_entry = lambda: self._make_step(my_entry.get())
        enter_entry = tk.Button(self.panel_frame, text="Ввести", command=ret_entry)
        enter_entry .pack()
