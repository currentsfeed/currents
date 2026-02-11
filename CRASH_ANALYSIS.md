# 🔍 App Crash Analysis - Currents Flask App

**Date:** 2026-02-11  
**Issue:** Flask app crashing approximately every 1-1.5 hours  
**Impact:** Site becomes inaccessible (ERR_NGROK_8012)

---

## 📊 Crash Timeline

| Time (UTC) | Status | Notes |
|------------|--------|-------|
| 07:30 | ✅ Operational | Monitor check passed |
| 09:00 | ❌ DOWN | First detected crash |
| 09:00 | 🔄 Auto-restart attempted | Failed |
| 10:03 | ✅ Manual restart | Restarted via deploy script |
| 10:30 | ✅ Operational | Monitor check passed |
| 11:48 | ❌ DOWN | Second crash reported by Roy |
| 11:48 | ✅ Manual restart | Restarted immediately |

**Pattern:** App crashes approximately every 90-120 minutes

---

## 🔬 Root Cause Investigation

### Possible Causes:

1. **Memory Leak** ⚠️ HIGH LIKELIHOOD
   - Flask dev server not optimized for long-running processes
   - Personalization engine loading 200+ markets per request
   - No memory cleanup between requests
   - Evidence: Crashes after ~1-2 hours of operation

2. **SQLite Database Locking** 🟡 MEDIUM
   - Multiple concurrent reads/writes
   - No connection pooling configured
   - May cause deadlocks/crashes

3. **Nohup Process Management** 🟡 MEDIUM
   - nohup not reliably keeping process alive
   - No automatic restart on crash
   - Process killed by system without restart

4. **Resource Exhaustion** 🟡 MEDIUM
   - No memory limits set
   - No process supervision
   - OOM killer may be terminating process

5. **Flask Dev Server Limitations** 🟢 LOW
   - Not designed for production use
   - Single-threaded by default
   - May timeout on long requests

---

## ✅ Immediate Fix Applied

**Status:** ✅ SITE RESTORED (11:48 UTC)

**Action Taken:**
```bash
cd /home/ubuntu/.openclaw/workspace/currents-full-local
nohup python3 app.py > /tmp/currents-app.log 2>&1 &
```

**Verification:**
- ✅ Flask health check: OK
- ✅ Ngrok tunnel: Active
- ✅ Homepage loading: OK
- ✅ Hero rotation: Working

**URL:** https://proliferative-daleyza-benthonic.ngrok-free.dev

---

## 🛠️ Long-Term Solutions

### Option 1: Systemd Service (RECOMMENDED) ⭐

**Benefits:**
- Automatic restart on crash (within 10 seconds)
- Process supervision by systemd
- Centralized logging via journalctl
- Memory limits enforced (1GB max, 800MB high)
- Starts on server boot
- Industry-standard solution

**Setup:**
```bash
cd /home/ubuntu/.openclaw/workspace/currents-full-local
chmod +x setup-systemd.sh
./setup-systemd.sh
```

**Files Created:**
- `currents.service` - Systemd unit file
- `setup-systemd.sh` - Installation script

**Configuration:**
- Restart policy: Always
- Restart delay: 10 seconds
- Memory limit: 1GB (prevents OOM)
- Logs: /tmp/currents-app.log + journalctl

---

### Option 2: Production WSGI Server

**Use Gunicorn or uWSGI instead of Flask dev server:**

```bash
pip3 install gunicorn
gunicorn -w 4 -b 0.0.0.0:5555 app:app --daemon
```

**Benefits:**
- Multi-worker (better concurrency)
- Production-grade stability
- Better memory management
- Handles crashes gracefully

**Drawbacks:**
- Requires additional dependency
- More complex configuration

---

### Option 3: Supervisor

**Process control system:**

```bash
sudo apt install supervisor
# Configure supervisor to manage Flask app
```

**Benefits:**
- Automatic restart
- Web UI for monitoring
- Good for multiple processes

**Drawbacks:**
- Additional package to maintain
- Less native than systemd

---

## 📈 Current Monitoring

**Monitor Script:** `/home/ubuntu/.openclaw/workspace/currents-full-local/monitor_site.sh`  
**Cron Schedule:** Every 90 minutes  
**Logs:** `/tmp/site_monitor.log`

**Limitations:**
- Only checks every 90 minutes (downtime can last up to 90 min)
- Auto-restart often fails (requires manual intervention)
- No real-time alerting

---

## 🎯 Recommended Action Plan

### Immediate (Do Now):
1. ✅ **Manual restart completed** (site operational)
2. **Monitor closely** for next 2-3 hours

### Short-term (Next Session):
3. **Implement systemd service** (10 minutes setup)
   - Ensures automatic restart within 10 seconds
   - Prevents extended downtime
4. **Add memory profiling** to identify leaks
5. **Review personalization.py** for memory issues

### Medium-term (Before Demo):
6. **Switch to Gunicorn** for production stability
7. **Add database connection pooling**
8. **Implement proper error handling** in Flask routes
9. **Add health check endpoint** with memory stats

### Long-term (Production):
10. **Use Docker** with auto-restart policy
11. **Add proper logging** (structured logs, log rotation)
12. **Implement monitoring** (Prometheus/Grafana)
13. **Load testing** to identify breaking points

---

## 🚨 Emergency Restart Commands

**Quick restart (current method):**
```bash
pkill -f "python.*app.py"
cd /home/ubuntu/.openclaw/workspace/currents-full-local
nohup python3 app.py > /tmp/currents-app.log 2>&1 &
sleep 5
curl http://localhost:5555/health
```

**If systemd service installed:**
```bash
sudo systemctl restart currents
sudo systemctl status currents
```

**Check what killed the process:**
```bash
dmesg | grep -i kill | tail -20
tail -100 /var/log/syslog | grep -i python
```

---

## 📊 Memory Analysis (TODO)

**Commands to run during next crash:**
```bash
# Check memory usage before crash
ps aux | grep python | head -5

# Check OOM killer logs
dmesg | grep -i "out of memory"

# Monitor memory in real-time
watch -n 5 "ps aux | grep app.py"
```

---

## ✅ Current Status

**As of 2026-02-11 11:48 UTC:**
- ✅ Site operational
- ✅ Flask app running (PID: 81946)
- ✅ Ngrok tunnel active
- ⚠️ Using nohup (temporary, will crash again)
- ⚠️ No automatic restart configured

**Expected behavior:**
- Site will likely crash again in 1-2 hours
- Manual restart will be needed again UNLESS systemd is implemented

**Next crash prediction:** ~13:30-14:30 UTC

---

## 💡 Recommendation

**STRONGLY RECOMMEND implementing systemd service NOW** to prevent future crashes from causing extended downtime. Takes 5 minutes to set up and provides automatic recovery.

**Command:**
```bash
cd /home/ubuntu/.openclaw/workspace/currents-full-local
chmod +x setup-systemd.sh
./setup-systemd.sh
```

---

*Analysis completed: 2026-02-11 11:50 UTC*
