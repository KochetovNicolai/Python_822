import sys
from PyQt5.QtWidgets import (QWidget, QHBoxLayout,
                             QLabel, QApplication, QMainWindow)
from PyQt5.QtGui import QPixmap, QKeyEvent


class Novel(QMainWindow):
    index = 1

    def __init__(self):
        super().__init__()
        self.lbl = QLabel(self)
        self.setCentralWidget(self.lbl)
        self.initUI()

    def initUI(self):
        pixmap = QPixmap('{}.jpg'.format(str(self.index)))
        self.lbl.setPixmap(pixmap.scaled(1024, 768))
        self.setWindowTitle('First picture')
        self.show()

    def UpdatePixmap(self):
        pixmap = QPixmap('{}.jpg'.format(str(self.index)))
        self.lbl.setPixmap(pixmap.scaled(1024, 768))

    def typeEvent(self, par=0):
        if self.index == -1:
            self.index = 15
            return

        if self.index == -2:
            self.index = 14
            return

        if self.index == 8:
            if par == 1:
                self.index += 1
            if par == 2:
                self.index = -1
            if par == 3:
                self.index = -2
            return

        if self.index == 30:
            if par == 1:
                self.index += 1
            if par == 2:
                self.index = -18
            return

        if self.index == 35:
            if par == 1:
                self.index += 1
            if par == 2:
                self.index = -26
            return

        if self.index == -21:
            self.index = -15
            return

        if self.index == -8:
            self.index = 48
            return

        self.index += 1

    def keyPressEvent(self, event):
        if event.text() == ' ':
            self.typeEvent()
            self.UpdatePixmap()
            return

        if event.text() == '1':
            self.typeEvent(1)
        if event.text() == '2':
            self.typeEvent(2)
        if event.text() == '3':
            self.typeEvent(3)

        self.UpdatePixmap()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Novel()
    sys.exit(app.exec_())
