import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from content import content


class OverlayLabel(QLabel):
    def __init__(self, parent=None):
        super(OverlayLabel, self).__init__(parent)
        # self.setAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
        self.x_size = 1024
        self.y_size = 148
        self.setFixedSize(QSize(self.x_size, self.y_size))
        self.content = content
        self.message = self.content['oleg'][0]
        self.oleg = 1
        self.zhen = 0
        self.tima = 0
        self.voice = 0

    def paintEvent(self, event):
        p = QPainter(self)
        r = event.rect()
        p.fillRect(r, QBrush(Qt.white))
        p.drawText(450, 70, str(self.message))

    def change_text(self, param):

        if param == 0:
            self.message = self.content['oleg'][self.oleg]
            self.oleg += 1

        if param == 1:
            self.message = self.content['zhen'][self.zhen]
            self.zhen += 1

        if param == 2:
            self.message = self.content['tima'][self.time]
            self.tima += 1

        if param == 3:
            self.message = self.content['voice'][self.voice]
            self.voice += 1

        self.update()

    def resize(self, param):
        if param == 0:
            self.x_size = 1600
            self.y_size = 177

        if param == 1:
            self.x_size = 1024
            self.y_size = 145

        self.setFixedSize(self.x_size, self.y_size)
        self.update()


class Novel(QMainWindow):
    def __init__(self):
        super().__init__()
        self.lbl = QLabel(self)
        self.x_size = 1024
        self.y_size = 768
        self.setGeometry(100, 100, self.x_size, self.y_size)
        self.over = OverlayLabel(self)
        self.initUI()
        self.index = 1

    def initUI(self):
        self.setWindowTitle('Novel')
        w = QWidget(self)
        self.layout = QVBoxLayout(self)
        self.layout.addStretch()
        self.layout.addWidget(self.over)
        w.setLayout(self.layout)
        self.setCentralWidget(w)
        self.show()

    def paintEvent(self, event):
        p = QPainter(self)
        r = event.rect()
        p.drawImage(r, QImage('pictures/{}.jpg'.format(str(self.index))))

    def type_event(self, param):
        self.over.change_text(param)
        self.update()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Space:
            self.type_event(0)

        if event.key() == Qt.Key_1:
            self.type_event(1)

        if event.key() == Qt.Key_2:
            self.type_event(2)

        if event.key() == Qt.Key_3:
            self.type_event(3)

        if event.key() == Qt.Key_Z:
            self.x_size = 1600
            self.y_size = 900
            self.index -= 1
            self.over.resize(0)
            self.setGeometry(100, 100, self.x_size, self.y_size)

        if event.key() == Qt.Key_X:
            self.x_size = 1024
            self.y_size = 768
            self.index -= 1
            self.setGeometry(100, 100, self.x_size, self.y_size)
            self.over.resize(1)
            self.update()

        self.setGeometry(100, 100, self.x_size, self.y_size)
        self.index += 1
        self.update()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Novel()
    sys.exit(app.exec_())