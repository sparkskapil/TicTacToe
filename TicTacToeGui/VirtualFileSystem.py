"""
This module contains VirtualFileSystem
"""
import os
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

    def OpenFolder(self, folderName):
        if folderName in self.Folders:
            newDir= FileSystem.JoinPath(self.CurrentDirectory, folderName)
            
            if FileSystem.IsValidDirectory(newDir):
                self.BackDirectories.append(self.CurrentDirectory)
                self.CurrentDirectory = newDir
                self.ForwardDirectories.clear()
            self.RefreshContents()

    def RefreshContents(self):
        contents = FileSystem.GetDirectoryContents(self.CurrentDirectory)
        for item in contents:
            if FileSystem.IsValidFile(item):
                self.Files.append(FileSystem.GetFileNameWithExtension(item))
            elif FileSystem.IsValidDirectory(item):
                self.Folders.append(FileSystem.GetDirectoryName(item))
    
    def Back(self):
        if not len(self.BackDirectories):
            return
        self.ForwardDirectories.append(self.CurrentDirectory)
        self.CurrentDirectory = self.BackDirectories.pop()
        self.RefreshContents()

    def Forward(self):
        if not len(self.ForwardDirectories):
            return
        self.BackDirectories.append(self.CurrentDirectory)
        self.CurrentDirectory = self.ForwardDirectories.pop()
        self.RefreshContents()
            
