"""
This module contains VirtualFileSystem
"""
from ImGuiCustomControls import FileSystem


class VirtualFileSystem:
    """
    This maps relative path with actual path for all files in project.
    """

    def __init__(self, rootDirectory):
        self.Root = rootDirectory

        self.BackDirectories = list()
        self.ForwardDirectories = list()

        self.CurrentDirectory = self.Root
        self.Folders = list()
        self.Files = list()
        self.RefreshContents()

    def OpenFolder(self, foldername):
        """
        Opens a Folder
        """
        if foldername in self.Folders:
            newDir = FileSystem.JoinPath(self.CurrentDirectory, foldername)

            if FileSystem.IsValidDirectory(newDir):
                self.BackDirectories.append(self.CurrentDirectory)
                self.CurrentDirectory = newDir
                self.ForwardDirectories.clear()
            self.RefreshContents()

    def RefreshContents(self):
        """
        Updates the files and folders list when CurrentDirectory changes
        """
        self.Files.clear()
        self.Folders.clear()
        contents = FileSystem.GetDirectoryContents(self.CurrentDirectory)
        for item in contents:
            if FileSystem.IsValidFile(item):
                self.Files.append(FileSystem.GetFileNameWithExtension(item))
            elif FileSystem.IsValidDirectory(item):
                self.Folders.append(FileSystem.GetDirectoryName(item))

    def Back(self):
        """
        Moves back a directory
        """
        if len(self.BackDirectories) == 0:
            return
        self.ForwardDirectories.append(self.CurrentDirectory)
        self.CurrentDirectory = self.BackDirectories.pop()
        self.RefreshContents()

    def Forward(self):
        """
        Moves ahead a directory
        """
        if len(self.ForwardDirectories) == 0:
            return
        self.BackDirectories.append(self.CurrentDirectory)
        self.CurrentDirectory = self.ForwardDirectories.pop()
        self.RefreshContents()
