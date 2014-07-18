import sys
import subprocess
import textwrap


MAIN_LOOP = """
import sys
while True:
    history = eval(raw_input())
    move = player.pick_move(history)
    assert move is not None
    print move
    sys.stdout.flush()
"""


class ExternalPlayer(object):
    def __init__(self, repo, setup):
        self.proc = subprocess.Popen(
            ['python', '-c', textwrap.dedent(setup) + MAIN_LOOP],
            cwd=repo.path,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE)

    def query(self, input):
        self.proc.stdin.write(input)
        self.proc.stdin.flush()
        return self.proc.stdout.readline()

    def pick_move(self, history):
        return int(self.query(repr(history) + '\n'))

    def __del__(self):
        self.proc.terminate()
        self.proc.wait()


if __name__ == '__main__':
    import other_versions

    repo = other_versions.Repo('test')
    repo.checkout('origin/master')

    setup = """
    import numpy

    from cpp import build_extensions
    build_extensions.build_extensions(silent=True)
    from cpp import game
    import minimax

    weights = numpy.ones((game.Position.num_features(),), dtype=numpy.float32)
    weights[-1] = 0  # white player does not use mobility feature
    player = minimax.Player(depth=2, weights=weights)
    """
    p = ExternalPlayer(repo, setup)
    print p.pick_move([])
