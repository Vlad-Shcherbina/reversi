import random

from cpp import game

cnt = 0


class Player(object):
    def __init__(self, depth, weights):
        self.depth = depth
        self.weights = weights

    def heuristic(self, position):
        w = position.weight_features(self.weights)
        return max(-1100, min(w, 1100))

    def pick_move(self, history):
        # we pass history to avoid serializing position
        position = game.Position.initial()
        for move in history:
            ok = position.try_move_inplace(move)
            assert ok
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
            best = 10 * position.final_score()

        for q in successors:
            move = q.first
            next_position = q.second
            score = -self.minimax(next_position, depth - 1)[0]
            if score > best:
                best_move = move
                best = score

        return best, best_move
