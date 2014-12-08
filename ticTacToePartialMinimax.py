__author__ = 'rsimpson'

from ticTacToeAlphaBeta import *

DEPTHLIMIT = 2

class PartialMinimaxMachine(Machine):
    def __init__(self, name):
        # call constructor for parent class
        Machine.__init__(self, name)

    def evaluationFunction(self, board):
        """
        This function is used by AlphaBeta pruning to evaluate a non-terminal state.
        """
        value = 0

        return value

    def atTerminalState(self, board, depth):
        """
        Checks to see if we've reached a terminal state. Terminal states are:
           * somebody won
           * we have a draw
           * we've hit the depth limit on our search
        Returns a tuple (<terminal>, <value>) where:
           * <terminal> is True if we're at a terminal state, False if we're not
           * <value> is the value of the terminal state
        """
        global DEPTHLIMIT
        # Yay, we won!
        if board.isWinner(self.name):
            # Return a positive number
            return (True, 10)
        # Darn, we lost!
        elif board.isWinner(self.opponent):
            # Return a negative number
            return (True, -10)
        # if it's a draw,
        elif (board.isBoardFull()):
            # return the value 0
            return (True, 0)
        # if we've hit our depth limit
        elif (depth >= DEPTHLIMIT):
            # use the evaluation function to return a value for this state
            return (True, self.evaluationFunction(board))
        return (False, 0)

    def partialMinimax(self, board, player, depth):
        """
        This function implements a minimax search that cuts off its search at a
        specified depth
        The function always returns a tuple: (<move>, <value>). <move> only matters
        for the top node in the search tree, when the function is sending back which
        move to make to the game.
        """
        # are we at a terminal state?
        terminalTuple = self.atTerminalState(board, depth)
        if terminalTuple[0] == True:
            return (0, terminalTuple[1])
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
                minimax = self.partialMinimax(board, self.opponent, depth+1)
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
                minimax = self.partialMinimax(board, self.name, depth+1)
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
        return self.partialMinimax(board, self.name, 0)[0]


