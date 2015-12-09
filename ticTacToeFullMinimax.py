__author__ = 'rsimpson'

from ticTacToeMachine import *


class FullMinimaxMachine(Machine):
    def __init__(self, name):
        # call constructor for parent class
        Machine.__init__(self, name)

    def fullMinimax(self, board, player):
        """
        This function implements a minimax search that always goes to the very end
        of the search tree. Only useful for games that don't have big search trees.
        The function always returns a tuple: (<move>, <value>). <move> only matters
        for the top node in the search tree, when the function is sending back which
        move to make to the game.
        """
        # Yay, we won!
        if board.isWinner(self.name):
            # Return a positive number
            return (1, 1)
        # Darn, we lost!
        elif board.isWinner(self.opponent):
            # Return a negative number
            return (-1, -1)
        # if it's a draw,
        elif (board.isBoardFull()):
            # return the value 0
            return (0, 0)
        # get all open spaces
        possibleMoves = board.possibleNextMoves()
        # are we considering our move or our opponent's move
        if self.name == player:
            # if it's our move, we want to find the move with the highest number, so start with low numbers
            bestMove = -1
            bestScore = -1000
            # loop through all possible moves
            for m in possibleMoves:
                # make the move
                board.makeMove(player, m)
                # get the minimax vaue of the resulting state
                minimax = self.fullMinimax(board, self.opponent)
                # is this move better than any other moves we found?
                if bestScore < minimax[1]:
                    # save the move...
                    bestMove = m
                    # and its score
                    bestScore = minimax[1]
                # undo the move
                board.clearSquare(m)
        else:
        # if it's our opponent's move, we want to find a low number, so start with big numbers
            bestMove = -1
            bestScore = 1000
            # consider all possible moves
            for m in possibleMoves:
                # make the move
                board.makeMove(player, m)
                # get the minimax vaue of the resulting state
                minimax = self.fullMinimax(board, self.name)
                # is this better (for our opponent) than any other moves we found?
                if bestScore > minimax[1]:
                    # save the move...
                    bestMove = m
                    # and its score
                    bestScore = minimax[1]
                # undo the move
                board.clearSquare(m)
        # return the best move and best score we found for this state
        return (bestMove, bestScore)

    def move(self, board):
        return self.fullMinimax(board, self.name)[0]


