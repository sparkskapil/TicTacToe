from os import system, name
from copy import deepcopy
from enum import Enum


def ClearConsole():
  # for windows
    if name == 'nt':
        _ = system('cls')

    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')


class GameModes(Enum):
    # Player Vs Player
    PvP = 1
    # Player Vs Computer
    Computer = 2


class PlayersFactory:
    def GetPlayers(GameMode):
        if GameMode == GameModes.PvP:
            return [Player('X'),  Player('O')]
        if GameMode == GameModes.Computer:
            return [Player('X'), AIPlayerFast('O', 'X')]


class Player:
    def __init__(self, symbol):
        self.symbol = symbol

    def GetCell(self, grid=None):
        print('Player ({})'.format(self.symbol))
        cell = input('Enter Cell: ')
        return int(cell)


class Grid:
    def __init__(self):
        self.grid = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

    def SetCell(self, row, col, symbol):
        if symbol == None:
            raise ValueError('Symbol is required to set value in the cell')
        if self.grid[row][col] == 0:
            self.grid[row][col] = symbol
            return True
        return False

    def CheckWin(self):
        for i in range(3):
            if self.grid[i][0] == self.grid[i][1] == self.grid[i][2] and not self.grid[i][0] == 0:
                return True

        for i in range(3):
            if self.grid[0][i] == self.grid[1][i] and self.grid[0][i] == self.grid[2][i] and not self.grid[0][i] == 0:
                return True

        # Diagonal Check
        if self.grid[0][0] == self.grid[1][1] == self.grid[2][2] and not self.grid[1][1] == 0:
            return True
        if self.grid[0][2] == self.grid[1][1] == self.grid[2][0] and not self.grid[1][1] == 0:
            return True

        return False

    def CheckTie(self):
        for i in range(3):
            for j in range(3):
                if self.grid[i][j] == 0:
                    return False
        return True

    def PrintGrid(self):
        for i in range(3):
            for j in range(3):
                if self.grid[i][j] == 0:
                    print(i*3 + j + 1, end=' ')
                else:
                    print(self.grid[i][j], end=' ')
            print()


# Bot with Simple Mini Max Algorithm
class AIPlayer:
    def __init__(self, symbol, opponent):
        self.symbol = symbol
        self.opponent = opponent

    def Score(self, grid, maximize):
        if grid.CheckWin():
            return -1 if maximize else 1
        if grid.CheckTie():
            return 0

        scores = []
        minScore = 100
        maxScore = -100
        for i in range(3):
            for j in range(3):
                if grid.grid[i][j] == 0:
                    node = deepcopy(grid)
                    if maximize:
                        node.SetCell(i, j, self.symbol)
                    else:
                        node.SetCell(i, j, self.opponent)
                    score = self.Score(node, not maximize)
                    scores.append(score)

        if maximize:
            return max(scores)
        else:
            return min(scores)

    def MiniMax(self, grid):
        scores = {}
        for i in range(3):
            for j in range(3):
                if not grid.grid[i][j] == 0:
                    continue
                node = deepcopy(grid)
                node.SetCell(i, j, self.symbol)
                score = self.Score(node, False)
                cell = i*3 + j + 1
                scores[cell] = score
        return max(scores, key=scores.get)

    def GetCell(self, grid):
        cell = self.MiniMax(grid)
        return int(cell)


# Bot with Simple Mini Max Algorithm with Alpha Beta Pruning
class AIPlayerFast:
    def __init__(self, symbol, opponent):
        self.symbol = symbol
        self.opponent = opponent

    def Score(self, grid, maximize, alpha=[-1000], beta=[1000]):
        if grid.CheckWin():
            return -1 if maximize else 1
        if grid.CheckTie():
            return 0

        scores = []
        for i in range(3):
            for j in range(3):
                if grid.grid[i][j] == 0:
                    node = deepcopy(grid)
                    if maximize:
                        node.SetCell(i, j, self.symbol)
                    else:
                        node.SetCell(i, j, self.opponent)
                    score = self.Score(node, not maximize)
                    scores.append(score)

                    if maximize:
                        alpha[0] = max(alpha[0], score)
                    else:
                        beta[0] = min(beta[0], score)

                    if beta[0] < alpha[0]:
                        break

        if maximize:
            return max(scores)
        else:
            return min(scores)

    def MiniMax(self, grid):
        scores = {}
        for i in range(3):
            for j in range(3):
                if not grid.grid[i][j] == 0:
                    continue
                node = deepcopy(grid)
                node.SetCell(i, j, self.symbol)
                score = self.Score(node, False)
                cell = i*3 + j + 1
                scores[cell] = score
        return max(scores, key=scores.get)

    def GetCell(self, grid):
        cell = self.MiniMax(grid)
        return int(cell)


class Game:
    def __init__(self):
        self.Players = PlayersFactory.GetPlayers(GameModes.Computer)
        self.ResetGame()

    def ResetGame(self):
        self.Finished = False
        self.Winner = None
        self.PlayerIndex = 0
        self.Player = self.Players[self.PlayerIndex]
        self.Grid = Grid()

    def SwitchPlayer(self):
        self.PlayerIndex = (self.PlayerIndex + 1) % 2
        self.Player = self.Players[self.PlayerIndex]

    def DrawGrid(self):
        ClearConsole()
        self.Grid.PrintGrid()

    def GetGrid(self):
        return self.Grid.grid

    def IsFinished(self):
        return self.Finished

    def IsTied(self):
        return self.Winner == None and self.Finished

    def GetWinner(self):
        return self.Player.symbol

    def TakeTurn(self, cell):
        if not 0 < cell < 10:
            return False

        row = (cell-1) // 3
        col = (cell-1) % 3

        isSet = self.Grid.SetCell(row, col, self.Player.symbol)
        if isSet == False:
            return False

        isWon = self.Grid.CheckWin()
        if isWon:
            self.Winner = self.Player
            self.Finished = True
            return False

        isTied = self.Grid.CheckTie()
        if isTied:
            self.Finished = True
            return False

        self.SwitchPlayer()
        if isinstance(self.Player, AIPlayerFast) or isinstance(self.Player, AIPlayer):
            cell = self.Player.GetCell(self.Grid)
            self.TakeTurn(cell)

    def StartConsoleGame(self):
        while self.Finished == False:
            self.DrawGrid()

            cell = self.Player.GetCell(self.Grid)
            self.TakeTurn(cell)

        # Declare Game Result
        self.DrawGrid()
        if self.Winner == None:
            print('Game Tied !!!')

        else:
            print('Player ({}) Wins'.format(self.Player.symbol))


if __name__ == "__main__":
    game = Game()
    game.StartConsoleGame()
