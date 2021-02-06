from dearpygui import core, simple

import time

class ScanInProgressWindowView:

    def __init__(self):

        self._window_name: str = 'Scan in progress'

        main_window_size = core.get_main_window_size()

        self._window_x_pos: int = int(main_window_size[0]/2) - 200
        self._window_y_pos: int = int(main_window_size[1]/2) - 100

        with simple.window(self._window_name):
            core.configure_item(
                self._window_name,
                    width=300,
                    height=200,
                    x_pos=self._window_x_pos,
                    y_pos=self._window_y_pos,
                    label='Scan in progress')

            core.add_text('Scan in progress')

            core.add_text('Number of scanned images: ')
            core.add_same_line()
            core.add_text('##number_of_scanned_images', source='number_of_scanned_images')


    def ShowWindow(self):

        simple.show_item(self._window_name)

    def HideWindow(self):

        simple.hide_item(self._window_name)



