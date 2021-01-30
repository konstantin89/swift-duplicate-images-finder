
from DuplicateImagesManager import DuplicateImagesManager
from View import View


class DuplicateImagesController:

    def __init__(self):

        supported_image_formats = ('.png', '.jpg', '.jpeg', '.bmp', '.gif')


        start_scan_callback = lambda scan_directories: self._start_scan_click_callback(scan_directories)
        delete_image_callback = lambda path_to_delete: print('Delete callback for [%s]' % path_to_delete)

        self._view = View(start_scan_callback, delete_image_callback)
        self._imageManager = DuplicateImagesManager(supported_image_formats)


    def Start(self):

        self._view.Init()

        

    def _start_scan_click_callback(self, scan_directories):

        self._view.ShowScanInProgressWindow()

        self._imageManager.ScanDirectories(scan_directories)

        self._view.HideScanInProgressWindow()       

        
        duplicates = self._imageManager.GetDuplicates()

        print (duplicates)

        self._view.ShowResultsWindows(duplicates)



