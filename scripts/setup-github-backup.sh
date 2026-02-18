#!/bin/bash
# GitHub Backup Setup Script
# このスクリプトは対話的にGitHub Personal Access Tokenを設定します

WORKSPACE_DIR="/root/openclaw_data/lin"
GITHUB_USER="KEIOKUTANI"
GITHUB_REPO="openclaw-lin-backup"

echo "=== GitHub Backup Setup ==="
echo ""
echo "Repository: https://github.com/${GITHUB_USER}/${GITHUB_REPO}"
echo ""

# トークンを安全に入力
echo "Please enter your GitHub Personal Access Token:"
echo "(入力は表示されません)"
read -s GITHUB_TOKEN

if [ -z "$GITHUB_TOKEN" ]; then
    echo "Error: Token is empty"
    exit 1
fi

echo ""
echo "Setting up Git remote..."

cd "$WORKSPACE_DIR" || exit 1

# 既存のremoteを削除（もしあれば）
git remote remove origin 2>/dev/null

# トークンを含むURLでremoteを追加
git remote add origin "https://${GITHUB_TOKEN}@github.com/${GITHUB_USER}/${GITHUB_REPO}.git"

echo "Testing connection..."
if git ls-remote origin >/dev/null 2>&1; then
    echo "✅ Connection successful!"
else
    echo "❌ Connection failed. Please check your token."
    git remote remove origin
    exit 1
fi

# Initial push
echo ""
echo "Pushing to GitHub..."
git push -u origin master

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Backup setup complete!"
    echo ""
    echo "Your workspace is now backed up to:"
    echo "https://github.com/${GITHUB_USER}/${GITHUB_REPO}"
    echo ""
    echo "Next: Set up automatic backups with cron"
else
    echo "❌ Push failed"
    exit 1
fi
