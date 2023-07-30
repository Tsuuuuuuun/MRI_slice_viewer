import os
import sys
import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QSlider, QHBoxLayout, QComboBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

class MRIViewer(QWidget):
    def __init__(self, data, cmap="gray"):
        super().__init__()
        self.data = data
        self.cmap = cmap

        # Initial slice positions
        self.x_pos = self.data.shape[0] // 2
        self.y_pos = self.data.shape[1] // 2
        self.z_pos = self.data.shape[2] // 2
        self.direction = 'X'

        # GUI components
        self.img_label = QLabel(self)
        self.update_image()

        self.direction_combo = QComboBox(self)
        self.direction_combo.addItems(['X', 'Y', 'Z'])
        self.direction_combo.currentTextChanged.connect(self.change_direction)

        self.x_slider = QSlider(Qt.Horizontal, self)
        self.x_slider.setMaximum(self.data.shape[0] - 1)
        self.x_slider.setValue(self.x_pos)
        self.x_slider.valueChanged.connect(self.change_x_slice)

        self.y_slider = QSlider(Qt.Horizontal, self)
        self.y_slider.setMaximum(self.data.shape[1] - 1)
        self.y_slider.setValue(self.y_pos)
        self.y_slider.valueChanged.connect(self.change_y_slice)

        self.z_slider = QSlider(Qt.Horizontal, self)
        self.z_slider.setMaximum(self.data.shape[2] - 1)
        self.z_slider.setValue(self.z_pos)
        self.z_slider.valueChanged.connect(self.change_z_slice)
        self.set_sliders_enabled_for_direction(self.direction)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.img_label)
        layout.addWidget(QLabel("Direction:"))
        layout.addWidget(self.direction_combo)
        layout.addWidget(QLabel("X Slice:"))
        layout.addWidget(self.x_slider)
        layout.addWidget(QLabel("Y Slice:"))
        layout.addWidget(self.y_slider)
        layout.addWidget(QLabel("Z Slice:"))
        layout.addWidget(self.z_slider)

        self.setLayout(layout)
        self.setWindowTitle('MRI Slice Viewer')

    def change_direction(self, direction):
        self.direction = direction
        self.set_sliders_enabled_for_direction(direction)
        self.update_image()

    def change_x_slice(self, value):
        self.x_pos = value
        if self.direction == 'X':
            self.update_image()

    def change_y_slice(self, value):
        self.y_pos = value
        if self.direction == 'Y':
            self.update_image()

    def change_z_slice(self, value):
        self.z_pos = value
        if self.direction == 'Z':
            self.update_image()

    def set_sliders_enabled_for_direction(self, direction):
        self.x_slider.setEnabled(direction == 'X')
        self.y_slider.setEnabled(direction == 'Y')
        self.z_slider.setEnabled(direction == 'Z')
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

    if len(sys.argv) < 2:
        print("Usage: python MRI_slice_viewer.py <path_to_nii_file> [cmap]")
        sys.exit()

    filepath = sys.argv[1]
    cmap = "gray"
    if len(sys.argv) > 2:
        cmap = sys.argv[2]

    nii_data = nib.load(filepath)
    data = nii_data.get_fdata()
    viewer = MRIViewer(data, cmap)
    viewer.show()
    app.exec_()
    viewer.cleanup()
