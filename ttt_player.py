__author__ ="Daniel S. Fava"
__license__="License: CC BY 4.0, https://creativecommons.org/licenses/by/4.0/"
__year__   ="2018"

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
   Pick the child c that yields the largest fraction of winners.

This player works OK,  the obvious issue is that
the player does not play defensively when it is about to lose.
  '''

  name = "Attack only player"

  def __init__(self, p, params=None):
    self.p = p
    if params != None: raise ValueError("Player does not take parameters.")

  def start(self):
    pass

  def play(self,b):
    stats = {}
    cs = b.get_children()
    for c in cs:
      stats[c] = {b.p1 : 0.0, b.p2 : 0.0, None : 0.0}
      ds = c.get_descendants()
      for d in ds:
        stats[c][d.who_won()] += 1
      total = stats[c][None] + stats[c][b.p1] + stats[c][b.p2]
      stats[c][None] = stats[c][None] / total
      stats[c][b.p1] = stats[c][b.p1] / total
      stats[c][b.p2] = stats[c][b.p2] / total
    best_score = -float("inf")
    best_board = None
    for el in stats:
      if stats[el][self.p] > best_score:
        best_board = el
        best_score = stats[el][self.p]
    play = get_play_from_parent_and_child(b,best_board)
    return play


class DPlayer(ttt.AbsPlayer):
  '''
Play (i,j) if the adversary can win on the next move by playing on (i,j),
else, play randomly.
  '''

  name = "Defend player, otherwise random"

  def __init__(self, p, params=None):
    self.p = p
    if params != None: raise ValueError("Player does not take parameters.")

  def start(self):
    pass

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
play (i,j) if the adversary can win on the next move by playing on (i,j), else
play according to APlayer, which means, play the square that has
the largest number of winning descendants.
  '''

  name = "Attack and defend player"

  def __init__(self, p, params=None):
    self.p = p
    if params != None: raise ValueError("Player does not take parameters.")

  def start(self):
    pass

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
    # Otherwise, play on the square with largest fraction of winning descendants
    for c in cs:
      stats[c] = {b.p1 : 0.0, b.p2 : 0.0, None : 0.0}
      ds = c.get_descendants()
      for d in ds:
        stats[c][d.who_won()] += 1
      total = stats[c][None] + stats[c][b.p1] + stats[c][b.p2]
      stats[c][None] = stats[c][None] / total
      stats[c][b.p1] = stats[c][b.p1] / total
      stats[c][b.p2] = stats[c][b.p2] / total
    best_score = -float("inf")
    best_board = None
    for el in stats:
      if stats[el][self.p] > best_score:
        best_board = el
        best_score = stats[el][self.p]
    return get_play_from_parent_and_child(b,best_board)

class DRPlayer(ttt.AbsPlayer):
  '''Applies discount on future rewards for loss/tie/win.'''

  name = "Discounted reward player"

  # Default parameters
  # dr -> discounted return rate
  # win -> reward for winning
  # tie -> reward for tie
  # los -> reward for loosing
  params = {'dr': 
              {'valfun' : lambda v: float(v) if float(v) > 0 and float(v) <= 1 else int('raise value error'),
               'def' : 0.96,
               'msg' : 'Choose a discount reward rate in (0,1], default %.2f: ',
               'errmsg' : 'Invalid rate.  Must be greater than 0 and less than or equal to 1.  Try again.'},
            'win':
              {'valfun' : lambda v: float(v),
               'def' : 1,
               'msg' : 'Choose a floating point number as reward for winning, default %.2f: ',
               'errmsg' : 'Invalid reward.  Must be a number.  Try again.'},
            'tie':
              {'valfun' : lambda v: float(v),
               'def' : 0,
               'msg' : 'Choose a floating point number as reward for tie, default %.2f: ',
               'errmsg' : 'Invalid reward.  Must be a number.  Try again.'},
            'los':
              {'valfun' : lambda v: float(v),
               'def' : -1,
               'msg' : 'Choose a floating point number as reward for loosing, default %.2f: ',
               'errmsg' : 'Invalid reward.  Must be a number.  Try again.'},
            }

  def __init__(self, p, params={}):
    self.p = p
    self.params = {}
    for param in DRPlayer.params:
      self.params[param] = DRPlayer.params[param]['def'] # Set params to default
    # If parameters have been passed to constructure, then override the parameter here
    for param in params:
      self.params[param] = params[param]
    self.rewards = {}

  def start(self):
    pass

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
    try: return self.rewards[b]  # Try to return a precomputed reward
    except KeyError: pass # if reward has not been pre-computed, compute it..

    if b.is_over():
      w = b.who_won()
      if w == None: return self.params['tie']
      elif w == self.p: return self.params['win']
      else: return self.params['los']
    cs = b.get_children()
    reward = 0.0;
    for c in cs:
      reward += self.compute_reward(c)
    reward = reward / len(cs) # reward as the average of children's reward
    self.rewards[b] = self.params['dr'] * reward
    return self.rewards[b]

# TODO:
# Idea for a new player: learn the win, tie, los parameters
# Idea for another player:
#   don't simulate the games, learn from playing.
#   So the player's performance starts poor,
#   and improves from playing against others.

class RLPlayer(ttt.AbsPlayer):

  name = "Reinforcement learning player"

  # TODO: Think about having an adjustable learn rate, one that decreases with time
  params = {'lr': 
              {'valfun' : lambda v: float(v) if float(v) >= 0 and float(v) < 1 else int('raise value error'),
               'def' : 0.05,
               'msg' : 'Choose a learn rate in [0,1), default %.2f: ',
               'errmsg' : 'Invalid rate.  Must be greater or equal to 0 and less than 1.  Try again.'},
            }

  def __init__(self, p, params={}):
    self.p = p
    self.params = {}
    for param in DRPlayer.params:
      self.params[param] = DRPlayer.params[param]['def'] # Set params to default
    # If parameters have been passed to constructure, then override the parameter here
    for param in params:
      self.params[param] = params[param]
    self.rewards = {}
    self.prev_b = None

  def start(self):
    self.prev_b = None

  # TODO: Sometimes don't pick the best play but a random one (exploration)
  # TODO: If there is more than one "best option", randomly pick among them
  def play(self, b):
    best_b = None
    best_reward = -float("inf")
    cs = b.get_children()
    for c in cs:
      if c not in self.rewards:
        if c.who_won() == self.p:
          self.rewards[c] = 1.0
        elif c.who_won() != None: # We lost
          self.rewards[c] = 0.0
        else:
          self.rewards[c] = 0.5 # coin-toss
      tmp = self.rewards[c]
      if best_reward < tmp:
        best_reward = tmp
        best_b = c
    assert(best_b != None)
    if self.prev_b != None:
      self.rewards[self.prev_b] += self.params['lr'] * (self.rewards[best_b] 
                                    - self.rewards[self.prev_b])
    self.prev_b = best_b
    return get_play_from_parent_and_child(b,best_b)



if __name__ == "__main__":
  #ap = APlayer(ttt.Board.default_p1)
  #ap = DPlayer(ttt.Board.default_p1)
  #ap = ADPlayer(ttt.Board.default_p1)
  ap = DRPlayer(ttt.Board.default_p1)
  ap.play(ttt.Board())
