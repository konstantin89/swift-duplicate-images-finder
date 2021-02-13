# Standard library imports
from typing import Callable

# Third party imports
from dearpygui import core, simple

# Local application imports
from FileMetaData import FileMetaDataList
from FileMetaData import FileMetaData

from utils import visit_source_web_page

from ScanInProgressWindowView import ScanInProgressWindowView
from HelloScreenView import HelloScreenView
from ResultsWindowView import ResultsWindowView
from StartNewScanWindowView import StartNewScanWindowView


class MainView:
    """ View class of the MVC (Model View Controller) design pattern.
        This class implements all GUI related logic.
    """

    def __init__(self, 
        start_scan_callback: Callable, 
        delete_image_callback: Callable,
        delete_all_duplicates_callback: Callable):

        self._app_windows_size = {}
        self._app_windows_size['width'] = 1280
        self._app_windows_size['height'] = 780

        self._duplicates_list: [FileMetaDataList] = []     

        self._scan_in_progress_window = ScanInProgressWindowView()

        self._hello_screen_window = HelloScreenView(
            new_scan_click_callback=lambda: self.ShowNewScanWindow())

        self._results_window = ResultsWindowView(                    
            width=self._app_windows_size['width'],
            height=self._app_windows_size['height'],
            x_pos=0,
            y_pos=20,
            delete_image_callback=delete_image_callback, 
            delete_all_duplicates_callback=delete_all_duplicates_callback)


        self._start_new_scan_window = StartNewScanWindowView(
            width=self._app_windows_size['width'],
            height=self._app_windows_size['height'],
            x_pos=0,
            y_pos=20,
            start_scan_callback=start_scan_callback)

        self._primary_window_name: str = 'Duplicate Image Manager'


    def Init(self) -> None:

        self._create_primary_window()
        self.ShowHelloWindow()
        core.start_dearpygui(primary_window=self._primary_window_name)


    def ShowScanInProgressWindow(self)-> None:

        self._hide_all_windows()
        self._scan_in_progress_window.ShowWindow()


    def ShowResultsWindows(self, dupicates: [FileMetaDataList]) -> None:
        
        self._duplicates_list = dupicates
        self._hide_all_windows()
        self._results_window.ShowWindow(dupicates)


    def ShowNewScanWindow(self) -> None:
        
        self._hide_all_windows()
        self._start_new_scan_window.ShowWindow()


    def ShowHelloWindow(self) -> None:
        
        self._hide_all_windows()
        self._hello_screen_window.ShowWindow()


    def _hide_all_windows(self)-> None:

        self._scan_in_progress_window.HideWindow()
        self._hello_screen_window.HideWindow()
        self._results_window.HideWindow()
        self._start_new_scan_window.HideWindow()
        

    def _create_primary_window(self) -> None:

        core.set_main_window_title('Swift Duplicate Images Finder')

        core.set_main_window_size(
            self._app_windows_size['width'] + 20, 
            self._app_windows_size['height'] + 65)

        with simple.window(self._primary_window_name):

            core.configure_item(
                self._primary_window_name,
                label='Duplicate Images Manager')

            core.add_menu_bar("MenuBar")

            core.add_menu("Actions")
            core.add_menu_item("Start new scan", callback=self._new_scan_click_callback)
            core.add_menu_item("Quit", callback=self._quit_app_click_handler)                                       
            core.end()

            core.add_menu("Themes")
            core.add_menu_item("Dark", callback=self._theme_callback)
            core.add_menu_item("Light", callback=self._theme_callback)
            core.add_menu_item("Classic", callback=self._theme_callback)
            core.add_menu_item("Dark 2", callback=self._theme_callback)
            core.add_menu_item("Grey", callback=self._theme_callback)
            core.add_menu_item("Dark Grey", callback=self._theme_callback)
            core.add_menu_item("Cherry", callback=self._theme_callback)
            core.add_menu_item("Purple", callback=self._theme_callback)
            core.add_menu_item("Gold", callback=self._theme_callback)
            core.add_menu_item("Red", callback=self._theme_callback)
            core.end()

            core.add_menu("Tools")
            core.add_menu_item("Show Logger", callback=core.show_logger)
            core.end()

            core.add_menu("About")
            core.add_menu_item("Visit source page", callback=self._visit_source_page_click_callback)
            core.end()

            core.end()


    def _theme_callback(self, theme_str: str, data: None) -> None:
        """ Set application GUI theme.
        """
        core.set_theme(theme_str)

    def _visit_source_page_click_callback(self, theme_str: str, data: None) -> None:
        """ Visit project source page
        """
        visit_source_web_page()


    def _new_scan_click_callback(self, sender: str, data: None) -> None:
        """ Open the 'start scan window'
        """
        self.ShowNewScanWindow()


    def _quit_app_click_handler(self, sender: str, data: None) -> None:
        """ Terminate application
        """
        core.stop_dearpygui()


