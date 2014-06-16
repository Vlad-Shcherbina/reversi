import sys
import time
import numpy


from cpp import build_extensions
from cpp import game

cnt = 0


class Player(object):
    def __init__(self, weights):
        self.weights = weights

    def heuristic(self, position):
        w = position.weight_features(self.weights)
        return max(-1100, min(w, 1100))

    def minimax(self, position, depth):
        global cnt
        cnt += 1

        if depth == 0:
            return self.heuristic(position), None

        best = -1e10
        best_move = None

        successors = position.generate_successors()
        if len(successors) == 0:
            best = position.leaf_score()

        for q in position.generate_successors():
            move = q.first
            next_position = q.second
            score = -self.minimax(next_position, depth - 1)[0]
            if score > best:
                best_move = move
                best = score

        return best, best_move


if __name__ == '__main__':
    print sys.argv
    weights = numpy.ones((game.Position.num_features(),), dtype=numpy.float32)

    start = time.clock()

    player = Player(weights)

    p = game.Position.initial()
    while True:
        score, move = player.minimax(p, 5)
        print p, score, move
        if move is None:
            break
        ok = p.try_move_inplace(move)
        assert ok

    print cnt
    print int(cnt / (time.clock() - start + 0.001)), 'positions per second'
