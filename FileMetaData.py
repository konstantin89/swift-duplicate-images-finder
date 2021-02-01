from typing import NewType


class FileMetaData:

    def __init__(self, path: str, size: int, last_edit_time: float):
        self.path = path
        self.size = size
        self.last_edit_time = last_edit_time

    def GetSize(self):
        return self.size

    def GetPath(self):
        return self.path

    def GetLastEditTime(self):
        return self.last_edit_time

FileMetaDataList = NewType('FileMetaDataList', [FileMetaData])
