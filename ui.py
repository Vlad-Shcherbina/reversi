import flask
import jinja2
import numpy
import run

from cpp import build_extensions
from cpp import game


web_app = flask.Flask(__name__)
web_app.secret_key = 'zzz'

template_loader = jinja2.FileSystemLoader('templates')
web_app.jinja_loader = template_loader


@web_app.route('/')
def index():
    return flask.redirect(flask.url_for('choose_move'))


@web_app.route('/choose_move')
def choose_move():
    args = flask.request.args
    history = args.get('history')
    if history:
        history = map(int, history.split(','))
    else:
        history = []

    position = game.Position.initial()
    for move in history:
        ok = position.try_move_inplace(move)
        assert ok

    moves = [succ[0] for succ in position.generate_successors()]

    return flask.render_template(
        'position.html',
        game=game,  # for constants
        history=history,
        position=position,
        moves=moves)


@web_app.route('/ai_move')
def ai_move():
    args = flask.request.args
    history = args.get('history')
    if history:
        history = map(int, history.split(','))
    else:
        history = []

    position = game.Position.initial()
    for move in history:
        ok = position.try_move_inplace(move)
        assert ok

    weights = numpy.ones((game.Position.num_features(),), dtype=numpy.float32)
    player = run.Player(depth=4, weights=weights)
    move = player.pick_move(position)
    if move is None:
        return 'game ended'

    history.append(move)

    flask.flash('AI made a move {}'.format(move))

    return flask.redirect('{}?history={}'.format(
        flask.url_for('choose_move'),
        ','.join(map(str, history))))


if __name__ == '__main__':
    web_app.debug = True
    web_app.run()
