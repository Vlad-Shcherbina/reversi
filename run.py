from __future__ import division

import sys
import time
import numpy
import collections

from cpp import build_extensions
build_extensions.build_extensions()

from cpp import game
import bayes
import minimax
import other_versions
import external_player


def match(black_player, white_player):
    """ Return black player score. """
    p = game.Position.initial()
    history = []
    while True:
        if p.black_to_move():
            player = black_player
        else:
            player = white_player
        if not p.generate_successors():
            break
        move = player.pick_move(history)
        #print p, move
        assert move is not None
        ok = p.try_move_inplace(move)
        assert ok
        history.append(move)
    score = p.final_score()
    if not p.black_to_move():
        score = -score
    return score


def print_hist(hist):
    m = max(hist.values())
    for x in range(min(hist), max(hist) + 1, 2):
        print '{:>3} {}'.format(x, hist[x] * 75 // m * '*')


if __name__ == '__main__':
    print sys.argv

    start = time.clock()

    weights = numpy.ones((game.Position.num_features(),), dtype=numpy.float32)
    black_player = minimax.Player(depth=2, weights=weights)

    if False:
        # local player
        weights = numpy.ones((game.Position.num_features(),), dtype=numpy.float32)
        weights[-1] = 0  # white player does not use mobility feature
        white_player = minimax.Player(depth=2, weights=weights)
    else:
        # remote player
        repo = other_versions.Repo('test')
        repo.checkout('origin/master')

        setup = """
        import numpy

        from cpp import build_extensions
        build_extensions.build_extensions(silent=True)
        from cpp import game
        import minimax

        weights = numpy.ones((game.Position.num_features(),), dtype=numpy.float32)
        weights[-1] = 0  # don't use mobility feature
        player = minimax.Player(depth=2, weights=weights)
        """
        white_player = external_player.ExternalPlayer(repo, setup)

    hist = collections.Counter()

    NUM_MATCHES = 100

    score_model = bayes.GaussianConjugatePrior()

    total_score = 0
    for i in range(NUM_MATCHES):
        if i % 10 == 0:
            print i
        score = match(black_player, white_player)
        #print score
        total_score += score
        score_model.update(score)
        hist[score] += 1

    print 'average score:', total_score / NUM_MATCHES

    print_hist(hist)
    print '-' * 20

    model_hist = collections.Counter()
    for _ in range(10000):
        score = (int(0.5 * score_model.draw_sample() + 0.5 + 1000) - 1000) * 2
        if abs(score) <= game.N ** 2:
            model_hist[score] += 1
    print_hist(model_hist)

    print minimax.cnt, 'positions explored'
    print int(minimax.cnt / (time.clock() - start + 0.001)), 'positions per second'
