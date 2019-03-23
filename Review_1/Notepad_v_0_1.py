#Console Notepad V.0.1

import sys

import urwid

urwid.set_encoding("UTF-8")

class LineNavigate(urwid.ListWalker):

    def __init__(self, name):
        self.file = open(name)
        self.lines = []
        self.focus = 0

    def get_focus(self):
        return self.change_position(self.focus)

    def set_focus(self, focus):
        self.focus = focus
        self._modified()

    def get_next(self, start_from):
        #return self.change_position(start_from + 1)
        return self.change_position(start_from + 1)

    def get_prev(self, start_from):
        return self.change_position(start_from - 1)

    def read_next_line(self):

        next_line = self.file.readline()

        if not next_line or next_line[-1:] != '\n':
            # no newline on last line of file
            self.file = None
        else:
            # trim newline characters
            next_line = next_line[:-1]

        expanded = next_line.expandtabs()

        edit = urwid.Edit("", expanded, allow_tab=True)
        edit.set_edit_pos(0)
        edit.original_text = next_line
        self.lines.append(edit)

        return next_line

    def change_position(self, pos):

        if pos < 0:
            # line 0 is the start of the file, no more above
            return None, None

        if len(self.lines) > pos:
            # we have that line so return it
            return self.lines[pos], pos

        if self.file is None:
            # file is closed, so there are no more lines
            return None, None

        assert pos == len(self.lines), "problem"

        self.read_next_line()

        return self.lines[-1], pos

    def split_focus(self):

        focus = self.lines[self.focus]
        pos = focus.edit_pos
        edit = urwid.Edit("",focus.edit_text[pos:], allow_tab=True)
        edit.original_text = ""
        focus.set_edit_text(focus.edit_text[:pos])
        edit.set_edit_pos(0)
        self.lines.insert(self.focus+1, edit)

    def combine_focus_with_prev(self):

        above, ignore = self.get_prev(self.focus)
        if above is None:
            # already at the top
            return

        focus = self.lines[self.focus]
        above.set_edit_pos(len(above.edit_text))
        above.set_edit_text(above.edit_text + focus.edit_text)
        del self.lines[self.focus]
        self.focus -= 1

    def combine_focus_with_next(self):

        below, ignore = self.get_next(self.focus)
        if below is None:
            # already at bottom
            return

        focus = self.lines[self.focus]
        focus.set_edit_text(focus.edit_text + below.edit_text)
        del self.lines[self.focus+1]


class EditDisplay:
    palette = [
        ('body','white', 'dark red'),
        ('header','white', 'black', 'bold'),
        ('key','white', 'black', 'underline'),
        ]

    header_text = ('header', [
        "Console Notepad v.0.1 (alpha)  Press ",
        ('key', "F2"), " to quit, ",
        ('key', "F5"), " to save ",
        ])

    def __init__(self, name):
        self.save_name = name
        self.Navigate = LineNavigate(name)
        self.listbox = urwid.ListBox(self.Navigate)
        self.header = urwid.AttrWrap(urwid.Text(self.header_text),
            "header")
        self.view = urwid.Frame(urwid.AttrWrap(self.listbox, 'body'),
            header=self.header)

    def main(self):
        self.loop = urwid.MainLoop(self.view, self.palette,
            unhandled_input=self.unhandled_keypress, handle_mouse=False)
        self.loop.run()

    def unhandled_keypress(self, k):

        if k == "f5":
            self.save_file()
        elif k == "f2":
            raise urwid.ExitMainLoop()
        elif k == "delete":
            # delete at end of line
            self.Navigate.combine_focus_with_next()
        elif k == "backspace":
            # backspace at beginning of line
            self.Navigate.combine_focus_with_prev()
        elif k == "enter":
            # start new line
            self.Navigate.split_focus()
            # move the cursor to the new line and reset pref_col
            self.loop.process_input(["down", "home"])
        elif k == "right":
            w, pos = self.Navigate.get_focus()
            w, pos = self.Navigate.get_next(pos)
            if w:
                self.listbox.set_focus(pos, 'above')
                self.loop.process_input(["home"])
        elif k == "left":
            w, pos = self.Navigate.get_focus()
            w, pos = self.Navigate.get_prev(pos)
            if w:
                self.listbox.set_focus(pos, 'below')
                self.loop.process_input(["end"])
        else:
            return
        return True


    def save_file(self):

        l = []
        walk = self.Navigate
        for edit in walk.lines:
            # collect the text already stored in edit widgets
            if edit.original_text.expandtabs() == edit.edit_text:
                l.append(edit.original_text)
            else:
                l.append(re_tab(edit.edit_text))

        # then the rest
        while walk.file is not None:
            l.append(walk.read_next_line())

        # write back to disk
        outfile = open(self.save_name, "w")

        prefix = ""
        for line in l:
            outfile.write(prefix + line)
            prefix = "\n"

def re_tab(s):
    l = []
    p = 0
    for i in range(8, len(s), 8):
        if s[i-2:i] == "  ":
            # collapse two or more spaces into a tab
            l.append(s[p:i].rstrip() + "\t")
            p = i

    if p == 0:
        return s
    else:
        l.append(s[p:])
        return "".join(l)

def main():
    try:
        name = sys.argv[1]
        assert open(name, "a")
    except:
        sys.stderr.write(__doc__)
        return
    EditDisplay(name).main()

if __name__=="__main__":
    main()
