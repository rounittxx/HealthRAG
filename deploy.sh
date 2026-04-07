#!/bin/bash
# HealthRAG one-click deploy
# Usage: chmod +x deploy.sh && ./deploy.sh

set -e

GITHUB_USER="rounittxx"
REPO_NAME="HealthRAG"

# put your token in .env or export before running:  export GITHUB_TOKEN=ghp_xxx
if [ -z "$GITHUB_TOKEN" ]; then
  echo "Error: GITHUB_TOKEN not set. Export it before running this script."
  exit 1
fi

REMOTE_URL="https://${GITHUB_TOKEN}@github.com/${GITHUB_USER}/${REPO_NAME}.git"

echo "HealthRAG Deploy"
echo "---"

# Create GitHub repo (skips if it already exists)
HTTP_CODE=$(curl -s -o /tmp/gh_resp.json -w "%{http_code}" \
  -X POST https://api.github.com/user/repos \
  -H "Authorization: token ${GITHUB_TOKEN}" \
  -H "Content-Type: application/json" \
  -d "{\"name\": \"${REPO_NAME}\", \"description\": \"AI Medical Symptom Checker\", \"private\": false}")

[ "$HTTP_CODE" == "201" ] && echo "Repo created." || echo "Repo already exists, continuing..."

git remote remove origin 2>/dev/null || true
git remote add origin "${REMOTE_URL}"
git push -u origin main

echo "Pushed to: https://github.com/${GITHUB_USER}/${REPO_NAME}"
