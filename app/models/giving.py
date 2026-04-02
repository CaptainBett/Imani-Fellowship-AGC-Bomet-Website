from datetime import datetime, timezone
from app.extensions import db


class GivingCategory(db.Model):
    __tablename__ = 'giving_categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(100), unique=True, nullable=False, index=True)
    description = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    sort_order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    donations = db.relationship('Donation', backref='category', lazy='dynamic')

    def __repr__(self):
        return f'<GivingCategory {self.name}>'


class Donation(db.Model):
    __tablename__ = 'donations'

    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('giving_categories.id'), nullable=True)
    amount = db.Column(db.Numeric(12, 2), nullable=False)
    currency = db.Column(db.String(3), default='KES')
    payment_method = db.Column(db.String(20), default='mpesa')  # mpesa, card
    transaction_id = db.Column(db.String(100), unique=True, nullable=True)  # M-Pesa receipt
    phone_number = db.Column(db.String(20))
    donor_name = db.Column(db.String(100))
    status = db.Column(db.String(20), default='pending', index=True)  # pending, completed, failed
    mpesa_checkout_id = db.Column(db.String(100), index=True)  # Daraja CheckoutRequestID
    callback_data = db.Column(db.Text)  # JSON string of full callback for audit
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    completed_at = db.Column(db.DateTime, nullable=True)

    @property
    def is_completed(self):
        return self.status == 'completed'

    @property
    def is_pending(self):
        return self.status == 'pending'

    def __repr__(self):
        return f'<Donation {self.amount} {self.currency} - {self.status}>'
