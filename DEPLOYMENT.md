# Continuous Investigation System - Deployment Guide

## 🚀 Quick Deploy

This system runs **autonomously on GitHub Actions** with self-healing capabilities.

### Step 1: Deploy Workflows

Run the deployment script to generate GitHub Actions workflows:

```bash
python3 deploy_workflows.py
```

This creates:
- `.github/workflows/continuous-investigation.yml` - Main investigation system (runs every 6 hours)
- `.github/workflows/self-healing.yml` - Self-healing system (runs every 2 hours)

### Step 2: Commit and Push

```bash
git add .github/workflows/
git commit -m "🚀 Deploy continuous investigation workflows"
git push origin main
```

### Step 3: Verify Deployment

1. Go to your GitHub repository
2. Click on the **Actions** tab
3. You should see two workflows:
   - **Continuous Investigation System**
   - **Self-Healing System**

### Step 4: Manual Trigger (Optional)

To start an investigation immediately:

1. Go to **Actions** tab
2. Select **Continuous Investigation System**
3. Click **Run workflow**
4. Click the green **Run workflow** button

---

## 🤖 How It Works

### Continuous Investigation System

**Schedule:** Runs every 6 hours automatically

**What it does:**
1. Checks out the repository
2. Initializes the investigation system
3. Runs error recovery checks
4. Executes autonomous research cycle:
   - Autonomous research (15 minutes)
   - AI orchestration (15 minutes)
   - Continuous task system (15 minutes)
5. Commits any new findings automatically
6. Generates investigation reports

**Automatic commits when:**
- New entities discovered
- New connections found
- New evidence collected
- Data updated

### Self-Healing System

**Schedule:** Runs every 2 hours automatically

**What it does:**
1. Checks system health
2. Validates Python syntax
3. Checks data integrity
4. Verifies directory structure
5. Runs all system tests
6. Auto-fixes detected issues
7. Commits fixes automatically

**Auto-fixes:**
- Missing directories
- Corrupted data files
- Broken dependencies
- Configuration issues

---

## 📊 Monitoring

### View Investigation Progress

Check the **Actions** tab to see:
- Workflow runs
- Success/failure status
- Investigation reports (downloadable artifacts)
- Cycle logs

### Download Reports

1. Go to a completed workflow run
2. Scroll to **Artifacts** section
3. Download:
   - `investigation-report-XXX` - Investigation cycle details
   - `health-report-XXX` - System health status

### Check Progress Locally

```bash
python3 progress_tracker.py
```

This shows:
- Total cycles run
- Success rate
- Entities discovered
- Connections found
- Evidence collected
- Errors detected and fixed

---

## 🔧 Configuration

### Change Investigation Frequency

Edit `.github/workflows/continuous-investigation.yml`:

```yaml
on:
  schedule:
    - cron: '0 */6 * * *'  # Change this line
```

Cron examples:
- `'0 */1 * * *'` - Every hour
- `'0 */12 * * *'` - Every 12 hours
- `'0 0 * * *'` - Once daily at midnight
- `'0 0 * * 0'` - Once weekly on Sunday

### Adjust Investigation Duration

Edit the workflow file, find the "Run Autonomous Investigation Cycle" step:

```yaml
python3 run_autonomous_cycle.py \
  --research-duration 15 \      # Change these values
  --orchestration-duration 15 \
  --tasks-duration 15
```

### Change Self-Healing Frequency

Edit `.github/workflows/self-healing.yml`:

```yaml
on:
  schedule:
    - cron: '0 */2 * * *'  # Change this line
```

---

## 🛡️ Security Features

### Identity Protection
- Investigation bot uses anonymous identity
- No personal information in commits
- Secure data handling

### Data Encryption
- Sensitive data encrypted
- Access control implemented
- Progressive disclosure

### Sealed Until Release
- Findings sealed until 95%+ complete
- Safety criteria must be met
- Controlled release process

---

## 📈 System Capabilities

### Autonomous Research
- Multi-source data collection
- Document analysis
- Web scraping
- Pattern recognition
- Knowledge gap discovery

### AI Orchestration
- Multi-AI coordination
- Long-game strategy planning
- Hypothesis generation
- Adaptive learning

### Continuous Tasks
- Swarm agent execution
- Parallel processing
- Priority-based scheduling
- Result aggregation

### Self-Healing
- Automatic error detection
- Self-diagnosis
- Auto-fix capabilities
- System validation

---

## 🚨 Troubleshooting

### Workflows Not Running

**Check:**
1. Repository is public (required for free GitHub Actions)
2. Actions are enabled in repository settings
3. Workflow files are in `.github/workflows/` directory
4. YAML syntax is valid

**Fix:**
```bash
# Regenerate workflows
python3 deploy_workflows.py

# Commit and push
git add .github/workflows/
git commit -m "Fix workflows"
git push
```

### Investigation Failing

**Check workflow logs:**
1. Go to Actions tab
2. Click on failed run
3. Expand failed step
4. Review error messages

**Common issues:**
- Python syntax errors → Self-healing will fix
- Data corruption → Self-healing will reinitialize
- Missing dependencies → Check setup.py

### No New Findings

**This is normal if:**
- No new data sources available
- All current leads exhausted
- Waiting for new information

**The system will:**
- Continue monitoring
- Search for new sources
- Identify knowledge gaps
- Plan future research

---

## 📞 Support

For issues or questions:
1. Check workflow logs in Actions tab
2. Review `data/recovery_log.json` for errors
3. Run `python3 autonomous_error_recovery.py` locally
4. Check `data/progress.json` for system status

---

## 🎯 Next Steps

After deployment:

1. **Monitor first few runs** - Check Actions tab
2. **Review reports** - Download and examine artifacts
3. **Adjust schedule** - Based on findings frequency
4. **Scale up** - Increase duration if needed
5. **Add data sources** - Configure new sources in code

---

## 📝 Notes

- **Free tier limit:** 2,000 minutes/month on GitHub Actions
- **Each cycle:** ~45-55 minutes
- **Frequency:** 4 runs per day = ~40 cycles/month
- **Well within limits** for continuous operation

For unlimited runs, upgrade to GitHub Pro or use self-hosted runners.
