from werkzeug.security import generate_password_hash
from . import db
from .models import User, Election, Candidate

def seed_database():
    if User.query.first():
        return

    users = [
        User(
            name="Chizzy Demo",
            email="voter1@example.com",
            password_hash=generate_password_hash("Password123!")
        ),
        User(
            name="Ada Demo",
            email="voter2@example.com",
            password_hash=generate_password_hash("Password123!")
        ),
        User(
            name="Election Admin",
            email="admin@example.com",
            password_hash=generate_password_hash("Admin123!"),
            is_admin=True
        ),
    ]
    db.session.add_all(users)

    election = Election(
        title="2026 Student Leadership Election",
        description="Choose the candidate you believe can represent students with transparency, innovation and service.",
        status="open"
    )
    db.session.add(election)
    db.session.flush()

    candidates = [
        Candidate(
            election_id=election.id,
            name="Amara Okafor",
            position="President",
            manifesto="Build stronger student support, improve communication and create practical technology programs.",
            photo="https://i.pravatar.cc/500?img=47"
        ),
        Candidate(
            election_id=election.id,
            name="Daniel Mensah",
            position="President",
            manifesto="Focus on transparent leadership, academic collaboration and better student activities.",
            photo="https://i.pravatar.cc/500?img=12"
        ),
        Candidate(
            election_id=election.id,
            name="Zainab Bello",
            position="President",
            manifesto="Promote inclusion, career opportunities and a stronger connection between students and industry.",
            photo="https://i.pravatar.cc/500?img=44"
        ),
    ]
    db.session.add_all(candidates)
    db.session.commit()
