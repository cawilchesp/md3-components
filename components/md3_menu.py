"""
PyQt Menu component adapted to follow Material Design 3 guidelines


"""

from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt

from components.style_color import colors

import sys

# ----
# Menú
# ----
class MD3Menu(QtWidgets.QComboBox):
    def __init__(self, parent, attributes: dict) -> None:
        """ Material Design 3 Component: Menu

        Parameters
        ----------
        attributes: dict
            name: str
                Widget name
            position: tuple
                Button position
                (x, y) -> x, y: upper left corner
            width: tuple
                Menu width
            options: dict
                Menu options with translations
                Format: {0: ('es_1', 'en_1'), 1: ('es_2', 'en_2')}
            set: int
                Selected option
                -1: No option selected
            theme: bool
                App theme
                True: Light theme, False: Dark theme
            language: int
                App language
                0: Spanish, 1: English
        
        Returns
        -------
        None
        """
        super(MD3Menu, self).__init__(parent)

        self.attributes = attributes

        self.name = attributes['name']
        self.setObjectName(self.name)

        x, y = attributes['position'] if 'position' in attributes else (8,8)
        w = attributes['width'] if 'width' in attributes else 32
        self.setGeometry(x, y, w, 32)

        if 'options' in attributes:
            self.max_items = len(attributes['options']) if len(attributes['options']) < 6 else 10
            self.language_text(attributes['language'])
        else:
            self.max_items = 10

        self.setMaxVisibleItems(self.max_items)
        self.setMaxCount(self.max_items)
        self.setSizeAdjustPolicy(QtWidgets.QComboBox.SizeAdjustPolicy.AdjustToMinimumContentsLengthWithIcon)
        self.setCurrentIndex(attributes['set'])
        self.view().window().setWindowFlags(Qt.WindowType.Popup | Qt.WindowType.FramelessWindowHint | Qt.WindowType.NoDropShadowWindowHint)
        self.view().window().setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        self.apply_styleSheet(attributes['theme'])


    def apply_styleSheet(self, theme: bool) -> None:
        """ Apply theme style sheet to component """

        background_color = colors(theme, 'transparent_background')
        color = colors(theme, 'on_surface')
        border_color = colors(theme, 'outline')
        disable_color = colors(theme, 'surface_variant')

        if theme: icon_theme = 'L'
        else: icon_theme = 'D'
        current_path = sys.path[0].replace("\\","/")
        images_path = f'{current_path}/icons'

        self.setStyleSheet(f'QComboBox#{self.name} {{ '
                           f'border: 1px solid {color};'
                           f'border-radius: 4; '
                           f'background-color: {background_color}; '
                           f'color: {color} '
                           f'}}'
                           f'QComboBox#{self.name}::drop-down {{ '
                           f'border-color: {border_color} '
                           f'}}'
                           f'QComboBox#{self.name}::down-arrow {{ '
                           f'width: 16; height: 16;'
                           f'image: url({images_path}/menu_right_{icon_theme}.png) '
                           f'}}'
                           f'QComboBox#{self.name}:!Enabled {{ '
                           f'background-color: {disable_color} '
                           f'}}'
                           f'QComboBox#{self.name} QListView {{ '
                           f'border: 1px solid {color}; '
                           f'border-radius: 4;'
                           f'background-color: {background_color}; '
                           f'color: {color} '
                           f'}}')

    def language_text(self, language: int) -> None:
        """ Change language of label text """
        if 'options' in self.attributes:
            for key, value in self.attributes['options'].items():
                self.addItem('')
                if language == 0:   self.setItemText(key, value[0])
                elif language == 1: self.setItemText(key, value[1])