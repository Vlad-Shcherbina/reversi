import os
from distutils.core import setup, Extension

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
