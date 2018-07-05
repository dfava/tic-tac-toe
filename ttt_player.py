__author__  = "Daniel S. Fava"
__license__ = "License: CC BY 4.0, https://creativecommons.org/licenses/by/4.0/"
__year__    = "2018"

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

  def __init__(self, p):
    self.p = p

  def play(self,b):
    self.stats = {}
    cs = b.get_children()
    for c in cs:
      self.stats[c] = {b.p1 : 0, b.p2 : 0}
      ds = c.get_descendants()
      for d in ds:
        w = d.who_won()
        if w != None:
          self.stats[c][w] += 1
    best_score = -1
    best_board = None
    for el in self.stats:
      if self.stats[el][self.p] > best_score:
        best_board = el
        best_score = self.stats[el][self.p]
    play = get_play_from_parent_and_child(b,best_board)
    return play


class BPlayer(ttt.AbsPlayer):
  '''
Play a square (i,j) if the adversary can win on the next move by playing on (i,j),
else, play according to APlayer.
  '''

  def __init__(self, p):
    self.p = p

  def play(self,b):
    self.stats = {}
    cs = b.get_children()
    # Defense first
    for c in cs:
      gcs = c.get_children() # grand-children
      for gc in gcs:
        if gc.who_won() != None and gc.who_won() != self.p:
          # The adversary can win if we play according to c
          # Try to defend
          return get_play_from_parent_and_child(c,gc)

    # Now think about attack
    for c in cs:
      self.stats[c] = {b.p1 : 0, b.p2 : 0}
      ds = c.get_descendants()
      for d in ds:
        w = d.who_won()
        if w != None:
          self.stats[c][w] += 1
    best_score = -1
    best_board = None
    for el in self.stats:
      if self.stats[el][self.p] > best_score:
        best_board = el
        best_score = self.stats[el][self.p]
    return get_play_from_parent_and_child(b,best_board)


if __name__ == "__main__":
  ap = BPlayer(ttt.Board.default_p1)
  ap.play(ttt.Board())
