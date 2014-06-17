import sys

import nose

from cpp import build_extensions


if __name__ == '__main__':
    nose.run_exit(argv=sys.argv + [
        '--verbose', '--with-doctest',
        '--logging-level=DEBUG'
        ])
