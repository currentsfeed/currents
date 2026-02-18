#!/usr/bin/env python3
"""
Fix Israeli/Iran markets - update 2025 references to 2026 and add dates to indefinite questions
"""

import sqlite3

# Markets to update
UPDATES = [
    # Update 2025 -> 2026 in questions
    ('israel_iran_c63e5615', 'Will Hamas remain in power in Gaza through 2026?', '2027-01-01'),
    ('israel_iran_cc132ea9', 'Will Israeli hostages all be released by July 2026?', '2026-08-01'),
    ('israel_iran_db250a54', 'Will Iran join BRICS officially in 2026?', '2027-01-01'),
    ('israel_iran_cc2db7b7', 'Will Gaza ceasefire last >90 days in 2026?', '2027-01-01'),
    ('israel_iran_ef04a424', 'Will Israeli judicial reform pass in 2026?', '2027-01-01'),
    ('israel_iran_0bc0e128', 'Will Iran enrich uranium above 90% by July 2026?', '2026-08-01'),
    ('israel_iran_6da148b7', 'Will EU sanction Israeli officials in 2026?', '2027-01-01'),
    ('israel_iran_d659bdce', 'Will >100K Israelis emigrate in 2026?', '2027-01-01'),
    ('israel_iran_49501c7d', 'Will Saudi Arabia normalize relations with Israel in 2026?', '2027-01-01'),
    ('israel_iran_c8f7f250', 'Will Israel invade South Lebanon in 2026?', '2027-01-01'),
    ('israel_iran_f2ba41d8', 'Will US strike Iranian targets in 2026?', '2027-01-01'),
    ('israel_iran_7ce10b74', 'Will Israel strike Iranian nuclear sites in 2026?', '2027-01-01'),
    ('israel_iran_382aaf0b', 'Will Iran directly attack Israel in 2026?', '2027-01-01'),
    ('israel_iran_fb35b3aa', 'Will Netanyahu remain PM through 2026?', '2027-01-01'),
    ('israel_iran_42838fca', 'Will US/Iran revive nuclear deal in 2026?', '2027-01-01'),
    ('israel_iran_9227999a', 'Will Israel hold early elections in 2026?', '2027-01-01'),
    
    # Add specific dates to questions that lack them
    ('israel_iran_a5451d7b', 'Will Hezbollah fire >1000 rockets at Israel in single day by Dec 2026?', '2027-01-01'),
    ('israel_iran_8848cddf', 'Will Israeli settlers surpass 1M in West Bank by Dec 2026?', '2027-01-01'),
    ('israel_iran_15fe4c12', 'Will Iran launch major cyberattack on Israel by Dec 2026?', '2027-01-01'),
    ('israel_iran_ed9b5959', 'Will ICC issue Netanyahu arrest warrant by Dec 2026?', '2027-01-01'),
    ('israel_iran_1b8f014b', 'Will Iran close Strait of Hormuz for >7 days by Dec 2026?', '2027-01-01'),
    ('israel_iran_8630eb70', 'Will Israel hit Iranian nuclear scientist by Dec 2026?', '2027-01-01'),
    ('israel_iran_19089d69', 'Will Iran sanctions be fully reimposed by US by Dec 2026?', '2027-01-01'),
    ('israel_iran_22b3a897', 'Will Nasrallah be killed/removed by Dec 2026?', '2027-01-01'),
]

def main():
    conn = sqlite3.connect('brain.db')
    cursor = conn.cursor()
    
    print("=" * 70)
    print("FIXING ISRAELI/IRAN MARKET DATES")
    print("=" * 70)
    
    updated_count = 0
    not_found = []
    
    for market_id, new_title, new_resolution_date in UPDATES:
        # Check if market exists
        cursor.execute("SELECT title FROM markets WHERE market_id = ?", (market_id,))
        result = cursor.fetchone()
        
        if result:
            old_title = result[0]
            
            # Update the market
            cursor.execute("""
                UPDATE markets 
                SET title = ?, resolution_date = ?
                WHERE market_id = ?
            """, (new_title, new_resolution_date, market_id))
            
            print(f"\n✅ {market_id}")
            print(f"  OLD: {old_title}")
            print(f"  NEW: {new_title}")
            print(f"  Resolution: {new_resolution_date}")
            
            updated_count += 1
        else:
            print(f"\n❌ NOT FOUND: {market_id}")
            not_found.append(market_id)
    
    conn.commit()
    conn.close()
    
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"✅ Updated: {updated_count}")
    print(f"❌ Not found: {len(not_found)}")
    
    if not_found:
        print("\nMarkets not found:")
        for mid in not_found:
            print(f"  - {mid}")

if __name__ == "__main__":
    main()
