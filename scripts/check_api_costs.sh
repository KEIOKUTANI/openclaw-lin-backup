#!/bin/bash
# Check API costs and alert if $2 threshold crossed

TRACKER_FILE="/root/openclaw_data/lin/data/api_costs.json"
ALERT_FILE="/root/openclaw_data/lin/data/cost_alert.txt"

# Get current total from Anthropic API (if available)
# Otherwise, parse OpenClaw logs for token usage

# For now, show summary
python3 /root/openclaw_data/lin/api_cost_tracker.py summary

# Check for alerts
if [ -f "$ALERT_FILE" ]; then
    echo ""
    echo "🚨 COST ALERT PENDING:"
    cat "$ALERT_FILE"
    # Clear alert after showing
    rm "$ALERT_FILE"
fi
