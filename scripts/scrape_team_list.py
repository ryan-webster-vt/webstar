import cbbpy.mens_scraper as s
import json

conferences = [
    'American Athletic Conference', 'Atlantic 10 Conference', 'ASUN Conference', 'Big East Conference',
    'Big Sky Conference', 'Big South Conference', 'Big West Conference', 'Big 12 Conference', 'Big Ten Conference',
    'Coastal Athletic Association', 'Conference USA', 'Horizon League', 'Metro Atlantic Athletic Conference', 'Mountain West Conference',
    'Missouri Valley Conference', 'Southeastern Conference', 'Patriot League', 'Southern Conference', 'Summit League',
    'Sun Belt Conference', 'Atlantic Coast Conference', 'Southland Conference',
    'Mid-Eastern Athletic Conference', 'America East Conference', 'Northeast Conference', 'Southwestern Athletic Conference', 'Ivy League', 'Mid-American Conference', 'Ohio Valley Conference', 'West Coast Conference', 'Western Athletic Conference'
]

teams = set()

for conf in conferences:
    conf_teams = s.get_teams_from_conference(conf, season=2025)
    teams.update(conf_teams)

teams.add('New Haven')

teams = sorted(list(teams))

# Save to JSON file
with open("data/ncaa_teams.json", "w") as f:
    json.dump(teams, f, indent=4)

