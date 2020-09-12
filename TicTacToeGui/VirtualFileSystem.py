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

    def CreateFolder(self, foldername):
        """
        Creates a folder with specified name in the current directory
        """
        folderToCreate = FileSystem.JoinPath(self.CurrentDirectory, foldername)
        if FileSystem.IsValidDirectory(folderToCreate) or FileSystem.IsValidFile(folderToCreate):
            raise Exception("File or Folder with same name already exists.")
        FileSystem.CreateDirectory(folderToCreate)
        self.RefreshContents()

    def ImportSprite(self, sprite_path):
        """
        Imports image/sprite files to the current directory after validating
        """
        supportedFormats = ('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')
        if not sprite_path.lower().endswith(supportedFormats):
            raise Exception("The selected sprite format is not supported.")
        self.__importFileToCurrentDirectory(sprite_path)

    def ImportFont(self, font_path):
        """
        Imports font files to the current directory after validating
        """
        supportedFormats = ('.otf', '.ttf', '.fnt')
        if not font_path.lower().endswith(supportedFormats):
            raise Exception("The selected font is not supported.")
        self.__importFileToCurrentDirectory(font_path)

    def ImportScript(self, script_path):
        """
        Imports python script files to the current directory after validating
        """
        supportedFormats = ('.py')
        if not script_path.lower().endswith(supportedFormats):
            raise Exception("The selected file is not a python file.")
        self.__importFileToCurrentDirectory(script_path)

    def ImportScene(self, scene_path):
        """
        Imports ProtoTypeEngine Scene files to the current directory after validating
        """
        supportedFormats = ('.pts')
        if not scene_path.lower().endswith(supportedFormats):
            raise Exception("The selected file is not a scene.")
        self.__importFileToCurrentDirectory(scene_path)

    def __importFileToCurrentDirectory(self, path):
        """
        Import specified file to the current directory
        """
        if not FileSystem.IsValidFile(path):
            raise Exception("The selected file is invalid.")
        fileName = FileSystem.GetFileNameWithExtension(path)
        importFilePath = FileSystem.JoinPath(self.CurrentDirectory, fileName)

        if FileSystem.IsValidFile(importFilePath):
            raise Exception(
                "File with same name already exist in the directory")
        FileSystem.CopyFile(path, importFilePath)
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
