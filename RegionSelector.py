import sys
import numpy as np
import cv2
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QGraphicsView,
    QGraphicsScene, QGraphicsRectItem, QSlider, QPushButton,
    QMainWindow
)
from PyQt5.QtGui import QImage, QPixmap, QPen, QColor, QBrush
from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtWidgets import QGraphicsPixmapItem


import sys
import numpy as np
import cv2
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QGraphicsView,
    QGraphicsScene, QGraphicsRectItem, QSlider, QPushButton,
    QMainWindow
)
from PyQt5.QtGui import QImage, QPixmap, QPen, QColor, QBrush
from PyQt5.QtCore import Qt, QRectF


from PyQt5.QtCore import QPointF

class FTRegionSelector(QWidget):
    def __init__(self, fft: np.ndarray, magnitude: np.ndarray, width: int, height: int, slider: QSlider):
        super().__init__()
        self.setWindowTitle("Fourier Transform Region Selector")
        self.fft = fft
        self.magnitude = magnitude
        self.image_width = width
        self.image_height = height
        self.rect_width = min(self.image_width, self.image_height) // 2
        self.rect_height = self.rect_width
        self.slider = slider
        self.rect_item = None

        # Set slider max to the larger dimension
        self.slider.setMaximum(max(self.image_width, self.image_height))
        self.slider.valueChanged.connect(self.update_rectangle_size)

        # Layout
        self.main_layout = QVBoxLayout(self)

        # Graphics View and Scene
        self.ft_view = QGraphicsView()
        self.ft_scene = QGraphicsScene()
        self.ft_view.setScene(self.ft_scene)
        self.main_layout.addWidget(self.ft_view)

        # Display the magnitude image
        self.display_image(self.magnitude, self.ft_scene)

        # Initialize rectangle
        self.add_rectangle()

    def display_image(self, image, scene):
        """Display a given image in the specified QGraphicsScene."""
        scene.clear()
        qimage = QImage(image.data, self.image_width, self.image_height, QImage.Format_Grayscale8)
        pixmap = QPixmap.fromImage(qimage)
        pixmap_item = QGraphicsPixmapItem(pixmap)
        scene.addItem(pixmap_item)

    def add_rectangle(self):
        """Add or update the rectangle based on the slider value."""
        slider_value = self.slider.value()
        center_x = self.image_width // 2
        center_y = self.image_height // 2

        # Calculate dimensions proportionally
        half_width = int(slider_value * self.image_width / max(self.image_width, self.image_height)) // 2
        half_height = int(slider_value * self.image_height / max(self.image_width, self.image_height)) // 2

        rect_x = max(0, center_x - half_width)
        rect_y = max(0, center_y - half_height)
        rect_w = min(2 * half_width, self.image_width - rect_x)
        rect_h = min(2 * half_height, self.image_height - rect_y)

        if self.rect_item:
            self.ft_scene.removeItem(self.rect_item)

        self.rect_item = QGraphicsRectItem(QRectF(rect_x, rect_y, rect_w, rect_h))
        self.rect_item.setPen(QPen(QColor(255, 0, 0), 2))  # Red border
        self.rect_item.setBrush(QBrush(QColor(255, 0, 0, 50)))  # Semi-transparent fill

        self.rect_item.setFlag(QGraphicsRectItem.ItemIsMovable, True)
        self.rect_item.setFlag(QGraphicsRectItem.ItemIsSelectable, True)

        # Restrict movement within the image bounds
        self.rect_item.setPos(QPointF(*self.get_constrained_position(rect_x, rect_y)))

        self.ft_scene.addItem(self.rect_item)

    def get_constrained_position(self, x, y):
        """Ensure the rectangle stays within the image bounds."""
        rect_width, rect_height = self.rect_item.rect().width(), self.rect_item.rect().height()
        x = max(0, min(x, self.image_width - rect_width))
        y = max(0, min(y, self.image_height - rect_height))
        return x, y

    def update_rectangle_size(self):
        """Update the rectangle size dynamically based on the slider."""
        self.add_rectangle()

    def get_selected_region(self):
        """Return the coordinates and size of the selected region."""
        if self.rect_item:
            rect = self.rect_item.rect()
            return int(rect.x()), int(rect.y()), int(rect.width()), int(rect.height())
        return None

    def get_inside_indices(self):
        """Return indices inside the selected region."""
        if self.rect_item:
            x, y, w, h = self.get_selected_region()
            x_indices, y_indices = np.meshgrid(
                np.arange(x, x + w), np.arange(y, y + h), indexing="ij"
            )
            return x_indices.flatten(), y_indices.flatten()
        return None, None

    def get_outside_indices(self):
        """Return indices outside the selected region."""
        if self.rect_item:
            x, y, w, h = self.get_selected_region()

            x_all, y_all = np.meshgrid(
                np.arange(self.image_width), np.arange(self.image_height), indexing="ij"
            )

            mask = (
                (x_all >= x)
                & (x_all < x + w)
                & (y_all >= y)
                & (y_all < y + h)
            )

            x_outside = x_all[~mask].flatten()
            y_outside = y_all[~mask].flatten()
            return x_outside, y_outside
        return None, None

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Load a sample image
    image = cv2.imread("imgaes/IMG_20230807_000054_971.jpg", cv2.IMREAD_GRAYSCALE)
    if image is None:
        print("Failed to load the image.")
        sys.exit()

    fft = np.fft.fft2(image)
    fft_shifted = np.fft.fftshift(fft)
    magnitude = np.log(np.abs(fft_shifted) + 1)

    # Main window
    main_window = QMainWindow()
    central_widget = QWidget()
    layout = QVBoxLayout(central_widget)

    # Slider
    slider = QSlider(Qt.Horizontal)
    slider.setMinimum(10)
    slider.setValue(50)
    layout.addWidget(slider)

    # Fourier Transform Selector
    selector = FTRegionSelector(fft=fft_shifted, magnitude=magnitude, width=image.shape[1], height=image.shape[0], slider=slider)
    layout.addWidget(selector)

    # Buttons
    inside_button = QPushButton("Get Inside Indices")
    outside_button = QPushButton("Get Outside Indices")

    def print_inside_indices():
        x, y = selector.get_inside_indices()
        print("Inside Indices:", x, y)

    def print_outside_indices():
        x, y = selector.get_outside_indices()
        print("Outside Indices:", x, y)

    inside_button.clicked.connect(print_inside_indices)
    outside_button.clicked.connect(print_outside_indices)

    layout.addWidget(inside_button)
    layout.addWidget(outside_button)

    main_window.setCentralWidget(central_widget)
    main_window.setWindowTitle("Fourier Transform Region Selector")
    main_window.show()

    sys.exit(app.exec_())
