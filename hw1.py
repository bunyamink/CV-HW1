import sys
from PyQt5.QtCore import QDate, QTime, QDateTime, Qt
from PyQt5.QtWidgets import QApplication, QWidget


def main():
    app = QApplication(sys.argv)
    ex = UserInterface()
    sys.exit(app.exec_())


class UserInterface(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):
        self.setGeometry(100, 100, 500, 500)
        self.setWindowTitle('Histogram Equalization')

        self.show()

if __name__ == '__main__':
    main()
