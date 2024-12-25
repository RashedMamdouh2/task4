from PyQt5.QtWidgets import (QApplication, QMainWindow)
import sys
from qt_material import apply_stylesheet
from UI import Ui_MainWindow
from ImageMixingWorker import ImageMixingWorker
import Image
from ImageSelector import ImageSelector
class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.output_label = self.output_1_label
        self.reconstruction_pair = "Magnitude and Phase"

    def remove_widget_from_grid(self,layout, row, column):
        for i in range(layout.count()):
            item = layout.itemAt(i)
            if item is not None:
                widget = item.widget()
                if widget is not None:
                    # Get the position of the widget in the grid
                    r, c, rs, cs = layout.getItemPosition(i)
                    if r == row and c == column:
                        # Remove the widget from the layout
                        layout.removeWidget(widget)
                        widget.deleteLater()  # Optionally delete the widget
                        return widget  # Return the removed widget if needed
        return None

    def change_ft_component(self, text, image, ft_label,slider,layout):

        pixmap=None
        if text == "Magnitude":
            magnitude_8bit = Image.normalize_to_8bit(image.magnitude_log)
            mag_pixmap = Image.array_to_pixmap(magnitude_8bit)
            pixmap=mag_pixmap


        if text == "Phase":
            phase_8bit = Image.normalize_to_8bit(image.phase_spectrum)
            phase_pixmap = Image.array_to_pixmap(phase_8bit)
            pixmap=phase_pixmap

        if text == "Real":
            real_8bit = Image.normalize_to_8bit(image.real_component)
            real_pixmap = Image.array_to_pixmap(real_8bit)
            pixmap=real_pixmap

        if text == "Imaginary":
            imaginary_8bit = Image.normalize_to_8bit(image.imaginary_component)
            imaginary_pixmap = Image.array_to_pixmap(imaginary_8bit)
            pixmap=imaginary_pixmap
        self.remove_widget_from_grid(layout, 0, 3)
        selector=ImageSelector(slider=slider,pixmap=pixmap)
        layout.addWidget(selector, 0, 3, 1, 2)
        # layout.removeWidget(ft_label)
        # ft_label.deleteLater()  # Optionally delete the label if it's no longer needed

        # Add the image_selector to the layout at the same grid position



    def mix_images(self, images):
        if hasattr(self, "worker") and self.worker.isRunning():
            self.worker.cancel()
            self.worker.wait()

        self.worker = ImageMixingWorker(images, self.reconstruction_pair)
        self.worker.progress.connect(self.update_progress_bar)
        self.worker.result_ready.connect(self.display_mixed_image)
        self.worker.start()

    def update_progress_bar(self, value):
        self.progress_bar.setValue(value) 

    def display_mixed_image(self, mixed_image):
        mixed_image_8bit = Image.normalize_to_8bit(mixed_image)
        mixed_image_pixmap = Image.array_to_pixmap(mixed_image_8bit)
        self.output_label.setPixmap(mixed_image_pixmap)
        self.progress_bar.setValue(0)

    def change_reconstruction_pairs(self, images):
        self.reconstruction_pair = self.ft_pairs_combobox.currentText()
        pairs = [["Magnitude", "Phase"], ["Real", "Imaginary"]]
        for image in images:
            image.magnitude_real_label.setText(pairs[self.ft_pairs_combobox.currentIndex()][0])
            image.phase_imaginary_label.setText(pairs[self.ft_pairs_combobox.currentIndex()][1])
            image.magnitude_real_slider.setValue(100)
            image.phase_imaginary_slider.setValue(100)

    def switch_output_label(self):
        if self.output_1_radiobutton.isChecked():
            self.output_label = self.output_1_label
        else:
            self.output_label = self.output_2_label

    def resize_images(self):
        self.minimum_height = min(image.image.image.shape[0] for image in self.images)
        self.minimum_width = min(image.image.image.shape[1] for image in self.images)
        for image in self.images:
            image.image.resize_image(self.minimum_width, self.minimum_height)
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    apply_stylesheet(app, "dark_purple.xml")
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
