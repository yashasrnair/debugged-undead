from datetime import datetime
from .extensions import db

class Survivor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    start_time = db.Column(db.DateTime, default=datetime.utcnow)
    end_time = db.Column(db.DateTime, nullable=True)
    
    challenges = db.relationship('Challenge', backref='survivor', lazy='dynamic', cascade="all, delete-orphan")

    def get_completion_time(self):
        if not self.end_time or not self.start_time:
            return None
        duration = self.end_time - self.start_time
        return str(duration).split('.')[0]

    def __repr__(self):
        return f'<Survivor {self.username}>'

class Challenge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    level = db.Column(db.Integer, index=True)
    buggy_code = db.Column(db.Text)
    solution = db.Column(db.Text)
    error_type = db.Column(db.String(50))
    expected_output = db.Column(db.Text)
    is_solved = db.Column(db.Boolean, default=False)
    start_time = db.Column(db.DateTime, default=datetime.utcnow)  # Add this
    end_time = db.Column(db.DateTime, nullable=True)  # Add this
    survivor_id = db.Column(db.Integer, db.ForeignKey('survivor.id'))

    def get_level_time(self):
        """Get time taken for this specific level"""
        if not self.end_time or not self.start_time:
            return None
        duration = self.end_time - self.start_time
        return str(duration).split('.')[0]

    def __repr__(self):
        return f'<Challenge Level {self.level} for Survivor {self.survivor_id}>'