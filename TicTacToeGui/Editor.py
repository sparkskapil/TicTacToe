# pylint: skip-file
import sys
import pygame
import OpenGL.GL as gl
from imgui.integrations.pygame import PygameRenderer
import imgui
from PygameHelpers import *
from SceneManager import SceneManager

from Scene import TicTacToeGame
from ECS.Components import Vector, TransformComponent, TagComponent, LabelComponent
from ECS.Components import Vector, SpriteComponent, ButtonComponent, ScriptComponent
from ECS.Scene import Scene
from ECS.Systems.BoundsComputingSystem import BoundsComputingSystem

from ImGuiCustomControls import FileSystem
from ImGuiCustomControls import OpenFileDialog, SaveFileDialog, MessageBox


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
        self.offscreenSurface = pygame.Surface((width, height))
        self.ViewPortSize = (width, height)
        self.SceneMangaer.SetSurface(self.offscreenSurface)

    def __init__(self):
        pygame.init()

        size = 800, 600
        mode = pygame.DOUBLEBUF | pygame.OPENGL | pygame.RESIZABLE

        pygame.display.set_mode(size, mode)
        pygame.display.set_caption("Editor")
        pygame.display.init()
        SDL_Maximize()
        info = pygame.display.Info()

        self.Clock = clock = pygame.time.Clock()

        self.SetupImGUI(size)
        self.SceneMangaer = SceneManager()
        self.BoundsRenderer = None
        self.updateViewPortSize(size[0], size[1])
        self.Running = True
        self.SelectedEntity = None
        self.selected = -1
        self.ScenePosition = (0, 0)
        self.GameMode = False
        self.File = None

    def __modifyEventRelativeToScene(self, event):
        x, y = self.ScenePosition
        if event.type == pygame.MOUSEBUTTONDOWN:
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
        changed, text = imgui.input_text("TAGNAME", text, 100,
                                         imgui.INPUT_TEXT_CHARS_UPPERCASE)
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
            "WIDTH", width, 1, 0, self.WindowSize[0])
        if changed:
            component.width = width

        height = component.height
        changed, height = imgui.drag_int(
            "HEIGHT", height, 1, 0, self.WindowSize[1])
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
        action = component.action
        changed, action = imgui.input_text(
            "ONCLICK", component.GetActionName(), 256, imgui.INPUT_TEXT_READ_ONLY)
        # if changed:
        #     component.action = action

        width = component.width
        changed, width = imgui.drag_int(
            "WIDTH", width, 1, 0, self.WindowSize[0])
        if changed:
            component.width = width

        height = component.height
        changed, height = imgui.drag_int(
            "HEIGHT", height, 1, 0, self.WindowSize[1])
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
        imgui.same_line()

    def __imguiDrawScriptComponent(self, component):
        module = component.Module
        changed, module = imgui.input_text(
            "MODULE", module, len(module)+1, imgui.INPUT_TEXT_READ_ONLY)
        # if changed:
        #     component.action = action

        scriptClass = component.Class
        changed, scriptClass = imgui.input_text(
            "CLASS", scriptClass, len(scriptClass)+1, imgui.INPUT_TEXT_READ_ONLY)

    def __imguiDrawComponent(self, component):
        compName = component.__class__.__name__
        expanded, _ = imgui.collapsing_header(compName, True)
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

    def __onSaveFile(self, file):
        if not self.SceneMangaer.HasScene():
            return None
        if not FileSystem.GetFileExtension(file) == '.hsc':
            file += ".hsc"
        self.SceneMangaer.CurrentScene.SaveScene(file)

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
                self.SceneMangaer.Event(
                    self.__modifyEventRelativeToScene(event))

    def OnRender(self):
        if self.SceneMangaer.HasScene():
            if self.BoundsRenderer is None:
                self.SelectionRenderer = BoundsComputingSystem(
                    self.SceneMangaer.CurrentScene, self.offscreenSurface)
            if self.GameMode:
                self.SceneMangaer.Update()
            self.SceneMangaer.Render()

            # Selection should be rendered after the scene is rendered
            if not self.GameMode and not self.SelectedEntity is None:
                self.SelectionRenderer.DrawRectForEntity(self.SelectedEntity)

    def OnImGuiRender(self):
        self.OnApplicationResize()
        imgui.new_frame()
        menubarWidth = 0
        menubarHeight = 0
        openFileDialogState = False
        saveFileDialogState = False
        if imgui.begin_main_menu_bar():
            if imgui.begin_menu("File", True):

                clicked_open, selected_open = imgui.menu_item(
                    "Open", 'Ctrl+O', False)
                if clicked_open:
                    openFileDialogState = True

                clicked_save, selected_save = imgui.menu_item(
                    "Save", 'Ctrl+S', False, self.SceneMangaer.HasScene()
                )
                if clicked_save:
                    saveFileDialogState = True

                clicked_quit, selected_quit = imgui.menu_item(
                    "Quit", 'Ctrl+Q', False, True
                )
                if clicked_quit:
                    self.Running = False

                imgui.end_menu()
            if imgui.begin_menu("Game", True):
                clicked_run, selected_quit = imgui.menu_item(
                    "Run", 'Cmd+R', False, not self.GameMode
                )
                if clicked_run:
                    self.GameMode = True
                clicked_stop, selected_quit = imgui.menu_item(
                    "Stop", 'Cmd+T', False, self.GameMode
                )
                if clicked_stop:
                    self.GameMode = False
                imgui.end_menu()
            menubarWidth, menubarHeight = imgui.get_item_rect_size()
            imgui.end_main_menu_bar()

        if openFileDialogState:
            OpenFileDialog.ShowDialog(self.__onOpenFile)
        openFileDialogState = False
        OpenFileDialog.DrawDialog()

        if saveFileDialogState:
            SaveFileDialog.ShowDialog(self.__onSaveFile)
        saveFileDialogState = False
        SaveFileDialog.DrawDialog()

        # Create texture from Pygame Surface
        if hasattr(self, "Texture"):
            GLHelpers.DeleteTexture(self.Texture)
        tex, w, h = GLHelpers.SurfaceToTexture(self.offscreenSurface)
        self.Texture = tex

        windowFlags = imgui.WINDOW_NO_RESIZE | imgui.WINDOW_NO_MOVE | imgui.WINDOW_NO_COLLAPSE

        YOffset = menubarHeight - 2
        Width = self.WindowSize[0]
        Height = self.WindowSize[1] - YOffset

        # Draw Left Pane
        imgui.set_next_window_position(0, YOffset)
        imgui.set_next_window_size(Width*0.25, Height)
        imgui.begin("Scene Hierarchy", False, windowFlags)

        if imgui.tree_node("Scene [{}]".format(self.SceneMangaer.CurrentSceneName)):
            scene = self.SceneMangaer.GetScene()
            if not scene is None:
                for entId in scene.Entities.keys():
                    _, currentlySelected = imgui.selectable(
                        "Entity {}".format(entId), self.selected == entId)
                    if currentlySelected:
                        self.selected = entId
            imgui.tree_pop()
        imgui.end()

        entId = self.selected
        if not entId == -1:
            self.SelectedEntity = self.SceneMangaer.GetScene().Entities[entId]

        # Draw ViewPort
        imgui.set_next_window_position(Width*0.25, YOffset)
        imgui.set_next_window_size(Width*0.50, Height)
        imgui.begin("Viewport", False, windowFlags)
        winWidth, winHeight = imgui.get_window_size()
        self.ScenePosition = Width*0.25 + \
            (winWidth - w)/2, YOffset + (winHeight - h)/2
        imgui.set_cursor_pos_x(self.ScenePosition[0] - Width*0.25)
        imgui.set_cursor_pos_y(self.ScenePosition[1] - YOffset)

        imgui.image(tex, w, h)
        imgui.end()

        # Draw Right Pane
        imgui.set_next_window_position(Width*0.75, YOffset)
        imgui.set_next_window_size(Width*0.25, Height)
        imgui.begin("Inspector", False, windowFlags)
        if not self.SelectedEntity is None:
            imgui.text("Entity {}".format(self.SelectedEntity.entity))
            for component in self.SelectedEntity.GetComponents():
                self.__imguiDrawComponent(component)
        imgui.end()

        gl.glClearColor(1, 1, 1, 1)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        imgui.render()
        self.ImGUIImpl.render(imgui.get_draw_data())

    def Run(self):
        while self.Running:
            dt = self.Clock.tick(60)
            self.OnEvent()
            self.offscreenSurface.fill((51, 51, 51))
            self.OnRender()
            self.OnImGuiRender()
            pygame.display.flip()
        pygame.quit()


def main():
    editor = Editor()
    editor.updateViewPortSize(500, 500)
    editor.SceneMangaer.AddScene("MainScene", TicTacToeGame())
    # scene = Scene()
    # scene.LoadScene("MainScene.hcs")
    # editor.SceneMangaer.AddScene("MainScene", scene)
    editor.Run()


if __name__ == "__main__":
    main()
