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
        self.inputImg, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)

        if self.inputImg:
            l1 = QLabel()
            l1.setPixmap(QPixmap(self.inputImg))
            self.vbox1.addWidget(l1)

            self.histogramOfImage(self.inputImg,"input")

            l1 = QLabel()
            l1.setPixmap(QPixmap(self.histInputImg))
            self.vbox1.addWidget(l1)

    def openFileTarget(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.targetImg, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)

        if self.targetImg:
            l2 = QLabel()
            l2.setPixmap(QPixmap(self.targetImg))
            self.vbox2.addWidget(l2)

            self.histogramOfImage(self.targetImg, "target")

            l2 = QLabel()
            l2.setPixmap(QPixmap(self.histTargetImg))
            self.vbox2.addWidget(l2)

    def equalizeHistogram(self):
        if self.inputImg and self.targetImg:
            img = mpimg.imread(self.inputImg)
            img2 = mpimg.imread(self.targetImg)

            r = img[:,:,0];
            g = img[:,:,1];
            b = img[:,:,2];

            r2 = img2[:,:,0];
            g2 = img2[:,:,1];
            b2 = img2[:,:,2];

            oldshape = r.shape

            s_values, bin_idx, s_counts = np.unique(r, return_inverse=True,return_counts=True)
            t_values, t_counts = np.unique(r2, return_counts=True)

            s_quantiles = np.cumsum(s_counts).astype(np.float64)
            s_quantiles /= s_quantiles[-1]
            t_quantiles = np.cumsum(t_counts).astype(np.float64)
            t_quantiles /= t_quantiles[-1]

            interp_t_values = np.interp(s_quantiles, t_quantiles, t_values)

            matched_r = interp_t_values[bin_idx].reshape(oldshape)

            oldshape = g.shape

            s_values, bin_idx, s_counts = np.unique(g, return_inverse=True,return_counts=True)
            t_values, t_counts = np.unique(g2, return_counts=True)

            s_quantiles = np.cumsum(s_counts).astype(np.float64)
            s_quantiles /= s_quantiles[-1]
            t_quantiles = np.cumsum(t_counts).astype(np.float64)
            t_quantiles /= t_quantiles[-1]

            interp_t_values = np.interp(s_quantiles, t_quantiles, t_values)

            matched_g = interp_t_values[bin_idx].reshape(oldshape)

            oldshape = b.shape

            s_values, bin_idx, s_counts = np.unique(b, return_inverse=True,return_counts=True)
            t_values, t_counts = np.unique(b2, return_counts=True)

            s_quantiles = np.cumsum(s_counts).astype(np.float64)
            s_quantiles /= s_quantiles[-1]
            t_quantiles = np.cumsum(t_counts).astype(np.float64)
            t_quantiles /= t_quantiles[-1]

            interp_t_values = np.interp(s_quantiles, t_quantiles, t_values)

            matched_b = interp_t_values[bin_idx].reshape(oldshape)

            newImage = np.zeros((r.shape[0],r.shape[1],3), np.float64)
            newImage[..., 0] = matched_r * 1
            newImage[..., 1] = matched_g * 1
            newImage[..., 2] = matched_b * 1

            plt.clf()
            plt.imshow(newImage)
            plt.savefig("resultPic.png")

            l2 = QLabel()
            l2.setPixmap(QPixmap("resultPic.png"))
            self.vbox3.addWidget(l2)

            plt.clf()

            r = newImage[:,:,0];
            g = newImage[:,:,1];
            b = newImage[:,:,2];

            hist = np.zeros((256), np.float64)
            for i in range(0,r.shape[0]):
                for j in range(0,r.shape[1]):
                    hist[int(round(r[i,j]*255,0))] += 1

            x = np.arange(0,256)
            plt.subplot(3,1,1)
            plt.bar(x,hist,color="red",align="center")

            hist = np.zeros((256), np.float64)
            for i in range(0,g.shape[0]):
                for j in range(0,g.shape[1]):
                    hist[int(round(g[i,j]*255,0))] += 1

            x = np.arange(0,256)
            plt.subplot(3,1,2)
            plt.bar(x,hist,color="green",align="center")

            hist = np.zeros((256), np.float64)
            for i in range(0,b.shape[0]):
                for j in range(0,b.shape[1]):
                    hist[int(round(b[i,j]*255,0))] += 1

            x = np.arange(0,256)
            plt.subplot(3,1,3)
            plt.bar(x,hist,color="blue",align="center")

            plt.savefig("histResult.png")

            l2 = QLabel()
            l2.setPixmap(QPixmap("histResult.png"))
            self.vbox3.addWidget(l2)

            '''row,col=r.shape #height,witdh
            hist = np.zeros((256), np.uint64)
            for i in range(0,row):
                for j in range(0,col):
                    hist[int(round(r[i,j]*255,0))] += 1

            cdf = np.zeros((256), np.float64)
            cdf[0] = hist[0]
            for i in range(1,len(hist)):
                cdf[i] = cdf[i-1] + hist[i]

            cdf_normalized = cdf * hist.max() / cdf.max()

            cdf_m = np.ma.masked_equal(cdf,0)
            cdf_m = (cdf_m - cdf_m.min())*255/(cdf_m.max()-cdf_m.min())
            cdf = np.ma.filled(cdf_m,0).astype('uint8')

            J = np.uint64(255*cdf)

            #Re-map values from equalized histogram into the image
            for i in range(0,row):
                for j in range(0,col):
                    tmp = r[i,j]
                    r[i,j]= J[int(round(tmp*255,0))]

            row,col=g.shape #height,witdh
            hist = np.zeros((256), np.uint64)
            for i in range(0,row):
                for j in range(0,col):
                    hist[int(round(g[i,j]*255,0))] += 1

            cdf = np.zeros((256), np.float64)
            cdf[0] = hist[0]
            for i in range(1,len(hist)):
                cdf[i] = cdf[i-1] + hist[i]

            cdf_normalized = cdf * hist.max() / cdf.max()

            cdf_m = np.ma.masked_equal(cdf,0)
            cdf_m = (cdf_m - cdf_m.min())*255/(cdf_m.max()-cdf_m.min())
            cdf = np.ma.filled(cdf_m,0).astype('uint8')

            J = np.uint64(255*cdf)

            #Re-map values from equalized histogram into the image
            for i in range(0,row):
                for j in range(0,col):
                    tmp = g[i,j]
                    g[i,j]= J[int(round(tmp*255,0))]

            row,col=b.shape #height,witdh
            hist = np.zeros((256), np.uint64)
            for i in range(0,row):
                for j in range(0,col):
                    hist[int(round(b[i,j]*255,0))] += 1

            cdf = np.zeros((256), np.float64)
            cdf[0] = hist[0]
            for i in range(1,len(hist)):
                cdf[i] = cdf[i-1] + hist[i]

            cdf_normalized = cdf * hist.max() / cdf.max()

            cdf_m = np.ma.masked_equal(cdf,0)
            cdf_m = (cdf_m - cdf_m.min())*255/(cdf_m.max()-cdf_m.min())
            cdf = np.ma.filled(cdf_m,0).astype('uint8')

            J = np.uint64(255*cdf)

            #Re-map values from equalized histogram into the image
            for i in range(0,row):
                for j in range(0,col):
                    tmp = b[i,j]
                    b[i,j]= J[int(round(tmp*255,0))]

            newImage = np.zeros((row,col,4), np.float64)
            newImage[..., 0] = r * 1
            newImage[..., 1] = g * 1
            newImage[..., 2] = b * 1
            newImage[..., 3] = img[:,:,3]

            plt.clf()
            plt.imshow(newImage)
            plt.savefig("resultPic.png")

            l2 = QLabel()
            l2.setPixmap(QPixmap("resultPic.png"))
            self.vbox3.addWidget(l2)'''




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
