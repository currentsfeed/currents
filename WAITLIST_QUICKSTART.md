# Currents Waitlist - Quick Start Guide

## 🔗 URLs

**Coming Soon Page**: https://proliferative-daleyza-benthonic.ngrok-free.dev/coming-soon  
**Main Site** (via bottom button): https://proliferative-daleyza-benthonic.ngrok-free.dev/

## 📱 How It Works

### User Experience
1. See question: "Will Currents be live by March 20?"
2. Choose: YES or NO
3. Enter email
4. Get confirmation: "Your belief has been recorded"
5. Promise: Early access if correct

### Test Mode
- **Bottom button** "Go to site" allows you to still access main Currents
- Remove this button when ready for public launch

## 🧪 Testing

### Test Email Override
Use email: **testtt**

**Benefits**:
- ✅ No email validation
- ✅ Unlimited submissions (no duplicate rejection)
- ✅ Excluded from stats/analytics
- 📧 Future emails will go to: **roy@rain.one**

**Example Test Flow**:
1. Go to /coming-soon
2. Click YES or NO
3. Enter: testtt
4. Click "Save my answer"
5. See confirmation ✅

You can repeat this as many times as you want.

## 📊 Check Submissions

### Quick Script
```bash
cd /home/ubuntu/.openclaw/workspace/currents-full-local
./check_waitlist.sh
```

This shows:
- Total submissions (real vs test)
- YES/NO breakdown
- Recent entries
- Device types

### API Endpoint
```bash
curl https://proliferative-daleyza-benthonic.ngrok-free.dev/api/waitlist/stats
```

Returns JSON with:
- total, yes, no counts
- yes_percentage, no_percentage
- devices breakdown

## 📧 Email Logic

### Test Submissions (email = "testtt")
- All emails sent to: **roy@rain.one**
- Excluded from public stats
- Marked as test in database

### Real Submissions
- Emails sent to actual address
- Included in stats
- Unique per email (duplicates rejected)

## 🎯 Resolution (After March 20)

### Manual Resolution
1. Determine if Currents is live by March 20
2. Mark correct users: `UPDATE waitlist_submissions SET resolved_correct = 1 WHERE belief_choice = 'YES'` (or NO)
3. Send resolution emails:
   - **Correct users**: Early access link + "Founding Believer" recognition
   - **Incorrect users**: Outcome explanation + access link

### Database Query
```sql
-- Get all unresolved submissions
SELECT * FROM waitlist_submissions 
WHERE resolved_correct IS NULL 
AND is_test_submission = 0
ORDER BY timestamp_submitted;

-- Mark correct beliefs (example: YES was correct)
UPDATE waitlist_submissions 
SET resolved_correct = 1 
WHERE belief_choice = 'YES' AND is_test_submission = 0;

UPDATE waitlist_submissions 
SET resolved_correct = 0 
WHERE belief_choice = 'NO' AND is_test_submission = 0;
```

## 🚀 Launch Checklist

When ready to make this the main landing page:

### Option 1: Keep as Separate Page
- Share link: /coming-soon
- Main site still at /
- Users can toggle between them

### Option 2: Make Default
Modify `app.py`:
```python
@app.route('/')
def home():
    # Redirect to coming soon until launch
    return redirect('/coming-soon')
```

### Option 3: Full Replacement
1. Remove "Go to site" button from coming_soon.html
2. Make /coming-soon the only accessible page
3. Disable all other routes until launch

## 🎨 Customization

### Change Question/Date
Edit `templates/coming_soon.html`:
```html
<h1>Will Currents be live by<br><span class="currents-red">March 20?</span></h1>
```

### Change Colors
```css
.currents-red { color: #ef4444; }  /* Change to your preferred color */
```

### Change Copy
All text is in `coming_soon.html`:
- Tagline: "News, measured in belief"
- Disclaimer: "No money. No wagering. Just belief."
- Confirmation messages

## 📈 Success Metrics

Monitor these:
- **Conversion Rate**: Belief clicks → Email submissions
- **Belief Distribution**: YES% vs NO%
- **Device Split**: Mobile vs Desktop
- **Duplicate Attempts**: How many tried to submit twice
- **Resolution Open Rate**: Email opens after March 20

## ⚠️ Important Notes

### Compliance
- ✅ No odds displayed
- ✅ No probabilities shown
- ✅ No financial language
- ✅ Clear "No money. No wagering. Just belief."
- ✅ Editorial participation framing

### Data Privacy
- Store minimal data
- Clear purpose: resolution + early access
- No third-party sharing
- Secure storage

### Test Email Handling
- "testtt" is case-insensitive
- Automatically flagged in database
- Never counted in public metrics
- Always routes to roy@rain.one

## 💬 Support

Questions? Issues?
- Check logs: `sudo journalctl -u currents -f`
- Check database: `sqlite3 brain.db "SELECT * FROM waitlist_submissions ORDER BY id DESC LIMIT 10;"`
- Test API: `curl -X POST .../api/waitlist/submit -d '{"email":"testtt","belief_choice":"YES",...}'`

---

**Version**: v176  
**Deployed**: 2026-02-16 09:21 UTC  
**Status**: ✅ Ready for testing
