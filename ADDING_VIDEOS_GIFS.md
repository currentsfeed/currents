# Adding Videos & GIFs to Markets

**Quick guide to replace market images with videos or animated GIFs**

---

## 🎬 **Supported Formats:**

- ✅ **GIF** (`.gif`) - Animated images
- ✅ **MP4** (`.mp4`) - Best for videos (widely supported)
- ✅ **WebM** (`.webm`) - Alternative video format
- ✅ **JPEG/PNG** (`.jpg`, `.png`) - Still images (current)

---

## 📁 **Step 1: Add Video/GIF Files**

Place your video/GIF files in the images directory:

```bash
/home/ubuntu/.openclaw/workspace/currents-full-local/static/images/

# Examples:
static/images/nba-lakers-warriors.mp4
static/images/tech-ai-news.gif
static/images/crypto-bitcoin.webm
```

---

## 🗄️ **Step 2: Update Database**

Update the market's `image_url` to point to the video/GIF:

```sql
UPDATE markets 
SET image_url = '/static/images/nba-lakers-warriors.mp4'
WHERE market_id = 'nba-lakers-warriors-feb19';

-- Or for GIF:
UPDATE markets 
SET image_url = '/static/images/crypto-bitcoin.gif'
WHERE market_id = 'btc-100k-2026';
```

---

## 🎨 **Step 3: Templates Auto-Detect**

The templates will automatically:
- Detect file extensions (`.mp4`, `.webm`, `.gif`)
- Render `<video>` tags for videos
- Render `<img>` tags for GIFs and images
- Auto-play videos (muted, looping)

---

## 💡 **Quick Test:**

Try replacing 3-5 sports markets with videos/GIFs to see how they look!

**Good candidates:**
- NBA/NFL games → action highlight videos
- Tech markets → product demo GIFs
- Crypto markets → animated charts

---

## 📏 **Video Recommendations:**

**Optimal specs:**
- **Resolution**: 1920x1080 (1080p) or 1280x720 (720p)
- **Aspect ratio**: 16:9 (landscape)
- **Duration**: 3-10 seconds (short loops work best)
- **File size**: Under 5MB for fast loading
- **Format**: MP4 (H.264 codec) for best compatibility

**Compress videos:**
```bash
# Using ffmpeg to optimize:
ffmpeg -i input.mp4 -vcodec h264 -acodec aac -b:v 1000k output.mp4
```

---

## 🔄 **Current Template Support:**

Templates automatically support mixed media:
- Hero section: Videos/GIFs/Images
- Grid cards: Videos/GIFs/Images  
- Mobile feed: Videos/GIFs/Images
- Detail pages: Videos/GIFs/Images

**No code changes needed** - just update the database `image_url`!

---

## 📝 **Example: Replace 5 Markets**

```sql
-- Replace with videos
UPDATE markets SET image_url = '/static/images/nba-action.mp4' WHERE market_id = 'nba-lakers-warriors-feb19';
UPDATE markets SET image_url = '/static/images/nfl-highlights.mp4' WHERE market_id = 'nfl-superbowl-2026';

-- Replace with GIFs
UPDATE markets SET image_url = '/static/images/crypto-chart.gif' WHERE market_id = 'btc-100k-2026';
UPDATE markets SET image_url = '/static/images/tech-demo.gif' WHERE market_id = 'apple-vision-pro';
UPDATE markets SET image_url = '/static/images/politics-debate.gif' WHERE market_id = 'us-election-2026';
```

---

## 🎯 **Where to Find Videos/GIFs:**

**Free sources:**
- **Pexels Videos**: https://pexels.com/videos/
- **Pixabay**: https://pixabay.com/videos/
- **Giphy**: https://giphy.com (GIFs)
- **Tenor**: https://tenor.com (GIFs)

**Sports:**
- NBA/NFL highlight clips
- ESPN replays

**Tech:**
- Product demos
- UI animations

---

## ⚙️ **Technical Details:**

Videos will render as:
```html
<video autoplay muted loop playsinline class="...">
  <source src="/static/images/market.mp4" type="video/mp4">
  <source src="/static/images/market.webm" type="video/webm">
</video>
```

GIFs render as regular images:
```html
<img src="/static/images/market.gif" alt="...">
```

---

## 🚀 **Next Steps:**

1. Download 5 test videos/GIFs
2. Upload to `static/images/`
3. Update 5 markets in database
4. Test on dev site
5. If good, expand to more markets!

Ready to try it? Let me know which markets you want to convert first! 🎬
