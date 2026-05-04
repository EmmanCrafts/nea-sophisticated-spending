from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date

db = SQLAlchemy()


class User(db.Model):
    """User model for storing user information"""

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    # Survey fields
    survey_completed = db.Column(db.Boolean, default=False, nullable=False)
    stakeholder_type = db.Column(db.String(100))
    financial_goal = db.Column(db.String(100))
    spending_frequency = db.Column(db.String(50))

    # Monthly budget goal — optional, user sets this from the dashboard
    # NOTE: delete users.db before running if you had a previous version
    monthly_budget = db.Column(db.Float, nullable=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'


class Transaction(db.Model):
    """Stores a single spending transaction for a user"""

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    date = db.Column(db.Date, nullable=False, default=date.today)

    user = db.relationship('User', backref='transactions')

    def __repr__(self):
        return f'<Transaction {self.description} £{self.amount}>'
