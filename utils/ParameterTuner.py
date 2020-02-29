import sys
from PyQt5.QtWidgets import  *#QApplication, QWidget, QLabel
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class App(QWidget):

    def __init__(self, image):
        super().__init__()
        self.image_ = image
        self.pixmap = QPixmap(self.image_)
        self.label = QLabel(self)
        button = QPushButton("Export ROI")
        button.clicked.connect(self.export)
        self.newfont = QFont("Times", 28)
        self.newfont2 = QFont("Times", 20)
        button.setFont(self.newfont2)
        self.label_bl = QLabel(self)
        self.label_ul = QLabel(self)
        self.label_br = QLabel(self)
        self.label_ur = QLabel(self) 
        self.label_ur.setFont(self.newfont)
        self.label_bl.setFont(self.newfont)# = QLabel(self)
        self.label_br.setFont(self.newfont)
        self.label_ul.setFont(self.newfont)
        self.label_ur.setAlignment(Qt.AlignRight)
        self.label_br.setAlignment(Qt.AlignRight)
        self.title = 'Region of Interest Tuner'
        self.left = 0
        self.top = 0
        self.width = self.pixmap.width() 
        self.height = self.pixmap.height()
        self.info_layout_up = QHBoxLayout()
        self.info_layout_down = QHBoxLayout()
        self.pic_layout = QHBoxLayout()
        self.top_slider_layput = QHBoxLayout()
        self.slider_pic_layout = QHBoxLayout()
        self.slider_pic_layout.addLayout(self.pic_layout)
        self.slider_pic_layout.addLayout(self.top_slider_layput)
        self.all_pic_layout = QVBoxLayout()
        self.all_layouts = QVBoxLayout()
        self.info_layout_down.addWidget(self.label_bl)
        #self.info_layout_down.addStretch(1000)
        self.info_layout_down.addWidget(self.label_br)
        self.info_layout_up.addWidget(self.label_ul)
        #self.info_layout_up.addStretch(.01 )
        self.info_layout_up.addWidget(self.label_ur)
        self.all_pic_layout.addLayout(self.info_layout_up)
        self.all_pic_layout.addLayout(self.slider_pic_layout)
        self.all_pic_layout.addLayout(self.info_layout_down)
        self.knobs_layout_up = QHBoxLayout()
        self.knobs_layout_down = QHBoxLayout()
        self.left_ = (0,self.pixmap.height(), 0, 0 )
        self.right_ = (self.pixmap.width(), self.pixmap.height(), self.pixmap.width(), 0)
        self.top_ = (0, 0, self.pixmap.width(), 0 )
        self.first_draw_ = True
        self.button_left_x = QSlider(Qt.Horizontal)
        self.button_left_x.setMaximum(self.pixmap.width())
        self.button_left_x.setMinimum(0)
        self.button_left_x.setValue(0)
        self.button_right_x = QSlider(Qt.Horizontal)
        self.button_right_x.setMaximum(self.pixmap.width())
        self.button_right_x.setValue(self.pixmap.width())
        self.button_right_x.setMinimum(0)
        self.top_right_x = QSlider(Qt.Horizontal)
        self.top_right_x.setMaximum(self.pixmap.width())
        self.top_right_x.setValue(self.pixmap.width())
        self.top_right_x.setMinimum(0)
        self.top_left_x = QSlider(Qt.Horizontal)
        self.top_left_x.setMaximum(self.pixmap.width())
        self.top_left_x.setValue(0)
        self.top_left_x.setMinimum(0)
        self.top_y = QSlider(Qt.Vertical)
        self.top_y.setMaximum(self.pixmap.height())
        self.top_y.setValue(self.pixmap.height())
        self.top_y.setMinimum(0)

        self.all_layouts.insertLayout(0,self.knobs_layout_up)
        self.all_layouts.insertLayout(2,self.knobs_layout_down)
        #self.all_layouts.insertLayout(1,self.pic_layout)
        self.knobs_layout_down.addWidget(self.button_left_x)
        self.knobs_layout_down.addWidget(button)
        #self.knobs_layout_down.addStretch(.1)
        self.knobs_layout_down.addWidget(self.button_right_x)
        self.knobs_layout_up.addWidget(self.top_left_x)
        self.knobs_layout_up.addStretch(.1)
        self.knobs_layout_up.addWidget(self.top_right_x)
        self.top_slider_layput.addWidget(self.top_y)
        self.button_left_x.valueChanged.connect(self.u_button_left_x)
        self.button_right_x.valueChanged.connect(self.u_button_right_x)
        self.top_left_x.valueChanged.connect(self.u_top_left_x)
        self.top_right_x.valueChanged.connect(self.u_top_right_x)
        self.top_y.valueChanged.connect(self.u_top_y)
        self.all_layouts.insertLayout(1,self.all_pic_layout)
        self.setLayout(self.all_layouts)
        self.initUI()
    def export(self):
        
        print("bottom_left = ("+str(self.left_[0])+","+str(self.left_[1])+")")
        print("upper_left = ("+str(self.left_[2])+","+str(self.left_[3])+")")
        print("bottom_right = ("+str(self.right_[0])+","+str(self.right_[0])+")")
        print("upper_right = ("+str(self.right_[2])+","+str(self.right_[3])+")")
    def u_button_left_x(self, value):
        all_data = self.left_
        self.left_ = (value, all_data[1], all_data[2], all_data[3])
        # set butom_right minimum
        current = self.button_right_x.value()
        self.button_right_x.setMinimum(value)
        self.button_right_x.setValue(current)
        self.redraw()
    def u_button_right_x(self, value):
        all_data = self.right_
        self.right_ = (value, all_data[1], all_data[2], all_data[3])
        # SEt button_left maximum
        current = self.button_left_x.value()
        self.button_left_x.setMaximum(value)
        self.button_left_x.setValue(current)
        self.redraw()
    def u_top_left_x(self, value):
        all_data = self.left_
        self.left_ = (all_data[0], all_data[1], value, all_data[3])
        all_data = self.top_
        self.top_ = (value, all_data[1], all_data[2], all_data[3])
        #Set top_right minimum
        current = self.top_right_x.value()
        self.top_right_x.setMinimum(value)
        self.top_right_x.setValue(current)
        self.redraw()
    def u_top_right_x(self, value):
        all_data = self.right_
        self.right_ = (all_data[0], all_data[1], value, all_data[3])
        all_data = self.top_
        self.top_ = (all_data[0], all_data[1], value, all_data[3])
        #Set top_right maximum
        current = self.top_left_x.value()
        self.top_left_x.setMaximum(value)
        self.top_left_x.setValue(current)
        self.redraw()
    def u_top_y(self, value):
        val = self.pixmap.height() - value
        all_data = self.top_
        self.top_ = (all_data[0], val, all_data[2], val)
        all_datal = self.left_
        self.left_ = (all_datal[0], all_datal[1], all_datal[2], val)
        all_datar = self.right_
        self.right_ = (all_datar[0], all_datar[1], all_datar[2], val)
        self.redraw()
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.redraw()
        #self.resize(self.pixmap.width(), self.pixmap.height()+100)
        #self.setLayout(all_layouts)
        self.show()
    def redraw(self):
        #painter.setRenderHint(QPainter.Antialiasing)
	
        painter = QPainter()
        painter.begin(self)
        self.pixmap.load(self.image_)
        painter.drawPixmap(self.pixmap.width(), self.pixmap.height(), self.pixmap)
        painter.end()
        painter.begin(self.pixmap)
       # painter = QPainter(pixmap)
        pen = QPen(Qt.red,3, Qt.SolidLine, Qt.SquareCap, Qt.BevelJoin)
        painter.setPen(pen)
        for i in [self.left_, self.right_, self.top_]:
                painter.drawLine(i[0],i[1],i[2],i[3]);
        self.label.setPixmap(self.pixmap)
        self.label_bl.setText("["+str(self.left_[0])+","+str(self.left_[1])+"]")
        self.label_ul.setText("["+str(self.left_[2])+","+str(self.left_[3])+"]")
        self.label_br.setText("["+str(self.right_[0])+","+str(self.right_[0])+"]")
        self.label_ur.setText("["+str(self.right_[2])+","+str(self.right_[3])+"]")
        if not self.first_draw_:
                self.info_layout_down.itemAt(0).widget().deleteLater()
                self.info_layout_down.itemAt(1).widget().deleteLater()
                self.info_layout_up.itemAt(0).widget().deleteLater()
                self.info_layout_up.itemAt(1).widget().deleteLater()
                self.pic_layout.itemAt(0).widget().deleteLater()
                self.label = QLabel(self)
                self.label_bl = QLabel(self)
                self.label_ul = QLabel(self)
                self.label_br = QLabel(self)
                self.label_ur = QLabel(self)
                self.label_ur.setAlignment(Qt.AlignRight)
                self.label_br.setAlignment(Qt.AlignRight)
                self.label_ur.setFont(self.newfont)
                self.label_bl.setFont(self.newfont)# = QLabel(self)
                self.label_br.setFont(self.newfont)
                self.label_ul.setFont(self.newfont)
                self.label_bl.setText("["+str(self.left_[0])+","+str(self.left_[1])+"]")
                self.label_ul.setText("["+str(self.left_[2])+","+str(self.left_[3])+"]")
                self.label_br.setText("["+str(self.right_[0])+","+str(self.right_[0])+"]")
                self.label_ur.setText("["+str(self.right_[2])+","+str(self.right_[3])+"]")
                self.label.setPixmap(self.pixmap)
                #self.all_layouts.itemAt(1).width().deleteLater()
        self.first_draw_ = False
        #self.all_layouts.itemAt(1).widget().deleteLater()
        #self.pic_layout = QVBoxLayout()
        self.info_layout_up.insertWidget(0,self.label_ul)
        self.info_layout_up.insertWidget(1,self.label_ur)
        self.info_layout_down.insertWidget(0,self.label_bl)
        self.info_layout_down.insertWidget(1,self.label_br)
        self.pic_layout.insertWidget(0, self.label)
        #self.all_layouts.insertLayout(1,self.pic_layout)
        painter.end()
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App('../test_images/solidYellowCurve2.jpg')
    sys.exit(app.exec_())
