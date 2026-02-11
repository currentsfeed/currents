#!/usr/bin/env python3
"""Add editorial descriptions to top 9 markets"""
import sqlite3

descriptions = {
    '517311': "ICE removed 271,000 non-citizens in FY2024, but Trump's campaign promises dwarf that number. Mass deportation infrastructure and political will remain the critical unknowns.",
    '553842': "The Islanders haven't hoisted the Cup since their dynasty era ended in 1983. With a retooled roster and playoff experience, this could finally be their year to end the drought.",
    '553838': "Minnesota has never won a Stanley Cup despite decades of hockey tradition. Strong goaltending and a deep forward group have them positioned for a historic breakthrough.",
    '549874': "Dutch coalition talks are at a critical juncture after months of deadlock. Jetten's D66 party holds leverage in forming the next government, but kingmaker status doesn't guarantee the crown.",
    '540881': "Rockstar's most anticipated release in over a decade has been delayed multiple times. June 2026 is the current target, but industry insiders are hedging their bets on another pushback.",
    '550694': "The Azzurri's shocking absence from the 2022 World Cup sent shockwaves through Italian football. With qualifying underway, redemption—or continued humiliation—hangs in the balance.",
    '517313': "Trump's deportation rhetoric has escalated from hundreds of thousands to millions. Logistical realities, court challenges, and local resistance could dramatically slow enforcement.",
    '544093': "Harvey Weinstein faces resentencing after his 2020 conviction was overturned on appeal. Prosecutors are pushing for maximum time, but his age and health complications may factor into the judge's decision.",
    'multi_003': "Trump takes office with a flurry of executive actions expected on Day One. Immigration crackdowns, trade tariffs, and energy policy reversals are all reportedly on the table—but which comes first?"
}

conn = sqlite3.connect('brain.db')
cursor = conn.cursor()

for market_id, desc in descriptions.items():
    cursor.execute(
        "UPDATE markets SET editorial_description = ? WHERE market_id = ?",
        (desc, market_id)
    )
    print(f"✓ Updated {market_id}")

conn.commit()
conn.close()
print("\n✅ All descriptions added!")
