# Standard library imports
import os 
from datetime import datetime

# Third party imports
from dearpygui import core

# Local application imports
from DuplicateImagesManager import DuplicateImagesManager
from MainView import MainView
from FileMetaData import FileMetaDataList
from core_values_names import SCAN_DURATION_IN_SECS


class DuplicateImagesController:
    """ Controller for 'Duplicate image finder' application.
        Implements the 'Controller' from MVC design pattern.
    """

    def __init__(self):

        supported_image_formats = ('.png', '.jpg', '.jpeg', '.bmp', '.gif')

        start_scan_callback = lambda scan_directories: self._start_scan_click_callback(scan_directories)
        delete_image_callback = lambda path_to_delete: self._delete_file(path_to_delete)
        delete_all_duplicates = lambda duplicates: self._delete_all_duplicated_keep_newest(duplicates)

        self._main_view = MainView(
            start_scan_callback, 
            delete_image_callback, 
            delete_all_duplicates)

        self._imageManager = DuplicateImagesManager(supported_image_formats)


    def Start(self) -> None:

        self._main_view.Init()


    def _start_scan_click_callback(self, scan_directories: [str]) -> None:
        """ Handler method for click on 'start scan' button.
        """

        core.log_debug('DuplicateImagesController - starting scan on dirs [%s]' % (scan_directories))

        self._main_view.ShowScanInProgressWindow()

        scan_start_time = datetime.now()

        self._imageManager.CleanResults()
        self._imageManager.ScanDirectories(scan_directories)
        duplicates = self._imageManager.GetDuplicates()

        scan_end_time = datetime.now()

        scan_duration_in_secs = (scan_end_time-scan_start_time).total_seconds()

        core.log_debug('DuplicateImagesController - Scan duration in secs is [%d]' % scan_duration_in_secs)

        self._main_view.ShowResultsWindows(duplicates)


    def _delete_file(self, file_path):

        try:
            core.log_debug('DuplicateImagesController - deleting file [%s]' % (file_path))
            os.remove(file_path)

        except Exception as e:
            core.log_error('DuplicateImagesController - delete file  [%s] failed with exception [%s]' 
                % (file_path, e))


    def _delete_all_duplicated_keep_newest(self, duplicates: FileMetaDataList) -> FileMetaDataList:

        updated_duplicate_list = []
        
        for duplicate_file_list in duplicates:
            newest_file = self._get_newest_file(duplicate_file_list)

            for file in duplicate_file_list:
                if file.GetPath() == newest_file.GetPath():
                    continue
                else:
                    self._delete_file(file.GetPath())

            updated_duplicate_list.append([newest_file])
        
        return updated_duplicate_list
    
    def _get_newest_file(self, files: FileMetaDataList):
        return max(files, key=lambda file: file.GetLastEditTime())