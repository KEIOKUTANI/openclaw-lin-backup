#!/bin/bash
# Backup script for Mac mini migration
# Run on DigitalOcean before migration

BACKUP_DIR="/root/openclaw_migration_backup_$(date +%Y%m%d_%H%M%S)"
WORKSPACE="/root/openclaw_data/lin"

echo "======================================"
echo "OpenClaw Migration Backup"
echo "======================================"
echo ""
echo "Creating backup at: $BACKUP_DIR"
echo ""

# Create backup directory
mkdir -p "$BACKUP_DIR"

# Copy entire workspace
echo "📦 Backing up workspace..."
cp -r "$WORKSPACE" "$BACKUP_DIR/"

# Create environment info file
echo "📋 Recording environment info..."
cat > "$BACKUP_DIR/environment_info.txt" << EOF
Backup Date: $(date)
Hostname: $(hostname)
IP Address: $(curl -s https://ipapi.co/ip/)
Python Version: $(python3 --version)
Node Version: $(node --version)
OpenClaw Version: $(openclaw --version 2>/dev/null || echo "Not installed")

Installed Python Packages:
EOF

# List Python packages (if venv exists)
if [ -d "$WORKSPACE/polymarket-agents/.venv" ]; then
    source "$WORKSPACE/polymarket-agents/.venv/bin/activate"
    pip list >> "$BACKUP_DIR/environment_info.txt"
    deactivate
fi

# Compress backup
echo "🗜️  Compressing backup..."
cd /root
tar -czf "openclaw_migration_backup_$(date +%Y%m%d).tar.gz" "$(basename $BACKUP_DIR)"

BACKUP_FILE="/root/openclaw_migration_backup_$(date +%Y%m%d).tar.gz"
BACKUP_SIZE=$(du -h "$BACKUP_FILE" | cut -f1)

echo ""
echo "======================================"
echo "✅ Backup Complete!"
echo "======================================"
echo ""
echo "Backup file: $BACKUP_FILE"
echo "Size: $BACKUP_SIZE"
echo ""
echo "To download to Mac mini:"
echo "  scp root@<DO_IP>:$BACKUP_FILE ~/Downloads/"
echo ""
echo "Or use rsync:"
echo "  rsync -avz root@<DO_IP>:$BACKUP_DIR/ ~/openclaw_data/lin/"
echo ""
echo "======================================"
