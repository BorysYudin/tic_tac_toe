from flask_login import UserMixin
from sqlalchemy import Integer, String, Boolean, or_
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.extensions import db
from app.models.game import Game


class User(UserMixin, db.Model):
    """
    User model.
    """
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String, unique=True)
    password: Mapped[str] = mapped_column(String)
    age: Mapped[int] = mapped_column(Integer, nullable=True)
    phone: Mapped[str] = mapped_column(String, nullable=True)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)

    user_rate: Mapped["UserRate"] = relationship(back_populates="user")

    @property
    def games(self):
        """
        Get games in which current user is creator or opponent.
        :return: list of Game objects
        """
        return db.session.query(Game).filter(or_(Game.creator_id == self.id, Game.opponent_id == self.id)).all()
