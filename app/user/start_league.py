"""
This script should be used in cron job and be set to execute each week day or each month to update all the values in the
`user_rates` table and set values with zero rate for all the users.
"""

from app import create_app
from app.extensions import db
from app.models import UserRate

app = create_app()
with app.app_context():
    db.session.query(UserRate).update({UserRate.rate: 0}, synchronize_session=False)
    db.session.commit()
