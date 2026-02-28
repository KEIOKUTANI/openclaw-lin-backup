#!/bin/bash
# Auto backup to GitHub after changes

REPO_DIR="/root/openclaw_data/lin"
cd "$REPO_DIR"

# Check if there are changes
if [[ -n $(git status -s) ]]; then
    # Add all changes
    git add -A
    
    # Create commit message with timestamp
    TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
    COMMIT_MSG="Auto backup: $TIMESTAMP"
    
    git commit -m "$COMMIT_MSG"
    
    # Push to remote (detect branch name)
    BRANCH=$(git branch --show-current)
    git push origin $BRANCH 2>&1
    
    echo "✅ Backed up to GitHub: $COMMIT_MSG"
else
    echo "No changes to backup"
fi
