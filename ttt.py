#!/usr/bin/env python3
__author__  = "Daniel S. Fava"
__license__ = "License: CC BY 4.0, https://creativecommons.org/licenses/by/4.0/"
__year__    = "2018"

import sys
import abc
import copy

class Board():

  default_p1 = 'x'
  default_p2 = 'o'

  @classmethod
  def enum_confs():
    '''Enumerate all possible tic-tac-toe board configurations.
Play starts with player p1.'''
    b = Board()
    return b.get_descendants()

  def __init__(self, b=None, e=' ', p1=default_p1, p2=default_p2, it=0):
    '''New board.  If b is None, start with an empty board.
Does not check for validity of the board; user can pass, for example, a board configuration that does not make sense, or value of it that is not consistent with the passed board configuration.'''
    self.e = e
    self.p1 = p1
    self.p2 = p2
    if b==None:
      self.b = ((e, e, e), (e, e, e), (e, e, e))
    else:
      self.b = b
    self.it = it # Iteration of the game

  def __hash__(self):
    map_val = {self.e : '0', self.p1 : '1', self.p2 : '2'}
    return int('1' + ''.join([map_val[el] for r in self.b for el in r]))

  def __eq__(self, other):
    '''Boards are equal if their hashes are equal'''
    return hash(self) == hash(other)

  def __le__(self, other):
    for idx_r,r in enumerate(self.b):
      for idx_c,el in enumerate(r):
        le = el == other[idx_r][idx_c] or el == self.e
        if not le: return False
    return True

  def play(self, i, j=0):
    # A bit of a hack here (of the good kind).
    # Usually we assume play() will be called with two arguments i and j,
    # the first being a row index and the seconds a column index.
    # But, we also want to support calling play() with a tuple (i,j) or list [i,j].
    # To support the tuple, we check if i is a tuple/list,
    # and then unpack the tuple/list on the local variables i and j
    if type(i) == list or type(i) == tuple:
      j = i[1]
      i = i[0]
    player = self.next_player()
    if player == None:
      raise RuntimeWarning("Function play() was called on a game that is over.")
    if self.b[i][j] != self.e:
      raise RuntimeWarning("Board not empty at position (%d,%d)" % (i,j))
    new_board = []
    for r_idx,r in enumerate(self.b):
      if r_idx == i:
        new_board.append(tuple([el if el_idx!=j else player for el_idx,el in enumerate(r)]))
      else:
        new_board.append(r)
    return Board(b=tuple(new_board), e=self.e, p1=self.p1, p2=self.p2, it=self.it+1)

  def get_children(self):
    '''Return all possible children of the given board configuration.'''
    player = self.next_player()
    if player == None: return []
    children = []
    idxs = self.get_empty_idxs()
    for idx in idxs:
      nb = self.play(idx)
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

  def next_player(self):
    '''Determine who may be the next player.
If the game is over (i.e. someone won or the board is full), return the empty list
If player A played one less time than player B, then it is player A's turn.
If player A played the same number of times as B, then it may be player A's or player B's turns (we don't know for sure which).'''
    if self.is_over(): return None
    if self.it % 2 == 0: return self.p1
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


class AbsPlayer(metaclass=abc.ABCMeta):
  name = "Abstract player"

  @abc.abstractmethod
  def __init__(self, p, params):
    raise NotImplementedError('Must first implement abstract methods before using it')

  @abc.abstractmethod
  def start(self):
    raise NotImplementedError('Must first implement abstract methods before using it')

  @abc.abstractmethod
  def play(self, b):
    raise NotImplementedError('Must first implement abstract methods before using it')

def get_input(validate, default, message, err_message):
  '''Read inputs from the user:
validate: a function that takes a string and attempts to transform it into a value in an expected type, and then check if the value is in an expected range.  If so, return the transformed/validated value
message: a message to prompt the user with
err_message: an error message when validate() fails on an input
    '''
  if default != None:
    message = message % default
  while True:
    val_v = input(message)
    if val_v == '' and default != None: return default # User chose default
    try:
      return validate(val_v) 
    except ValueError:
      print(err_message);

class TerminalPlayer(AbsPlayer):
  name = "Human player"
  validate_func = lambda v: int(v) if int(v) in [0,1,2] else int('raise value error')
  validate_err_msg = 'Invalid play. Value must be in [0,1,2]. Try again.'

  def __init__(self, p, params=None):
    self.p = p
    if params != None: raise ValueError("Player does not take parameters.")

  def start(self):
    pass

  def play(self, b):
    print(b)
    print('Player %s' % self.p)
    r = get_input(TerminalPlayer.validate_func, None, 'row: ', TerminalPlayer.validate_err_msg)
    c = get_input(TerminalPlayer.validate_func, None, 'col: ', TerminalPlayer.validate_err_msg)
    return (r,c)

class Game():

  def __init__(self, p1, p2):
    self.b = Board()
    self.ps = (p1,p2)

  def start(self, verbose=False):
    self.ps[0].start()
    self.ps[1].start()
    it = 0
    if verbose: print(self.b);print()
    while not self.b.is_over():
      (r,c) = self.ps[it % 2].play(self.b)
      try:
        self.b = self.b.play(r,c)
        if verbose: print(self.b);print()
      except RuntimeWarning as e:
        print(e)
        continue
      it = it + 1

  def __str__(self):
    string = "%s\n" % self.b
    if self.b.is_over():
      winner = self.b.who_won()
      if winner == None:
        string += "Cat's game"
      else:
        string += "Player %s won" % winner
    else:
      string += "Game in progress"
    return string


import ttt_player

def main(argv):
  options = ( TerminalPlayer,
              ttt_player.APlayer, 
              ttt_player.DPlayer, 
              ttt_player.ADPlayer,
              ttt_player.DRPlayer,
              ttt_player.RLPlayer )
  validate_func = lambda v: int(v) if int(v) in range(0,len(options)) else int('raise value error')
  for idx,o in enumerate(options):
    print("%d %s" % (idx, o.name))
  p_class = []
  p_params = []
  for idx in range(0,2):
    p_class.append(options[get_input(validate_func, None, "Select player %d: " % (idx+1), 
        "Invalid player.  Must be a number from 0 to %d. Try again." % (len(options)-1))])
    # Prompt user for his given player's parameters.  Some player don't have parameters, some do.
    try:
      params = {} 
      for param in p_class[idx].params:
        params[param] = get_input(
            p_class[idx].params[param]['valfun'],
            p_class[idx].params[param]['def'],
            '  ' + p_class[idx].params[param]['msg'],
            p_class[idx].params[param]['errmsg'],
            )
    except AttributeError:
      params = None # Player does not have parameters
    p_params.append(params)
  g = Game(p_class[0](Board.default_p1, params=p_params[0]), p_class[1](Board.default_p2, params=p_params[1]))
  # If both players are machines, we want verbose==True so that
  # we get board configurations printed to stdout
  verb = p_class[0] != TerminalPlayer and p_class[1] != TerminalPlayer
  g.start(verbose=verb)
  print(g)
  return 0

if __name__ == '__main__':
  sys.exit(main(sys.argv))
