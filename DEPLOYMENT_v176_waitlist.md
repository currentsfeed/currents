# Deployment v176 - Coming Soon / Waiting List Page

**Date**: February 16, 2026 09:21 UTC  
**Status**: ✅ DEPLOYED  
**Request**: Roy Shaham - Full-site coming soon page with belief-based waitlist

## Overview

Created a complete "Coming Soon" page that:
- Collects email addresses via belief-driven interaction
- Frames waitlist as editorial question: "Will Currents be live by March 20?"
- Provides deterministic reason to return at launch
- NO markets, wagering, money, odds, or probabilities
- Works on mobile and desktop
- Includes "Go to site" button for testing access

## Core Concept

**Single Editorial Belief Question**: "Will Currents be live by March 20?"
- Users select YES or NO
- Submit email to record belief
- Get confirmation message
- Promise of resolution email + early access if correct

## Page URL

**Coming Soon Page**: https://proliferative-daleyza-benthonic.ngrok-free.dev/coming-soon

**Main Site** (still accessible): https://proliferative-daleyza-benthonic.ngrok-free.dev/

## User Flow

### State A - Initial
- Currents logo + tagline "News, measured in belief"
- Large headline: "Will Currents be live by March 20?"
- Disclaimer: "No money. No wagering. Just belief."
- Two large buttons: YES | NO
- Both buttons active

### State B - Belief Selected
**Triggered**: Immediately after YES or NO selection
**Behavior**:
- Selected button highlighted (red glow)
- Non-selected button disabled (opacity 0.3)
- Buttons locked (no change allowed)
- Animation: pulse on selected button
- Message appears: "We'll record your belief and notify you when the outcome is known."
- Email input slides in after 800ms

### State C - Email Submission
**Email Input**:
- Large input field: "your@email.com"
- Primary CTA button: "Save my answer"
- Email validation (format + uniqueness)
- Error messages for invalid/duplicate emails

**Validation Rules**:
- Standard emails: Must be valid format + unique
- Test email "testtt": Bypasses all validation

### State D - Confirmation
**Shown after successful submission**:
- ✅ Green checkmark icon
- "Your belief has been recorded."
- "If you're correct, you'll receive early access to Currents before public launch."
- "We'll email you when the answer is known."

## Database Schema

**Table**: `waitlist_submissions`

```sql
CREATE TABLE waitlist_submissions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL,
    belief_choice TEXT NOT NULL CHECK(belief_choice IN ('YES', 'NO')),
    timestamp_submitted DATETIME DEFAULT CURRENT_TIMESTAMP,
    source TEXT DEFAULT 'currents_launch_waitlist',
    device_type TEXT,
    locale TEXT,
    resolved_correct INTEGER,
    is_test_submission INTEGER DEFAULT 0,
    user_agent TEXT,
    ip_address TEXT
);
```

**Indexes**:
- `idx_email` on email (for duplicate checking)
- `idx_test` on is_test_submission (for filtering)

## API Endpoints

### POST /api/waitlist/submit
Submits waitlist entry with belief and email.

**Request**:
```json
{
  "email": "user@example.com",
  "belief_choice": "YES",
  "device_type": "mobile",
  "locale": "en-US"
}
```

**Success Response (200)**:
```json
{
  "success": true,
  "submission_id": 123,
  "belief": "YES"
}
```

**Duplicate Email Error (409)**:
```json
{
  "error": "This email is already on the Currents waiting list.",
  "secondary": "We'll notify you when the outcome is known."
}
```

**Validation Error (400)**:
```json
{
  "error": "Please enter a valid email address"
}
```

### GET /api/waitlist/stats
Returns waitlist statistics (excludes test submissions).

**Response**:
```json
{
  "total": 42,
  "yes": 30,
  "no": 12,
  "yes_percentage": 71.4,
  "no_percentage": 28.6,
  "devices": {
    "mobile": 25,
    "desktop": 17
  }
}
```

## Test Email Override

**Special Email**: `testtt` (case-insensitive)

**Behavior**:
- ✅ Email format validation: SKIPPED
- ✅ Duplicate checking: BYPASSED (allows multiple submissions)
- ✅ Database flag: `is_test_submission = 1`
- ✅ Excluded from analytics/stats
- 📧 Email routing: All outbound emails sent to **roy@rain.one**

**Use Cases**:
- Testing submission flow without real emails
- Multiple test submissions without cleaning database
- QA verification without affecting real user counts

## Email Uniqueness

**Standard Emails**:
- Must be unique (one submission per email)
- Duplicate attempt returns 409 error with friendly message
- Original belief preserved (no overwriting)

**Test Email Exception**:
- "testtt" allows unlimited duplicates
- Each submission gets unique ID
- All marked as test submissions

## Data Captured Per Submission

- `email`: User's email address (or "testtt")
- `belief_choice`: "YES" or "NO"
- `timestamp_submitted`: Auto-generated
- `source`: "currents_launch_waitlist"
- `device_type`: "mobile" or "desktop" (from User-Agent)
- `locale`: Browser locale (e.g., "en-US")
- `resolved_correct`: NULL until resolution (true/false after March 20)
- `is_test_submission`: 0 (real) or 1 (test email)
- `user_agent`: Full browser User-Agent string
- `ip_address`: User's IP (from X-Forwarded-For or remote_addr)

## Resolution Logic (Post-March 20)

**Resolution Date**: March 20, 2026 or later

**Outcome Determination**:
- YES is correct if Currents is publicly accessible by March 20
- NO is correct otherwise
- Resolution can be manual or automated

**Email Cases**:

### User Correct
Email content:
- ✅ Confirmation: "You were right!"
- 🎁 Early access link (if site is live)
- 🏆 Recognition as "Founding Believer"

### User Incorrect
Email content:
- 📊 Outcome explanation
- 🔗 Access link (if site is live)
- Neutral/positive tone (no penalty language)

## "Bonus" for Correct Belief

**Non-Financial Rewards**:
- ✅ Early access to Currents before public launch
- ✅ Conceptual recognition as early believer

**Explicitly Excluded**:
- ❌ Money
- ❌ Tokens
- ❌ Points
- ❌ Rankings
- ❌ Leaderboards

## Testing Access

**Bottom Button**: "Go to site"
- Fixed position at bottom center
- Always visible
- Links to main Currents site (/)
- For testing/development access only
- **Roy will remove when ready for public launch**

## Responsive Design

**Mobile**:
- Vertical layout
- Large touch targets (buttons 6-8 rem padding)
- 3xl-4xl text for question
- Single column form

**Desktop**:
- Centered content (max-width: 2xl)
- 5xl-6xl text for question
- Side-by-side YES/NO buttons
- Larger spacing

**Typography**:
- Font: Inter (Google Fonts)
- Weights: 300-800 range
- Clean, modern aesthetic

## Visual Design

**Colors**:
- Background: Dark gradient (slate-900 → slate-700)
- Primary: Currents red (#ef4444)
- Text: White with gray variations
- Buttons: Gray-800 → Red hover/selected

**Animations**:
- Fade-in transitions (0.5s)
- Button hover: translateY(-2px) + shadow
- Selected: Red glow (box-shadow)
- Pulse animation on confirmation message

**Branding**:
- Currents horizontal logo
- Consistent red accent color
- Currents typography style

## Compliance & Safety

**Clear Microcopy**:
- "No money. No wagering. Just belief."
- Explicitly not a prediction market
- Editorial participation framing

**No Financial Elements**:
- ❌ No odds display
- ❌ No probabilities
- ❌ No implied payouts
- ❌ No competitive ranking

## Success Metrics (Tracked)

**Interaction Rates**:
- YES/NO selection rate
- Email submission rate post-belief
- Duplicate email attempt rate

**Resolution Metrics**:
- Email open rate (resolution emails)
- Click-through to Currents at launch
- Early access conversion

## Files Created/Modified

**New Files**:
- `templates/coming_soon.html` - Full coming soon page
- `DEPLOYMENT_v176_waitlist.md` - This documentation

**Modified Files**:
- `app.py` - Added 3 routes:
  - `/coming-soon` (page)
  - `/api/waitlist/submit` (submission)
  - `/api/waitlist/stats` (analytics)
- `brain.db` - Added `waitlist_submissions` table with indexes

## Verification Tests

✅ **Page loads**: https://proliferative-daleyza-benthonic.ngrok-free.dev/coming-soon
✅ **Test email submission**: testtt → YES → Success (id=1)
✅ **Regular email submission**: test@example.com → NO → Success (id=2)
✅ **Duplicate rejection**: test@example.com → YES → Error 409
✅ **Test email duplicate**: testtt → NO → Success (id=3) - allowed
✅ **Stats endpoint**: Correctly excludes test submissions (total=1)
✅ **Database storage**: All fields populated correctly
✅ **Mobile responsive**: Tested with mobile viewport
✅ **Desktop layout**: Tested with desktop viewport
✅ **"Go to site" button**: Links to main site correctly

## Implementation Notes

**Test Email Behavior**:
- Stored as-is in database ("testtt")
- Not transformed or hashed
- Easy to identify and filter
- Separate flag for clarity

**Duplicate Detection**:
- Query checks for existing email WHERE is_test_submission = 0
- Test submissions don't interfere with real user checks
- Efficient index on email column

**Error Handling**:
- Validation errors: 400 status
- Duplicate emails: 409 status with friendly message
- Server errors: 500 status with generic message
- All errors logged to Flask logger

## Future Enhancements (Out of Scope)

**Post-MVP Features**:
- Show aggregate belief distribution (%)
- Multiple belief questions
- Belief history inside Currents account
- Social sharing of belief
- Countdown timer to March 20

## Deployment Commands

```bash
# Create database table
cd /home/ubuntu/.openclaw/workspace/currents-full-local
sqlite3 brain.db < create_waitlist_table.sql

# Restart service
sudo systemctl restart currents

# Verify service
sudo systemctl status currents

# Test submission
curl -X POST https://proliferative-daleyza-benthonic.ngrok-free.dev/api/waitlist/submit \
  -H "Content-Type: application/json" \
  -d '{"email":"testtt","belief_choice":"YES","device_type":"desktop","locale":"en-US"}'
```

## Next Steps

1. **Roy Review**: Check mobile + desktop layouts, copy, flow
2. **Email Integration**: Set up resolution emails (correct/incorrect)
3. **Launch Decision**: Roy removes "Go to site" button when ready
4. **Route Configuration**: Optionally make /coming-soon the default route
5. **Analytics**: Monitor submission rates and belief distribution
6. **March 20 Resolution**: Determine outcome and send resolution emails

---

**Status**: ✅ Fully functional, ready for Roy's review
**Version**: v176
**Deployment Time**: 2026-02-16 09:21 UTC
