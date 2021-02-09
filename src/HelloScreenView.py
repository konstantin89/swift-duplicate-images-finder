from dearpygui import core, simple

import time
import webbrowser

from resources import get_resource_full_path

class HelloScreenView:

    def __init__(self, new_scan_click_callback: callable):

        self._window_name: str = 'Hello Screen'

        self._source_webpage_url:str = 'https://github.com/konstantin89/swift-duplicate-images-finder'

        self._new_scan_click_callback:callable = new_scan_click_callback

        main_window_size = core.get_main_window_size()

        self._window_x_pos: int = int(main_window_size[0]/2) - 200
        self._window_y_pos: int = int(main_window_size[1]/2) - 100

        self._logo_full_path = get_resource_full_path('resources/logo.png')

        with simple.window(self._window_name):
            core.configure_item(
                self._window_name,
                    width=300,
                    height=200,
                    x_pos=self._window_x_pos,
                    y_pos=self._window_y_pos,
                    label='Welcome!')

            core.add_text('Welcome to Duplicate Image Finder!')
            
            core.add_drawing(
                name='hello_screen_logo', 
                width=100, 
                height=100)

            core.draw_image(
                drawing='hello_screen_logo', 
                file=self._logo_full_path, 
                pmin=[0, 0], 
                pmax=[100, 100],
                uv_min=[0, 0], 
                uv_max=[1, 1], 
                tag="image")
           
            core.add_button(
                name='start_new_scan_button',
                label='Start New Scan', 
                callback=self._internal_new_scan_click_callback)

            core.add_button(
                name='visit_source_page_button',
                label='Visit Github source page', 
                callback=self._visit_source_page_click_callback)


    def ShowWindow(self):

        simple.show_item(self._window_name)


    def HideWindow(self):

        simple.hide_item(self._window_name)


    def _internal_new_scan_click_callback(self, sender: str, data: None):

         self._new_scan_click_callback()


    def _visit_source_page_click_callback(self, sender: None, data: None):
        try:
            webbrowser.open(self._source_webpage_url, new=2)

        except Exception as e:
            core.log_error('HelloScreenView - Failed to visit source page with exception : [%s]' % (e))