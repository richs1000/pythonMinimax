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


    def switchPlayer(self, player):
        """
        Alternate between the two players
        """
        # if player one just went...
        if (player is self.p1):
            # switch to player two
            return self.p2
        # otherwise, player two just went...
        else:
            # so switch to player one
            return self.p1


    def play(self):
        """
        This function runs the actual game. It loops until someone wins or we get a draw
        """
        # start with player 1
        player = self.p1
        # loop until we get a win or a draw
        while (True):
            # display the board
            self.drawBoard()
            # say which player goes next
            print("Your move, " + player.name)
            # get the player's move
            move = player.move(self.board)
            # perform the player's move
            self.makeMove(player.name, move)
            # if we have a winner...
            if self.isWinner(player.name):
                # display the board
                self.drawBoard()
                # say who won
                print(player.name + " won!")
                # break out of the loop
                break
            # if the board is full, then it's a draw
            elif self.isBoardFull():
                # display the board
                self.drawBoard()
                # say we have a tie
                print('The game is a tie!')
                # break out of the loop
                break
            # otherwise, switch players and repeat
            else:
                player = self.switchPlayer(player)


class Player():
    def __init__(self, myName):
        # name of this player - either X or O
        self.name = myName
        # name of player's opponent
        if myName == 'X':
            self.opponent = 'O'
        else:
            self.opponent = 'X'

    def isSpaceFree(self, board, move):
        # make sure move is in bounds
        if move in range(0, 9):
            # Return true if the passed move is free on the passed board.
            return board[move] == ' '

    def move(self, board):
        # Let the player type in his move.
        move = -1
        # keep seeking input until we get an integer between 0 and 8 that corresponds to
        # an empty square on the board
        while (int(move) not in range(0, 9)) or (not self.isSpaceFree(board, int(move))):
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
        moveIndex = random.randint(0, len(moves))
        # send it back
        return moves[moveIndex]

    def isWinner(self, bo, le):
        # Given a board and a player's letter, this function returns True if that player has won.
        # We use bo instead of board and le instead of letter so we don't have to type as much.
        return (
            (bo[0] == le and bo[1] == le and bo[2] == le) or # across the top
            (bo[3] == le and bo[4] == le and bo[5] == le) or # across the middle
            (bo[6] == le and bo[7] == le and bo[8] == le) or # across the bottom
            (bo[0] == le and bo[3] == le and bo[6] == le) or # down the left side
            (bo[1] == le and bo[4] == le and bo[7] == le) or # down the middle
            (bo[2] == le and bo[5] == le and bo[8] == le) or # down the right side
            (bo[0] == le and bo[4] == le and bo[8] == le) or # diagonal
            (bo[2] == le and bo[4] == le and bo[6] == le)) # diagonal

    def possibleNextMoves(self, board):
        # start with an empty list of possible next moves
        possibleMoves = []
        # find all the empty squares
        for i in range(0,9):
        # if a square hasn't already been filled with an X or an 0
            if self.isSpaceFree(board, i):
            # add it to the list of possible moves
                possibleMoves.append(i)
        return possibleMoves


    def boardFull(self, board):
        for i in range(0, 9):
            if board[i] != 'X' and board[i] != 'O':
                return False
        return True


    def fullMinimax(self, board, player):
        if self.isWinner(board, self.name):
            return (1, 1)
        elif self.isWinner(board, self.opponent):
            return (-1, -1)
        # if it's a draw, return the move and the value 0
        elif (self.boardFull(board)):
            return (0, 0)
        # get all open spaces
        possibleMoves = self.possibleNextMoves(board)
        # are we considering our move or our opponent's move
        if self.name == player:
            # if it's our move, we want to find a high number, so initialize this to low
            bestMove = -1
            bestScore = -1000
            # if I go next, return the highest value of my child nodes
            for m in possibleMoves:
                copy = board[:]
                copy[m] = player
                minimax = self.fullMinimax(copy, self.opponent)
                if bestScore < minimax[1]:
                    bestMove = m
                    bestScore = minimax[1]
        else:
        # if it's our opponent's move, we want to find a low number, so initialize this high
            bestMove = -1
            bestScore = 1000
            # if my opponent goes next, return the lowest value of my child nodes
            # if I go next, return the highest value of my child nodes
            for m in possibleMoves:
                copy = board[:]
                copy[m] = player
                minimax = self.fullMinimax(copy, self.name)
                if bestScore > minimax[1]:
                    bestMove = m
                    bestScore = minimax[1]
        return (bestMove, bestScore)

    def kindOfSmart(self, board):
        # get all open spaces
        possibleMoves = self.possibleNextMoves(board)
        # First, check if we can win in the next move
        for i in possibleMoves:
            copy = board[:]
            if self.isSpaceFree(copy, i):
                copy[i] = self.name
                if self.isWinner(copy, self.name):
                    return i
            else:
                copy[i] = ' '
        # Check if the player could win on his next move, and block them.
        for i in possibleMoves:
            copy = board[:]
            if self.isSpaceFree(copy, i):
                copy[i] = self.opponent
                if self.isWinner(copy, self.opponent):
                    return i
                else:
                    copy[i] = ' '
        # Try to take the center, if it is free.
        if self.isSpaceFree(board, 4):
            return 4
        # Try to take one of the corners, if they are free.
        corners = [0, 2, 6, 8]
        for corner in corners:
            if self.isSpaceFree(board, corner):
                return corner
        # Move on one of the sides.
        return self.chooseRandomly([1, 3, 5, 7])


    def randomMove(self, board):
        # get all open spaces
        possibleMoves = self.possibleNextMoves(board)
        # pick a move randomly
        move = self.chooseRandomly(possibleMoves)
        # return the move chosen by the player
        return move


    def move(self, board):
        return self.fullMinimax(board, self.name)[0]


#Sets Up Game
def main():
    print("Welcome to Tic-Tac-Toe")
    p1 = Player('X')
    p2 = Machine('O')
    myBoard = Board(p1,p2)
    myBoard.play()

if __name__ == "__main__":
    main()


