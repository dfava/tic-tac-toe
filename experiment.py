#!/usr/bin/env python3

import sys

import ttt
import ttt_player

def main(argv):
  configs= (
    (ttt_player.APlayer(ttt.Board.default_p1),  ttt_player.APlayer(ttt.Board.default_p2)),
    (ttt_player.APlayer(ttt.Board.default_p1),  ttt_player.ADPlayer(ttt.Board.default_p2)),
    (ttt_player.APlayer(ttt.Board.default_p1),  ttt_player.DPlayer(ttt.Board.default_p2)),
    (ttt_player.ADPlayer(ttt.Board.default_p1), ttt_player.APlayer(ttt.Board.default_p2)),
    (ttt_player.ADPlayer(ttt.Board.default_p1), ttt_player.ADPlayer(ttt.Board.default_p2)),
    (ttt_player.ADPlayer(ttt.Board.default_p1), ttt_player.DPlayer(ttt.Board.default_p2)),
    (ttt_player.DPlayer(ttt.Board.default_p1),  ttt_player.APlayer(ttt.Board.default_p2)),
    (ttt_player.DPlayer(ttt.Board.default_p1),  ttt_player.ADPlayer(ttt.Board.default_p2)),
    (ttt_player.DPlayer(ttt.Board.default_p1),  ttt_player.DPlayer(ttt.Board.default_p2)),
  )
  configs= (
    (ttt_player.DRPlayer(ttt.Board.default_p1,params={'dr':0.95}), ttt_player.DRPlayer(ttt.Board.default_p2)),
    (ttt_player.DRPlayer(ttt.Board.default_p1), ttt_player.DRPlayer(ttt.Board.default_p2,params={'dr':0.95})),
  )
  configs = (
    (ttt_player.DRPlayer(ttt.Board.default_p1,params={'dr':0.95}), ttt_player.APlayer(ttt.Board.default_p2)),
    (ttt_player.DRPlayer(ttt.Board.default_p1,params={'dr':0.9}), ttt_player.ADPlayer(ttt.Board.default_p2)),
    (ttt_player.DRPlayer(ttt.Board.default_p1,params={'dr':0.95}), ttt_player.DPlayer(ttt.Board.default_p2)),
    (ttt_player.DRPlayer(ttt.Board.default_p1,params={'dr':0.95}), ttt_player.DRPlayer(ttt.Board.default_p2)),

    (ttt_player.APlayer(ttt.Board.default_p2),  ttt_player.DRPlayer(ttt.Board.default_p1,params={'dr':0.95})),
    (ttt_player.ADPlayer(ttt.Board.default_p2), ttt_player.DRPlayer(ttt.Board.default_p1,params={'dr':0.95})),
    (ttt_player.DPlayer(ttt.Board.default_p2),  ttt_player.DRPlayer(ttt.Board.default_p1,params={'dr':0.95})),
    (ttt_player.DRPlayer(ttt.Board.default_p2), ttt_player.DRPlayer(ttt.Board.default_p1,params={'dr':0.95})),
  )


  res = []
  for idx,config in enumerate(configs):
    res.append({None:0, ttt.Board.default_p1:0, ttt.Board.default_p2:0})
    for exper in range(0, 10):
      g = ttt.Game(config[0],config[1])
      g.start()
      res[idx][g.b.who_won()] += 1
    print('%s, %s vs %s' % (res[idx], config[0].name, config[1].name))
    

if __name__ == '__main__':
  sys.exit(main(sys.argv))
