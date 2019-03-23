import json
import glob


class Answer(object):
    def __init__(self, desc):
        self.text = desc['text']
        self.req_lvl = desc['req_lvl']
        self.next_page_name = desc['next_page_name']
        self.next_lvl = desc['next_lvl']

    def equals(self, answer, usr_lvl):
        return self.text.lower() == answer.lower() and usr_lvl in self.req_lvl

    def get_button_text(self):
        return self.text

    def is_fit(self, usr_lvl):
        return usr_lvl in self.req_lvl


class Page(object):
    def __init__(self, path_to_file):
        with open(path_to_file) as f:
            try:
                data = json.load(f)
            except:
                print("Faul to load file: " + path_to_file)
                exit(1)

            try:
                self.name = data['name']
                self.text = data['text']
                self.quest_type = data['quest_type']
                self.next_page_name = None
                self.answers = None

                if self.quest_type == 0:
                    self.next_page_name = data['next_page_name']

                else:
                    self.next_page_name = None
                    self.answers = []

                    if self.name == "12.2":
                        print(data['answers'])
                    for answer in data['answers']:
                        self.answers.append(Answer(answer))

            except:
                print(path_to_file)
                exit(1)

    def next_state(self, usr_ans, usr_lvl):
        if self.next_page_name is not None:
            return self.next_page_name, usr_lvl

        for a in self.answers:
            if a.equals(usr_ans, usr_lvl):
                return a.next_page_name, a.next_lvl
        return None, None

    def get_answers(self, usr_lvl):
        res = []
        for ans in self.answers:
            if ans.is_fit(usr_lvl):
                res.append(ans)

        return res


class Game(object):
    def __init__(self):
        self.path_to_dir = "data/"
        self.pages = dict()
        files = glob.glob(self.path_to_dir + "**.json")
        for file in files:
            page = Page(file)
            self.pages[page.name] = page

        self.curr_page = self.pages["start"]
        self.usr_lvl = 1

    def get_text(self):
        return self.curr_page.text

    def get_quest_type(self):
        return self.curr_page.quest_type

    def get_answers(self):
        return self.curr_page.get_answers(self.usr_lvl)

    def pick_ans(self, ans_text):
        next_page, next_lvl = self.curr_page.next_state(ans_text, self.usr_lvl)
        if next_page is None:
            return False

        self.curr_page = self.pages[next_page]
        self.usr_lvl = next_lvl
        return True
