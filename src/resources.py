import pathlib
import sys
import os

def get_resource_full_path(relative_path: str) -> str:
    """ Get full path of resource.
        This method supports both in pyinstaller run enviroment and python dev run.
    """

    relative_path_obj = pathlib.Path(relative_path)

    development_base_path = pathlib.Path(__file__).resolve().parent.parent

    # _MEIPASS is pyinstaller run time directory. development_base_path is default value.
    base_path = getattr(sys, '_MEIPASS', development_base_path)

    return os.path.join(base_path, relative_path_obj)