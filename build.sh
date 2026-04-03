#!/usr/bin/env bash
# Render build script — runs on every deploy
set -o errexit

pip install --upgrade pip
pip install -r requirements.txt

# Run database migrations
flask db upgrade

# Create default admin user if none exists
flask seed-admin
