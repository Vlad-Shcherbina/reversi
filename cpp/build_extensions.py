import os
import sys
from distutils.core import setup, Extension

def build_extensions(silent=False):
    if silent:
        devnull = open(os.devnull, 'w')
        oldstdout = os.dup(sys.stdout.fileno())
        os.dup2(devnull.fileno(), sys.stdout.fileno())
        oldstderr = os.dup(sys.stderr.fileno())
        os.dup2(devnull.fileno(), sys.stderr.fileno())
        try:
            build_extensions(silent=False)
        finally:
            os.dup2(oldstdout, sys.stdout.fileno())
            os.dup2(oldstderr, sys.stderr.fileno())
            devnull.close()
        return

    cur_dir = os.getcwd()
    try:
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        setup(
            name='game',
            py_modules=['game'],
            ext_modules=[
                Extension('_game',
                    ['game.i', 'game.cpp'],
                    depends=['game.h'],
                    swig_opts=['-c++'],
                    extra_compile_args = ['--std=c++0x'],
                ),
            ],
            script_args=['build_ext', '--inplace']
        )
    finally:
        os.chdir(cur_dir)
