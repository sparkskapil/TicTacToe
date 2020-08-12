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

    @staticmethod
    def IsValidFile(path):
        return os.path.exists(path) and os.path.isfile(path)


BUTTON_WIDTH = 50
BUTTON_HEIGHT = 25


class MessageBox:
    TITLE = "MESSAGE BOX"
    MESSAGE = ""

    @staticmethod
    def DrawMessageBox():
        popupFlags = imgui.WINDOW_NO_SCROLLBAR | imgui.WINDOW_NO_RESIZE
        if imgui.begin_popup_modal(MessageBox.TITLE, None, popupFlags)[0] and not MessageBox.MESSAGE == "":
            imgui.text_wrapped(MessageBox.MESSAGE)

            offsetX = imgui.get_window_width() - BUTTON_WIDTH
            imgui.set_cursor_pos_x(offsetX/2)

            offsetY = imgui.get_window_height() - BUTTON_HEIGHT - 5
            imgui.set_cursor_pos_y(offsetY)

            if imgui.button("OK", BUTTON_WIDTH, BUTTON_HEIGHT):
                MessageBox.__disposeDialog()
            imgui.end_popup()

    @staticmethod
    def ShowMessageBox(title, message):
        MessageBox.TITLE = title
        MessageBox.MESSAGE = message
        imgui.open_popup(MessageBox.TITLE)
        imgui.set_next_window_size(300, 150)

    @staticmethod
    def __disposeDialog():
        MessageBox.TITLE = "MESSAGE BOX"
        MessageBox.MESSAGE = ""
        imgui.close_current_popup()


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
        imgui.set_next_window_size(400, 100)

    @staticmethod
    def DrawDialog():
        popupFlags = imgui.WINDOW_NO_SCROLLBAR | imgui.WINDOW_NO_RESIZE
        if imgui.begin_popup_modal("Open File", None, popupFlags)[0]:

            imgui.text("Filepath")
            imgui.push_item_width(-1)
            _, OpenFileDialog.SelectedFile = imgui.input_text(
                "", OpenFileDialog.SelectedFile, 256)
            imgui.pop_item_width()

            offset = imgui.get_window_width() - 2 * BUTTON_WIDTH - 20
            imgui.set_cursor_pos_x(offset)
            
            if imgui.button("Open", BUTTON_WIDTH, BUTTON_HEIGHT):
                
                if not FileSystem.IsValidFile(OpenFileDialog.SelectedFile):
                    MessageBox.ShowMessageBox(
                        "FILE ERROR", "The path for file is invalid.")
                else:
                    OpenFileDialog.OnOpen(OpenFileDialog.SelectedFile)
                    OpenFileDialog.__disposeDialog()

            imgui.same_line()

            if imgui.button("Close", BUTTON_WIDTH, BUTTON_HEIGHT):
                if not OpenFileDialog.OnClose is None:
                    OpenFileDialog.OnClose()
                OpenFileDialog.__disposeDialog()
            
            MessageBox.DrawMessageBox()
            imgui.end_popup()
