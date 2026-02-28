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
2. **DO NOT stop work due to address mismatch between .env and UI**
3. **DO NOT suggest changing the private key in .env**
4. **DO NOT treat address discrepancy as an error**

### ✅ What to Do

- Proceed with all Polymarket operations using the `.env` configuration
- This setup is **intentional and correct**
- User has confirmed this multiple times
- Any address-related "issues" are already resolved

---

**Last Updated**: 2026-02-20 15:19 JST
**Confirmed By**: User (Kei O)

---

## OpenClaw Quant Trading Philosophy (2026-02-22)

### Core Insight: Bottleneck is NOT Knowledge, but Experiment Cycle Time

**Traditional Quant Research Timeline:**
- Model validation: ~1 week
- Correlation analysis: ~3 weeks
- Edge confirmation: 2-3 months
- Full validation (WFO, out-of-sample, robustness): months

**The Real Problem:**
- Physical limit on "number of ideas testable"
- Sequential bottleneck: can only test one hypothesis at a time
- "Experiment queue problem" is the true rate-limiting step

### OpenClaw's Value Proposition

**NOT about making individual tests faster**
**IS about parallelizing research throughput**

| Workflow Stage | Traditional | With OpenClaw |
|----------------|-------------|---------------|
| Data collection | Sequential manual | Parallel autonomous |
| Backtest design | One at a time | Multiple frameworks simultaneously |
| Feature exploration | Sequential hypothesis testing | Parallel hypothesis exploration |
| Results aggregation | Manual reports | Auto-generated dashboards |

**Result:** 3 hypotheses/month → 10-15 hypotheses/month

### Critical Warnings

#### 1. Not All Processes Can Be Parallelized
- Future data doesn't exist
- Live trading validation requires real time
- Cross-regime testing needs time to pass

**OpenClaw's value:** Compress the parallelizable parts to increase number of hypotheses reaching the unavoidable wait times

#### 2. Multiple Testing Problem
- More trials = more false discoveries (5% significance = 5 false positives per 100 tests)
- **Must implement:**
  - Complete experiment logging & reproducibility
  - Automated data leak detection
  - Fixed holdout datasets
  - Pre-registration of hypotheses
  - Bonferroni correction / FDR control

**OpenClaw advantage:** Can automate the experiment management itself

#### 3. Security Risks
- Trading strategies = highly confidential IP
- Third-party Skills may have vulnerabilities (Cisco findings)
- **Minimum safeguards:**
  - API keys: NEVER grant withdrawal permissions
  - Docker sandboxing
  - Testnet validation first

### The True Innovation

Not "parallel execution" but **"Research Production Systemization"**:

1. **Automate repetitive work** - Data, preprocessing, backtesting
2. **Loop-ify research cycle** - Exploration → Evaluation → Recording → Learning
3. **High-leverage human decisions** - Focus on "which hypothesis" and "how to interpret results"

**Bottom line:** OpenClaw elevates individual quant productivity to institutional level

---

**Implications for Polymarket Bot:**
- Apply same philosophy: parallel market monitoring
- Multiple strategy testing simultaneously
- Rigorous experiment logging (avoid multiple testing traps)
- Focus human judgment on: which markets, which strategies, risk management

**Last Updated**: 2026-02-22 17:48 JST

---

## Infrastructure Migration Plan (2026-02-25)

### Current Setup
- **Platform**: DigitalOcean VPS (Singapore)
- **Issue**: Polymarket geo-restriction (Singapore IP blocked)
- **Status**: Free proxies failed, paid proxy not set up

### Migration Plan
- **Target**: Mac mini (local, arriving 2026-02-26)
- **Purpose**: 
  - Bypass geo-restriction (Japan/local IP)
  - Blog access from local machine
- **Timeline**: Migration starts after Mac mini arrival (Feb 26+)

### Migration Checklist (TODO)
- [ ] Mac mini initial setup
- [ ] OpenClaw installation on Mac mini
- [ ] Repository sync (DigitalOcean → Mac mini)
- [ ] Environment variables transfer (.env files)
- [ ] Python environment setup (pyenv, virtualenv)
- [ ] Polymarket agents setup
- [ ] Test Polymarket access from Mac mini IP
- [ ] Verify no geo-restriction

### Notes
- Keep DigitalOcean for backup/redundancy
- Mac mini will be primary development/trading environment
- Blog operations will also run from Mac mini

**Last Updated**: 2026-02-25 22:40 JST
