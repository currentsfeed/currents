# Development Environment URL

**Updated**: February 24, 2026

## Current Dev URL

**https://sonic-ben-weekends-sao.trycloudflare.com**

This URL is running via Cloudflare Quick Tunnel (no account needed).

## Accessing Dev Environment

| Environment | URL | Branch | Port |
|-------------|-----|--------|------|
| **Production** | https://currents.global | main | 5555 |
| **Development** | https://sonic-ben-weekends-sao.trycloudflare.com | dev | 5556 |

## Important Notes

### ✅ Pros
- ✅ **Free** - No account needed
- ✅ **Stable** - URL stays the same as long as service runs
- ✅ **Automatic** - Restarts on reboot
- ✅ **Fast** - Cloudflare global CDN

### ⚠️ Limitations
- URL changes if service restarts
- No uptime guarantee (Cloudflare can kill it anytime)
- Random URL (not custom subdomain)

## Getting Current Dev URL

If the URL changes or you forget it, run:

```bash
tail -50 /var/log/cloudflared-dev.log | grep "trycloudflare.com"
```

Or:

```bash
sudo journalctl -u cloudflared-dev | grep "trycloudflare.com"
```

Output will show:
```
|  https://YOUR-URL-HERE.trycloudflare.com  |
```

## Service Management

### Check Status
```bash
sudo systemctl status cloudflared-dev
```

### Restart (will generate new URL)
```bash
sudo systemctl restart cloudflared-dev
# Wait 5 seconds, then check logs for new URL
tail -50 /var/log/cloudflared-dev.log | grep "trycloudflare.com"
```

### Stop/Start
```bash
sudo systemctl stop cloudflared-dev    # Stop tunnel
sudo systemctl start cloudflared-dev   # Start tunnel (new URL)
```

### View Logs
```bash
sudo journalctl -u cloudflared-dev -f  # Follow logs
tail -f /var/log/cloudflared-dev.log   # Or from log file
```

## Both Services Running

```bash
# Check all services
sudo systemctl status currents          # Production (5555)
sudo systemctl status currents-dev      # Dev app (5556)
sudo systemctl status cloudflared-dev   # Dev tunnel
```

All three services auto-start on reboot.

## Testing Dev Changes

1. Make changes in `/home/ubuntu/.openclaw/workspace/currents-dev`
2. Restart dev app: `sudo systemctl restart currents-dev`
3. Visit dev URL (tunnel stays running, no restart needed)
4. Test thoroughly
5. When ready, deploy to production (main branch)

## Upgrading to Permanent URL (Optional)

If you want a permanent `dev.currents.global` URL:

**Option A: Cloudflare Named Tunnel** (requires account access)
- Custom subdomain: dev.currents.global
- Permanent URL
- Better reliability

**Option B: Ngrok Paid** ($10/month)
- Custom subdomain
- Better than free tier

For now, the Quick Tunnel works and is free! 🎉

## Summary

✅ **Production**: https://currents.global (main branch, port 5555)
✅ **Development**: https://sonic-ben-weekends-sao.trycloudflare.com (dev branch, port 5556)

Both running independently - you control when to deploy dev → prod.
