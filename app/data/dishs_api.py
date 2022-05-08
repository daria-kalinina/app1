import flask
from flask import jsonify, request
from . import db_session
from .dishs import Dishs

blueprint = flask.Blueprint(
    'dishs_api',
    __name__,
    template_folder='templates'
)

@blueprint.route('/api/dishs')
def get_dishs():
    db_sess = db_session.create_session()
    dishs = db_sess.query(Dishs).all()
    return jsonify(
        {
            'dishs':
                [item.to_dict(only=('title', 'content', 'user.name', 'proteins', 'fats', 'carbohydrates', 'calories'))
                 for item in dishs]
        }
    )
