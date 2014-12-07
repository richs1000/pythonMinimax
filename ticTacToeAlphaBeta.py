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

import random

DEPTHLIMIT = 2

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


class Player():
    def __init__(self, myName):
        # name of this player - either X or O
        self.name = myName
        # name of player's opponent
        if myName == 'X':
            self.opponent = 'O'
        else:
            self.opponent = 'X'

    def move(self, board):
        # Let the player type in his move.
        move = -1
        # keep seeking input until we get an integer between 0 and 8 that corresponds to
        # an empty square on the board
        while (int(move) not in range(0, 9)) or (not board.isSpaceFree(int(move))):
            # get input from keyboard
            move = int(raw_input("Choose a square: "))
        # return the move
        return int(move)


class Machine(Player):
    def __init__(self, name):
        # call constructor for parent class
        Player.__init__(self, name)

    def chooseRandomly(self, moves):
        """
        Given a list of potential moves, pick one at random and return it
        """
        # pick a move randomly
        moveIndex = random.randint(0, len(moves) - 1)
        # send it back
        return moves[moveIndex]

    def randomMove(self, board):
        # get all open spaces
        possibleMoves = board.possibleNextMoves()
        # pick a move randomly
        move = self.chooseRandomly(possibleMoves)
        # return the move chosen by the player
        return move

    def move(self, board):
        #return self.partialMinimax(board, self.name, 0)[0]
        #return self.fullMinimax(board, self.name)[0]
        #return self.kindOfSmart(board)
        return self.randomMove(board)


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
        print "depth = " + str(depth)
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
    p1 = Machine('X')
    p2 = FullMinimaxMachine('O')
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

