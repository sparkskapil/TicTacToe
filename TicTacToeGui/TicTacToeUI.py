import pygame
from TicTacToe import *

class Layer:
    def Init(self, Width, Height, Surface, Application):
        self.Width = Width
        self.Height = Height
        self.Surface = Surface
        self.App = Application
        self.Setup()

    def Setup(self):
        pass

    def Update(self):
        pass

    def Draw(self):
        pass

    def OnEvent(self, event):
        pass


class Sprite(Layer):
    def __init__(self, image, X, Y, scalex=None, scaley=None):
        super().__init__()
        self.X = X
        self.Y = Y
        self.MaxWidth = scalex
        self.MaxHeight = scaley
        self.Image = image

    def Setup(self):
        # Fit sprite to Screen
        if self.MaxWidth == None:
            self.MaxWidth = self.Width
        if self.MaxHeight == None:
            self.MaxHeight = self.Height

        self.image = pygame.image.load(self.Image)
        self.image = pygame.transform.scale(
            self.image, (self.MaxWidth, self.MaxHeight))

    def Draw(self):
        self.Surface.blit(self.image, (self.X, self.Y))


class Grid(Layer):
    def __init__(self, padding, color, thickness=1):
        super().__init__()
        self.padding = padding
        self.color = color
        self.thickness = thickness
        self.Game = Game()
        self.Drawn = []

    def Setup(self):
        self.turn = False
        self.XImg = 'T3X_BLACK.png'
        self.OImg = 'T3O_BLACK.png'

        P = self.padding
        W = self.Width - 2 * P
        H = self.Height - 2 * P
        self.boxes = []
        self.boxes.append([0, 0, W//3, H//3])
        self.boxes.append([W//3, 0, 2*W//3, H//3])
        self.boxes.append([2*W//3, 0, W, H//3])

        self.boxes.append([0, H//3, W//3, 2*H//3])
        self.boxes.append([W//3, H//3, 2*W//3, 2*H//3])
        self.boxes.append([2*W//3, H//3, W, 2*H//3])

        self.boxes.append([0, 2*H//3, W//3, H])
        self.boxes.append([W//3, 2*H//3, 2*W//3, H])
        self.boxes.append([2*W//3, 2*H//3, W, H])
    
    def DrawXO(self):
        P = self.padding
        grid = self.Game.GetGrid()
        for i in range(3):
            for j in range(3):
                cell = grid[i][j]
                index = i*3+j;
                if index in self.Drawn:
                    continue
                #Get Corresponding Rect for Cell
                x1,y1,x2,y2 = self.boxes[index]
                w = x2-x1
                h = y2-y1
                # print(cell)
                if cell == 'X':
                    XSprite = Sprite('T3X_BLACK.png',x1+P,y1+P,w,h)
                    self.App.AttachLayer(XSprite)
                    self.Drawn.append(index)
                elif cell == 'O':
                    OSprite = Sprite('T3O_BLACK.png',x1+P,y1+P,w,h)
                    self.App.AttachLayer(OSprite)
                    self.Drawn.append(index)
        
    def Draw(self):
        P = self.padding
        W = self.Width - 2 * P
        H = self.Height - 2 * P
        T = self.thickness
        C = self.color

        pygame.draw.line(self.Surface, C, (W//3 + P, P),
                         (W//3 + P, H + P), T)
        pygame.draw.line(self.Surface, C, (2*W//3 + P, P),
                         (2*W//3 + P, H + P), T)

        pygame.draw.line(self.Surface, C, (P, H//3 + P),
                         (W + P, H//3 + P), T)
        pygame.draw.line(self.Surface, C, (P, 2*H//3 + P),
                         (W + P, 2*H//3 + P), T)
        self.DrawXO()

    def Update(self):
        pass

    def OnEvent(self, event):
        if not (event.type == pygame.MOUSEBUTTONUP and event.button == pygame.BUTTON_LEFT):
            return

        P = self.padding
        for index, rect in enumerate(self.boxes):
            x1 = rect[0] + P
            y1 = rect[1] + P
            x2 = rect[2] + P
            y2 = rect[3] + P
            X, Y = pygame.mouse.get_pos()
            if x1 < X < x2 and y1 < Y < y2:
                #print(index + 1)
                w = x2-x1
                h = y2-y1
                self.Game.TakeTurn(index+1)



class Application:
    def __init__(self, Width, Height, Title):
        self.Width = Width
        self.Height = Height
        self.Title = Title
        pygame.init()
        self.screen = pygame.display.set_mode([self.Width, self.Height])
        pygame.display.set_caption(self.Title)
        self.clock = pygame.time.Clock()

        self.Layers = []
        self.Running = True

    def AttachLayer(self, Layer):
        Layer.Init(self.Width, self.Height, self.screen, self)
        self.Layers.append(Layer)

    def DetachLayer(self, Layer):
        pass

    def OnEvent(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.Running = False
            if event.type == pygame.KEYDOWN and pygame.K_ESCAPE == event.key:
                self.Running = False
            for layer in self.Layers:
                layer.OnEvent(event)

    def Run(self):

        while self.Running:
            # Handle events
            self.OnEvent()

            # Update Layers
            for layer in self.Layers:
                layer.Update()

            # Draw Layers
            self.screen.fill((0, 0, 0))
            for layer in self.Layers:
                layer.Draw()

            pygame.display.flip()
        pygame.quit()


# Application Constants
COLOR_BLUE = (33, 85, 205)

game = Application(512, 512, "Tic Tac Toe")
bgLayer = Sprite('background.jpg', 0, 0)
gridLayer = Grid(100, COLOR_BLUE, 3)
game.AttachLayer(bgLayer)
game.AttachLayer(gridLayer)
game.Run()
