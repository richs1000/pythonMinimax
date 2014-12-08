__author__ = 'rsimpson'

from ticTacToeAlphaBeta import *
from ticTacToeFullMinimax import *
from ticTacToeKindaSmart import *
from ticTacToePartialMinimax import *

def main():
    print("Welcome to Tic-Tac-Toe")
    # create the player objects
    p2 = KindaSmartMachine('X')
    p1 = FullMinimaxMachine('O')
    #p2 = KindaSmartMachine('O')
    #p2 = Machine('O')
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

