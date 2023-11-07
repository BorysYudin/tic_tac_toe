from flask import request
from flask_login import login_required, current_user
from sqlalchemy import func

from app.user import bp
from app.extensions import db
from app.models import User, UserRate
from app.user.schemas import GetUserSchema, UpdateUserSchema, ListUserSchema, UserChartSchema
from app.game.schemas import GameSchema


def _user_subquery():
    """
    Subquery to join User and UserRate tables to retrieve user data together with user rate and he's position in the
    table depending on the rate.
    :return: sqlalchemy subquery
    """
    return db.session.query(
        User,
        UserRate.rate,
        func.rank().over(
            order_by=UserRate.rate.desc()
        ).label('position')
    ).join(UserRate, UserRate.user_id == User.id).subquery()


@bp.route('/users/current')
@login_required
def get_current_user():
    """
    Get currently logged in user details.
    :return: user details and status code
    """
    subquery = _user_subquery()
    value = db.session.query(subquery).filter_by(id=int(current_user.id)).first()
    return GetUserSchema().dump(value), 200


@bp.route('/users/<user_id>')
@login_required
def get_user(user_id):
    """
    Get user details by user id.
    :param user_id: id of a user
    :return: user details and status code
    """
    subquery = _user_subquery()
    value = db.session.query(subquery).filter_by(id=int(user_id)).first()
    return GetUserSchema().dump(value), 200


@bp.route('/users')
@login_required
def list_users():
    """
    Get all users details together with user rate and user position in rate table.
    :return: list of user details
    """
    subquery = _user_subquery()
    values = db.session.query(subquery).all()
    return ListUserSchema().dump(values, many=True), 200


@bp.route('/users/current/update', methods=['POST'])
@login_required
def update_user():
    """
    Update current user details.
    :return:
    """
    data, errors = UpdateUserSchema().load(request.get_json())
    if errors:
        return errors, 400
    current_user.update(**data)
    db.session.commit()
    return {'msg': 'Success.'}, 200


@bp.route('/users/current/delete')
@login_required
def delete_user():
    """
    Soft delete of current user. We use soft delete to not break the logic of existing games.
    :return:
    """
    current_user.is_deleted = True
    db.session.commit()
    return {'msg': 'Success.'}, 200


@bp.route('/users/current/games')
@login_required
def get_user_games():
    """
    Get current user games history.
    :return: list with games details
    """
    return GameSchema().dump(current_user.games, many=True), 200


@bp.route('/users/rate_chart')
@login_required
def get_users_rate_chart():
    """
    Get all users chart with `x` and `y` values where `x` values are users names and `y` values are users rate.
    :return:
    """
    subquery = db.session.query(
        User.username.label('x'),
        UserRate.rate.label('y'),
    ).join(UserRate, UserRate.user_id == User.id).order_by(UserRate.rate.desc()).subquery()
    values = db.session.query(subquery).all()
    return UserChartSchema().dump(values, many=True), 200
