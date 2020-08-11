"""
This module contains custom reusable imgui controls.
"""
import os
#import imgui


class FileSystem:
    """
    This class has all static methods to interact with windows filesystem.
    """
    @staticmethod
    def GetCurrentDirectory():
        """
        Returns current working directory.
        """
        return os.getcwd()

    @staticmethod
    def GetDirectoryContents(directory):
        """
        Returns contents of the specified directory.
        """
        if not os.exists(directory):
            raise ValueError("The directory does not exist.")
        if not os.isdir(directory):
            raise ValueError("Parameter for directory is not an actual directory.")
        contents = os.listdir(directory)
        return contents
    
    @staticmethod
    def GetAbsolutePath(path):
        return os.path.abspath(path)
        


class OpenFileDialogOptions:
    def __init__(self):
        self.Filter = None
        self.InitialDirectory = FileSystem.GetCurrentDirectory()
        self.Filename = None


def OpenFileDialog():
    """
    -------------------------------------
    | Open File                         |
    -------------------------------------
    |PWD    _______________________     |
    |-----------------------------------|
    |                                   |
    |                                   |
    |                                   |
    |                                   |
    |                                   |
    |                                   |
    |                                   |
    -------------------------------------
    | _______________________ FILE      |
    |                     OPEN  CANCEL  |
    -------------------------------------
    """

if __name__ == "__main__":
    pwd = FileSystem.GetCurrentDirectory()
    FileSystem.GetDirectoryContents(pwd)
