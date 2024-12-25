from PyQt5.QtCore import Qt, QRect, QPoint
from PyQt5.QtGui import QPainter, QColor, QPen

class RectangleSelector:
    def __init__(self, label, image_width, image_height):
        self.label = label
        self.image_width = image_width
        self.image_height = image_height

        # Rectangle parameters
        self.rect_x = 50
        self.rect_y = 50
        self.rect_size = 100

        # Store the original pixmap reference
        self.original_pixmap = None

    def update_pixmap(self, new_pixmap):
        """Update the pixmap reference and redraw."""
        self.original_pixmap = new_pixmap
        self.image_width = new_pixmap.width()
        self.image_height = new_pixmap.height()
        self.update_image_with_rectangle()

    def update_image_with_rectangle(self):
        """Redraw the image on the label with a rectangle outline."""
        if self.original_pixmap is None:
            print("Error: No original pixmap to update.")
            return

        # Copy the original pixmap
        pixmap_copy = self.original_pixmap.copy()
        painter = QPainter(pixmap_copy)

        # Set a thick red border with no fill
        pen = QPen(QColor(255, 0, 0), 4)  # Red color, 4-pixel thick
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)  # Ensure no fill for the rectangle

        # Draw the rectangle outline
        painter.drawRect(QRect(self.rect_x, self.rect_y, self.rect_size, self.rect_size))

        painter.end()
        self.label.setPixmap(pixmap_copy)

    def update_rectangle(self, x=None, y=None, size=None):
        """Update rectangle parameters and redraw."""
        if x is not None:
            self.rect_x = x
        if y is not None:
            self.rect_y = y
        if size is not None:
            self.rect_size = size

        self.update_image_with_rectangle()
