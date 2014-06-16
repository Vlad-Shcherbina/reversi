import re
import ui
import unittest

from cpp import build_extensions


class FlaskrTestCase(unittest.TestCase):
    def setUp(self):
        ui.web_app.config['TESTING'] = True
        self.app = ui.web_app.test_client()

    def test_stuff(self):
        q = self.app.get('/', follow_redirects=True)
        assert q.status_code == 200, q.status
        assert 'black to move' in q.data

        # test user move
        m = re.search(r'href="(/choose_move\?history=[^"]*)"', q.data)
        assert m

        q = self.app.get(m.group(1), follow_redirects=True)
        assert q.status_code == 200, q.status
        assert 'white to move' in q.data

        # test ai move
        m = re.search(r'href="(/ai_move\?history=[^"]*)"', q.data)
        assert m

        q = self.app.get(m.group(1), follow_redirects=True)
        assert q.status_code == 200, q.status
        assert 'AI made a move' in q.data
        assert 'black to move' in q.data


if __name__ == '__main__':
    unittest.main()
