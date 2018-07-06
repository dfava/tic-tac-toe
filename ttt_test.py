#!/usr/bin/env python3

import sys
import unittest

import ttt

class TttTest(unittest.TestCase):

    def test_get_empty_idxs(self):
      b = ttt.Board()
      self.assertEqual(b.get_empty_idxs(), [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)])

      b=b.play(0,0)
      self.assertEqual(b.get_empty_idxs(), [(0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)])

    def test_who_won(self):
      b = ttt.Board()
      self.assertEqual(b.who_won(), None)
      b=b.play(1,1)
      b=b.play(1,0)
      b=b.play(2,2)
      self.assertEqual(b.who_won(), None)
      b=b.play(0,0)
      b=b.play(0,2)
      b=b.play(2,0)
      self.assertEqual(b.who_won(), 'o')

    def test_is_over(self):
      # Cases of "over" because someone won
      b = ttt.Board()
      self.assertFalse(b.is_over())
      b=b.play(1,1)
      b=b.play(1,0)
      b=b.play(2,2)
      self.assertFalse(b.is_over())
      b=b.play(0,0)
      b=b.play(0,2)
      b=b.play(2,0)
      self.assertTrue(b.is_over())
     
      # Cases of "over" because the board is full
      b = ttt.Board()
      for r in [0,2,1]:
        for c in range(0,3):
          b=b.play(r,c)
      self.assertTrue(b.is_over())


    def test_next_player(self):
      b = ttt.Board()
      self.assertEqual(b.next_player(), b.p1)
      b=b.play(1,1)
      self.assertEqual(b.next_player(), b.p2)
      b=b.play(1,0)
      self.assertEqual(b.next_player(), b.p1)
      b=b.play(2,2)
      self.assertEqual(b.next_player(), b.p2)
      b=b.play(0,0)
      b=b.play(2,0)
      self.assertEqual(b.next_player(), b.p2)
      b=b.play(0,1)
      self.assertEqual(b.next_player(), b.p1)
      b=b.play(0,2)
      self.assertEqual(b.next_player(), None)

    def test_get_children(self):
      b = ttt.Board()
      bs = b.get_children()
      answer = [ ((b.p1, b.e, b.e),(b.e, b.e, b.e),(b.e, b.e, b.e)),
                 ((b.e, b.p1, b.e),(b.e, b.e, b.e),(b.e, b.e, b.e)),
                 ((b.e, b.e, b.p1),(b.e, b.e, b.e),(b.e, b.e, b.e)),
                 ((b.e, b.e, b.e),(b.p1, b.e, b.e),(b.e, b.e, b.e)),
                 ((b.e, b.e, b.e),(b.e, b.p1, b.e),(b.e, b.e, b.e)),
                 ((b.e, b.e, b.e),(b.e, b.e, b.p1),(b.e, b.e, b.e)),
                 ((b.e, b.e, b.e),(b.e, b.e, b.e),(b.p1, b.e, b.e)),
                 ((b.e, b.e, b.e),(b.e, b.e, b.e),(b.e, b.p1, b.e)),
                 ((b.e, b.e, b.e),(b.e, b.e, b.e),(b.e, b.e, b.p1)),
              ]
      for idx,b in enumerate(bs):
        self.assertIn(b.b, answer)

    def test_equality(self):
      b1 = ttt.Board()
      b2 = ttt.Board()
      s = set([b1])
      self.assertEqual(b1, b2)
      self.assertIn(b1, s)
      self.assertIn(b2, s)

    def test_is_empty(self):
      ori_b = ttt.Board()
      self.assertTrue(ori_b.is_empty())
      b=ori_b.play(0,1)
      self.assertFalse(b.is_empty())
      self.assertTrue(ori_b.is_empty())

    def test_play(self):
      ori_b = ttt.Board()
      b = ori_b.play(0,0)
      # Make sure old board has not changed
      self.assertEqual(ori_b, ttt.Board())
      try:
        b=b.play(0,0)
        self.assertTrue(False) # Execution must not reach here
      except RuntimeWarning:
        pass
      b=b.play(0,1) 
      b=b.play(1,0) 
      b=b.play(1,1) 
      b=b.play(2,0) 
      try:
        b=b.play(2,1) 
        self.assertTrue(False) # Execution must not reach here
      except RuntimeWarning:
        pass

    def test_get_descendants(self):
      bs = ttt.Board().get_descendants()
      #for b in bs:
      #  print(b)
      #  print()
      #print(len(bs))
      self.assertEqual(len(bs), 5478)
      
      p1 = [b for b in bs if b.who_won() == b.p1]
      #for b in p1: print(b); print()
      #print(len(p1))
      self.assertEqual(len(p1), 626)

      p2 = [b for b in bs if b.who_won() == b.p2]
      #for b in p2: print(b); print()
      #print(len(p2))
      self.assertEqual(len(p2), 316)

      cats = [b for b in bs if b.who_won() == None and b.is_over()]
      #for b in cats: print(b); print()
      #print(len(cats))
      self.assertEqual(len(cats), 16)

    def test_le(self):
      b1 = ttt.Board()
      b2 = ttt.Board()
      self.assertTrue(b1 <= b2)
      self.assertTrue(b2 <= b1)
      b2=b2.play(1,1)
      self.assertFalse(b2 <= b1)
      b1=b1.play(1,1)
      self.assertTrue(b1 <= b2)
      self.assertTrue(b2 <= b1)

    def test_get_input(self):
      options = (
          (lambda v: int(v) in [0,1,2], 'Player 1: ', 'Value must be in [0,1,2]'),
          )
      for o in options:
        ttt.get_input(o[0],o[1],o[2])
    

if __name__ == "__main__":
  test = unittest.TestLoader().loadTestsFromName("ttt_test.TttTest.test_get_input")
  unittest.TextTestRunner().run(test)
  #unittest.main()
