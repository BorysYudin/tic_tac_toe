from sqlalchemy import String, Boolean, Uuid, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.extensions import db


class Game(db.Model):
    """
    Game model.
    """
    id: Mapped[str] = mapped_column(Uuid, primary_key=True)

    creator_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    creator: Mapped['User'] = relationship('User', foreign_keys=[creator_id])

    opponent_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    opponent: Mapped['User'] = relationship('User', foreign_keys=[opponent_id])

    last_move_user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=True)
    last_move_user: Mapped['User'] = relationship('User', foreign_keys=[last_move_user_id])

    latest_game_board = mapped_column(String)
    is_finished = mapped_column(Boolean, default=False)

    winner_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=True)
    winner: Mapped['User'] = relationship('User', foreign_keys=[winner_id])
