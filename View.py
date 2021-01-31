from typing import Callable


from dearpygui import core, simple

from FileMetaData import FileMetaDataList

class View:

    def __init__(self, 
        start_scan_callback: Callable, 
        delete_image_callback: Callable,
        delete_all_duplicates_callback: Callable):

        self._scan_directories = []        

        self._primary_window_name = 'Duplicate Image Manager'
        self._new_scan_window_name = 'Start New Scan'
        self._scan_in_progress_window_name = 'Scan in progress'
        self._results_window_name = 'Results'

        self._start_scan_callback = start_scan_callback
        self._delete_image_callback = delete_image_callback
        self._delete_all_duplicates_callback = delete_all_duplicates_callback

        self._app_windows_size = {}
        self._app_windows_size['width'] = 1280
        self._app_windows_size['height'] = 780

        self._control_text_color=[0, 200, 255]


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

   
    def ShowResultsWindows(self, dupicates: [[str]]) -> None:
        
        with simple.window(self._results_window_name):

            core.configure_item(
            self._results_window_name,
                width=self._app_windows_size['width'],
                height=self._app_windows_size['height'],
                x_pos=0,
                y_pos=20,
                label='Results')


            core.add_text(
                name='Group operations',
                color=self._control_text_color)

            core.add_button(
                    'Delete all duplicates, keep newest file', 
                    callback=self._delete_all_duplicate_click_hander,
                    callback_data=dupicates)

            core.add_separator()

            core.add_text(
                'Results', 
                color=self._control_text_color)


            for dupicate_image in dupicates:

               self._draw_duplicates_set(dupicate_image)


    def ShowNewScanWindow(self) -> None:

        with simple.window(self._new_scan_window_name):

            core.configure_item(
                self._new_scan_window_name,
                    width=self._app_windows_size['width'],
                    height=self._app_windows_size['height'],
                    x_pos=0,
                    y_pos=20,
                    label='Start New Scan')

        self._update_start_scan_window()
            

    def _delete_all_duplicate_click_hander(self, sender, dupicates: [FileMetaDataList]) -> None:
        self._delete_all_duplicates_callback(dupicates)
        

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



    def _theme_callback(self, sender, data: str) -> None:
        core.set_theme(sender)


    ## Results Window

    def _delete_file_button_click_handler(self, sender, file_path: str) -> None:

        self._delete_image_callback(file_path)


    def _draw_duplicates_set(self, duplicate_images_list: FileMetaDataList) -> None:
        
        try:

            file_path = duplicate_images_list[0].GetPath()

            core.add_drawing(file_path, width=100, height=100)

            core.draw_image(file_path, file_path, 
                    [0, 0], pmax=[100, 100], uv_min=[0, 0], uv_max=[1, 1], tag="image")

            for file in duplicate_images_list:
                
                file_path = file.GetPath()

                core.add_button(
                    'Delete ##' +file_path, 
                    callback=self._delete_file_button_click_handler, 
                    callback_data=file_path)

                core.add_same_line()
                core.add_text(file_path)

            core.add_separator()


        except Exception as e:
            core.log_error('View::_draw_duplicates_set - Exception : [%s]' % (e))
        



    ## Start Scan Window

    def _remove_scan_dir_click_handler(self, sender, scan_dir):

        print(scan_dir)

        self._scan_directories.remove(scan_dir)

        self._update_start_scan_window()


    def _update_start_scan_window(self):
        
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

        self._update_start_scan_window()

        
    def _start_scan_click_handler(self, sender, scan_directories):

        if len(scan_directories) == 0:
            core.log_error('View: - scan dirs list is empty')
            return

        core.log_debug('View: Starting scan on dirs: %s' % self._scan_directories)

        self._start_scan_callback(self._scan_directories)

