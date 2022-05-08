import flask
from flask import jsonify, request
from . import db_session
from .users import Users

blueprint = flask.Blueprint(
    'users_api',
    __name__,
    template_folder='templates'
)
@blueprint.route('/api/users')
def get_users():
    db_sess = db_session.create_session()
    users = db_sess.query(Users).all()
    return jsonify(
        {
            'users':
                [item.to_dict(only=('id', 'name', 'email', 'password', 'weight', 'height', 'age', 'allergic'))
                 for item in users]
        }
    )

@blueprint.route('/api/users/<int:users_id>', methods=['GET'])
def get_one_users(users_id):
    db_sess = db_session.create_session()
    users = db_sess.query(Users).get(users_id)
    if not users:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'jobs': users.to_dict(only=('id', 'name', 'email', 'password', 'weight', 'height', 'age', 'allergic'))
        }
    )

@blueprint.route('/api/users', methods=['POST'])
def create_users():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['id', 'name', 'email', 'password', 'weight', 'height', 'age', 'allergic']):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    users = Users(
        id=request.json['id'],
        name=request.json['name'],
        email=request.json['email'],
        password=request.json['password'],
        weight=request.json['weight'],
        height=request.json['height'],
        age=request.json['age'],
        allergic=request.json['allergic']
    )
    db_sess.add(users)
    db_sess.commit()
    return jsonify({'success': 'OK'})

### редактирование


@blueprint.route('/api/users/<int:users_id>', methods=['DELETE'])
def delete_users(users_id):
    db_sess = db_session.create_session()
    users = db_sess.query(Users).get(users_id)
    if not users:
        return jsonify({'error': 'Not found'})
    db_sess.delete(users)
    db_sess.commit()
    return jsonify({'success': 'OK'})

