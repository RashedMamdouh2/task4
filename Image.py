import cv2
import numpy as np
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import QPixmap, QImage

def normalize_to_8bit(array):
    norm = (255 * (array - array.min()) / (array.max() - array.min())).astype(np.uint8)
    return norm

def array_to_pixmap(array):
    height, width = array.shape
    bytes_per_line = width
    image_data = array.tobytes()
    qimage = QImage(image_data, width, height, bytes_per_line, QImage.Format_Grayscale8)
    return QPixmap.fromImage(qimage)

class Image:
    def __init__(self, image_label):
        super().__init__()
        self.image = None
        self.contrast = 1.0
        self.brightness = 0
        self.image_label = image_label
        self.image_label.setScaledContents(True)
        self.image_label.setFixedSize(300, 400)
    
    def update_display(self):
        """Update the displayed image based on brightness and contrast adjustments."""
        pixmap = array_to_pixmap(self.image)
        self.image_label.setPixmap(pixmap)

    def load_image(self, image_path= None):
        """"Load Image and get Magnitude, Phase, Real and Imaginary parts of the Image FT"""
        if image_path is None:
            image_path, _ = QFileDialog.getOpenFileName(
                None, 
                "Open File", 
                "", 
                "All Files (*.*);;Text Files (*.txt);;Images (*.png *.xpm *.jpg *.jpeg *.bmp *.gif)"
            )
        if image_path:
            self.image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
            self.adjust_brightness_contrast(reset= True)
            self.update_display()
        
    def compute_magnitude_phase(self):
        self.magnitude_spectrum = np.sqrt(self.real_component**2 + self.imaginary_component**2)
        self.magnitude_log = np.log1p(self.magnitude_spectrum)
        self.phase_spectrum = np.arctan2(self.imaginary_component, self.real_component)

    def compute_real_imaginary_parts(self):
        self.real_component = self.magnitude_spectrum * np.cos(self.phase_spectrum)
        self.imaginary_component = self.magnitude_spectrum * np.sin(self.phase_spectrum)

    def resize_image(self, width = None, height = None):
        if width and height:
            self.image = cv2.resize(self.image, (width, height))
        self.compute_ft_components()
        self.update_display()

    def compute_ft_components(self):
        self.ft = np.fft.fft2(self.image)
        self.ft_shifted = np.fft.fftshift(self.ft)
        self.magnitude_spectrum = np.abs(self.ft_shifted)
        self.magnitude_log = np.log1p(self.magnitude_spectrum) 
        self.phase_spectrum = np.angle(self.ft_shifted)
        self.real_component = np.real(self.ft_shifted)
        self.imaginary_component = np.imag(self.ft_shifted)

    def adjust_brightness_contrast(self, reset= False):
        if reset:
            self.brightness, self.contrast = 0, 1.0

        self.image= cv2.convertScaleAbs(self.image, alpha=self.contrast, beta=self.brightness)                                                                   
        self.update_display()

    def reconstruct_image(self):
        ft_inverse_shift = np.fft.ifftshift(self.ft_shifted)
        self.image = np.fft.ifft2(ft_inverse_shift)
        self.image = np.abs(self.image)
        self.update_display()

    def modify_magnitude(self, gain):
        gain = gain /100
        self.magnitude_spectrum = self.magnitude_spectrum * gain 
        self.ft_shifted = self.magnitude_spectrum * np.exp(1j * self.phase_spectrum)
        self.magnitude_log = np.log1p(self.magnitude_spectrum)
        self.compute_real_imaginary_parts()
        self.reconstruct_image()

    def modify_phase(self, angle_in_degrees):
        angle_in_degrees = angle_in_degrees/100
        shift_in_rad = angle_in_degrees * np.pi / 180.0
        self.phase_spectrum = self.phase_spectrum + shift_in_rad 
        self.ft_shifted = self.magnitude_spectrum * np.exp(1j * self.phase_spectrum)
        self.compute_real_imaginary_parts()
        self.reconstruct_image()

    def modify_real_parts(self, gain):
        self.real_component *= gain
        self.ft_shifted = self.real_component + 1j * self.imaginary_component
        self.compute_magnitude_phase()

    def modify_imaginary_parts(self, gain):
        self.imaginary_component *= gain
        self.ft_shifted = self.real_component + 1j * self.imaginary_component
        self.compute_magnitude_phase()

    def modify_selected_part(compoent_to_modify, selected_row, selected_coloumn, gain, phase_to_modify = None):
        if phase_to_modify is None:
            row_start, row_end = selected_row[0], selected_row[-1]
            col_start, col_end = selected_coloumn[0], selected_coloumn[-1]
            compoent_to_modify[row_start:row_end, col_start:col_end] *= gain 
        else:
            angle_in_rad = gain * np.pi / 180.0
            phase_to_modify[row_start:row_end, col_start:col_end] += angle_in_rad

    def modify_low_frequencies(compoent_to_modify, gain, phase_to_modify = None):
        rows, cols = compoent_to_modify.shape
        center_x, center_y = rows // 2, cols // 2
        radius = 30 
        y, x = np.ogrid[:rows, :cols]
        mask = (x - center_x)**2 + (y - center_y)**2 <= radius**2

        if phase_to_modify is None:
            compoent_to_modify[mask] *= gain  
        else:
            shift_in_rad = gain * np.pi / 180.0
            phase_to_modify[mask] += shift_in_rad

    def modify_high_frequencies(compoent_to_modify, gain, phase_to_modify = None):
        rows, cols = compoent_to_modify.shape
        center_x, center_y = rows // 2, cols // 2
        radius = 30 
        y, x = np.ogrid[:rows, :cols]
        mask = (x - center_x)**2 + (y - center_y)**2 >= radius**2

        if phase_to_modify is None:
            compoent_to_modify[mask] *= gain  

        else:
            shift_in_rad = gain * np.pi / 180.0
            phase_to_modify[mask] += shift_in_rad
