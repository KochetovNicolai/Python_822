#!/usr/bin/python3
# -*- coding: utf-8 -*-
import getch as g
import sys
from PyQt5.QtWidgets import (QWidget, QHBoxLayout,
                             QLabel, QApplication, QMainWindow)
from PyQt5.QtGui import QPixmap, QKeyEvent


class Example(QMainWindow):
    index = 1

    def __init__(self):
        super().__init__()
        self.lbl = QLabel(self)
        self.setCentralWidget(self.lbl)
        self.initUI()

    def initUI(self):
        # hbox = QHBoxLayout(self)
        pixmap = QPixmap('{}.jpg'.format(str(self.index)))
        # self.resize(pixmap.width(), pixmap.height())
        self.lbl.setPixmap(pixmap.scaled(1024, 768))

        # hbox.addWidget(self.lbl)
        # self.setLayout(hbox)
        self.setWindowTitle('First picture')
        self.show()

    def UpdatePixmap(self):
        pixmap = QPixmap('{}.jpg'.format(str(self.index)))
        self.lbl.setPixmap(pixmap.scaled(1024, 768))

    def keyPressEvent(self, event):
        if event.text() == 'w':
            # print('kek')
            self.index += 1
        self.UpdatePixmap()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
