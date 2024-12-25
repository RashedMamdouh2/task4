from PyQt5 import QtCore
from PyQt5.QtWidgets import (QLabel, QProgressBar, QSlider, QGridLayout,
                QFrame, QComboBox, QRadioButton, QPushButton, QWidget)
from PyQt5.QtCore import QPoint
from PyQt5.QtCore import Qt
import Image
import ImageSelector

def create_line(central_widget, horizontal = False, thick = True):
        line = QFrame(central_widget)  
        if horizontal:
            line.setFrameShape(QFrame.HLine)
        else:
            line.setFrameShape(QFrame.VLine)

        line.setFrameShadow(QFrame.Sunken)
        if thick:
            line.setStyleSheet("border: 1px solid white;")
        return line

def create_slider(minimum, maximum):
    slider = QSlider()
    slider.setOrientation(Qt.Horizontal)
    slider.setMinimum(minimum)
    slider.setMaximum(maximum)
    slider.setValue(100)
    return slider

def create_radio_button(MainWindow, state = False):
    radio_button = QRadioButton()
    radio_button.setText("Show")
    radio_button.setChecked(state)
    radio_button.toggled.connect(MainWindow.switch_output_label)
    return radio_button

class ImageLabel(QLabel):
    def __init__(self, MainWindow, region_slider, parent=None):
        super().__init__(parent)
        self.MainWindow = MainWindow
        self.image = Image.Image(self)
        self.image.load_image("imgaes\Screen Shot 2024-11-10 at 10.27.12 AM.png")
        self.image.resize_image()
        self.last_mouse_pos = QPoint()
        self.ft_label = QLabel()
        self.label = ImageSelector.ImageSelector(slider= region_slider)
        self.magnitude_real_slider = create_slider(10, 200)
        self.phase_imaginary_slider = create_slider(10, 200)
        self.magnitude_real_label = QLabel("Magnitude")
        self.phase_imaginary_label = QLabel("Phase")
        combobox_label = QLabel("FT Component:")

        self.ft_combobox = QComboBox()

        self.ft_combobox.addItems( ["Magnitude", "Phase", "Real", "Imaginary"])

        line = create_line(MainWindow.centralwidget, thick=True)

        self.image_layout = QGridLayout()
        self.image_layout.addWidget(self, 0, 0, 1, 2)
        # self.image_layout.addWidget(self.ft_label, 0, 3, 1, 2)
        self.image_layout.addWidget(self.magnitude_real_label, 1, 0)
        self.image_layout.addWidget(self.magnitude_real_slider, 1, 1)
        self.image_layout.addWidget(line, 1, 2, 2, 1)
        self.image_layout.addWidget(combobox_label, 1, 3, 2, 1)
        self.image_layout.addWidget(self.ft_combobox, 1, 4, 2, 1)
        self.image_layout.addWidget(self.phase_imaginary_label, 2, 0)
        self.image_layout.addWidget(self.phase_imaginary_slider, 2, 1)
        self.ft_combobox.currentIndexChanged.connect(lambda: MainWindow.change_ft_component(
                        self.ft_combobox.currentText(), self.image, self.ft_label,slider= self.region_slider,layout=self.image_layout))
        MainWindow.change_ft_component(self.ft_combobox.currentText(), self.image, self.ft_label,slider= region_slider,layout=self.image_layout)

        self.ft_label.setFixedSize(300,400)
        self.ft_label.setScaledContents(True)


    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.image.load_image()
            self.MainWindow.resize_images()
            self.MainWindow.change_ft_component(self.ft_combobox.currentText(), self.image, self.ft_label,slider= self.selected_region_slider,layout=self.image_layout)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.last_mouse_pos = event.pos()
            self.in_brightness = self.image.brightness
            self.in_con = self.image.contrast

    def mouseMoveEvent(self, event):
        if self.image.image is not None and event.buttons() & Qt.LeftButton:
            delta = event.pos() - self.last_mouse_pos
            self.last_mouse_pos = event.pos()
            new_brightness = self.in_brightness - delta.y() /10
            new_contrast = max(0.1, self.in_con + delta.x()/10 * 0.01) 
            brightness_min, brightness_max = -50, 50  
            contrast_min, contrast_max = 0.5, 2.0  
            self.image.brightness = max(brightness_min, min(brightness_max, new_brightness))
            self.image.contrast = max(contrast_min, min(contrast_max, new_contrast))
            self.image.adjust_brightness_contrast()


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setWindowTitle("FT Image Mixer")
        MainWindow.resize(1233, 799)
        self.centralwidget = QWidget(MainWindow)
        self.main_gridLayout = QGridLayout(self.centralwidget)
        self.output_layout = QGridLayout()
        self.main_controls_layout = QGridLayout()

        self.selected_region_slider = create_slider(10, 400)
        line_1 = create_line(self.centralwidget)
        line_2 = create_line(self.centralwidget)
        line_3 = create_line(self.centralwidget)
        line_4 = create_line(self.centralwidget)
        line_5 = create_line(self.centralwidget, horizontal= True)
        line_6 = create_line(self.centralwidget, horizontal= True)
        line_7 = create_line(self.centralwidget)
        line_8 = create_line(self.centralwidget)
        line_9 = create_line(self.centralwidget, horizontal= True)

        self.image_1_label = ImageLabel(MainWindow, self.selected_region_slider, self.centralwidget)
        self.image_2_label = ImageLabel(MainWindow, self.selected_region_slider, self.centralwidget)
        self.image_3_label = ImageLabel(MainWindow, self.selected_region_slider, self.centralwidget)
        self.image_4_label = ImageLabel(MainWindow, self.selected_region_slider, self.centralwidget)
        self.images = [self.image_1_label, self.image_2_label, self.image_3_label, self.image_4_label]

        self.output_1_label = QLabel(self.centralwidget)
        self.output_2_label = QLabel(self.centralwidget)
        self.select_region_label = QLabel(text= "Selected Region:")
        self.ft_pairs_label = QLabel("Reconstruction Pairs:")
        self.progress_label = QLabel("Mixing Progress:")

        self.output_1_image = Image.Image(self.output_1_label)
        self.output_2_image = Image.Image(self.output_2_label)
        self.output_1_radiobutton = create_radio_button(MainWindow, state= True)
        self.output_2_radiobutton = create_radio_button(MainWindow)

        self.output_layout.addWidget(self.output_1_label, 0, 0)
        self.output_layout.addWidget(self.output_2_label, 0, 2)
        self.output_layout.addWidget(line_8, 0, 1, 2, 1)
        self.output_layout.addWidget(self.output_1_radiobutton, 1, 0, 2, 1)
        self.output_layout.addWidget(self.output_2_radiobutton, 1, 2, 2, 1)
        self.output_layout.addWidget(line_9, 2, 0, 1, 3)

        self.ft_pairs_combobox = QComboBox()
        self.ft_pairs_combobox.addItems(["Magnitude and Phase", "Real and Imaginary"])
        self.ft_pairs_combobox.currentIndexChanged.connect(lambda:MainWindow.change_reconstruction_pairs(self.images))

        self.mix_button = QPushButton()
        self.mix_button.setText("Mix Images")
        self.mix_button.clicked.connect(lambda: MainWindow.mix_images(self.images))

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100) 
        self.progress_bar.setValue(0)

        self.main_controls_layout.addWidget(self.mix_button, 0, 0, 1, 1)
        self.main_controls_layout.addWidget(line_7, 0, 1, 1, 1)
        self.main_controls_layout.addWidget(self.progress_label, 0, 2, 1, 1)
        self.main_controls_layout.addWidget(self.progress_bar, 0, 3, 1, 1)
        self.main_controls_layout.addWidget(self.select_region_label, 2, 0, 1, 1)
        self.main_controls_layout.addWidget(self.selected_region_slider, 2, 2, 1, 2)
        self.main_controls_layout.addWidget(self.ft_pairs_label, 3, 0, 1, 1)
        self.main_controls_layout.addWidget(self.ft_pairs_combobox, 3, 2, 1, 2)

        self.main_gridLayout.addLayout(self.image_1_label.image_layout, 0, 0)
        self.main_gridLayout.addLayout(self.image_2_label.image_layout, 0, 2)
        self.main_gridLayout.addLayout(self.image_3_label.image_layout, 2, 0)
        self.main_gridLayout.addLayout(self.image_4_label.image_layout, 2, 2)
        self.main_gridLayout.addLayout(self.output_layout, 0, 4, 1, 1)
        self.main_gridLayout.addLayout(self.main_controls_layout, 1, 4, 2, 1)
        self.main_gridLayout.addWidget(line_1, 0, 3, 1, 1)
        self.main_gridLayout.addWidget(line_2, 2, 3, 1, 1)
        self.main_gridLayout.addWidget(line_3, 0, 1, 1, 1)
        self.main_gridLayout.addWidget(line_4, 2, 1, 1, 2)
        self.main_gridLayout.addWidget(line_5, 1, 0, 1, 1)
        self.main_gridLayout.addWidget(line_6, 1, 2, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
