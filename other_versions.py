import re
import os
import subprocess
import shutil
import contextlib


OTHER_VERSIONS_DIR = 'other_versions'


@contextlib.contextmanager
def in_dir(dir):
    cur_dir = os.getcwd()
    os.chdir(dir)
    try:
        yield
    finally:
        os.chdir(cur_dir)


class Repo(object):
    def __init__(self, name):
        assert re.match(r'\w+$', name)
        self.name = name
        self.path = os.path.join(OTHER_VERSIONS_DIR, name)
        assert os.path.exists(OTHER_VERSIONS_DIR)
        if os.path.exists(self.path):
            return
        subprocess.check_output(
            'git clone .. {}'.format(name), shell=True, cwd=OTHER_VERSIONS_DIR)

    def checkout(self, commit):
        subprocess.check_call('git fetch', shell=True, cwd=self.path)
        subprocess.check_call('git reset --hard', shell=True, cwd=self.path)
        subprocess.check_call(
            'git checkout {}'.format(commit), shell=True, cwd=self.path)

    def delete(self):
        shutil.rmtree(self.path)


if __name__ == '__main__':
    repo = Repo('test')
    repo.checkout('origin/master~1')
    repo.delete()
