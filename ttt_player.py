import ttt

# Notation:
# Let b + (i,j) represent the board b' that matches b everywhere except for at (i,j),
# b'(i,j) will be equal to b.get_next_player()
#
# The play function works as follows.
# Algorithm:
#   Let idxs be the list of empty slots in the board
#   For every configuration b' + (i,j) for (i,j) in idx
#     Compute the descendents of b' + (i,j), and, from the descendents,
#     the fraction of winnning descendants
#     Pick (i,j) that yields the largest fraction
#     Else, if there are no winning descendants, pick the (i,j) with the largest fraction of draws
#     Else, pick at random

class APlayer(ttt.AbsPlayer):

  def __init__(self, p):
    self.p = p

  def get_play_from_parent_and_child(self, p, c):
    for i in range(0,3):
      for j in range(0,3):
        if p.b[i][j] != c.b[i][j]: return (i,j)
    assert(0)

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
    play = self.get_play_from_parent_and_child(b,best_board)
    return play

if __name__ == "__main__":
  print("APlayer!")
  ap = APlayer(ttt.Board.default_p1)
  ap.play(ttt.Board())
