from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QSlider, QWidget, QPushButton
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QPixmap, QPainter, QPen, QImage
import numpy as np

class ImageSelector(QWidget):
    def __init__(self, pixmap = None, slider = None, label_size=(300, 400),  parent=None):
        super().__init__(parent)
        self.slider=slider
        self.layout_ = QVBoxLayout(self)
        hawhaw_label = QLabel()
        hawhaw_label.setFixedSize(*label_size)
        hawhaw_label.setScaledContents(True)
        # Image Label
        self.image_label = ImageLabel(hawhaw_label)
        self.image_label.setScaledContents(True)
        self.image_label.setFixedSize(*label_size)
        self.layout_.addWidget(self.image_label)


        # Slider for rectangle size

        self.slider.setMinimum(10)  # Minimum rectangle size (as percentage)
        self.slider.setMaximum(90)  # Maximum rectangle size (as percentage)
        self.slider.setValue(50)    # Initial value
        self.slider.valueChanged.connect(self.updateRectangleSize)
        # self.layout_.addWidget(self.slider)
        # inner_b = QPushButton("inner", self)
        # outer_b = QPushButton("outer", self)
        # self.layout_.addWidget(inner_b)
        # self.layout_.addWidget(outer_b)
        # self.layout_.addWidget(hawhaw_label)
        # inner_b.clicked.connect(lambda: self.image_label.getModifiedPixmap())
        # outer_b.clicked.connect(lambda: self.image_label.getModifiedPixmap(inner= False))

        # Set initial pixmap if provided
        if pixmap:
            self.setPixmap(QPixmap(pixmap))

    def setPixmap(self, pixmap):
        """
        Set or update the pixmap displayed in the QLabel.
        """
        self.image_label.setPixmap(pixmap)
        self.image_label.update()

    def updateRectangleSize(self, value):
        self.image_label.setRectSizePercentage(value)

    def get_inner_region(self):
        """
        Return a QPixmap with the inner rectangle region preserved and outer regions set to zero.
        """
        return self.image_label.getModifiedPixmap(inner=True)

    def get_outer_region(self):
        """
        Return a QPixmap with the outer regions preserved and the inner rectangle region set to zero.
        """
        return self.image_label.getModifiedPixmap(inner=False)


class ImageLabel(QLabel):
    def __init__(self, hawhaw_label,  *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.hawhaw_label = hawhaw_label
        self.rect_percentage = 50  # Initial rectangle size (percentage of label)
        self.hawhaw = None

    def setRectSizePercentage(self, percentage):
        self.rect_percentage = percentage
        self.update()

    def paintEvent(self, event):
        super().paintEvent(event)
        if not self.pixmap():
            return

        # Draw the rectangle
        painter = QPainter(self)
        pen = QPen(Qt.red, 2, Qt.SolidLine)
        painter.setPen(pen)

        # Calculate the rectangle's size and position (centered and scaled to QLabel)
        label_width = self.width()
        label_height = self.height()
        rect_size = min(label_width, label_height) * self.rect_percentage / 100
        rect_x = (label_width - rect_size) / 2
        rect_y = (label_height - rect_size) / 2
        rect = QRect(int(rect_x), int(rect_y), int(rect_size), int(rect_size))

        painter.drawRect(rect)
        painter.end()

    def getModifiedPixmap(self, inner=True):
        """
        Return a QPixmap with either the inner rectangle region preserved (and outer set to zero)
        or the outer region preserved (and inner set to zero).
        """
        pixmap = self.pixmap()
        if pixmap is None:
            return None

        image = pixmap.toImage()
        width, height = image.width(), image.height()

        # Convert QImage to a NumPy array using pixel data directly
        image = image.convertToFormat(QImage.Format_RGBA8888)  # Ensure the format is RGBA
        ptr = image.bits()
        ptr.setsize(image.byteCount())
        image_data = np.frombuffer(ptr, np.uint8).reshape((height, width, 4))

        # Calculate the rectangle bounds (scaled to pixmap's size)
        rect_size = min(width, height) * self.rect_percentage / 100
        x1 = int((width - rect_size) / 2)
        y1 = int((height - rect_size) / 2)
        x2 = x1 + int(rect_size)
        y2 = y1 + int(rect_size)

        # Create masks for inner and outer regions
        mask = np.zeros((height, width), dtype=bool)
        mask[y1:y2, x1:x2] = True

        # Modify the image data
        if inner:
            image_data[~mask] = 0  # Set outer region to zero
        else:
            image_data[mask] = 0  # Set inner region to zero

        # Convert back to QImage and QPixmap
        new_image = QImage(image_data, width, height, image.bytesPerLine(), image.format())
        self.hawhaw = QPixmap.fromImage(new_image)
        self.hawhaw_label.setPixmap(self.hawhaw)
        return QPixmap.fromImage(new_image)


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    # Create an instance of ImageSelector
    window = ImageSelector("imgaes\IMG_20230807_000054_971.jpg")
    window.show()
    sys.exit(app.exec_())
