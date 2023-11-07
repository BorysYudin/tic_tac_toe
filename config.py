import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """
    Config class that is used for app creation.
    """
    SECRET_KEY = os.environ.get('SECRET_KEY', 'secret_key')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')\
        or f"sqlite:///{os.path.join(basedir, 'tic_tac_toe.db')}"
