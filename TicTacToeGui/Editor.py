# pylint: skip-file
import sys
import pygame
import OpenGL.GL as gl
from imgui.integrations.pygame import PygameRenderer
import imgui
from PygameHelpers import *
from SceneManager import SceneManager

from Scene import TicTacToeGame


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
        self.WindowSize = imgui.get_io().display_size
        self.ImGUIImpl = impl

    def OnApplicationResize(self):
        pass

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

        self.SetupImGUI(size)
        self.SceneMangaer = SceneManager()
        self.updateViewPortSize(size[0], size[1])
        self.Running = True

    def OnEvent(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.Running = False
            if event.type == pygame.KEYDOWN and pygame.K_ESCAPE == event.key:
                self.Running = False
            self.ImGUIImpl.process_event(event)
            

    def OnRender(self):
        # BUTTER = (255, 245, 100)
        # textFont = pygame.font.Font(None, 30)  # some default font
        # words = textFont.render(
        #     "Count: " + str(pygame.time.get_ticks()), True, BUTTER)
        # self.offscreenSurface.blit(words, (150, 250))
        self.SceneMangaer.Render()

    def OnImGuiRender(self):
        imgui.new_frame()
        
        if imgui.begin_main_menu_bar():
            if imgui.begin_menu("File", True):
                clicked_quit, selected_quit = imgui.menu_item(
                    "Quit", 'Cmd+Q', False, True
                )
                if clicked_quit:
                    exit(1)

                imgui.end_menu()
            imgui.end_main_menu_bar()
        # Create texture from Pygame Surface
        if hasattr(self, "Texture"):
            GLHelpers.DeleteTexture(self.Texture)
        tex, w, h = GLHelpers.SurfaceToTexture(self.offscreenSurface)
        self.Texture = tex

        imgui.begin("Viewport", True)
        winWidth, winHeight = imgui.get_window_size()
        imgui.set_cursor_pos_x((winWidth - w)/2)
        imgui.set_cursor_pos_y((winHeight - h)/2)
        imgui.image(tex, w, h)
        imgui.end()
        gl.glClearColor(1, 1, 1, 1)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        imgui.render()
        self.ImGUIImpl.render(imgui.get_draw_data())

    def Run(self):
        while self.Running:
            self.OnEvent()
            self.offscreenSurface.fill((51, 51, 51))
            self.OnRender()
            self.OnImGuiRender()
            pygame.display.flip()
        pygame.quit()


'''
 def main():
    pygame.init()
    size = 800, 600
    pygame.display.set_mode(
        size, pygame.DOUBLEBUF | pygame.OPENGL | pygame.RESIZABLE)
    pygame.display.init()
    info = pygame.display.Info()

    imgui.create_context()
    impl = PygameRenderer()

    io = imgui.get_io()
    io.display_size = size

    SDL_Maximize()
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            impl.process_event(event)

        imgui.new_frame()

        if imgui.begin_main_menu_bar():
            if imgui.begin_menu("File", True):

                clicked_quit, selected_quit = imgui.menu_item(
                    "Quit", 'Cmd+Q', False, True
                )

                if clicked_quit:
                    exit(1)

                imgui.end_menu()
            imgui.end_main_menu_bar()

        offscreenSurface = pygame.Surface((info.current_w, info.current_h))
        # colours
        MIDNIGHT = (15, 0, 100)
        BUTTER = (255, 245, 100)
        textFont = pygame.font.Font(None, 30)  # some default font
        words = textFont.render(
            "Count: " + str(pygame.time.get_ticks()), True, BUTTER)
        offscreenSurface.fill(MIDNIGHT)
        offscreenSurface.blit(words, (150, 250))
        tex, w, h = surfaceToTexture(offscreenSurface)

        imgui.begin("Viewport", True)
        imgui.text("Bar")
        imgui.image(tex, w, h)
        imgui.end()
        # note: cannot use screen.fill((1, 1, 1)) because pygame's screen
        #       does not support fill() on OpenGL sufraces
        gl.glClearColor(1, 1, 1, 1)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        imgui.render()
        impl.render(imgui.get_draw_data())

        pygame.display.flip()

        gl.glDeleteTextures([tex])
'''


def main():
    editor = Editor()
    editor.updateViewPortSize(500, 500)
    editor.SceneMangaer.AddScene("MainScene", TicTacToeGame())
    editor.Run()


if __name__ == "__main__":
    main()
