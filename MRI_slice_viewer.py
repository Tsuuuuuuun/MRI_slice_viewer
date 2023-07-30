import os
import sys
import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QSlider, QHBoxLayout, QComboBox, QPushButton, QFileDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

class MRIViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.data = None
        self.cmap = "gray"

        # GUI components
        self.img_label = QLabel(self)

        self.select_button = QPushButton("Select MRI File", self)
        self.select_button.clicked.connect(self.show_dialog)
        
        self.cmap_combo = QComboBox(self)
        self.cmap_combo.addItems(['gray', 'viridis', 'plasma', 'inferno', 'magma', 'cividis'])
        self.cmap_combo.currentTextChanged.connect(self.change_cmap)
        
        self.direction_combo = QComboBox(self)
        self.direction_combo.addItems(['X', 'Y', 'Z'])
        self.direction_combo.currentTextChanged.connect(self.change_direction)

        self.x_pos = self.data.shape[0] // 2 if self.data is not None else 0
        self.x_slider = QSlider(Qt.Horizontal, self)
        self.x_slider.valueChanged.connect(self.change_x_slice)
        self.x_pos_label = QLabel(f"X Position: {self.x_pos}", self)

        self.y_pos = self.data.shape[0] // 2 if self.data is not None else 0
        self.y_slider = QSlider(Qt.Horizontal, self)
        self.y_slider.valueChanged.connect(self.change_y_slice)
        self.y_pos_label = QLabel(f"Y Position: {self.y_pos}", self)

        self.z_pos = self.data.shape[0] // 2 if self.data is not None else 0
        self.z_slider = QSlider(Qt.Horizontal, self)
        self.z_slider.valueChanged.connect(self.change_z_slice)
        self.z_pos_label = QLabel(f"Z Position: {self.z_pos}", self)

        self.set_sliders_enabled(False)
        self.direction_combo.setEnabled(False)
        self.cmap_combo.setEnabled(False)

        self.direction = 'X'
        self.set_sliders_enabled_for_direction(self.direction)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.select_button)
        layout.addWidget(self.img_label)
        layout.addWidget(QLabel("Color Map:"))
        layout.addWidget(self.cmap_combo)
        layout.addWidget(QLabel("Direction:"))
        layout.addWidget(self.direction_combo)

        layout.addWidget(QLabel("X Slice:"))
        layout.addWidget(self.x_slider)
        layout.addWidget(self.x_pos_label)
        layout.addWidget(QLabel("Y Slice:"))
        layout.addWidget(self.y_slider)
        layout.addWidget(self.y_pos_label)
        layout.addWidget(QLabel("Z Slice:"))
        layout.addWidget(self.z_slider)
        layout.addWidget(self.z_pos_label)

        self.setLayout(layout)
        self.setWindowTitle('MRI Slice Viewer')

    def show_dialog(self):
        options = QFileDialog.Options()
        filepath, _ = QFileDialog.getOpenFileName(self, "Select MRI File", "", "Nifti Files (*.nii *.nii.gz);;All Files (*)", options=options)
        if filepath:
            self.load_data(filepath)

    def load_data(self, filepath):
        nii_data = nib.load(filepath)
        self.data = nii_data.get_fdata()

        self.x_slider.setMaximum(self.data.shape[0] - 1)
        self.y_slider.setMaximum(self.data.shape[1] - 1)
        self.z_slider.setMaximum(self.data.shape[2] - 1)

        # Initial slice positions
        self.x_pos = self.data.shape[0] // 2
        self.y_pos = self.data.shape[1] // 2
        self.z_pos = self.data.shape[2] // 2
        self.direction = 'X'

        self.set_sliders_enabled(True)
        self.direction_combo.setEnabled(True)
        self.cmap_combo.setEnabled(True)

        self.change_direction('X')

        self.update_image()

    def change_cmap(self, cmap):
        self.cmap = cmap
        self.update_image()

    def set_sliders_enabled(self, enabled=True):
        self.x_slider.setEnabled(enabled)
        self.y_slider.setEnabled(enabled)
        self.z_slider.setEnabled(enabled)
        self.direction_combo.setEnabled(enabled)
        self.cmap_combo.setEnabled(enabled)
        


    def change_direction(self, direction):
        self.direction = direction
        self.set_sliders_enabled_for_direction(direction)
        self.update_image()

    def set_sliders_enabled_for_direction(self, direction):
        self.x_slider.setEnabled(direction == 'X')
        self.y_slider.setEnabled(direction == 'Y')
        self.z_slider.setEnabled(direction == 'Z')


    def change_x_slice(self, value):
        self.x_pos = value
        self.x_pos_label.setText(f"X Position: {self.x_pos}")
        if self.direction == 'X':
            self.update_image()

    def change_y_slice(self, value):
        self.y_pos = value
        self.y_pos_label.setText(f"Y Position: {self.y_pos}")
        if self.direction == 'Y':
            self.update_image()

    def change_z_slice(self, value):
        self.z_pos = value
        self.z_pos_label.setText(f"Z Position: {self.z_pos}")
        if self.direction == 'Z':
            self.update_image()

    def update_image(self):
        if self.direction == 'X':
            slice_data = self.data[self.x_pos, :, :]
        elif self.direction == 'Y':
            slice_data = self.data[:, self.y_pos, :]
        else:
            slice_data = self.data[:, :, self.z_pos]

        plt.figure(figsize=(6, 6))
        plt.imshow(slice_data, cmap=self.cmap, origin="lower")
        plt.axis('off')
        plt.savefig('temp.png', bbox_inches='tight', pad_inches=0)
        plt.close()

        pixmap = QPixmap('temp.png')
        self.img_label.setPixmap(pixmap)

    def cleanup(self):
        if os.path.exists("temp.png"):
            os.remove("temp.png")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    viewer = MRIViewer()
    viewer.show()
    app.exec_()
    viewer.cleanup()
