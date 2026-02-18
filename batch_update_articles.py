#!/usr/bin/env python3
"""
Batch update article content for key markets
"""

import sqlite3
from datetime import datetime

DB_PATH = 'brain.db'

ARTICLES = {
    # GTA VI Markets
    '527079': {
        'title': 'GTA 6 Pricing Discussion',
        'text': '''## Industry Context

The gaming industry has seen AAA titles increase from $60 to $70 standard pricing in recent years. However, $100+ price points remain rare for base editions, typically reserved for collector's or ultimate editions with extensive bonus content.

## Rockstar's Position

Rockstar Games historically prices main entries conservatively for maximum market penetration. GTA V launched at $60 (2013) and became the most profitable entertainment product ever, largely due to accessible pricing combined with long-tail microtransaction revenue from GTA Online.

## Market Dynamics

**Arguments for $100+:**
- Decade-long development cycle with massive production costs
- Industry-leading production values and scope
- Inflation-adjusted pricing could justify premium positioning

**Arguments Against:**
- Console manufacturers typically resist extreme base pricing (affects hardware sales)
- Market precedent: even The Last of Us Part II, God of War Ragnarök remained at $70
- Rockstar's revenue strategy focuses on accessible base price + long-term online monetization

Most analysts expect standard edition at $70-80, with premium editions offering $100+ price points for collectors.
'''
    },
    
    'gta-6-release-2026': {
        'title': 'GTA 6 Release Timeline Analysis',
        'text': '''## Official Announcements

Rockstar Games officially announced GTA VI in December 2023, releasing the first trailer which showcased the game's setting (Vice City-inspired location) and confirmed 2025 as the release window. However, the company has since updated guidance to "2025" without specifying a quarter.

## Development History

Grand Theft Auto games have historically experienced delays:
- **GTA V**: Originally announced for Spring 2013, released September 2013
- **Red Dead Redemption 2**: Delayed twice from Fall 2017 to October 2018

## Industry Analysis

Most major analysts expect a late 2025 release at earliest, with 2026 being increasingly likely:

**Factors Supporting 2025:**
- Take-Two Interactive's fiscal guidance suggests major release
- Marketing cycle typically begins 6-9 months before launch
- Next-gen console installed base now mature

**Factors Supporting 2026:**
- Minimal marketing activity beyond initial trailer
- Rockstar's quality-first approach and history of delays
- Reports of extensive playtesting and polish phase

A Spring/Summer 2026 release would give adequate time for marketing buildup while meeting Take-Two's fiscal targets.
'''
    },
    
    'taylor-swift-new-album-2026-hypothetical': {
        'title': 'Taylor Swift Album Release Patterns',
        'text': '''## Release History

Taylor Swift has maintained an extraordinarily active release schedule in recent years:
- **2020**: folklore (July), evermore (December)
- **2021**: Fearless (Taylor's Version), Red (Taylor's Version)
- **2022**: Midnights (new album)
- **2023**: Speak Now (Taylor's Version), 1989 (Taylor's Version)
- **2024**: The Tortured Poets Department

## Current Projects

Swift is completing her re-recording project ("Taylor's Version" albums) to reclaim masters of her early work. Two albums remain: debut self-titled album and Reputation. Many fans expect these before new original material.

## Tour Schedule

The Eras Tour concluded in late 2024 after an unprecedented 18-month run. Historically, Swift takes creative breaks between tours to write new material, though her 2020-2024 output defied conventional release patterns.

## Surprise Album Precedent

Swift has established a pattern of surprise releases (folklore, evermore) without traditional marketing cycles. Her digital-first strategy and massive fanbase make surprise drops commercially viable.

A 2026 surprise album is plausible given her prolific output and fan base expectations, though completing re-recordings may take priority.
'''
    },
    
    'mcu-fantastic-four-box-office-2026': {
        'title': 'MCU Box Office Performance and Fantastic Four Expectations',
        'text': '''## MCU Box Office Context

Marvel Studios has delivered multiple $1B+ grossers, but recent performance has been mixed:
- **2023**: Guardians Vol. 3 ($845M), The Marvels ($206M)
- **2024**: Deadpool & Wolverine ($1.3B+), others varied

## Fantastic Four History

Previous Fantastic Four films underperformed:
- **2005**: $330M worldwide
- **2007**: $289M worldwide
- **2015**: $168M worldwide (critical disaster)

The franchise has struggled with general audiences despite strong comic book pedigree.

## 2026 Film Prospects

**Positive Factors:**
- MCU integration brings established universe and crossover potential
- Galactus rumored as villain (massive scale event)
- Post-Multiverse Saga positioning as new era foundation
- Pedro Pascal rumored casting brings star power

**Challenging Factors:**
- Franchise fatigue concerns in superhero genre
- Previous FF films created stigma
- Competition from other 2026 tentpoles

$1B+ is achievable but far from guaranteed. The film needs exceptional reviews and strong word-of-mouth to overcome franchise history and superhero fatigue. Comparable: Doctor Strange in the Multiverse of Madness ($955M) and Thor: Love and Thunder ($760M) show MCU branding alone doesn't guarantee $1B.
'''
    },
    
    'new_60034': {
        'title': 'Barbie Oscar Campaign and Best Picture Prospects',
        'text': '''## Box Office and Cultural Impact

*Barbie* (2023) became a genuine cultural phenomenon, grossing $1.4+ billion worldwide and dominating summer 2023 conversation. The film's success transcended typical blockbuster metrics, spawning memes, fashion trends, and serious cultural commentary about gender, identity, and nostalgia.

## Oscar Precedent for Blockbusters

Historically, box office juggernauts face uphill battles for Best Picture:
- **Winners**: Lord of the Rings: Return of the King (2003), Titanic (1997)
- **Nominees that Lost**: Avatar, Black Panther, Top Gun: Maverick
- **Snubbed**: The Dark Knight controversy led to field expansion

## Critical Reception

*Barbie* received positive reviews (88% Rotten Tomatoes, 80 Metacritic) with particular praise for:
- Greta Gerwig's direction
- Meta-commentary and satirical edge
- Production design and visual creativity
- Ryan Gosling and Margot Robbie's performances

However, some critics found the film's messaging heavy-handed or narratively uneven.

## 2026 Oscar Competition

The 2026 Oscars (recognizing 2025 films) will feature strong competition from auteur-driven projects, potential Oppenheimer-style biopics, and prestige dramas from A24, Netflix, and traditional studios.

Academy voters historically prefer dramas with social/historical weight over colorful comedies. *Barbie*'s chances depend on whether voters view it as substantive commentary or entertaining spectacle. Likely strong showings in technical categories, but Best Picture remains a longshot.
'''
    }
}

def update_articles():
    """Batch update article content"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    updated = 0
    for market_id, content in ARTICLES.items():
        cursor.execute("""
            UPDATE markets
            SET article_text = ?,
                article_source = ?,
                article_fetched_at = ?
            WHERE market_id = ?
        """, (
            content['text'],
            f"{content['title']} (Editorial Analysis)",
            datetime.now().isoformat(),
            market_id
        ))
        
        if cursor.rowcount > 0:
            updated += 1
            print(f"✓ Updated {market_id}: {content['title']}")
        else:
            print(f"✗ Market not found: {market_id}")
    
    conn.commit()
    conn.close()
    
    print(f"\n✅ Updated {updated}/{len(ARTICLES)} articles")

if __name__ == '__main__':
    update_articles()
