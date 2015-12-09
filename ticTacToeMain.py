__author__ = 'rsimpson'

# from ticTacToePlayer import *
# from ticTacToeMachine import *
# from ticTacToeAlphaBeta import *
# from ticTacToeFullMinimax import *
from ticTacToeKindaSmart import *
from ticTacToePartialMinimax import *
#from ticTacToeAlphaBeta import *


class Board(object):
#Used as a container for the Game
    def __init__(self,p1,p2):
        # keep a pointer to the first player (either a person or machine)
        self.p1 = p1
        # keep a pointer to the second player (either a person or machine)
        self.p2 = p2
        # start with an empty board
        self.board = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']

    def makeMove(self, letter, move):
        """
        Make sure a move is legal and then do it.
        """
        # make sure move is in bounds
        if move in range(0, 9):
            # set the value of board to the player's letter
            self.board[move] = letter

    def clearSquare(self, square):
        """
        Make a square empty - I use this to "undo" a move
        """
        # make sure square is in bounds
        if square in range(0, 9):
            # set the value of board to the player's letter
            self.board[square] = ' '

    def drawBoard(self):
        # Pretty-print the board.
        print('   |   |')
        print(' ' + self.board[0] + ' | ' + self.board[1] + ' | ' + self.board[2])
        print('   |   |')
        print('-----------')
        print('   |   |')
        print(' ' + self.board[3] + ' | ' + self.board[4] + ' | ' + self.board[5])
        print('   |   |')
        print('-----------')
        print('   |   |')
        print(' ' + self.board[6] + ' | ' + self.board[7] + ' | ' + self.board[8])
        print('   |   |')

    def isWinner(self, le):
        # Given a player's letter, this function returns True if that player has won.
        # We use bo instead of board and le instead of letter so we don't have to type as much.
        bo = self.board
        return (
            (bo[0] == le and bo[1] == le and bo[2] == le) or # across the top
            (bo[3] == le and bo[4] == le and bo[5] == le) or # across the middle
            (bo[6] == le and bo[7] == le and bo[8] == le) or # across the bottom
            (bo[0] == le and bo[3] == le and bo[6] == le) or # down the left side
            (bo[1] == le and bo[4] == le and bo[7] == le) or # down the middle
            (bo[2] == le and bo[5] == le and bo[8] == le) or # down the right side
            (bo[0] == le and bo[4] == le and bo[8] == le) or # diagonal
            (bo[2] == le and bo[4] == le and bo[6] == le)) # diagonal

    def isSpaceFree(self, move):
        # make sure move is in bounds
        if move in range(0, 9):
            # Return true if the square is free on the board.
            return self.board[move] == ' '

    def isBoardFull(self):
        """
        Return True if every space on the board has been taken. Otherwise return False.
        """
        # loop through all the squares
        for i in range(0, 9):
            # check if the square is free
            if self.isSpaceFree(i):
                # if it's free, then we're done
                return False
        # all the squares have an X or O in them
        return True

    def possibleNextMoves(self):
        # start with an empty list of possible next moves
        possibleMoves = []
        # find all the empty squares
        for i in range(0,9):
        # if a square hasn't already been filled with an X or an 0
            if self.isSpaceFree(i):
            # add it to the list of possible moves
                possibleMoves.append(i)
        return possibleMoves


def switchPlayer(player, p1, p2):
    """
    Alternate between the two players
    """
    # if player one just went...
    if (player is p1):
        # switch to player two
        return p2
    # otherwise, player two just went...
    else:
        # so switch to player one
        return p1


def main():
    print("Welcome to Tic-Tac-Toe")
    # create the player objects
    p1 = Player('X')
    #p2 = AlphaBetaMachine('O')
    p2 = PartialMinimaxMachine('O')
    # create the game board
    myBoard = Board(p1, p2)
    # start with player 1
    player = p1
    # loop until we get a win or a draw
    while (True):
        # display the board
        myBoard.drawBoard()
        # say which player goes next
        print("Your move, " + player.name)
        # get the player's move
        move = player.move(myBoard)
        # perform the player's move
        myBoard.makeMove(player.name, move)
        # if we have a winner...
        if myBoard.isWinner(player.name):
            # display the board
            myBoard.drawBoard()
            # say who won
            print(player.name + " won!")
            # break out of the loop
            break
        # if the board is full, then it's a draw
        elif myBoard.isBoardFull():
            # display the board
            myBoard.drawBoard()
            # say we have a tie
            print('The game is a tie!')
            # break out of the loop
            break
        # otherwise, switch players and repeat
        else:
            player = switchPlayer(player, p1, p2)


if __name__ == "__main__":
    main()

