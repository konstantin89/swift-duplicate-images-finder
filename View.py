from typing import Callable

from dearpygui import core, simple

from FileMetaData import FileMetaDataList
from FileMetaData import FileMetaData

class View:
    """ View class of the MVC (Model View Controller) design pattern.
        This class implements all GUI related logic.
    """

    def __init__(self, 
        start_scan_callback: Callable, 
        delete_image_callback: Callable,
        delete_all_duplicates_callback: Callable):

        self._scan_directories: [str] = []   
        self._duplicates_list: [FileMetaDataList] = []     

        self._primary_window_name: str          = 'Duplicate Image Manager'
        self._new_scan_window_name: str         = 'Start New Scan'
        self._scan_in_progress_window_name: str = 'Scan in progress'
        self._results_window_name: str          = 'Results'

        self._start_scan_callback: Callable            = start_scan_callback
        self._delete_image_callback: Callable          = delete_image_callback
        self._delete_all_duplicates_callback: Callable = delete_all_duplicates_callback

        self._app_windows_size = {}
        self._app_windows_size['width'] = 1280
        self._app_windows_size['height'] = 780

        # RGB color of special text
        self._control_text_color = [0, 200, 255]


    def Init(self) -> None:

        self._create_primary_window()
        self.ShowNewScanWindow()

        core.start_dearpygui(primary_window=self._primary_window_name)


    def ShowScanInProgressWindow(self)-> None:
        simple.hide_item(self._new_scan_window_name)

        with simple.window(self._scan_in_progress_window_name):
            core.add_text('Scan in progress')


    def HideScanInProgressWindow(self) -> None:
        simple.hide_item(self._scan_in_progress_window_name)

   
    def ShowResultsWindows(self, dupicates: [FileMetaDataList]) -> None:
        
        self._duplicates_list = dupicates

        with simple.window(self._results_window_name):

            core.configure_item(
            self._results_window_name,
                width=self._app_windows_size['width'],
                height=self._app_windows_size['height'],
                x_pos=0,
                y_pos=20,
                label='Results')

            self._render_results_window()


    def ShowNewScanWindow(self) -> None:

        with simple.window(self._new_scan_window_name):

            core.configure_item(
                self._new_scan_window_name,
                    width=self._app_windows_size['width'],
                    height=self._app_windows_size['height'],
                    x_pos=0,
                    y_pos=20,
                    label='Start New Scan')

        self._render_start_scan_window()
            

    def _delete_all_duplicate_click_hander(self, sender, dupicates: [FileMetaDataList]) -> None:

        self._duplicates_list = self._delete_all_duplicates_callback(dupicates)
        self._render_results_window()
        

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

            core.end()


    def _theme_callback(self, theme_str: str, data: None) -> None:
        """ Set application GUI theme.
        """

        core.set_theme(theme_str)


    ### Results Window Logic ###

    def _delete_file_button_click_handler(self, sender: str, file_to_delete: FileMetaData) -> None:
        """ Click handler for the 'Delete File' button.
        """

        # Delete the image
        self._delete_image_callback(file_to_delete.GetPath())

        # Remove the deleted file from duplicates list
        for duplicates_set in self._duplicates_list:

            if file_to_delete in duplicates_set:
                duplicates_set.remove(file_to_delete)
                break

        self._render_results_window()


    def _draw_duplicates_set(self, duplicate_images_list: FileMetaDataList) -> None:
        """ Draw a single image and all the files containing it.
            All the files in duplicate_images_list containg duplicate of same image.
        """
        
        try:

            file_path = duplicate_images_list[0].GetPath()

            core.add_drawing(
                file_path, 
                width=100, 
                height=100, 
                parent=self._results_window_name)

            core.draw_image(
                file_path, 
                file_path, 
                [0, 0], 
                pmax=[100, 100],
                uv_min=[0, 0], 
                uv_max=[1, 1], 
                tag="image")

            for file in duplicate_images_list:
                
                file_path = file.GetPath()

                core.add_button(
                    'Delete ##'+file_path, 
                    callback=self._delete_file_button_click_handler, 
                    callback_data=file,
                    parent=self._results_window_name)

                core.add_same_line(parent=self._results_window_name)

                core.add_text(
                file_path, 
                parent=self._results_window_name)

            core.add_separator(parent=self._results_window_name)

        except Exception as e:
            core.log_error('View::_draw_duplicates_set - Exception : [%s]' % (e))
        

    def _render_results_window(self) -> None:

        core.delete_item(item=self._results_window_name, children_only=True)

        core.add_text(
            name='Group operations',
            color=self._control_text_color,
            parent=self._results_window_name)

        core.add_button(
                'Delete all duplicates, keep newest file', 
                callback=self._delete_all_duplicate_click_hander,
                callback_data=self._duplicates_list,
                parent=self._results_window_name)

        core.add_separator(parent=self._results_window_name)

        core.add_text(
            'Results', 
            color=self._control_text_color,
            parent=self._results_window_name)


        for dupicate_image in self._duplicates_list:

            self._draw_duplicates_set(dupicate_image)       



    ### Start Scan Window ###

    def _remove_scan_dir_click_handler(self, sender, scan_dir: str):

        core.log_debug('View: Removing dir [%s] from scan' % (scan_dir))

        self._scan_directories.remove(scan_dir)
        self._render_start_scan_window()


    def _render_start_scan_window(self):
        
        core.delete_item(item=self._new_scan_window_name, children_only=True)

        core.add_button(
            'Start Scan', 
            callback=self._start_scan_click_handler, 
            callback_data=self._scan_directories,
            parent=self._new_scan_window_name)

        core.add_same_line(parent=self._new_scan_window_name)

        core.add_button(
            'Add Scan Directory', 
            callback=self._add_scan_directory_callback,
            parent=self._new_scan_window_name)

        core.add_text('', parent=self._new_scan_window_name)

        core.add_text('Folders to scan', parent=self._new_scan_window_name)

        for scan_directory in self._scan_directories:

            core.add_button(
                name='Remove ##'+scan_directory, 
                parent=self._new_scan_window_name,
                callback=self._remove_scan_dir_click_handler,
                callback_data=scan_directory)

            core.add_same_line(
                parent=self._new_scan_window_name)

            core.add_text(
                name=scan_directory, 
                parent=self._new_scan_window_name)


    def _add_scan_directory_callback(self, sender, data):

        core.open_file_dialog(callback=self._handle_selected_scan_path, extensions=".*")      


    def _handle_selected_scan_path(self, sender, data):
        directory = data[0]

        if directory in self._scan_directories:
            return

        self._scan_directories.append(directory)

        self._render_start_scan_window()

        
    def _start_scan_click_handler(self, sender, scan_directories):

        if len(scan_directories) == 0:
            core.log_error('View: - scan dirs list is empty')
            return

        core.log_debug('View: Starting scan on dirs: %s' % self._scan_directories)

        self._start_scan_callback(self._scan_directories)

