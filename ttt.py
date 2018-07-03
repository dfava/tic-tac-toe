#!/usr/bin/env python3
__author__  = "Daniel S. Fava"
__license__ = "License: CC BY 4.0, https://creativecommons.org/licenses/by/4.0/"
__year__    = "2018"

import sys
import copy

class Board():

  @classmethod
  def enum_confs(p1='x', p2='o'):
    '''Enumerate all possible tic-tac-toe board configurations.
Play starts with player p1.'''
    b = Board()
    return b.get_descendants()
  
  def __hash__(self):
    '''Board hashes take into account the board configuration, the element e, p1, and p2.
Since lists are not hashable, we convert the board conf to tuples.
Note that boards are mutable, so their hashes can change over time;
therefore, putting boards in sets or using boards as keys to dicts can be "dangerous" given that the board can later be modified.'''
    return hash( (tuple(self.b[0]), tuple(self.b[1]), tuple(self.b[2]), self.e, self.p1, self.p2) )

  def __eq__(self, other):
    '''Boards are equal if their hashes are equal'''
    return hash(self) == hash(other)

  def __init__(self, e=' ', p1='x', p2='o'):
    '''New empty board'''
    self.e = e
    self.p1 = p1
    self.p2 = p2
    self.b = [[e, e, e], [e, e, e], [e, e, e]]
    self.iteration = 0

  def get_children(self):
    '''Return all possible children of the given board configuration.'''
    player = self.next_player()
    if player == None: return []
    children = []
    idxs = self.get_empty_idxs()
    for idx in idxs:
      nb = Board.new(self)
      nb[idx] = player; nb.iteration += 1
      children.append(nb)
    return children

  def get_descendants(self):
    '''Return all descendants of the given board.'''
    processed_lst = []  # Keeping a list simply because I like to see elements somewhat in order
    processed = set() 
    to_process = [self] # Add current board to "to_process"
    while len(to_process) != 0:
      # Remove a conf from to_process
      b_to_process = to_process.pop()
      processed.add(b_to_process)
      processed_lst.append(b_to_process)
      children = b_to_process.get_children()
      # For every board b in bs not already in "processed", add b to "to_process"
      for b in children:
        if b not in processed:
          to_process.append(b)
    return processed_lst

  @classmethod
  def new(cls, b2):
    '''New board with the same board configuration as b2'''
    b = Board(e=b2.e, p1=b2.p1, p2=b2.p2)
    b.iteration = b2.iteration
    b.b = copy.deepcopy(b2.b)
    return b

  def next_player(self):
    '''Determine who may be the next player.
If the game is over (i.e. someone won or the board is full), return the empty list
If player A played one less time than player B, then it is player A's turn.
If player A played the same number of times as B, then it may be player A's or player B's turns (we don't know for sure which).'''
    # Special case for handling the fact that p1 is the starting player
    if self.is_over(): return None
    if self.iteration % 2 == 0: return self.p1
    else: return self.p2

  def __str__(self):
    return str(self.b[0]) + '\n' + str(self.b[1]) + '\n' + str(self.b[2])

  def is_over(self):
    '''A check for whether the game is over.
Returns true if the board is full or one of the players won; returns false otherwise.'''
    return self.is_full() or self.who_won() != None

  def is_empty(self):
    return len(self.get_empty_idxs()) == 9

  def is_full(self):
    '''Return true if the board is full.'''
    return self.get_empty_idxs() == []

  def who_won(self):
    '''Return p if game has been won by a player p; None otherwise (i.e. no player has won the game)'''
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


def main(argv):
  print("ttt")
  return 0

if __name__ == '__main__':
  sys.exit(main(sys.argv))
