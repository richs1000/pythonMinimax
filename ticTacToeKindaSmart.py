__author__ = 'rsimpson'

from ticTacToeAlphaBeta import *

class KindaSmartMachine(Machine):
    def __init__(self, name):
        # call constructor for parent class
        Machine.__init__(self, name)

    def chooseRandomly(self, moves):
        """
        Given a list of potential moves, pick one at random and return it
        """
        # pick a move randomly
        moveIndex = random.randint(0, len(moves) - 1)
        # send it back
        return moves[moveIndex]

    def kindOfSmart(self, board):
        # get all open spaces
        possibleMoves = board.possibleNextMoves()
        # First, check if we can win in the next move
        for i in possibleMoves:
            board.makeMove(self.name, i)
            if board.isWinner(self.name):
                return i
            else:
                board.clearSquare(i)
        # Check if the player could win on his next move, and block them.
        for i in possibleMoves:
            board.makeMove(self.opponent, i)
            if board.isWinner(self.opponent):
                return i
            else:
                board.clearSquare(i)
        # Try to take the center, if it is free.
        if board.isSpaceFree(4):
            return 4
        # Try to take one of the corners, if they are free.
        corners = [0, 2, 6, 8]
        for corner in corners:
            if board.isSpaceFree(corner):
                return corner
        # Move on one of the sides.
        return self.chooseRandomly([1, 3, 5, 7])

    def move(self, board):
        return self.kindOfSmart(board)

