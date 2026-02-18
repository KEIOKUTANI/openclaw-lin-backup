#!/bin/bash
# OpenClaw Workspace Git Backup Script

WORKSPACE_DIR="/root/openclaw_data/lin"
LOG_FILE="/root/openclaw_data/lin/logs/git-backup.log"

# Create logs directory if it doesn't exist
mkdir -p "$(dirname "$LOG_FILE")"

# Timestamp function
timestamp() {
    date "+%Y-%m-%d %H:%M:%S"
}

echo "[$(timestamp)] Starting Git backup..." >> "$LOG_FILE"

cd "$WORKSPACE_DIR" || exit 1

# Check if there are changes
if [[ -n $(git status --porcelain) ]]; then
    echo "[$(timestamp)] Changes detected, committing..." >> "$LOG_FILE"
    
    # Add all changes (excluding sensitive files - already in .gitignore)
    git add -A
    
    # Commit with timestamp
    git commit -m "Auto-backup: $(date '+%Y-%m-%d %H:%M:%S')" >> "$LOG_FILE" 2>&1
    
    # Push to remote if configured
    if git remote | grep -q 'origin'; then
        echo "[$(timestamp)] Pushing to remote..." >> "$LOG_FILE"
        
        # Push with existing credentials (stored in remote URL)
        git push origin master >> "$LOG_FILE" 2>&1
        
        if [ $? -eq 0 ]; then
            echo "[$(timestamp)] ✅ Backup successful" >> "$LOG_FILE"
        else
            echo "[$(timestamp)] ⚠️ Push failed" >> "$LOG_FILE"
            exit 1
        fi
    else
        echo "[$(timestamp)] ✅ Local commit successful (no remote configured)" >> "$LOG_FILE"
    fi
else
    echo "[$(timestamp)] No changes to backup" >> "$LOG_FILE"
fi

echo "" >> "$LOG_FILE"

exit 0
