# VoteSphere — Election & Voting Platform

A presentation-ready DevOps voting application built with Flask, PostgreSQL, Redis, Docker Compose, and a small Node.js worker.

## Features

- Beautiful responsive election dashboard
- Voter registration and login
- One-vote-per-election protection
- Candidate cards with photos and manifestos
- Live-style results dashboard
- PostgreSQL for permanent data
- Redis for vote events
- Node.js worker for processing vote events
- Health endpoint for monitoring
- Docker Compose for the full stack
- Seed data for a demo election

## Architecture

Browser → Flask Web App → PostgreSQL
                         ↓
                       Redis → Node Worker

## Quick start

1. Install Docker Desktop.
2. Open this project folder.
3. Run:

```bash
docker compose up --build
```

4. Open http://localhost:5000

Demo accounts:
- voter1@example.com / Password123!
- voter2@example.com / Password123!
- admin@example.com / Admin123!

The demo users are already seeded when the database starts.

## Important

This is a capstone/demo voting system, not a production government election system. A real election platform would require much stronger identity verification, auditing, security controls, accessibility testing, legal compliance, and independent security review.
