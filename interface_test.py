from PyQt5 import QtWidgets
from PyQt5.QtWidgets import  QApplication, QMainWindow

import sys


class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()

        self.setWindowTitle("Window")
        self.setGeometry(300, 250, 350, 200)

        # Отображение объекта
        self.new_text = QtWidgets.QLabel(self)

        self.main_text = QtWidgets.QLabel(self)
        self.main_text.setText("Название программы")
        self.main_text.move(100, 100)
        self.main_text.adjustSize()

        self.button = QtWidgets.QPushButton(self)
        self.button.move(70, 150)
        self.button.setText("Button")
        self.button.setFixedWidth(200)
        self.button.clicked.connect(self.add_label)  # Активация по нажатию на кнопку


    def add_label(self):
        # Активация кнопки
        self.new_text.setText("Button")
        self.new_text.move(100, 50)
        self.new_text.adjustSize()

        #print("Pressed Button")


def application():
    app = QApplication(sys.argv)
    window = Window()

    window.show()
    sys.exit(app.exec_())


application()

