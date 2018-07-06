__author__  = "Daniel S. Fava"
__license__ = "License: CC BY 4.0, https://creativecommons.org/licenses/by/4.0/"
__year__    = "2018"

import random

import ttt

def get_play_from_parent_and_child(p, c):
  for i in range(0,3):
    for j in range(0,3):
      if p.b[i][j] != c.b[i][j]: return (i,j)
  assert(0)

class APlayer(ttt.AbsPlayer):
  '''
Algorithm:
   Given a board b
   Compute all children of b
   For each child c of b,
     get all descendants of c
     add the number of descendatns of c that are winner
   Pick the child c that yields the largest number of winners.

 This player works OK,
 the obvious issue is that it does not play defensively when it is about to lose.
  '''

  name = "Attack only player"

  def __init__(self, p):
    self.p = p

  def play(self,b):
    stats = {}
    cs = b.get_children()
    for c in cs:
      stats[c] = {b.p1 : 0, b.p2 : 0}
      ds = c.get_descendants()
      for d in ds:
        w = d.who_won()
        if w != None:
          stats[c][w] += 1
    best_score = -1
    best_board = None
    for el in stats:
      if stats[el][self.p] > best_score:
        best_board = el
        best_score = stats[el][self.p]
    play = get_play_from_parent_and_child(b,best_board)
    return play


class DPlayer(ttt.AbsPlayer):
  '''
Play a square (i,j) if the adversary can win on the next move by playing on (i,j),
else, play randomly.
  '''

  name = "Defend player, otherwise random"

  def __init__(self, p):
    self.p = p

  def play(self,b):
    cs = b.get_children()
    # Must we need to defend now?
    for c in cs:
      gcs = c.get_children() # grand-children
      for gc in gcs:
        if gc.who_won() != None and gc.who_won() != self.p:
          # The adversary can win if we play according to c
          # Try to defend
          return get_play_from_parent_and_child(c,gc)
    return random.choice(b.get_empty_idxs())


class ADPlayer(ttt.AbsPlayer):
  '''
Play a square (i,j) if we can win in one move, else,
play a square (i,j) if the adversary can win on the next move by playing on (i,j), else
play according to APlayer, which is, play the square that has the largest number of winning descendants.
  '''

  name = "Attack and defend player"

  def __init__(self, p):
    self.p = p

  def play(self,b):
    stats = {}
    cs = b.get_children()
    # Can we win on the next move?
    for c in cs:
      if c.who_won() == self.p:
        return get_play_from_parent_and_child(b,c)
    # Must we need to defend now?
    for c in cs:
      gcs = c.get_children() # grand-children
      for gc in gcs:
        if gc.who_won() != None and gc.who_won() != self.p:
          # The adversary can win if we play according to c
          # Try to defend
          return get_play_from_parent_and_child(c,gc)
    # Otherwise, play on the square with largest number of winning descendants
    for c in cs:
      stats[c] = {b.p1 : 0, b.p2 : 0, None : 0}
      ds = c.get_descendants()
      for d in ds:
        stats[c][d.who_won()] += 1
    best_score = -1
    best_board = None
    for el in stats:
      if stats[el][self.p] > best_score:
        best_board = el
        best_score = stats[el][self.p]
    return get_play_from_parent_and_child(b,best_board)

class DRPlayer(ttt.AbsPlayer):

  name = "Discounted reward player"

  def __init__(self, p, discount_rate=1):
    self.p = p
    self.dr = discount_rate

  def play(self, b):
    best_b = None
    best_reward = -float("inf")
    cs = b.get_children()
    for c in cs:
      tmp = self.compute_reward(c)
      if best_reward < tmp:
        best_reward = tmp
        best_b = c
    assert(best_b != None)
    return get_play_from_parent_and_child(b,best_b)

  def compute_reward(self, b):
    if b.is_over():
      w = b.who_won()
      if w == None: return 0
      elif w == self.p: return 1
      else: return -1
    reward = 0
    cs = b.get_children()
    for c in cs:
      reward += self.compute_reward(c)
    return self.dr * reward


if __name__ == "__main__":
  #ap = APlayer(ttt.Board.default_p1)
  #ap = DPlayer(ttt.Board.default_p1)
  #ap = ADPlayer(ttt.Board.default_p1)
  ap = DRPlayer(ttt.Board.default_p1)
  ap.play(ttt.Board())
