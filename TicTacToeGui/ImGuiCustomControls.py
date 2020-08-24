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
    def GetParentDirectory(path):
        absPath = FileSystem.GetAbsolutePath(path)
        return os.path.dirname(absPath)

    @staticmethod
    def IsValidFile(path):
        return os.path.exists(path) and os.path.isfile(path)

    @staticmethod
    def IsValidDirectory(directory):
        return os.path.exists(directory) and os.path.isdir(directory)

    @staticmethod
    def GetFileExtension(filepath):
        return os.path.splitext(filepath)[1]

    @staticmethod
    def DeleteFile(filepath):
        if not FileSystem.IsValidFile(filepath):
            raise Exception("File does not exist in the directory")
        os.remove(filepath)


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


class ConfirmationBox:
    TITLE = "CONFIRMATION BOX"
    MESSAGE = ""

    @staticmethod
    def DrawConfirmationBox():
        selection = None
        popupFlags = imgui.WINDOW_NO_SCROLLBAR | imgui.WINDOW_NO_RESIZE
        if imgui.begin_popup_modal(ConfirmationBox.TITLE, None, popupFlags)[0] and not ConfirmationBox.MESSAGE == "":
            imgui.text_wrapped(ConfirmationBox.MESSAGE)

            offsetX = imgui.get_window_width() - BUTTON_WIDTH
            imgui.set_cursor_pos_x(offsetX/2)

            offsetY = imgui.get_window_height() - BUTTON_HEIGHT - 5
            imgui.set_cursor_pos_y(offsetY)

            if imgui.button("Yes", BUTTON_WIDTH, BUTTON_HEIGHT):
                selection = True
                ConfirmationBox.__disposeDialog()

            imgui.same_line(spacing=30)

            if imgui.button("No", BUTTON_WIDTH, BUTTON_HEIGHT):
                selection = False
                ConfirmationBox.__disposeDialog()
            imgui.end_popup()
        return selection

    @staticmethod
    def ShowConfirmationBox(title, message):
        ConfirmationBox.TITLE = title
        ConfirmationBox.MESSAGE = message
        imgui.open_popup(ConfirmationBox.TITLE)
        imgui.set_next_window_size(300, 150)

    @staticmethod
    def __disposeDialog():
        ConfirmationBox.TITLE = "CONFIRMATION BOX"
        ConfirmationBox.MESSAGE = ""
        imgui.close_current_popup()


class InputTextControl:
    def __init__(self, textLabel: str, btnLabels: tuple = None, btnEvents: tuple = None):
        self.Text = ""
        self.TextLabel = textLabel
        self.Reset()
        if btnEvents:
            self.ButtonOneClickEvent = btnEvents[0]
            self.ButtonTwoClickEvent = btnEvents[1]

        if btnLabels:
            self.ButtonOneLabel = btnLabels[0]
            self.ButtonTwoLabel = btnLabels[1]

    def Reset(self):
        self.Text = ""
        self.ButtonOneClickEvent = None
        self.ButtonTwoClickEvent = None

    def SetEvents(self, eventOne=None, eventTwo=None):
        self.ButtonOneClickEvent = eventOne
        self.ButtonTwoClickEvent = eventTwo

    def DrawControl(self):
        imgui.text(self.TextLabel)
        imgui.push_item_width(-1)
        _, self.Text = imgui.input_text("", self.Text, 256)
        imgui.pop_item_width()

        offset = imgui.get_window_width() - 2 * BUTTON_WIDTH - 20
        imgui.set_cursor_pos_x(offset)

        if imgui.button(self.ButtonOneLabel, BUTTON_WIDTH, BUTTON_HEIGHT):
            if self.ButtonOneClickEvent:
                self.ButtonOneClickEvent()

        imgui.same_line()

        if imgui.button(self.ButtonTwoLabel, BUTTON_WIDTH, BUTTON_HEIGHT):
            if self.ButtonTwoClickEvent:
                self.ButtonTwoClickEvent()


class OpenFileDialog:
    """
    Custom control handling Opening of a file.
    """
    OnOpenEvent = None
    OnCloseEvent = None
    InputControl = None

    @staticmethod
    def OnOpen():
        filepath = OpenFileDialog.InputControl.Text
        if not FileSystem.IsValidFile(filepath):
            MessageBox.ShowMessageBox(
                "FILE ERROR", "The path for file is invalid.")
        else:
            OpenFileDialog.OnOpenEvent(filepath)
            OpenFileDialog.__disposeDialog()

    @staticmethod
    def OnClose():
        if OpenFileDialog.OnCloseEvent:
            OpenFileDialog.OnCloseEvent()
        OpenFileDialog.__disposeDialog()

    @staticmethod
    def __disposeDialog():
        OpenFileDialog.InputControl.Reset()
        imgui.close_current_popup()

    @staticmethod
    def ShowDialog(onOpen, onClose=None):
        OpenFileDialog.OnOpenEvent = onOpen
        OpenFileDialog.OnCloseEvent = onClose
        if OpenFileDialog.InputControl is None:
            OpenFileDialog.InputControl = InputTextControl(
                "Filepath", ("OPEN", "CANCEL"))
        OpenFileDialog.InputControl.SetEvents(
            OpenFileDialog.OnOpen, OpenFileDialog.OnClose)
        imgui.open_popup("Open File")
        imgui.set_next_window_size(400, 100)

    @staticmethod
    def DrawDialog():
        popupFlags = imgui.WINDOW_NO_SCROLLBAR | imgui.WINDOW_NO_RESIZE
        if imgui.begin_popup_modal("Open File", None, popupFlags)[0]:
            OpenFileDialog.InputControl.DrawControl()
            MessageBox.DrawMessageBox()
            imgui.end_popup()


class SaveFileDialog:
    """
    Custom control handling Saving of a file.
    """
    OnSaveEvent = None
    OnCloseEvent = None
    InputControl = None
    Confirm = False
    Message = False
    @staticmethod
    def OnSave():
        filepath = SaveFileDialog.InputControl.Text
        parentDir = FileSystem.GetParentDirectory(filepath)
        if not FileSystem.IsValidDirectory(parentDir):
            SaveFileDialog.Message = True
        if FileSystem.IsValidFile(filepath):
            SaveFileDialog.Confirm = True
        else:
            SaveFileDialog.OnSaveEvent(filepath)
            SaveFileDialog.__disposeDialog()

    @staticmethod
    def OnClose():
        if SaveFileDialog.OnCloseEvent:
            SaveFileDialog.OnCloseEvent()
        SaveFileDialog.__disposeDialog()

    @staticmethod
    def __disposeDialog():
        SaveFileDialog.InputControl.Reset()
        imgui.close_current_popup()

    @staticmethod
    def ShowDialog(onSave: callable, onClose: callable = None, DefaultFile: str = ""):
        SaveFileDialog.OnSaveEvent = onSave
        SaveFileDialog.OnCloseEvent = onClose

        if SaveFileDialog.InputControl is None:
            SaveFileDialog.InputControl = InputTextControl(
                "Filepath", ("SAVE", "CANCEL"))
        SaveFileDialog.InputControl.Text = DefaultFile
        SaveFileDialog.InputControl.SetEvents(
            SaveFileDialog.OnSave, SaveFileDialog.OnClose)

        imgui.open_popup("Save File")
        imgui.set_next_window_size(400, 100)

    @staticmethod
    def DrawDialog():
        popupFlags = imgui.WINDOW_NO_SCROLLBAR | imgui.WINDOW_NO_RESIZE
        if imgui.begin_popup_modal("Save File", None, popupFlags)[0]:
            SaveFileDialog.InputControl.DrawControl()

            if SaveFileDialog.Message:
                MessageBox.ShowMessageBox(
                    "FILE ERROR", "The path for file is invalid.")
            SaveFileDialog.Message = False
            MessageBox.DrawMessageBox()

            if SaveFileDialog.Confirm:
                msg = "The file with the same name already exist. Do you want to overwrite ?"
                ConfirmationBox.ShowConfirmationBox("File Exists", msg)
            SaveFileDialog.Confirm = False
            selection = ConfirmationBox.DrawConfirmationBox()

            if selection:
                filepath = SaveFileDialog.InputControl.Text
                FileSystem.DeleteFile(filepath)
                imgui.close_current_popup()

            imgui.end_popup()