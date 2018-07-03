#!/usr/bin/env python3

import sys
import unittest

import ttt

class TttTest(unittest.TestCase):

    def test_new(self):
      b = ttt.Board()
      b[0][0] = 'x'
      b2 = ttt.Board.new(b)
      b2[0][1] = 'o'
      # A change to the new board does not modify the old one
      self.assertEqual(b.get_empty_idxs(), [(0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)])
      # The new board has the old board's element plus its new change
      self.assertEqual(b2[0][0], 'x')
      self.assertEqual(b2.get_empty_idxs(), [(0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)])

    def test_get_empty_idxs(self):
      b = ttt.Board()
      self.assertEqual(b.get_empty_idxs(), [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)])

      b[0][0] = 'x'
      self.assertEqual(b.get_empty_idxs(), [(0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)])

    def test_who_won(self):
      b = ttt.Board()
      self.assertEqual(b.who_won(), None)
      b[1][1] = 'x'
      b[2][2] = 'x'
      self.assertEqual(b.who_won(), None)
      b[0][0] = 'x'
      b[2][0] = 'o'
      b[1][1] = 'o'
      b[0][2] = 'o'
      self.assertEqual(b.who_won(), 'o')
      b[1][0] = 'x'
      b[2][0] = 'x'
      self.assertEqual(b.who_won(), 'x')

    def test_is_over(self):
      b = ttt.Board()
      # Cases of "over" because someone won
      self.assertFalse(b.is_over())
      b[1][1] = 'x'
      b[2][2] = 'x'
      self.assertFalse((b.is_over()))
      b[0][0] = 'x'
      b[2][0] = 'o'
      b[1][1] = 'o'
      b[0][2] = 'o'
      self.assertTrue(b.is_over())
      b[1][0] = 'x'
      b[2][0] = 'x'
      self.assertTrue(b.is_over())

      # Cases of "over" because someone won or the board was full
      b = ttt.Board()
      self.assertFalse(b.is_over())
      b[1][1] = b.p1
      self.assertFalse(b.is_over())
      b[1][0] = b.p2
      self.assertFalse(b.is_over())
      b[2][2] = b.p2
      self.assertFalse(b.is_over())
      b[0][0] = b.p2
      b[2][0] = b.p2
      b[2][0] = b.p1
      self.assertFalse(b.is_over())
      b[0][1] = b.p1
      self.assertFalse(b.is_over())
      b[0][2] = b.p2
      self.assertFalse(b.is_over())
      b[1][2] = b.p1
      self.assertFalse(b.is_over())
      b[2][1] = b.p2
      self.assertTrue(b.is_over())


    def test_next_player(self):
      b = ttt.Board()
      self.assertEqual(b.next_player(), b.p1)
      b[1][1] = b.p1; b.iteration += 1
      self.assertEqual(b.next_player(), b.p2)
      b[1][0] = b.p2; b.iteration += 1
      self.assertEqual(b.next_player(), b.p1)
      b[2][2] = b.p1; b.iteration += 1
      self.assertEqual(b.next_player(), b.p2)
      b[0][0] = b.p2; b.iteration += 1
      b[2][0] = b.p1; b.iteration += 1
      self.assertEqual(b.next_player(), b.p2)
      b[0][1] = b.p2; b.iteration += 1
      self.assertEqual(b.next_player(), b.p1)
      b[0][2] = b.p1; b.iteration += 1
      self.assertEqual(b.next_player(), None)

    def test_get_children(self):
      b = ttt.Board()
      bs = b.get_children()
      answer = [ [['x', ' ', ' '],[' ', ' ', ' '],[' ', ' ', ' ']],
                 [[' ', 'x', ' '],[' ', ' ', ' '],[' ', ' ', ' ']],
                 [[' ', ' ', 'x'],[' ', ' ', ' '],[' ', ' ', ' ']],
                 [[' ', ' ', ' '],['x', ' ', ' '],[' ', ' ', ' ']],
                 [[' ', ' ', ' '],[' ', 'x', ' '],[' ', ' ', ' ']],
                 [[' ', ' ', ' '],[' ', ' ', 'x'],[' ', ' ', ' ']],
                 [[' ', ' ', ' '],[' ', ' ', ' '],['x', ' ', ' ']],
                 [[' ', ' ', ' '],[' ', ' ', ' '],[' ', 'x', ' ']],
                 [[' ', ' ', ' '],[' ', ' ', ' '],[' ', ' ', 'x']],
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
      b = ttt.Board()
      self.assertTrue(b.is_empty())
      b[0][1] = b.p1
      self.assertFalse(b.is_empty())

    def test_get_descendants(self):
      bs = ttt.Board().get_descendants()
      for b in bs:
        print(b)
        print()
      print(len(bs))
      
      p1 = [b for b in bs if b.who_won() == b.p1]
      #for b in p1: print(b); print()
      print(len(p1))

      p2 = [b for b in bs if b.who_won() == b.p2]
      #for b in p2: print(b); print()
      print(len(p2))
      pass
    

if __name__ == "__main__":
  #test = unittest.TestLoader().loadTestsFromName("ttt_test.TttTest.test_get_descendants")
  #unittest.TextTestRunner().run(test)
  unittest.main()
