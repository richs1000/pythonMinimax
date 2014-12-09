__author__ = 'rsimpson'


"""
I started with minimax code that I found here:
http://callmesaint.com/python-minimax-tutorial/
That code was written by Matthew Griffin

Then I added in code I got from here:
https://inventwithpython.com/tictactoe.py
That code was written by Al Sweigart

Then I started adding my own code
"""

from ticTacToeMachine import *


DEPTHLIMIT = 2


class AlphaBetaMachine(Machine):
    def __init__(self, name):
        # call constructor for parent class
        Machine.__init__(self, name)

    def evaluationFunction(self, board):
        """
        This function is used by minimax to evaluate a non-terminal state.
        """
        print "your code goes here"
        return 0

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

    def alphaBeta(self, board, player, depth, alpha, beta):
        """
        This function implements a minimax search that cuts off its search at a
        specified depth
        The function always returns a tuple: (<move>, <value>). <move> only matters
        for the top node in the search tree, when the function is sending back which
        move to make to the game.
        Alpha-Beta Pruning Algorithm:
            * the alpha value holds the best MAX value found;
            * the beta value holds the best MIN value found.
            * At MAX level, before evaluating each child path, compare the returned value with of the previous path with the beta value. If the value is greater than it abort the search for the current node;
            * At MIN level, before evaluating each child path, compare the returned value with of the previous path with the alpha value. If the value is lesser than it abort the search for the current node.
        """
        # check to see if we are at a terminal state - someone won, the board is full or we hit our search limit
        terminalTuple = self.atTerminalState(board, depth)
        # if we are at a terminal state
        if terminalTuple[0] == True:
            # return the value of this state
            return (0, terminalTuple[1])
        # get all open spaces
        possibleMoves = board.possibleNextMoves()
        # are we considering our move or our opponent's move
        if self.name == player:
            # if it's our move (MAX), we want to find the move with the highest number, so start with low numbers
            bestMove = -1
            bestScore = beta
            # loop through all possible moves
            for m in possibleMoves:
                # make the move
                board.makeMove(player, m)
                # get the minimax vaue of the resulting state
                minimax = self.alphaBeta(board, self.opponent, depth+1, alpha, beta)
                # is this move better than any other moves we found?
                if bestScore < minimax[1]:
                    # save the move...
                    bestMove = m
                    # and its score
                    bestScore = minimax[1]
                # undo the move
                board.clearSquare(m)
                # alpha-beta pruning: compare the returned value with of the previous path with the
                # beta value...
                if bestScore > alpha:
                    # If the value is greater than alpha abort the search for the current node;
                    return (bestMove, bestScore)
        else:
        # if it's our opponent's move (MIN), we want to find a low number, so start with big numbers
            bestMove = -1
            bestScore = alpha
            # consider all possible moves
            for m in possibleMoves:
                # make the move
                board.makeMove(player, m)
                # get the minimax vaue of the resulting state
                minimax = self.alphaBeta(board, self.name, depth+1, alpha, beta)
                # is this better (for our opponent) than any other moves we found?
                if bestScore > minimax[1]:
                    # save the move...
                    bestMove = m
                    # and its score
                    bestScore = minimax[1]
                # undo the move
                board.clearSquare(m)
                # compare the returned value with of the previous path with the alpha value...
                if bestScore < beta:
                    # If the value is less than beta abort the search for the current node
                    return (bestMove, bestScore)
        # return the best move and best score we found for this state
        return (bestMove, bestScore)

    def move(self, board):
        m = self.alphaBeta(board, self.name, 0, 2, -2)[0]
        print "move = " + str(m)
        return m


