import sys
import time
import numpy


from cpp import build_extensions
from cpp import game

cnt = 0


def heuristic(position):
    features = position.features_array(weights.size)
    return max(-1100, min(numpy.dot(features, weights), 1100))


def minimax(position, depth):
    global cnt, weights
    cnt += 1
    # return (score, best move)
    if depth == 0:
        return heuristic(position), None

    #resulting_score = 10

    best = -1e10
    best_move = None

    successors = position.generate_successors()
    if len(successors) == 0:
        best = position.leaf_score()

    for q in position.generate_successors():
        move = q.first
        next_position = q.second
        score = -minimax(next_position, depth - 1)[0]

        if score > best:
            best_move = move
            best = score

    features = position.features_array(weights.size)
    weights += 0.001 * (best - heuristic(position)) * features
    return best, best_move


if __name__ == '__main__':
    weights = numpy.ones((game.Position.num_features(),))

    start = time.clock()

    for _ in range(10):
        p = game.Position.initial()
        while True:
            score, move = minimax(p, 5)
            #print p, score, move
            if move is None:
                break
            ok = p.try_move_inplace(move)
            assert ok

        print (weights.reshape(game.N, game.N) * 100).astype(int)

    print cnt
    print int(cnt / (time.clock() - start + 0.001)), 'positions per second'
