from datetime import datetime
from . import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    votes = db.relationship("Vote", backref="voter", lazy=True)

class Election(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(30), default="open")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    candidates = db.relationship("Candidate", backref="election", lazy=True)
    votes = db.relationship("Vote", backref="election", lazy=True)

class Candidate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    election_id = db.Column(db.Integer, db.ForeignKey("election.id"), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(100), nullable=False)
    manifesto = db.Column(db.Text, nullable=False)
    photo = db.Column(db.String(500), nullable=False)

    votes = db.relationship("Vote", backref="candidate", lazy=True)

class Vote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    voter_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    election_id = db.Column(db.Integer, db.ForeignKey("election.id"), nullable=False)
    candidate_id = db.Column(db.Integer, db.ForeignKey("candidate.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (
        db.UniqueConstraint("voter_id", "election_id", name="one_vote_per_election"),
    )
