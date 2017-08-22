import numpy as np
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QGraphicsPixmapItem, QApplication

from urh.signalprocessing.Spectrogram import Spectrogram
from urh.ui.painting.SceneManager import SceneManager
from urh.ui.painting.SpectrogramScene import SpectrogramScene


class SpectrogramSceneManager(SceneManager):
    def __init__(self, samples, parent):
        super().__init__(parent)

        self.samples_need_update = True

        self.scene.clear()
        self.spectrogram = Spectrogram(samples)
        self.scene = SpectrogramScene()

    @property
    def num_samples(self):
        return len(self.spectrogram.samples)

    def set_parameters(self, samples: np.ndarray, window_size) -> bool:
        """

        :param samples:
        :param window_size:
        :param force_redraw:
        :return: True if redraw of scene is needed
        """
        redraw_needed = False
        if self.samples_need_update:
            self.spectrogram.samples = samples
            redraw_needed = True
            self.samples_need_update = False

        if window_size != self.spectrogram.window_size:
            self.spectrogram.window_size = window_size
            redraw_needed = True

        return redraw_needed

    def show_scene_section(self, x1: float, x2: float, subpath_ranges=None, colors=None):
        pass

    def update_scene_rect(self):
        self.scene.setSceneRect(0, 0, self.spectrogram.time_bins, self.spectrogram.freq_bins)

    def show_full_scene(self):
        for item in self.scene.items():
            if isinstance(item, QGraphicsPixmapItem):
                self.scene.removeItem(item)

        x_pos = 0
        for image in self.spectrogram.create_image_segments():
            item = self.scene.addPixmap(QPixmap.fromImage(image))
            item.setPos(x_pos, 0)
            x_pos += image.width()
            QApplication.instance().processEvents()

    def init_scene(self, apply_padding=True):
        pass

    def eliminate(self):
        self.spectrogram.samples = None
        self.spectrogram = None
        super().eliminate()
