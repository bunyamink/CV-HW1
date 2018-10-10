import sys
from PyQt5.QtCore import QDate, QTime, QDateTime, Qt
from PyQt5.QtWidgets import QApplication, QWidget, QMenu, QMainWindow, QAction, qApp
from PyQt5.QtGui import QIcon


def main():
    app = QApplication(sys.argv)
    ex = UserInterface()
    sys.exit(app.exec_())


class UserInterface(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):

        openInputAct = QAction('&OpenInput', self)
        openInputAct.setStatusTip('Open Input')
        #openInputAct.triggered.connect(qApp.quit)

        openTargetAct = QAction('&OpenTarget', self)
        openTargetAct.setStatusTip('Open Target')
        #openTargetAct.triggered.connect(qApp.quit)

        exitAct = QAction('&Exit', self)
        exitAct.setStatusTip('Exit')
        exitAct.triggered.connect(qApp.quit)

        self.statusBar()

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openInputAct)
        fileMenu.addAction(openTargetAct)
        fileMenu.addAction(exitAct)

        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('Histogram Equalization')
        self.show()

if __name__ == '__main__':
    main()
