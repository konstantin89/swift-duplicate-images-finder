class FileMetaData:

    def __init__(self, path, size):
        self.path = path
        self.size = size

    def GetSize(self):
        return self.size

    def GetPath(self):
        return self.path
