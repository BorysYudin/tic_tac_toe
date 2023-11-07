from flask import request

from flask_login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

from app.models import User, UserRate
from app.auth import bp
from app.extensions import db


@bp.route('/login', methods=['POST'])
def login():
    """
    Endpoint for user login
    :return: tuple with status message and status code
    """
    data = request.get_json()

    username = data['username']
    password = data['password']

    user = User.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password, password):
        return {'msg': 'Please check your login details and try again.'}, 400

    if user.is_deleted:
        return {'msg': 'User deleted.'}, 404

    login_user(user)
    return {'msg': 'Success'}, 200


@bp.route('/signup', methods=['POST'])
def signup():
    """
    Endpoint for user signup
    :return: tuple with status message and status code
    """
    data = request.get_json()

    user = User.query.filter_by(username=data['username']).first()

    if user:
        return {'msg': 'User with this username already exists.'}, 400

    # Here were create a new user and also add a record to `user_rate` table with default zero points in case if current
    # game season is in progress and we register a new user
    new_user = User(
        username=data['username'],
        password=generate_password_hash(data['password']),
        age=data.get('age')
    )
    new_user_rate = UserRate(user=new_user)

    db.session.add(new_user)
    db.session.add(new_user_rate)
    db.session.commit()

    return {'msg': 'Success.'}, 200


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return {'msg': 'Success.'}, 200
