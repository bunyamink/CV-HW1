'''
ITU - Computer Vision - HW1
Bunyamin Kurt - 150140145
'''
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
        self.inputImg = ""
        self.targetImg = ""
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

        # Create vertical box layout
        self.vbox2 = QVBoxLayout()

        # Add target label
        title = QLabel('Target')
        self.vbox2.addWidget(title)

        # Create third vertical box layout
        self.vbox3 = QVBoxLayout()

        # Add result label
        title = QLabel('Result')
        self.vbox3.addWidget(title)

        # Add vertical box layout into Horizantal box layout
        self.vboxH.addLayout(self.vbox1)
        self.vboxH.addLayout(self.vbox2)
        self.vboxH.addLayout(self.vbox3)
        wid.setLayout(self.vboxH)

        self.setGeometry(200, 200, 400, 300)
        self.setWindowTitle('Histogram Equalization')
        self.show()

    def openFileInput(self):
        # Open file dialog
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.inputImg, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)

        if self.inputImg:
            # Insert image into first vertical box layout
            l1 = QLabel()
            l1.setPixmap(QPixmap(self.inputImg))
            self.vbox1.addWidget(l1)

            # Calculate histogram of image
            self.histogramOfImage(self.inputImg,"input")

            # Insert histogram into first vertical box layout
            l1 = QLabel()
            l1.setPixmap(QPixmap(self.histInputImg))
            self.vbox1.addWidget(l1)

    def openFileTarget(self):
        # Open file dialog
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.targetImg, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)

        if self.targetImg:
            # Insert image into second vertical box layout
            l2 = QLabel()
            l2.setPixmap(QPixmap(self.targetImg))
            self.vbox2.addWidget(l2)

            # Calculate histogram of image
            self.histogramOfImage(self.targetImg, "target")

            # Insert histogram into second vertical box layout
            l2 = QLabel()
            l2.setPixmap(QPixmap(self.histTargetImg))
            self.vbox2.addWidget(l2)

    def equalizeHistogram(self):
        if self.inputImg and self.targetImg:

            # Get input and target image
            img = mpimg.imread(self.inputImg)
            img2 = mpimg.imread(self.targetImg)

            # Red, green and blue of input image
            r = img[:,:,0];
            g = img[:,:,1];
            b = img[:,:,2];

            # Red, green and blue of target image
            r2 = img2[:,:,0];
            g2 = img2[:,:,1];
            b2 = img2[:,:,2];

            # calculate matching histogram every color
            rMatched = self.histMatching(r,r2)
            gMatched = self.histMatching(g,g2)
            bMatched = self.histMatching(b,b2)

            # Combine every color and get new image
            newImage = np.zeros((img.shape[0],img.shape[1],3), np.float64)
            newImage[..., 0] = rMatched * 255
            newImage[..., 1] = gMatched * 255
            newImage[..., 2] = bMatched * 255

            # Save result image
            plt.clf()
            plt.imshow(newImage)
            plt.savefig("resultPic.png")

            # Insert result image into third vertical box layout
            l2 = QLabel()
            l2.setPixmap(QPixmap("resultPic.png"))
            self.vbox3.addWidget(l2)

            # Red, green and blue of result image
            r = newImage[:,:,0];
            g = newImage[:,:,1];
            b = newImage[:,:,2];

            # x-axis of result image histogram
            x = np.arange(0,256)

            # Calculate histogram of result image (red)
            hist = self.calcHist2(r)

            # Draw histogram of result image
            plt.subplot(3,1,1)
            plt.bar(x,hist,color="red",align="center")

            # Calculate histogram of result image (green)
            hist = self.calcHist2(g)

            # Draw histogram of result image
            plt.subplot(3,1,2)
            plt.bar(x,hist,color="green",align="center")

            # Calculate histogram of result image (blue)
            hist = self.calcHist2(b)

            # Draw histogram of result image
            plt.subplot(3,1,3)
            plt.bar(x,hist,color="blue",align="center")

            # Save histogram of result image
            plt.savefig("histResult.png")

            # Insert histogram of result image into third vertical box layout
            l2 = QLabel()
            l2.setPixmap(QPixmap("histResult.png"))
            self.vbox3.addWidget(l2)

    def calcHist(self,img):
        # Create empty array have 256 elements
        hist = np.zeros((256), np.float64)

        # Iterate over image and count pixels
        for i in range(0,img.shape[0]):
            for j in range(0,img.shape[1]):
                hist[int(round(img[i,j]*255,0))] += 1
        return hist

    def calcHist2(self,img):
        # Create empty array have 256 elements
        hist = np.zeros((256), np.float64)

        # Iterate over image and count pixels
        for i in range(0,img.shape[0]):
            for j in range(0,img.shape[1]):
                hist[int(round(img[i,j]/255,0))] += 1
        return hist

    def calcCDF(self, hist):
        # Create empty array have 256 elements
        cdf = np.zeros((256), np.float64)

        # Cdf first element equal to hist first element
        cdf[0] = hist[0]

        # Calculate Cdf
        for i in range(1,len(hist)):
            cdf[i] = cdf[i-1] + hist[i]
        return cdf

    def histMatching(self, img, imgTarget):
        # height, width and pixels of input image
        height = img.shape[0]
        width = img.shape[1]
        pixels = width * height

        # height, width and pixels of target image
        height_ref = imgTarget.shape[0]
        width_ref = imgTarget.shape[1]
        pixels_ref = width_ref * height_ref

        # Histogram of input image and target image
        hist = self.calcHist(img)
        hist_ref = self.calcHist(imgTarget)

        # Calculate CDF
        cum_hist = self.calcCDF(hist)
        cum_hist_ref = self.calcCDF(hist_ref)

        # Calculate PDF
        prob_cum_hist = cum_hist / pixels
        prob_cum_hist_ref = cum_hist_ref / pixels_ref

        K = 256
        new_values = np.zeros((K))

        # Calculate new values of new image
        for a in np.arange(K):
            j = K - 1
            while True:
                new_values[a] = j
                j = j - 1
                if j < 0 or prob_cum_hist[a] > prob_cum_hist_ref[j]:
                    break

        # Create new image
        for i in np.arange(height):
            for j in np.arange(width):
                a = img[i,j]
                b = new_values[int(round(a*255,0))]
                img[i,j] = b

        return img

    def histogramOfImage(self, fileName, type):
        # Clear all plots before
        plt.clf()

        # Import image
        img = mpimg.imread(fileName)

        # Red, green and blue of image
        r = img[:,:,0];
        g = img[:,:,1];
        b = img[:,:,2];

        # x-axis of histogram
        x = np.arange(0,256)

        # Caclulate red color histogram
        hist = self.calcHist(r)

        # Draw plot of histogram
        plt.subplot(3,1,1)
        plt.bar(x,hist,color="red",align="center")

        # Caclulate green color histogram
        hist = self.calcHist(g)

        # Draw plot of histogram
        plt.subplot(3,1,2)
        plt.bar(x,hist,color="green",align="center")

        # Caclulate blue color histogram
        hist = self.calcHist(b)

        # Draw plot of histogram
        plt.subplot(3,1,3)
        plt.bar(x,hist,color="blue",align="center")

        # Save histogram image
        if type == "input":
            plt.savefig(self.histInputImg)
        elif type == "target":
            plt.savefig(self.histTargetImg)


if __name__ == '__main__':
    main()
