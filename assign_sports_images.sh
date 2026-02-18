#!/bin/bash
# Assign existing sports images to new markets

IMG_DIR="static/images"

echo "============================================================"
echo "ASSIGNING EXISTING IMAGES TO NEW SPORTS MARKETS"
echo "============================================================"

# Copy existing images to new market filenames
cp "${IMG_DIR}/basketball_nba_action_1.jpg" "${IMG_DIR}/nba-lakers-warriors.jpg"
echo "✅ nba-lakers-warriors.jpg"

cp "${IMG_DIR}/basketball_nba_action_2.jpg" "${IMG_DIR}/nba-celtics-bucks.jpg"
echo "✅ nba-celtics-bucks.jpg"

cp "${IMG_DIR}/basketball_nba_arena_1.jpg" "${IMG_DIR}/nba-nuggets-suns.jpg"
echo "✅ nba-nuggets-suns.jpg"

cp "${IMG_DIR}/basketball_nba_player_1.jpg" "${IMG_DIR}/nba-embiid-knicks.jpg"
echo "✅ nba-embiid-knicks.jpg"

cp "${IMG_DIR}/hockey_nhl_action_1.jpg" "${IMG_DIR}/nhl-leafs-bruins.jpg"
echo "✅ nhl-leafs-bruins.jpg"

cp "${IMG_DIR}/ice_hockey_game_1.jpg" "${IMG_DIR}/nhl-oilers-flames.jpg"
echo "✅ nhl-oilers-flames.jpg"

cp "${IMG_DIR}/ice_hockey_match_1.jpg" "${IMG_DIR}/nhl-rangers-islanders.jpg"
echo "✅ nhl-rangers-islanders.jpg"

cp "${IMG_DIR}/ucl-bayern.jpg" "${IMG_DIR}/ucl-bayern-arsenal.jpg"
echo "✅ ucl-bayern-arsenal.jpg"

cp "${IMG_DIR}/ucl-psg-barca.jpg" "${IMG_DIR}/ucl-psg-sociedad.jpg"
echo "✅ ucl-psg-sociedad.jpg"

cp "${IMG_DIR}/soccer_ucl_match_1.jpg" "${IMG_DIR}/ucl-both-teams-score.jpg"
echo "✅ ucl-both-teams-score.jpg"

cp "${IMG_DIR}/epl-mancity.jpg" "${IMG_DIR}/epl-arsenal-mancity.jpg"
echo "✅ epl-arsenal-mancity.jpg"

cp "${IMG_DIR}/epl-liverpool-arsenal.jpg" "${IMG_DIR}/epl-liverpool-chelsea.jpg"
echo "✅ epl-liverpool-chelsea.jpg"

cp "${IMG_DIR}/soccer_premier_league_action_1.jpg" "${IMG_DIR}/epl-salah-chelsea.jpg"
echo "✅ epl-salah-chelsea.jpg"

cp "${IMG_DIR}/laliga-match.jpg" "${IMG_DIR}/laliga-madrid-derby.jpg"
echo "✅ laliga-madrid-derby.jpg"

cp "${IMG_DIR}/soccer_laliga_match_1.jpg" "${IMG_DIR}/laliga-barcelona-sevilla.jpg"
echo "✅ laliga-barcelona-sevilla.jpg"

cp "${IMG_DIR}/bundesliga-stadium.jpg" "${IMG_DIR}/bundesliga-bayern-leipzig.jpg"
echo "✅ bundesliga-bayern-leipzig.jpg"

cp "${IMG_DIR}/soccer_seriea_action_1.jpg" "${IMG_DIR}/seriea-juventus-napoli.jpg"
echo "✅ seriea-juventus-napoli.jpg"

cp "${IMG_DIR}/soccer_seriea_match_1.jpg" "${IMG_DIR}/seriea-inter-roma.jpg"
echo "✅ seriea-inter-roma.jpg"

cp "${IMG_DIR}/rugby_match_1.jpg" "${IMG_DIR}/rugby-france-scotland.jpg"
echo "✅ rugby-france-scotland.jpg"

cp "${IMG_DIR}/nfl-49ers-superbowl.jpg" "${IMG_DIR}/nfl-combine-record.jpg"
echo "✅ nfl-combine-record.jpg"

echo ""
echo "============================================================"
echo "COMPLETE: All 20 images assigned"
echo "============================================================"
