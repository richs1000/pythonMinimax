__author__ = 'rsimpson'


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


