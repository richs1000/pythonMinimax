__author__ = 'rsimpson'

from ticTacToePlayer import *

import random

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


