import pygame
import OpenGL.GL as gl
from imgui.integrations.pygame import PygameRenderer
import imgui
from PygameHelpers import GLHelpers, SDL_Maximize

from ECS.Components import Vector, TransformComponent, TagComponent, LabelComponent
from ECS.Components import SpriteComponent, ButtonComponent, ScriptComponent
from ECS.Systems.BoundsComputingSystem import BoundsComputingSystem

from ImGuiCustomControls import FileSystem, OpenFileDialog, SaveFileDialog, CreateProjectDialog

from ScriptInspector import ModuleInfo
from Project import Project


class Editor:
    def SetupImGUI(self, size=(800, 600)):
        '''
        Initialize IMGUI
        '''
        imgui.create_context()
        impl = PygameRenderer()

        io = imgui.get_io()
        io.display_size = size
        io = imgui.get_io()
        io.display_size = size
        self.ImGUIImpl = impl
        self.OnApplicationResize()

    def OnApplicationResize(self):
        self.WindowSize = imgui.get_io().display_size

    def updateViewPortSize(self, width, height):
        offscreenSurface = pygame.Surface((width, height))
        self.ViewPortSize = (width, height)
        self.Project.SceneManager.SetSurface(offscreenSurface)

    def __init__(self, projectPath):
        pygame.init()

        self.Texture = None
        self.WindowSize = (800, 600)

        mode = pygame.DOUBLEBUF | pygame.OPENGL | pygame.RESIZABLE

        pygame.display.set_mode(self.WindowSize, mode)
        pygame.display.set_caption("Editor")
        pygame.display.init()
        SDL_Maximize()

        self.Clock = pygame.time.Clock()
        self.SetupImGUI(self.WindowSize)
        self.BoundsRenderer = None
        self.Project = Project(projectPath)
        self.updateViewPortSize(
            int(self.WindowSize[0]), int(self.WindowSize[1]))

        self.Project.LoadProject()

        self.Running = True
        self.SelectedEntity = None

        self.ScenePosition = (0, 0)
        self.GameMode = False
        self.File = None

        self.SelectionRenderer = None
        self.Scripts = dict()

        self.ComponentsList = list()
        self.ComponentsList.append(("Add TransformComponent",
                                    lambda: self.SelectedEntity.AddComponent(TransformComponent())))
        self.ComponentsList.append(("Add TagComponent",
                                    lambda: self.SelectedEntity.AddComponent(TagComponent())))
        self.ComponentsList.append(("Add SpriteComponent",
                                    lambda: self.SelectedEntity.AddComponent(SpriteComponent())))
        self.ComponentsList.append(("Add LabelComponent",
                                    lambda: self.SelectedEntity.AddComponent(LabelComponent())))
        self.ComponentsList.append(("Add ButtonComponent",
                                    lambda: self.SelectedEntity.AddComponent(ButtonComponent())))
        self.ComponentsList.append(("Add ScriptComponent",
                                    lambda: self.SelectedEntity.AddComponent(ScriptComponent())))

    def __modifyEventRelativeToScene(self, event):
        x, y = self.ScenePosition
        if hasattr(event, 'pos'):
            event.pos = event.pos[0] - x, event.pos[1] - y
        return event

    def __imguiDrawTransformComponentComponent(self, component):
        limit = max(self.WindowSize[0], self.WindowSize[1])
        changed, values = imgui.drag_int3("POSITION", component.position.x, component.position.y,
                                          component.position.z, 1, -limit, limit)
        if changed:
            component.position = Vector(values)
        changed, values = imgui.drag_int3("ROTATION", component.rotation.x, component.rotation.y,
                                          component.rotation.z, 1, -limit, limit)
        if changed:
            component.rotation = Vector(values)

    def __imguiDrawTagComponent(self, component):
        text = component.name
        changed, text = imgui.input_text("TAGNAME", text, 100)
        if changed:
            component.name = text

    def __imguiDrawLabelComponent(self, component):
        text = component.text
        changed, text = imgui.input_text("TEXT", text, 256)
        if changed:
            component.text = text

        font = component.font
        changed, font = imgui.input_text("FONT", font, 256)
        if changed:
            component.font = font

        fontSize = component.size
        changed, fontSize = imgui.drag_int("FONTSIZE", fontSize, 1, 1, 120)
        if changed:
            component.size = fontSize

        # component.color
        foreground = tuple(map(lambda x: x/255, component.color))
        changed, foreground = imgui.color_edit3("TEXT COLOR", *foreground)
        if changed:
            component.color = tuple(map(lambda x: x*255, foreground))

        background = tuple(
            map(lambda x: x/255, (0, 0, 0, 255)))  # (0, 0, 0, 1)
        if not component.background is None:
            # component.background
            background = tuple(map(lambda x: x/255, component.background))
        changed, background = imgui.color_edit4("BG COLOR", *background)

        if changed:
            component.background = tuple(map(lambda x: x*255, background))

    def __imguiDrawSpriteComponent(self, component):
        image = component.image
        changed, image = imgui.input_text("IMAGE PATH", image, 256)
        if changed:
            component.image = image

        width = component.width
        changed, width = imgui.drag_int(
            "IMAGE WIDTH", width, 1, 0, self.WindowSize[0])
        if changed:
            component.width = width

        height = component.height
        changed, height = imgui.drag_int(
            "IMAGE HEIGHT", height, 1, 0, self.WindowSize[1])
        if changed:
            component.height = height
        modesMap = {1: "Original", 2: "Fit", 3: "RespectAspect"}
        if imgui.button("Select Sprite Mode"):
            imgui.open_popup("Sprite Mode")
        imgui.same_line()
        imgui.text(modesMap[component.mode])
        if imgui.begin_popup("Sprite Mode"):
            _, selected = imgui.selectable(
                "Original", component.mode == SpriteComponent.SpriteMode.Original)
            if selected:
                component.mode = SpriteComponent.SpriteMode.Original
            _, selected = imgui.selectable(
                "Fit", component.mode == SpriteComponent.SpriteMode.Fit)
            if selected:
                component.mode = SpriteComponent.SpriteMode.Fit
            _, selected = imgui.selectable(
                "RespectAspect", component.mode == SpriteComponent.SpriteMode.RespectAspect)
            if selected:
                component.mode = SpriteComponent.SpriteMode.RespectAspect
            imgui.end_popup()

    def __imguiDrawButtonComponent(self, component):
        # action = component.action
        # changed, action = imgui.input_text(
        #     "ONCLICK", component.GetActionName(), 256, imgui.INPUT_TEXT_READ_ONLY)
        # # if changed:
        # #     component.action = action

        # Attach OnClick Listener from Script/Scriptable entity

        width = component.width
        changed, width = imgui.drag_int(
            "BUTTON WIDTH", width, 1, 0, self.WindowSize[0])
        if changed:
            component.width = width

        height = component.height
        changed, height = imgui.drag_int(
            "BUTTON HEIGHT", height, 1, 0, self.WindowSize[1])
        if changed:
            component.height = height

        enabled = component.enabled
        imgui.text("ENABLED")
        if imgui.radio_button("True", enabled):
            enabled = True
        imgui.same_line()
        if imgui.radio_button("False", not enabled):
            enabled = False
        component.enabled = enabled

    def __imguiSetScriptInComponent(self, component, script):
        if not component.Module == "" and component.Module in self.Scripts.keys():
            self.Scripts.pop(component.Module)
        component.Module = script
        self.Scripts[script] = ModuleInfo(script)

    def __imguiDrawScriptComponent(self, component):
        module = component.Module

        if not module == "" and not module in self.Scripts.keys():
            self.Scripts[module] = ModuleInfo(module)

        if imgui.button("SELECT MODULE"):
            OpenFileDialog.ShowDialog(
                lambda x: self.__imguiSetScriptInComponent(component, x))
        OpenFileDialog.DrawDialog()

        if module in self.Scripts.keys():
            imgui.text("MODULE DIR")
            imgui.same_line(spacing=10)
            imgui.text_wrapped(self.Scripts[module].Location)
            imgui.text("MODULE NAME")
            imgui.same_line(spacing=10)
            imgui.text_wrapped(self.Scripts[module].Name)

        if module and module in self.Scripts.keys():
            scriptClass = component.Class
            classes = self.Scripts[module].GetScriptableClassesInModule()
            if not classes:
                return
            if scriptClass == "" and classes:
                scriptClass = classes[0]
            if imgui.button("SELECT CLASS"):
                imgui.open_popup("Select Scriptable Class")

            imgui.text("SCRIPTABLE CLASS NAME")
            imgui.same_line(spacing=10)
            imgui.text(scriptClass)

            if imgui.begin_popup("Select Scriptable Class"):
                for className in classes:
                    selected = scriptClass == className
                    _, selected = imgui.selectable(className, selected)
                    if selected:
                        scriptClass = className
                imgui.end_popup()
            component.Class = scriptClass

    def __imguiDrawComponent(self, component):
        compName = component.__class__.__name__
        expanded, visible = imgui.collapsing_header(compName, True)

        if expanded:
            if isinstance(component, TransformComponent):
                self.__imguiDrawTransformComponentComponent(component)

            elif isinstance(component, TagComponent):
                self.__imguiDrawTagComponent(component)

            elif isinstance(component, LabelComponent):
                self.__imguiDrawLabelComponent(component)

            elif isinstance(component, SpriteComponent):
                self.__imguiDrawSpriteComponent(component)

            elif isinstance(component, ButtonComponent):
                self.__imguiDrawButtonComponent(component)

            elif isinstance(component, ScriptComponent):
                self.__imguiDrawScriptComponent(component)

            else:
                imgui.text(component.__repr__())
                imgui.text("\n")
            return not visible

    def __imguiRemoveEntity(self, entity):
        scene = self.Project.SceneManager.GetScene()
        if not scene:
            return
        if entity:
            scene.RemoveEntity(entity)
            if self.SelectedEntity == entity:
                self.SelectedEntity = None

    def __imguiCloneEntity(self, entity):
        self.Project.SceneManager.GetScene().CloneEntity(entity)

    def __imguiDrawContextMenu(self, entity=None):
        if not self.Project.SceneManager.HasScene():
            return None
        options = list()
        options.append(("Create Entity ",
                        self.Project.SceneManager.GetScene().CreateEntity))
        if entity:
            options.append(("Remove Entity ",
                            lambda: self.__imguiRemoveEntity(entity)))
            options.append(("Clone Entity ",
                            lambda: self.__imguiCloneEntity(entity)))
            options.extend(self.ComponentsList)

        if imgui.is_window_hovered():
            if imgui.is_mouse_clicked(1) or imgui.is_mouse_released(1):
                return
            if imgui.is_mouse_released(2):
                imgui.open_popup("SceneContextMenu")

        # In pygame right mouse button is 2
        if imgui.begin_popup_context_window("SceneContextMenu"):
            for menuItem, action in options:
                if imgui.selectable(menuItem)[1]:
                    action()
            imgui.end_popup()

    def __onSaveFile(self, file):
        if not self.Project.SceneManager.HasScene():
            return None
        self.Project.SceneManager.CurrentScene.SaveScene(file)
        self.Project.SaveProject()

    def __onCreateNewScene(self, file):
        sceneName = FileSystem.GetFileName(file)
        self.Project.CreateNewScene(sceneName, file)

    def __onOpenFile(self, file):
        print(file)

    def OnEvent(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.Running = False
            if event.type == pygame.KEYDOWN and pygame.K_ESCAPE == event.key:
                self.Running = False
            self.ImGUIImpl.process_event(event)

            if self.GameMode:
                self.Project.SceneManager.Event(
                    self.__modifyEventRelativeToScene(event))

    def OnRender(self):
        if self.Project.SceneManager.HasScene():
            if self.BoundsRenderer is None:
                self.SelectionRenderer = BoundsComputingSystem(
                    self.Project.SceneManager.CurrentScene, self.Project.GetSurface())
            if self.GameMode:
                self.Project.SceneManager.Update()
            self.Project.SceneManager.Render()

            # Selection should be rendered after the scene is rendered
            if not self.GameMode and not self.SelectedEntity is None:
                self.SelectionRenderer.DrawRectForEntity(self.SelectedEntity)

    def __onCreateNewProject(self, projectName, projectDir):
        projectFile = Project.CreateNewProject(projectDir, projectName)
        self.__onOpenProjectFile(projectFile)
    
    def __onOpenProjectFile(self, projectFile):
        self.Project.ProjectFile = projectFile
        self.Project.LoadProject()
        
    def __imguiDrawProjectDialog(self):
        opened, _ = imgui.begin_popup_modal("Project Dialog")
        if opened:
            if imgui.button("Create New Project"):
                CreateProjectDialog.ShowDialog(
                    self.__onCreateNewProject, None)
            CreateProjectDialog.DrawDialog()
            
            if imgui.button("Open Existing Project"):
                OpenFileDialog.ShowDialog(self.__onOpenProjectFile, None)
            OpenFileDialog.DrawDialog()
            
            if FileSystem.IsValidFile(self.Project.ProjectFile):
                imgui.close_current_popup()
            imgui.end_popup()

        if self.Project.ProjectFile is None:
            imgui.open_popup("Project Dialog")
            self.Project.ProjectFile = ""

    def OnImGuiRender(self):
        self.OnApplicationResize()
        imgui.new_frame()
        menubarHeight = 0
        openFileDialogState = False
        saveFileDialogState = False
        createNewScene = False

        if imgui.begin_main_menu_bar():
            if imgui.begin_menu("File", True):

                clickedOpen, _ = imgui.menu_item(
                    "Open", 'Ctrl+O', False)
                if clickedOpen:
                    openFileDialogState = True

                clickedSave, _ = imgui.menu_item(
                    "Save", 'Ctrl+S', False, self.Project.SceneManager.HasScene()
                )
                if clickedSave:
                    path = self.Project.GetCurrentScene().SceneLocation
                    if path:
                        self.Project.GetCurrentScene().SaveScene(path)
                    else:
                        saveFileDialogState = True

                clickedSaveAs, _ = imgui.menu_item(
                    "Save As", 'Ctrl+Shift+S', False, self.Project.SceneManager.HasScene()
                )
                if clickedSaveAs:
                    saveFileDialogState = True

                clickedSaveProject, _ = imgui.menu_item(
                    "Save Project", None, False, self.Project.SceneManager.HasScene()
                )
                if clickedSaveProject:
                    self.Project.SaveProject()

                clickedQuit, _ = imgui.menu_item(
                    "Quit", 'Ctrl+Q', False, True
                )
                if clickedQuit:
                    self.Running = False

                imgui.end_menu()

            if imgui.begin_menu("Game", True):
                clickedRun, _ = imgui.menu_item(
                    "Run", 'Cmd+R', False, not self.GameMode
                )
                if clickedRun:
                    self.Project.SaveProject()
                    self.GameMode = True
                clickedStop, _ = imgui.menu_item(
                    "Stop", 'Cmd+T', False, self.GameMode
                )
                if clickedStop:
                    self.GameMode = False
                    self.Project.ResetScenes()
                imgui.end_menu()

            if imgui.begin_menu("Scene"):
                clickedCreateScene, _ = imgui.menu_item(
                    "Create Scene", None, False, True)
                if clickedCreateScene:
                    createNewScene = True
                    saveFileDialogState = True

                imgui.separator()

                currScene = self.Project.SceneManager.CurrentSceneName
                selectedScene = currScene
                for sceneName, scene in self.Project.SceneManager.Scenes.items():
                    selected = sceneName == currScene
                    clickedScene, _ = imgui.menu_item(
                        sceneName, None, selected, not selected)
                    if clickedScene:
                        selectedScene = sceneName
                if not selectedScene == currScene:
                    self.Project.SceneManager.SetScene(selectedScene)
                    self.SelectedEntity = None

                imgui.end_menu()
            _, menubarHeight = imgui.get_item_rect_size()
            imgui.end_main_menu_bar()

        if openFileDialogState:
            OpenFileDialog.ShowDialog(self.__onOpenFile)
        openFileDialogState = False
        OpenFileDialog.DrawDialog()

        if saveFileDialogState:
            sceneName = self.Project.SceneManager.CurrentSceneName
            if createNewScene:
                sceneName = "New Scene"
            defaultFile = FileSystem.JoinPath(
                self.Project.ProjectDir, "Scene", f"{sceneName}.pts")

            if createNewScene:
                SaveFileDialog.ShowDialog(
                    self.__onCreateNewScene, None, defaultFile)
            else:
                SaveFileDialog.ShowDialog(self.__onSaveFile, None, defaultFile)

        saveFileDialogState = False
        SaveFileDialog.DrawDialog()
        self.__imguiDrawProjectDialog()
        # Create texture from Pygame Surface
        if self.Texture:
            GLHelpers.DeleteTexture(self.Texture)
        tex, texWidth, texHeight = GLHelpers.SurfaceToTexture(
            self.Project.GetSurface())
        self.Texture = tex

        windowFlags = imgui.WINDOW_NO_RESIZE | imgui.WINDOW_NO_MOVE | imgui.WINDOW_NO_COLLAPSE

        yOffset = menubarHeight - 2
        windowWidth = self.WindowSize[0]
        windowHeight = self.WindowSize[1] - yOffset

        # Draw Left Pane
        imgui.set_next_window_position(0, yOffset)
        imgui.set_next_window_size(windowWidth*0.25, windowHeight)
        imgui.begin("Scene Hierarchy", False, windowFlags)

        self.__imguiDrawContextMenu(self.SelectedEntity)

        entityToRemove = None
        if imgui.tree_node("Scene [{}]".format(self.Project.SceneManager.CurrentSceneName)):
            scene = self.Project.SceneManager.GetScene()
            if scene:
                for entId in scene.Entities.keys():
                    _, currentlySelected = imgui.selectable(
                        "Entity {}".format(entId), self.SelectedEntity == scene.Entities[entId])

                    if imgui.is_item_hovered() and imgui.is_mouse_double_clicked():
                        entityToRemove = scene.Entities[entId]
                    elif currentlySelected and not entId == -1:
                        self.SelectedEntity = scene.Entities[entId]
            imgui.tree_pop()

        self.__imguiRemoveEntity(entityToRemove)
        imgui.end()

        # Draw ViewPort
        imgui.set_next_window_position(windowWidth*0.25, yOffset)
        imgui.set_next_window_size(windowWidth*0.50, windowHeight)
        imgui.begin("Viewport", False, windowFlags)
        winWidth, winHeight = imgui.get_window_size()
        self.ScenePosition = windowWidth*0.25 + \
            (winWidth - texWidth)/2, yOffset + (winHeight - texHeight)/2
        imgui.set_cursor_pos_x(self.ScenePosition[0] - windowWidth*0.25)
        imgui.set_cursor_pos_y(self.ScenePosition[1] - yOffset)

        imgui.image(tex, texWidth, texHeight)
        imgui.end()

        # Draw Right Pane
        imgui.set_next_window_position(windowWidth*0.75, yOffset)
        imgui.set_next_window_size(windowWidth*0.25, windowHeight)
        imgui.begin("Inspector", False, windowFlags)
        if not self.SelectedEntity is None:
            imgui.text("Entity {}".format(self.SelectedEntity.entity))
            imgui.same_line(
                position=imgui.get_content_region_available_width() - 90)
            if imgui.button("Add Component", 100):
                imgui.open_popup("ComponentsList")
            if imgui.begin_popup("ComponentsList"):
                for menuItem, action in self.ComponentsList:
                    if imgui.selectable(menuItem)[1]:
                        action()
                imgui.end_popup()

            componentToRemove = None
            for component in self.SelectedEntity.GetComponents():
                if self.__imguiDrawComponent(component):
                    componentToRemove = component
            if componentToRemove:
                self.SelectedEntity.RemoveComponent(componentToRemove)
        imgui.end()

        gl.glClearColor(1, 1, 1, 1)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        imgui.render()
        self.ImGUIImpl.render(imgui.get_draw_data())

    def Run(self):
        while self.Running:
            _ = self.Clock.tick(60)
            surface = self.Project.GetSurface()
            if surface:
                surface.fill((51, 51, 51))
            self.OnRender()
            self.OnEvent()
            self.OnImGuiRender()
            pygame.display.flip()
        pygame.quit()


def main():
    # "..\\PrototypeExample\\PrototypeExample.ptproj"
    editor = Editor(None)
    editor.updateViewPortSize(500, 500)
    editor.Run()


if __name__ == "__main__":
    main()
