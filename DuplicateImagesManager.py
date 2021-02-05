from dearpygui import core, simple

from os import walk
from os import stat
from os import path

from typing import TypedDict
from typing import Tuple

import hashlib

from dearpygui import core
from FileMetaData import FileMetaData
from FileMetaData import FileMetaDataList


class ScannedFilesDict(TypedDict):
    """ Dictionary that maintains all the scanned files.
        The key is the hash, and the value is list of files.
        Two same files will have same hash, so they will be 
        placed in same files list. 
    """
    hash_value: str
    files:FileMetaDataList

class DuplicateImagesManager:

    def __init__(self, supported_image_formats):
        """ Param supported_image_formats - Tuple of file types supported by scan.
            Example calue: ('.gif', '.png')
        """

        self.supported_image_formats = supported_image_formats

        self._number_of_scanned_images: int = 0

        # Dictionary of file_hash -> list of files with this hash.
        self.files_dict: ScannedFilesDict = {}

        # Each element of this list is list of duplicate files.
        self.duplicate_files: [FileMetaDataList] = []



    def CleanResults(self):
        """ Clear the results of previous scan.
        """
        self.files_dict.clear()
        self.duplicate_files.clear()
        self._number_of_scanned_images = 0


    def ScanDirectories(self, scan_roots):

        if not scan_roots:
            core.log_warning('ScanDirectories - paths list es empty')
            return []

        
        scan_roots = self._remove_duplicated_paths(scan_roots)

        for scan_root in scan_roots:
            core.log_debug('ScanDirectories - starting scan in [%s]' % (scan_root))
            self._scan_path(scan_root)


    def GetDuplicates(self) -> [FileMetaDataList]:

        duplicates = []

        for files in self.files_dict.values():

            if(len(files) > 1):
               duplicates = duplicates + self._handle_duplicate_candidates(files)
            
        return duplicates


    def _remove_duplicated_paths(self, original_path_list):
        """ Remove from list directories that are subdirectories of other 
            dirs in the list.

            For example: If the request list is ['C:\\', C:\\files],  
            C:\\files should be removed.

            This prevents multiple scannings of same directories.
        """

        sorted_path_list = sorted(original_path_list, key=len)

        for i in range(0, len(sorted_path_list)):
            for j in range(i+1, len(sorted_path_list)):
                
                if sorted_path_list[j].startswith(sorted_path_list[i]):
                    core.log_debug('DuplicateImagesManager - Skipping path [%s]' % (sorted_path_list[i]))
                    sorted_path_list.remove(sorted_path_list[i])
             
        return sorted_path_list


    def _scan_path(self, scan_root):

        if not scan_root:
            core.log_warning('DuplicateImagesManager - path is empty')
            return

        
        for (dirpath, dirnames, filenames) in walk(scan_root):

            for file_name in filenames:

                full_file_name =  path.join(dirpath, file_name)

                if(self._is_file_an_image(full_file_name)):  
                    self._handle_image_file(full_file_name)


    def _handle_image_file(self, file_path):

            try:
                self._number_of_scanned_images += 1

                core.set_value('number_of_scanned_images', self._number_of_scanned_images)

                stat_return_value = stat(file_path)

                file_size = stat_return_value.st_size
                last_edit_time = stat_return_value.st_mtime

                file_content = self._read_binary_file(file_path, 1024)

                hash_value = self._calc_hash(file_content)

                if hash_value in self.files_dict:
                     self.files_dict[hash_value].append(FileMetaData(file_path, file_size, last_edit_time))
                else:
                    self.files_dict[hash_value] = [FileMetaData(file_path, file_size, last_edit_time)]

            except Exception as e:
                print('Failed to handle file [%s] with exception: [%s]' % (file_path, e))


    def _is_file_an_image(self, file_path):
        return file_path.lower().endswith(self.supported_image_formats)


    def _calc_hash(self, value):
        h = hashlib.sha256()
        h.update(value)
        return h.hexdigest()


    def _handle_duplicate_candidates(self, duplicates_candidates: FileMetaDataList) -> [FileMetaDataList]:
        
        if len(duplicates_candidates) <= 1:
            return []

        files_dictionaty = {}
        
        for file in duplicates_candidates:
            
            file_content = self._read_binary_file(file.GetPath(), file.GetSize())

            if len(file_content) == 0:
                continue

            hash_value = self._calc_hash(file_content)

            if hash_value in files_dictionaty:
                files_dictionaty[hash_value].append(file)
            else:
                files_dictionaty[hash_value] = [file]

        duplicate_files = []

        for hash_value, files in files_dictionaty.items():
            
            if len(files) > 1:
                duplicate_files.append(files)

        return duplicate_files


    def _read_binary_file(self, file_path, bytes_to_read):

        file_content = ''
        
        try:
            file_object = open(file_path, 'rb')
            file_content = file_object.read(bytes_to_read)
            file_object.close()

        except Exception as e:
            print('Failed to read file [%s] with exception: [%s]' % (file_path, e))

        finally:
            return file_content
