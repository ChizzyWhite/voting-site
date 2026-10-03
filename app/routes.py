import os
import json
import redis
from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.security import check_password_hash
from sqlalchemy import func
from . import db
from .models import User, Election, Candidate, Vote

main = Blueprint("main", __name__)
redis_client = redis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379/0"))

@main.route("/")
def home():
    election = Election.query.filter_by(status="open").first()
    total_votes = Vote.query.filter_by(election_id=election.id).count() if election else 0
    return render_template("home.html", election=election, total_votes=total_votes)

@main.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"].strip().lower()
        password = request.form["password"]
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password_hash, password):
            session["user_id"] = user.id
            session["user_name"] = user.name
            session["is_admin"] = user.is_admin
            return redirect(url_for("main.dashboard"))

        flash("Invalid email or password.", "error")

    return render_template("login.html")

@main.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("main.home"))

@main.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("main.login"))

    election = Election.query.filter_by(status="open").first()
    candidates = Candidate.query.filter_by(election_id=election.id).all()
    already_voted = Vote.query.filter_by(
        voter_id=session["user_id"], election_id=election.id
    ).first()

    results = []
    for candidate in candidates:
        count = Vote.query.filter_by(candidate_id=candidate.id).count()
        results.append({"candidate": candidate, "count": count})

    return render_template(
        "dashboard.html",
        election=election,
        candidates=candidates,
        already_voted=already_voted,
        results=results,
        total_votes=sum(item["count"] for item in results)
    )

@main.route("/vote/<int:candidate_id>", methods=["POST"])
def vote(candidate_id):
    if "user_id" not in session:
        return redirect(url_for("main.login"))

    election = Election.query.filter_by(status="open").first()
    candidate = Candidate.query.filter_by(
        id=candidate_id, election_id=election.id
    ).first()

    if not candidate:
        flash("Candidate not found.", "error")
        return redirect(url_for("main.dashboard"))

    existing = Vote.query.filter_by(
        voter_id=session["user_id"], election_id=election.id
    ).first()

    if existing:
        flash("You have already voted in this election.", "error")
        return redirect(url_for("main.dashboard"))

    new_vote = Vote(
        voter_id=session["user_id"],
        election_id=election.id,
        candidate_id=candidate.id
    )
    db.session.add(new_vote)
    db.session.commit()

    event = {
        "event": "vote_cast",
        "vote_id": new_vote.id,
        "candidate_id": candidate.id,
        "candidate": candidate.name,
        "election_id": election.id
    }
    redis_client.rpush("vote_events", json.dumps(event))

    flash("Your vote has been recorded successfully.", "success")
    return redirect(url_for("main.dashboard"))

@main.route("/results")
def results():
    election = Election.query.filter_by(status="open").first()
    candidates = Candidate.query.filter_by(election_id=election.id).all()

    data = []
    total = Vote.query.filter_by(election_id=election.id).count()

    for candidate in candidates:
        count = Vote.query.filter_by(candidate_id=candidate.id).count()
        percentage = round((count / total) * 100, 1) if total else 0
        data.append({
            "name": candidate.name,
            "position": candidate.position,
            "votes": count,
            "percentage": percentage
        })

    return render_template("results.html", election=election, results=data, total=total)

@main.route("/health")
def health():
    try:
        db.session.execute(db.text("SELECT 1"))
        database = "healthy"
    except Exception:
        database = "unhealthy"

    try:
        redis_client.ping()
        redis_status = "healthy"
    except Exception:
        redis_status = "unhealthy"

    status = "healthy" if database == "healthy" and redis_status == "healthy" else "degraded"

    return jsonify({
        "status": status,
        "database": database,
        "redis": redis_status
    }), 200 if status == "healthy" else 503

@main.route("/admin")
def admin():
    if not session.get("is_admin"):
        flash("Admin access required.", "error")
        return redirect(url_for("main.dashboard"))

    election = Election.query.filter_by(status="open").first()
    total_votes = Vote.query.filter_by(election_id=election.id).count()
    voters = User.query.filter_by(is_admin=False).count()
    candidates = Candidate.query.filter_by(election_id=election.id).all()

    stats = []
    for candidate in candidates:
        count = Vote.query.filter_by(candidate_id=candidate.id).count()
        stats.append((candidate, count))

    return render_template(
        "admin.html",
        election=election,
        total_votes=total_votes,
        voters=voters,
        stats=stats
    )
