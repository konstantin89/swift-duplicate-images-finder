from dearpygui import core, simple

class StartNewScanWindowView:

    def __init__(self, 
        height: int, 
        width:  int,
        x_pos:  int,
        y_pos:  int,
        start_scan_callback: callable):

        self._window_name: str = 'Start new scan window'

        self._scan_directories: [str] = []

        self._start_scan_callback: callable = start_scan_callback

        # RGB color of special text
        self._control_text_color = [0, 200, 255]

        with simple.window(self._window_name):
            core.configure_item(
                self._window_name,
                    width=width,
                    height=height,
                    x_pos=x_pos,
                    y_pos=y_pos,
                    label='Results')



    def ShowWindow(self):

        simple.show_item(self._window_name)

        self._render_start_scan_window()


    def HideWindow(self):

        simple.hide_item(self._window_name)



    def _remove_scan_dir_click_handler(self, sender, scan_dir: str):

        core.log_debug('View: Removing dir [%s] from scan' % (scan_dir))

        self._scan_directories.remove(scan_dir)
        self._render_start_scan_window()


    def _render_start_scan_window(self):
        
        core.delete_item(item=self._window_name, children_only=True)

        core.add_text('Please choose directories to scan.', parent=self._window_name)
        core.add_text('Press \'Start Scan\' to run duplicate images search.', parent=self._window_name)

        core.add_text( '',  parent=self._window_name)
        core.add_separator(parent=self._window_name)

        core.add_button(
            'Add Scan Directory', 
            callback=self._add_scan_directory_callback,
            parent=self._window_name)

        core.add_text('', parent=self._window_name)

        core.add_text('Folders to scan', parent=self._window_name)

        if not self._scan_directories:
            core.add_text('No directories chosen', 
            parent=self._window_name,
            color=[249, 19, 19])

        for scan_directory in self._scan_directories:

            core.add_button(
                name='Remove ##'+scan_directory, 
                parent=self._window_name,
                callback=self._remove_scan_dir_click_handler,
                callback_data=scan_directory)

            core.add_same_line(
                parent=self._window_name)

            core.add_text(
                name=scan_directory, 
                parent=self._window_name)


        core.add_separator(parent=self._window_name)

        
        core.add_text( '',  parent=self._window_name)

        core.add_button(
            'Start Scan', 
            callback=self._start_scan_click_handler, 
            callback_data=self._scan_directories,
            parent=self._window_name)


    def _add_scan_directory_callback(self, sender: str, data: str) -> None:
        """ Click callback for add scan directory button
        """
        core.open_file_dialog(callback=self._handle_selected_scan_path, extensions=".*")      


    def _handle_selected_scan_path(self, sender: str, data: [str]) -> None:
        """ Callback for scan directory selector
            data[0] contains chosen directory.
            data[0] contains chosen file.
        """

        directory = data[0]

        if directory in self._scan_directories:
            return

        self._scan_directories.append(directory)

        self._render_start_scan_window()

        
    def _start_scan_click_handler(self, sender: str, scan_directories: [str]) -> None:
        """ Click callback for start scan button
        """

        if len(scan_directories) == 0:
            core.log_error('View: - scan dirs list is empty')
            return

        core.log_debug('View: Starting scan on dirs: %s' % self._scan_directories)

        self._start_scan_callback(self._scan_directories)

