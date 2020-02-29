import sys
from PyQt5.QtWidgets import  *#QApplication, QWidget, QLabel
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class App(QWidget):

    def __init__(self, image):
        super().__init__()
        self.image_ = image
        self.title = 'PyQt5 image - pythonspot.com'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.pic_layout = QVBoxLayout()
        self.all_layouts = QVBoxLayout()
        self.knobs_layout = QHBoxLayout()
        self.left_ = (50,600, 50, 100 )
        self.right_ = (200, 600, 200, 100)
        self.top_ = (50, 100, 200, 100 )
        self.first_draw_ = True
        self.button_left_x = QSlider(Qt.Horizontal)
        self.button_left_x.setMaximum(1000)
        self.button_right_x = QSlider(Qt.Horizontal)
        self.button_right_x.setMaximum(1000)
        self.top_right_x = QSlider(Qt.Horizontal)
        self.top_right_x.setMaximum(1000)
        self.top_left_x = QSlider(Qt.Horizontal)
        self.top_left_x.setMaximum(1000)
        self.top_y = QSlider(Qt.Horizontal)
        self.top_y.setMaximum(1000)

        self.all_layouts.insertLayout(0,self.knobs_layout)
        self.all_layouts.insertLayout(1,self.pic_layout)
        self.knobs_layout.addWidget(self.button_left_x)
        self.knobs_layout.addWidget(self.button_right_x)
        self.knobs_layout.addWidget(self.top_left_x)
        self.knobs_layout.addWidget(self.top_right_x)
        self.knobs_layout.addWidget(self.top_y)
        self.button_left_x.valueChanged.connect(self.u_button_left_x)
        self.button_right_x.valueChanged.connect(self.u_button_right_x)
        self.top_left_x.valueChanged.connect(self.u_top_left_x)
        self.top_right_x.valueChanged.connect(self.u_top_right_x)
        self.top_y.valueChanged.connect(self.u_top_y)

        self.initUI()
    def u_button_left_x(self, value):
        all_data = self.left_
        self.left_ = (value, all_data[1], all_data[2], all_data[3])
        self.redraw()
    def u_button_right_x(self, value):
        all_data = self.right_
        self.right_ = (value, all_data[1], all_data[2], all_data[3])
        self.redraw()
    def u_top_left_x(self, value):
        all_data = self.left_
        self.left_ = (all_data[0], all_data[1], value, all_data[3])
        all_data = self.top_
        self.top_ = (value, all_data[1], all_data[2], all_data[3])
        self.redraw()
    def u_top_right_x(self, value):
        all_data = self.right_
        self.right_ = (all_data[0], all_data[1], value, all_data[3])
        all_data = self.top_
        self.top_ = (all_data[0], all_data[1], value, all_data[3])
        self.redraw()
    def u_top_y(self, value):
        all_data = self.top_
        self.top_ = (all_data[0], value, all_data[2], value)
        all_datal = self.left_
        self.left_ = (all_datal[0], all_datal[1], all_datal[2], value)
        all_datar = self.right_
        self.right_ = (all_datar[0], all_datar[1], all_datar[2], value)
        print(value)
        print(self.left_)
        self.redraw()
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        command_gb = QGroupBox("Parameters")
        # Create widget
        self.redraw()
        #self.resize(pixmap.width(),pixmap.height()+100)
        #self.setLayout(all_layouts)
        self.show()
    def redraw(self):
        painter = QPainter()
        painter.begin(self)
        #painter.setRenderHint(QPainter.Antialiasing)
        label = QLabel(self)
        label2 = QLabel(self)
        pixmap = QPixmap(self.image_)
        painter.drawPixmap(self.rect(), pixmap)
        painter.begin(pixmap)
        pen = QPen(Qt.red, 9)
       # painter = QPainter(pixmap)
        pen = QPen(Qt.red,3, Qt.SolidLine, Qt.SquareCap, Qt.BevelJoin)
        painter.setPen(pen)
        for i in [self.left_, self.right_, self.top_]:
                painter.drawLine(i[0],i[1],i[2],i[3]);
        label.setPixmap(pixmap)
        label2.setText("asd")
        if not self.first_draw_:
                self.pic_layout.itemAt(0).widget().deleteLater()
                self.pic_layout.itemAt(1).widget().deleteLater()
                #self.all_layouts.itemAt(1).width().deleteLater()
        self.first_draw_ = False
        self.pic_layout.insertWidget(1, label)
        self.pic_layout.insertWidget(0,label2)
        #self.all_layouts.insertLayout(1,self.pic_layout)
        self.setLayout(self.all_layouts)
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App('../test_images/solidYellowCurve2.jpg')
    sys.exit(app.exec_())
