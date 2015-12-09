__author__ = 'rsimpson'

from ticTacToeMachine import *

DEPTHLIMIT = 2

class PartialMinimaxMachine(Machine):
    def __init__(self, name):
        # call constructor for parent class
        Machine.__init__(self, name)

    def inARow(self, board, le):
        '''
        This function counts the number of two-in-a-row combinations the player has,
        either in a row, column or diagonally
        '''
        # create a tuple for each pair of squares that can be in a row
        combos = [(0, 1), (1, 2), (0, 2),
                  (3, 4), (4, 5), (3, 5),
                  (6, 7), (7, 8), (6, 8),
                  (0, 3), (3, 6), (0, 6),
                  (1, 4), (4, 7), (1, 7),
                  (2, 5), (5, 8), (2, 8),
                  (0, 4), (4, 8), (0, 8),
                  (2, 4), (4, 6), (2, 6)]
        # we start with no squares in a row
        count = 0
        # for each of the pairs above...
        for c in combos:
            # if we have claimed both squares...
            if (board[c[0]] == le and board[c[1]] == le):
                # increase our count
                count += 1
        # return the total number of two-in-a-row pairs we have
        return count

    def cattyCorner(self, board, le):
        '''
        This function returns the number of "catty-corner" pairs the player has
        '''
        # create a tuple for each pair of catty-corner squares
        combos = [(1, 3), (1, 5), (7, 3), (7, 5)]
        # we start with no catty-corner squares
        count = 0
        # for each of the pairs above...
        for c in combos:
            # if we have claimed both squares...
            if (board[c[0]] == le and board[c[1]] == le):
                # increase our count
                count += 1
        # return the total number of catty-corner squares
        return count

    def haveCenter(self, board, le):
        # if we have the center square...
        if (board[4] == le):
            # return 1
            return 1
        # otherwise, we don't have the center square...
        else:
            # so return 0
            return 0

    def evaluationFunction(self, board):
        """
        This function is used by minimax to evaluate a non-terminal state.
        """
        # start with a value of zero
        score = 0
        # add number of two-in-a-row pairs we have
        score += 3 * self.inARow(board, self.name)
        # subtract number of two-in-a-row pairs opponent has
        score -= 3 * self.inARow(board, self.opponent)
        # add number of catty-corner pairs we have
        score += 2 * self.cattyCorner(board, self.name)
        # subtract number of catty-corner pairs opponent has
        score -= 2 * self.cattyCorner(board, self.opponent)
        # add one if we have the center square
        score += self.haveCenter(board, self.name)
        # subtract one if opponent has center square
        score -= self.haveCenter(board, self.opponent)
        # return the evaluation score
        return score

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
            return (True, 100)
        # Darn, we lost!
        elif board.isWinner(self.opponent):
            # Return a negative number
            return (True, -100)
        # if it's a draw,
        elif (board.isBoardFull()):
            # return the value 0
            return (True, 0)
        # if we've hit our depth limit
        elif (depth >= DEPTHLIMIT):
            # use the evaluation function to return a value for this state
            return (True, self.evaluationFunction(board.board))
        return (False, 0)

    def partialMinimax(self, board, player, depth):
        """
        This function implements a minimax search that cuts off its search at a
        specified depth
        The function always returns a tuple: (<move>, <value>). <move> only matters
        for the top node in the search tree, when the function is sending back which
        move to make to the game.
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
        mv = self.partialMinimax(board, self.name, 0)
        return mv[0]
        #return self.partialMinimax(board, self.name, 0)[0]


