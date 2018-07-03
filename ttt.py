#!/usr/bin/env python3

import sys
import copy

# In general, we'll abreviate the word board by b, so printb stands for "print board"

class Board():
  
  def __init__(self, e=' ', p1='x', p2='o'):
    '''New empty board'''
    self.e = e
    self.p1 = p1
    self.p2 = p2
    self.b = [[e, e, e], [e, e, e], [e, e, e]]

  @classmethod
  def new(cls, b2):
    '''New board with the same board configuration as b2'''
    b = Board(e=b2.e)
    b.b = copy.deepcopy(b2.b)
    return b

  def next_player(self):
    '''Determine who may be the next player.
If the game is over (i.e. someone won or the board is full), return the empty list
If player A played one less time than player B, then it is player A's turn.
If player A played the same number of times as B, then it may be player A's or player B's turns (we don't know for sure which).'''
    if self.is_over():
      return []
    p1cnt = len([1 for i in range(0,3) for j in range(0,3) if self.b[i][j] == self.p1])
    p2cnt = len([1 for i in range(0,3) for j in range(0,3) if self.b[i][j] == self.p2])
    if p1cnt > p2cnt: return [self.p2]
    elif p2cnt > p1cnt: return [self.p1]
    else: return [self.p1, self.p2]

  def __str__(self):
    return str(self.b[0]) + '\n' + str(self.b[1]) + '\n' + str(self.b[2])

  def is_over(self):
    '''Return true if the board is full or one of the players won'''
    return self.is_full() or self.who_won() != None

  def is_full(self):
    '''Return true if the board is full'''
    return self.get_empty_idxs() == []

  def who_won(self):
    '''Return p if game has been won by a player p, None otherwise'''
    # Columns
    for c in range(0,3):
      if self.b[0][c] != self.e and (self.b[0][c] == self.b[1][c] == self.b[2][c]): return self.b[0][c]
    # Rows
    for r in range(0,3):
      if self.b[r][0] != self.e and (self.b[r][0] == self.b[r][1] == self.b[r][2]): return self.b[r][0]

    # Diagonals
    if self.b[1][1] != self.e and \
          ((self.b[0][0] == self.b[1][1] == self.b[2][2]) or \
           (self.b[0][2] == self.b[1][1] == self.b[2][0])):
      return self.b[1][1]

  def get_empty_idxs(self):
    '''Return list of empty places in the board'''
    return [(i,j) for i in range(0,3) for j in range(0,3) if self.b[i][j] == self.e]

  def __getitem__(self, i):
    if type(i) == int:
      return self.b[i]
    if type(i) == tuple:
      return self.b[i[0]][i[1]]
    assert(0)

  def __setitem__(self, i, v):
    if type(i) == tuple:
      self.b[i[0]][i[1]] = v
      return
    assert(0)


def enum_confs():
  '''Enumerate all possible tic-tac-toe board configurations.
Play starts with player X.'''
  prev_itr_bs = [ Board() ]
  bs = prev_itr_bs
  # TODO: This is computing the same configuration more than once
  # Careful not to compute the same configuration via two different paths
  for play in [1,2,3,4,5,6,7]:#range(1,10):
    new_bs = []
    player = 'X' if play % 2 == 0 else 'O'
    print(player)
    for b in prev_itr_bs: 
      if b.is_over():
        continue
      empties = b.get_empty_idxs()
      for e in empties:
        nb = Board.new(b)
        nb[e] = player
        new_bs.append(nb)
        print(nb)
        if nb.is_over(): print("Over!"); input()
        print()
    prev_itr_bs = new_bs
    bs += new_bs
    #print(bs)
    #sys.exit(0)
  return bs


def main(argv):
  print("Hello world")
  enum_confs()

if __name__ == '__main__':
  sys.exit(main(sys.argv))
