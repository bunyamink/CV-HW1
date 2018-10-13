import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap, QImage

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

def main():
    app = QApplication(sys.argv)
    ex = UserInterface()
    sys.exit(app.exec_())


class UserInterface(QMainWindow):

    def __init__(self):
        super().__init__()
        self.histInputImg = "histInput.png"
        self.histTargetImg = "histTarget.png"
        self.initUI()

    def initUI(self):

        # Create Open Input Image Action
        openInputAct = QAction('&OpenInput', self)
        openInputAct.setStatusTip('Open Input')
        openInputAct.triggered.connect(self.openFileInput)

        # Create Target Input Image Action
        openTargetAct = QAction('&OpenTarget', self)
        openTargetAct.setStatusTip('Open Target')
        openTargetAct.triggered.connect(self.openFileTarget)

        # Create Exit Action
        exitAct = QAction('&Exit', self)
        exitAct.setStatusTip('Exit')
        exitAct.triggered.connect(qApp.quit)

        # Create menuBar
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openInputAct)
        fileMenu.addAction(openTargetAct)
        fileMenu.addAction(exitAct)

        # Equalize Histogram button in toolbar
        equalizeAct = QAction('Equalize Histogram', self)
        equalizeAct.triggered.connect(self.equalizeHistogram)

        # Add button in toolbar
        self.toolbar = self.addToolBar('Equalize Histogram')
        self.toolbar.addAction(equalizeAct)

        # Create main widget
        wid = QWidget(self)
        self.setCentralWidget(wid)

        # Create Horizantal and Vertical Box Layout
        self.vboxH = QHBoxLayout()
        self.vbox1 = QVBoxLayout()

        # Add input label
        title = QLabel('Input')
        self.vbox1.addWidget(title)

        self.vbox2 = QVBoxLayout()
        title = QLabel('Target')
        self.vbox2.addWidget(title)

        self.vbox3 = QVBoxLayout()
        title = QLabel('Result')
        self.vbox3.addWidget(title)

        self.vboxH.addLayout(self.vbox1)
        self.vboxH.addLayout(self.vbox2)
        self.vboxH.addLayout(self.vbox3)
        wid.setLayout(self.vboxH)

        self.setGeometry(200, 200, 400, 300)
        self.setWindowTitle('Histogram Equalization')
        self.show()

    def openFileInput(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)

        if fileName:
            l1 = QLabel()
            l1.setPixmap(QPixmap(fileName))
            self.vbox1.addWidget(l1)

            self.histogramOfImage(fileName,"input")

            l1 = QLabel()
            l1.setPixmap(QPixmap(self.histInputImg))
            self.vbox1.addWidget(l1)

    def openFileTarget(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            l2 = QLabel()
            l2.setPixmap(QPixmap(fileName))
            self.vbox2.addWidget(l2)

            self.histogramOfImage(fileName, "target")

            l2 = QLabel()
            l2.setPixmap(QPixmap(self.histTargetImg))
            self.vbox2.addWidget(l2)

    def equalizeHistogram(self):
        print("equalize")

    def histogramOfImage(self, fileName, type):
        # clear all plots before
        plt.clf()

        img = mpimg.imread(fileName)

        r = img[:,:,0];
        g = img[:,:,1];
        b = img[:,:,2];

        row, col = r.shape
        y = np.zeros((256), np.uint64)
        for i in range(0,row):
            for j in range(0,col):
                y[int(round(r[i,j]*255,0))] += 1
        x = np.arange(0,256)
        plt.subplot(3,1,1)
        plt.bar(x,y,color="red",align="center")

        row, col = g.shape
        y = np.zeros((256), np.uint64)
        for i in range(0,row):
            for j in range(0,col):
                y[int(round(g[i,j]*255,0))] += 1
        x = np.arange(0,256)
        plt.subplot(3,1,2)
        plt.bar(x,y,color="green",align="center")

        row, col = b.shape
        y = np.zeros((256), np.uint64)
        for i in range(0,row):
            for j in range(0,col):
                y[int(round(b[i,j]*255,0))] += 1
        x = np.arange(0,256)
        plt.subplot(3,1,3)
        plt.bar(x,y,color="blue",align="center")

        if type == "input":
            plt.savefig(self.histInputImg)
        elif type == "target":
            plt.savefig(self.histTargetImg)


if __name__ == '__main__':
    main()
