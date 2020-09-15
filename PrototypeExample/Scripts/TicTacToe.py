from os import system, name, getcwd
from copy import deepcopy
from enum import Enum
from threading import Thread
import socket
import json


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
    # Player Vs Player over Network
    Network = 3

    # Computer Alpha Beta Pruning
    ComputerV2 = 4


class PlayersFactory:
    @staticmethod
    def GetPlayers(GameMode):
        if GameMode == GameModes.PvP:
            return [Player('X'),  Player('O')]
        if GameMode == GameModes.Computer:
            return [Player('X'), AIPlayer('O', 'X')]
        if GameMode == GameModes.ComputerV2:
            return [Player('X'), AIPlayerFast('O', 'X')]
        if GameMode == GameModes.Network:
            player = NetworkPlayer('localhost', 5000)
            if player.symbol == 'X':
                return [player, Player('O')]
            else:
                return [Player('X'), player]


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
        if symbol is None:
            raise ValueError('Symbol is required to set value in the cell')
        if self.grid[row][col] == 0:
            self.grid[row][col] = symbol
            return True
        return False

    def ResetCell(self, row, col):
        self.grid[row][col] = 0

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

    def to_string(self):
        cellValues = ''
        for i in range(0, 3):
            for j in range(0, 3):
                cellValues += str(self.grid[i][j]) + ', '
        return cellValues

    def toNum(self):
        num = 0
        for i in range(0, 3):
            for j in range(0, 3):
                if self.grid[i][j] == 0:
                    num += 0
                elif self.grid[i][j] == 'X':
                    num += 1
                elif self.grid[i][j] == 'O':
                    num += 2
                num *= 10

# Bot with Simple Mini Max Algorithm


class AIPlayer:
    def __init__(self, symbol, opponent):
        self.symbol = symbol
        self.opponent = opponent
        with open('aistates.json') as reader:
            self.Scores = json.load(reader)

    def Score(self, grid, maximize):
        if grid.CheckWin():
            return -1 if maximize else 1
        if grid.CheckTie():
            return 0
        state = grid.toNum()
        if state in self.Scores.keys():
            return self.Scores[state]

        maxScore = -100
        minScore = 100
        for cell in range(0, 9):
            i = cell // 3
            j = cell % 3
            status = False
            if maximize:
                status = grid.SetCell(i, j, self.symbol)
            else:
                status = grid.SetCell(i, j, self.opponent)
            if not status:
                continue
            score = self.Score(grid, not maximize)
            if score > maxScore:
                maxScore = score
            if score < minScore:
                minScore = score
            grid.ResetCell(i, j)

        if maximize:
            return maxScore
        return minScore

    def MiniMax(self, grid):
        scores = {}
        for i in range(3):
            for j in range(3):
                if not grid.grid[i][j] == 0:
                    continue
                grid.SetCell(i, j, self.symbol)
                score = self.Score(grid, False)
                grid.ResetCell(i, j)
                cell = i*3 + j + 1
                scores[cell] = score
        return max(scores, key=scores.get)

    def GetCell(self, grid, game=None):
        if not game:
            return -1
        if game.Finished:
            game.Busy = False
            return -1
        gameState = deepcopy(grid)
        cell = self.MiniMax(gameState)
        game.TakeTurn(cell)
        return int(cell)


# Bot with Simple Mini Max Algorithm with Alpha Beta Pruning
class AIPlayerFast:
    def __init__(self, symbol, opponent):
        self.symbol = symbol
        self.opponent = opponent

    def Score(self, grid, maximize, depth, alpha=[-1000], beta=[1000]):
        if grid.CheckWin():
            return -10 + depth if maximize else 10 - depth
        if grid.CheckTie():
            return 0

        minScore = 100
        maxScore = -100
        for i in range(3):
            for j in range(3):
                if grid.grid[i][j] != 0:
                    continue

                if maximize:
                    grid.SetCell(i, j, self.symbol)
                else:
                    grid.SetCell(i, j, self.opponent)
                score = self.Score(grid, not maximize, depth+1, alpha, beta)
                grid.ResetCell(i, j)
                if score > maxScore:
                    maxScore = score
                if score < minScore:
                    minScore = score

                if maximize:
                    alpha[0] = max(alpha[0], score)
                else:
                    beta[0] = min(beta[0], score)

                if beta[0] <= alpha[0]:
                    break

        if maximize:
            return maxScore
        else:
            return minScore

    def MiniMax(self, grid):
        scores = {}
        for i in range(3):
            for j in range(3):
                if not grid.grid[i][j] == 0:
                    continue
                node = deepcopy(grid)
                node.SetCell(i, j, self.symbol)
                score = self.Score(node, False, 1)
                cell = i*3 + j + 1
                scores[cell] = score
        return max(scores, key=scores.get)

    def GetCell(self, grid, game=None):
        if not game:
            return -1
        if game.Finished:
            game.Busy = False
            return -1
        game.Busy = True
        gameState = deepcopy(grid)
        cell = self.MiniMax(gameState)
        game.TakeTurn(cell)
        return int(cell)


class NetworkPlayer:
    def __init__(self, server, port, symbol=None):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((server, port))
        if symbol is None:
            # Get Symbol for the player
            msg = self.connection.recv(1024)
            self.symbol = msg.decode('utf-8')
        else:
            self.symbol = symbol
        print('# [LOG] Network Player created with symbol {}'.format(self.symbol))

    def GetCell(self, grid, game=None):
        if not game.LastCell == -1:
            print('# [LOG] Send current grid over network')
            self.connection.sendall(str(game.LastCell).encode('utf-8'))
        if game.Finished:
            return -1
        print('# [LOG] Waiting for network to send other players move')
        # Get Players Turn
        msg = self.connection.recv(1024)
        cell = int(msg.decode('utf-8'))

        print('# [LOG] Cell Value from other player received -> {}'.format(cell))
        if game != None and cell != -1:
            print('# [LOG] Other player took turn on cell {}'.format(cell))
            game.TakeTurn(cell)

        return int(cell)

    def __del__(self):
        self.connection.close()

    def __repr__(self):
        return 'NetworkPlayer {}'.format(self.symbol)


class Game:
    def __init__(self, mode):
        self.Players = PlayersFactory.GetPlayers(mode)
        self.Busy = False
        self.ResetGame()
        self.LastCell = -1
        self.HandlePlayersOnSwitch()

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
        while(self.Busy):
            pass
        ClearConsole()
        self.Grid.PrintGrid()

    def GetGrid(self):
        return self.Grid.grid

    def IsFinished(self):
        return self.Finished

    def IsTied(self):
        return self.Winner is None and self.Finished

    def GetWinner(self):
        return self.Winner.symbol

    def HandlePlayersOnSwitch(self):
        if isinstance(self.Player, AIPlayerFast) or isinstance(self.Player, AIPlayer) or isinstance(self.Player, NetworkPlayer):
            thread = Thread(target=self.Player.GetCell, args=(self.Grid, self))
            thread.start()

    def IsBusy(self):
        return self.Busy

    def TakeTurn(self, cell):
        self.Busy = False
        if self.Finished or not 0 < cell < 10:
            return False

        row = (cell-1) // 3
        col = (cell-1) % 3

        isSet = self.Grid.SetCell(row, col, self.Player.symbol)
        self.LastCell = cell

        if not isSet:
            return False

        isWon = self.Grid.CheckWin()
        if isWon:
            self.Winner = self.Player
            self.Finished = True
            self.SwitchPlayer()
            self.HandlePlayersOnSwitch()
            return False

        isTied = self.Grid.CheckTie()
        if isTied:
            self.Finished = True
            self.SwitchPlayer()
            self.HandlePlayersOnSwitch()
            return False

        self.SwitchPlayer()
        self.HandlePlayersOnSwitch()

    def StartConsoleGame(self):
        while not self.Finished:
            self.DrawGrid()
            cell = self.Player.GetCell(self.Grid)
            self.TakeTurn(cell)

        # Declare Game Result
        self.DrawGrid()
        if self.Winner is None:
            print('Game Tied !!!')

        else:
            print('Player ({}) Wins'.format(self.Winner.symbol))


if __name__ == "__main__":
    game = Game(GameModes.Computer)
    game.StartConsoleGame()
