"""
This module contains custom reusable imgui controls.
"""
import os
import imgui


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
        if not os.path.exists(directory):
            raise ValueError("The directory does not exist.")
        if not os.path.isdir(directory):
            raise ValueError(
                "Parameter for directory is not an actual directory.")
        contents = os.listdir(directory)
        return contents

    @staticmethod
    def CreateDirectory(path):
        absolutePath = FileSystem.GetAbsolutePath(path)
        os.mkdir(absolutePath)
        return absolutePath

    @staticmethod
    def GetAbsolutePath(path):
        return os.path.abspath(path)


class OpenFileDialog:
    """
    Open file dialog static class.
    """
    SelectedFile = ""
    OnOpen = None
    OnClose = None

    @staticmethod
    def __disposeDialog():
        OpenFileDialog.OnOpen = None
        OpenFileDialog.OnClose = None
        OpenFileDialog.SelectedFile = ""
        imgui.close_current_popup()

    @staticmethod
    def ShowDialog(onOpen, onClose=None):
        OpenFileDialog.OnOpen = onOpen
        OpenFileDialog.OnClose = onClose
        imgui.open_popup("Open File")

    @staticmethod
    def DrawDialog():
        if imgui.begin_popup_modal("Open File")[0]:
            _, OpenFileDialog.SelectedFile = imgui.input_text(
                "Filepath", OpenFileDialog.SelectedFile, 256)

            if imgui.button("Open"):
                OpenFileDialog.OnOpen(OpenFileDialog.SelectedFile)
                OpenFileDialog.__disposeDialog()

            imgui.same_line()

            if imgui.button("Close"):
                if not OpenFileDialog.OnClose is None:
                    OpenFileDialog.OnClose()
                OpenFileDialog.__disposeDialog()
            imgui.end_popup()
