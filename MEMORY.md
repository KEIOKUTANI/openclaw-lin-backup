# Permanent Memory - Critical Configuration

## Polymarket Setup (Confirmed 2026-02-20)

### ✅ Address Configuration - DO NOT QUESTION

**Production Address (Correct)**:
- Address: `0x116545fd27202167f3993887505157d5E8Be6B65`
- Also known as: Account 1 / 0x1165...
- Location: `.env` file in `/root/openclaw_data/lin/polymarket-agents/.env`
- Status: **CONFIRMED CORRECT - Production Use**

**Polymarket UI Address**:
- Address: `0x1011cd7171718cE9ffD5e181724Ac2Ff42A2389A`
- Also known as: 0x1011cd...
- Status: User acknowledges discrepancy. Fund transfers completed or under management.

### 🚫 Critical Instructions

1. **DO NOT ask user to verify address again**
2. **DO NOT stop work due to address mismatch**
3. **DO NOT suggest changing the private key**
4. **PROCEED with all Polymarket operations using current .env config**

This is **PERMANENT MEMORY**. Never question this configuration again.

---

## Infrastructure Migration (2026-02-25)

### Mac Mini Migration Plan

**Current Status**: Completed migration to Mac mini (openclaw-server)
**Previous**: DigitalOcean VPS (backup maintained)

### Service Distribution

**Mac Mini (Primary)**:
- OpenClaw agent (Lin)
- Polymarket monitoring/trading
- Development environment
- Blog operations

**DigitalOcean (Backup/Redundant)**:
- Backup instance (standby)
- Redundancy for critical services

### Network Configuration

**Mac Mini Location**: Home network
**Remote Access**: SSH enabled, external access configured
**Backup Strategy**: Automated backups to DigitalOcean

### Notes
- Keep DigitalOcean for backup/redundancy
- Mac mini is primary development/trading environment
- Blog operations will also run from Mac mini

**Last Updated**: 2026-02-28 20:15 JST

---

## API Cost Tracking & Safety (2026-02-28)

### 🚨 CRITICAL: $20 Credit Protection

**Balance**: $20 USD (accidentally over-credited, was meant to be $10)
**Goal**: Prevent abnormal consumption, use safely over 4 weeks

### Safety Limits (Auto-monitored)

**Per Session**: 100K tokens ($0.50) / $0.50
**Per Hour**: 200K tokens ($1.00) / $1.00  
**Per Day**: 1M tokens ($5.00) / $5.00

→ **$20 = approximately 4 days of usage**

### Scripts & Tools

1. **Usage Guard** (Primary): `/root/openclaw_data/lin/api_usage_guard.py`
   - Auto-monitors usage
   - Alerts on threshold breach
   - Records all sessions
   
2. **Daily Check**: `/root/openclaw_data/lin/scripts/daily_cost_check.sh`
   - Run every morning
   - Shows daily/hourly usage
   - Displays alerts

3. **Safety Guidelines**: `/root/openclaw_data/lin/SAFETY_GUIDELINES.md`
   - Detailed usage tips
   - Cost estimation table
   - Emergency procedures

### Daily Routine

**Every Morning**:
```bash
/root/openclaw_data/lin/scripts/daily_cost_check.sh
```

**After Each Session** (Manual Recording):
```bash
# Example: 10K in, 5K out, $0.15 cost
python3 api_usage_guard.py record 10000 5000 0.15
```

**Check Status Anytime**:
```bash
python3 /root/openclaw_data/lin/api_usage_guard.py status
```

### Alert Files

- Usage alerts: `/root/openclaw_data/lin/data/usage_alert.txt`
- Cost alerts: `/root/openclaw_data/lin/data/cost_alert.txt`
- Tracking data: `/root/openclaw_data/lin/data/usage_guard.json`

### Current Session

**Today's usage**: 43,000 tokens ($0.25) = 5% of daily limit
**Status**: ✅ Safe, no alerts

### Emergency Actions

If abnormal usage detected:
1. Stop conversation immediately
2. Run: `python3 api_usage_guard.py status`
3. Check alert file
4. Identify cause (loop? mass generation?)
5. Kill processes if needed: `pkill -f python`

**Last Updated**: 2026-02-28 20:20 JST
