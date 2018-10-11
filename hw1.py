import sys
from PyQt5.QtCore import QDate, QTime, QDateTime, Qt
from PyQt5.QtWidgets import QApplication, QWidget, QMenu, QMainWindow, QAction, qApp, QFileDialog
from PyQt5.QtGui import QIcon


def main():
    app = QApplication(sys.argv)
    ex = UserInterface()
    sys.exit(app.exec_())


class UserInterface(QMainWindow):

    def __init__(self):
        super().__init__()
        self.inputImage = ""
        self.targetImage = ""
        self.initUI()


    def initUI(self):

        openInputAct = QAction('&OpenInput', self)
        openInputAct.setStatusTip('Open Input')
        openInputAct.triggered.connect(self.openFileInput)

        openTargetAct = QAction('&OpenTarget', self)
        openTargetAct.setStatusTip('Open Target')
        openTargetAct.triggered.connect(self.openFileTarget)

        exitAct = QAction('&Exit', self)
        exitAct.setStatusTip('Exit')
        exitAct.triggered.connect(qApp.quit)

        self.statusBar()

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openInputAct)
        fileMenu.addAction(openTargetAct)
        fileMenu.addAction(exitAct)

        self.setGeometry(200, 200, 400, 300)
        self.setWindowTitle('Histogram Equalization')
        self.show()

    def openFileInput(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            print(fileName)

    def openFileTarget(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            print(fileName)


if __name__ == '__main__':
    main()
