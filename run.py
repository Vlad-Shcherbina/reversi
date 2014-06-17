import sys
import time
import numpy
import random


from cpp import build_extensions
from cpp import game

cnt = 0


class Player(object):
    def __init__(self, depth, weights):
        self.depth = depth
        self.weights = weights

    def heuristic(self, position):
        w = position.weight_features(self.weights)
        return max(-1100, min(w, 1100))

    def pick_move(self, position):
        return self.minimax(position, self.depth)[1]

    def minimax(self, position, depth):
        global cnt
        cnt += 1

        if depth == 0:
            return self.heuristic(position), None

        best = -1e10
        best_move = None

        successors = list(position.generate_successors())
        random.shuffle(successors)
        if len(successors) == 0:
            best = position.leaf_score()

        for q in successors:
            move = q.first
            next_position = q.second
            score = -self.minimax(next_position, depth - 1)[0]
            if score > best:
                best_move = move
                best = score

        return best, best_move


def match(black_player, white_player):
    """Return 1, 0, -1 if black player wins, forces a draw, or looses."""
    p = game.Position.initial()
    while True:
        if p.black_to_move():
            player = black_player
        else:
            player = white_player
        move = player.pick_move(p)
        #print p, move
        if move is None:
            break
        ok = p.try_move_inplace(move)
        assert ok
    score = p.leaf_score()
    assert score == 0 or abs(score) >= 1000
    if not p.black_to_move():
        score = -score
    if score > 0:
        return 1
    elif score == 0:
        return 0
    else:
        return -1


if __name__ == '__main__':
    print sys.argv

    start = time.clock()

    weights = numpy.ones((game.Position.num_features(),), dtype=numpy.float32)
    black_player = Player(depth=3, weights=weights)

    weights = numpy.ones((game.Position.num_features(),), dtype=numpy.float32)
    weights[-1] = 0  # white player does not use mobility feature
    white_player = Player(depth=3, weights=weights)


    total_score = 0
    for i in range(100):
        if i % 10 == 0:
            print i
        q = match(black_player, white_player)
        #print q
        total_score += q
    print 'total:', total_score

    print cnt, 'positions explored'
    print int(cnt / (time.clock() - start + 0.001)), 'positions per second'
