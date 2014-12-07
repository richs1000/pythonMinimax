__author__ = 'rsimpson'


"""
I started with minimax code that I found here:
http://callmesaint.com/python-minimax-tutorial/
That code was written by Matthew Griffin

Then I added in code I got from here:
https://inventwithpython.com/tictactoe.py
That code was written by Al Sweigart
"""

import random

#Board Class
#Used as a container for the Game
#Matches Stores how many matches the game starts out with
#Limit stores how many matches a player may take per turn
#p1 and p2 are Player (or MachinePlayer) objects
#Use the Play method to start the game
class Board(object):

  def __init__(self,p1,p2):
    self.p1 = p1
    self.p2 = p2
    self.board = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
    #self.board = ['X', 'O', 'X', 'X', 'O', ' ', 'O', ' ', ' ']

  def makeMove(self, letter, move):
    # make sure move is in bounds
    if move in range(0, 9):
      # set the value of board to the player's letter
      self.board[move] = letter

  def drawBoard(self):
    # This function prints out the board that it was passed.
    # "board" is a 9-character string representing the board
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
    # Given a board and a player's letter, this function returns True if that player has won.
    # We use bo instead of board and le instead of letter so we don't have to type as much.
    bo = self.board
    return ((bo[0] == le and bo[1] == le and bo[2] == le) or # across the top
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
      # Return true if the passed move is free on the passed board.
      return self.board[move] == ' '

  def isBoardFull(self):
    # Return True if every space on the board has been taken. Otherwise return False.
    for i in range(0, 9):
      if self.isSpaceFree(i):
        return False
    return True

  def play(self):
    def switchPlayer(player):
      if(player is self.p1): return self.p2
      else: return self.p1

    player = self.p1
    while(True):
      #Print number of matches and tell player it's their turn
      self.drawBoard()
      print("Your move, " + player.name)
      #Get Player's Move (int)
      move = player.move(self.board)
      self.makeMove(player.name, move)

      if self.isWinner(player.name):
        self.drawBoard()
        self.win(player)
        break
      elif self.isBoardFull():
        self.drawBoard()
        print('The game is a tie!')
        break
      else:
        player = switchPlayer(player)

  def win(self,player):
    print(player.name + " won!")


#Human Player Class
#Name Simply differentiates between first and second player
#Move method gets user input as move
class Player():
  def __init__(self, myName, opponentName):
    self.name = myName
    self.opponent = opponentName

  def isSpaceFree(self, board, move):
    # make sure move is in bounds
    if move in range(0, 9):
      # Return true if the passed move is free on the passed board.
      return board[move] == ' '

  def move(self, board):
    # Let the player type in his move.
    move = -1
    while (int(move) not in range(0, 9)) or (not self.isSpaceFree(board, int(move))):
      move = int(raw_input("Choose a square: ")) - 1
    return int(move)


#Machine Player Class
#Uses Minimax to search Game Tree
#Best Variable stores best score and best move to get that score.
#best[0] is best score, and best[1] is associated move
#A positive 1 score represents a win for self
#A negative 1 score represents a win for oppoenet
#0 represents self, 1 represents opponent -- stored in side variable
class Machine(Player):
  def __init__(self, name, opponent):
    # call constructor for parent class
    Player.__init__(self, name, opponent)


  def chooseRandomly(self, moves):
    # pick a move randomly
    moveIndex = random.randint(0, len(moves))
    # send it back
    return moves[moveIndex]


  def isWinner(self, bo, le):
    # Given a board and a player's letter, this function returns True if that player has won.
    # We use bo instead of board and le instead of letter so we don't have to type as much.
    return ((bo[0] == le and bo[1] == le and bo[2] == le) or # across the top
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
  p1 = Player('X' ,'O')
  p2 = Machine('O', 'X')
  myBoard = Board(p1,p2)
  myBoard.play()

if __name__ == "__main__":
  main()


