from nose.tools import eq_

from cpp import game


def test_mobility():
    p = game.Position.initial()
    eq_(p.num_moves(), 4)
    eq_(p.mobility(), 0)
