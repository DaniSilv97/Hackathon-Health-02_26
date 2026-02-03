from app import db, login_manager
from flask_login import UserMixin
from datetime import datetime
import bcrypt


class UserRole:
    ADMIN = 'admin'
    CLINICIAN = 'clinician'
    PATIENT = 'patient'

    @classmethod
    def all(cls):
        return [cls.ADMIN, cls.CLINICIAN, cls.PATIENT]


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default=UserRole.PATIENT)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def set_password(self, password):
        """Hash and set the user's password."""
        self.password = bcrypt.hashpw(
            password.encode('utf-8'),
            bcrypt.gensalt()
        ).decode('utf-8')

    def check_password(self, password):
        """Check if the provided password matches the hash."""
        return bcrypt.checkpw(
            password.encode('utf-8'),
            self.password.encode('utf-8')
        )

    def is_admin(self):
        """Check if user is admin."""
        return self.role == UserRole.ADMIN

    def is_clinician(self):
        """Check if user is clinician."""
        return self.role == UserRole.CLINICIAN

    def is_patient(self):
        """Check if user is patient."""
        return self.role == UserRole.PATIENT

    def to_dict(self):
        """Convert user to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'role': self.role,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }

    def __repr__(self):
        return f'<User {self.email}>'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
