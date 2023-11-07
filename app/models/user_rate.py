from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.extensions import db


class UserRate(db.Model):
    """
    User rate model.
    """
    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(back_populates="user_rate")

    rate: Mapped[int] = mapped_column(Integer, default=0)
