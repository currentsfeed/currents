#!/usr/bin/env node
/**
 * MASS IMAGE REPLACEMENT SCRIPT
 * Replaces all dummyimage.com URLs with real professional photos from Unsplash
 * 
 * Run: node replace_all_images.js
 */

const sqlite3 = require('sqlite3').verbose();
const fs = require('fs');
const path = require('path');
const https = require('https');

const DB_PATH = './brain.db';
const IMAGES_DIR = './static/images';

// Unsplash Source API - curated high-quality photos
const UNSPLASH_BASE = 'https://images.unsplash.com';

// Category-based search terms for Unsplash
const CATEGORY_SEARCH_TERMS = {
  'Sports': [
    'photo-1461896836934-ffe607ba8211', // stadium
    'photo-1579952363873-27f3bade9f55', // basketball
    'photo-1554068865-24cecd4e34b8', // tennis court
    'photo-1517466787929-bc90951d0974', // hockey
    'photo-1577223625816-7546f9638e25', // soccer
  ],
  'Politics': [
    'photo-1529107386315-e1a2ed48a620', // capitol building
    'photo-1551269901-5c5e14c25df7', // government
    'photo-1432821596592-e2c18b78144f', // white house
    'photo-1529107386315-e1a2ed48a620', // washington dc
  ],
  'Economics': [
    'photo-1611974789855-9c2a0a7236a3', // stock market
    'photo-1460925895917-afdab827c52f', // business
    'photo-1559526324-593bc073d938', // finance
    'photo-1611974789855-9c2a0a7236a3', // wall street
  ],
  'Crypto': [
    'photo-1621416894569-0f39ed31d247', // cryptocurrency
    'photo-1639762681485-074b7f938ba0', // blockchain
    'photo-1622630998477-20aa696ecb05', // bitcoin
    'photo-1622186477895-f2af6a0f5a97', // digital currency
  ],
  'Entertainment': [
    'photo-1594908900066-3f47337549d8', // hollywood
    'photo-1489599849927-2ee91cede3ba', // cinema
    'photo-1440404653325-ab127d49abc1', // red carpet
    'photo-1574267432644-f74ea26ed8b7', // entertainment
  ],
  'Technology': [
    'photo-1518770660439-4636190af475', // tech
    'photo-1485827404703-89b55fcc595e', // AI/computers
    'photo-1526374965328-7f61d4dc18c5', // innovation
    'photo-1496171367470-9ed9a91ea931', // data
  ],
  'World': [
    'photo-1526778548025-fa2f459cd5c1', // international
    'photo-1451187580459-43490279c0fa', // global
    'photo-1488646953014-85cb44e25828', // diplomacy
    'photo-1523961131990-5ea7c61b2107', // world
  ],
  'Crime': [
    'photo-1589829545856-d10d557cf95f', // courthouse
    'photo-1516979187457-637abb4f9353', // justice
    'photo-1479142506502-19b3a3b7ff33', // legal
    'photo-1505142468610-359e7d316be0', // law
  ],
  'Culture': [
    'photo-1493711662062-fa541adb3fc8', // culture
    'photo-1523961131990-5ea7c61b2107', // society
    'photo-1519681393784-d120267933ba', // community
  ]
};

// Download image from URL
function downloadImage(url, filepath) {
  return new Promise((resolve, reject) => {
    const file = fs.createWriteStream(filepath);
    https.get(url, (response) => {
      response.pipe(file);
      file.on('finish', () => {
        file.close();
        resolve();
      });
    }).on('error', (err) => {
      fs.unlink(filepath, () => {});
      reject(err);
    });
  });
}

// Get Unsplash image URL for a market
function getUnsplashImageUrl(market, index = 0) {
  const category = market.category || 'Sports';
  const searchTerms = CATEGORY_SEARCH_TERMS[category] || CATEGORY_SEARCH_TERMS['Sports'];
  
  // Use market_id hash to pick consistent image for same market
  const photoIndex = Math.abs(market.market_id.split('').reduce((a, b) => {
    return ((a << 5) - a) + b.charCodeAt(0);
  }, 0)) % searchTerms.length;
  
  const photoId = searchTerms[photoIndex];
  return `${UNSPLASH_BASE}/${photoId}?w=1600&h=900&fit=crop&q=80`;
}

async function main() {
  console.log('🚀 MASS IMAGE REPLACEMENT STARTING...\n');
  
  // Connect to database
  const db = new sqlite3.Database(DB_PATH);
  
  // Get all markets with dummyimage URLs
  db.all(
    `SELECT market_id, title, category, image_url 
     FROM markets 
     WHERE image_url LIKE '%dummyimage%'
     ORDER BY category, market_id`,
    async (err, markets) => {
      if (err) {
        console.error('❌ Database error:', err);
        process.exit(1);
      }
      
      console.log(`📊 Found ${markets.length} markets with dummyimage URLs\n`);
      
      let successCount = 0;
      let failCount = 0;
      
      for (let i = 0; i < markets.length; i++) {
        const market = markets[i];
        const filename = `market_${market.market_id}.jpg`;
        const filepath = path.join(IMAGES_DIR, filename);
        
        try {
          // Get appropriate image URL
          const imageUrl = getUnsplashImageUrl(market);
          
          // Download image
          console.log(`[${i + 1}/${markets.length}] ${market.market_id}: ${market.title.substring(0, 50)}...`);
          await downloadImage(imageUrl, filepath);
          
          // Update database
          await new Promise((resolve, reject) => {
            db.run(
              `UPDATE markets SET image_url = ? WHERE market_id = ?`,
              [`/static/images/${filename}`, market.market_id],
              (err) => {
                if (err) reject(err);
                else resolve();
              }
            );
          });
          
          console.log(`   ✅ Downloaded and updated`);
          successCount++;
          
          // Rate limiting - wait 200ms between requests
          await new Promise(resolve => setTimeout(resolve, 200));
          
        } catch (error) {
          console.log(`   ❌ Failed: ${error.message}`);
          failCount++;
        }
      }
      
      console.log(`\n🎉 COMPLETE!`);
      console.log(`   ✅ Success: ${successCount}`);
      console.log(`   ❌ Failed: ${failCount}`);
      console.log(`   📊 Total: ${markets.length}`);
      
      db.close();
    }
  );
}

main().catch(console.error);
