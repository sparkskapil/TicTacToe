from ctypes import windll
user32 = windll.user32
ShowWindow = user32.ShowWindow

import pygame
import OpenGL.GL as gl


def getSDLWindow():
    return pygame.display.get_wm_info()['window']


def SDL_Maximize():
    return ShowWindow(getSDLWindow(), 3)


class GLHelpers:
    @staticmethod
    def SurfaceToTexture(pygame_surface):
        """
          Converts pygame surface to opengl texture.
          Returns texture id, texture_width, texture_height
        """
        texID = gl.glGenTextures(1)
        surface = pygame.image.tostring(pygame_surface, 'RGBA')
        gl.glBindTexture(gl.GL_TEXTURE_2D, texID)
        gl.glTexParameteri(
            gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)
        gl.glTexParameteri(
            gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
        surfaceRect = pygame_surface.get_rect()
        gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGBA, surfaceRect.width,
                        surfaceRect.height, 0, gl.GL_RGBA, gl.GL_UNSIGNED_BYTE, surface)
        return texID, surfaceRect.width, surfaceRect.height

    @staticmethod
    def DeleteTexture(texture):
        """
        Deletes texture
        """
        gl.glDeleteTextures([texture])
