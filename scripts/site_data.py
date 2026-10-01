"""Source-of-truth facts for regionalschoolbusco.wiki.

Every value here was read from a public source on the date in CHECKED.
Live counters (players, visits, favorites, badge awards) are operational
snapshots, not stable facts. Do not add codes unless 3+ independent sources
list them as working (see scripts/test_site.py).
"""

SITE = "https://regionalschoolbusco.wiki"
CHECKED = "2026-10-01"          # content round date (UTC)
CHECKED_HUMAN = "October 1, 2026"

GAME = {
    "name": "Regional School Bus Co",
    "alt_name": "RBC's School Bus Simulator: Upstate Region",
    "former_brand": "Regional Bus Company",
    "creator": "Regional Bus Community",
    "creator_group_id": 86590100,
    "place_id": 93172673274529,
    "universe_id": 10453366727,
    "url": "https://www.roblox.com/games/93172673274529/Regional-School-Bus-Co",
    "group_url": "https://www.roblox.com/communities/86590100/Regional-Bus-Community",
    "created": "2026-07-05",
    "updated_utc": "2026-09-30 20:39 UTC",
    "max_players": 8,
    "platforms": "Mobile, PC, Xbox and PS5",
    # roblox games API snapshot 2026-10-01 ~16:20 UTC
    "playing": 97,
    "visits": "2,930,399",
    "favorites": "10,097",
    "upvotes": "2,611",
    "downvotes": "690",
    "group_members": "123,534",
}

OLD_GAME = {
    "place_id": 15937818410,
    "universe_id": 5510910393,
    "name": "MOVED Regional School Bus Co",
    "group": "Regional Bus Company",
    "group_id": 33629244,
    "url": "https://www.roblox.com/games/15937818410/Regional-School-Bus-Co",
    "visits": "14,756,649",
    "playing": 0,
    "last_updated": "2026-08-16",
}

DISCORD = {"invite": "https://discord.gg/regional", "name": "Regional Bus Community", "members": "3,654"}

# badges.roblox.com/v1/universes/10453366727/badges, checked 2026-10-01
BADGES = [
    ("Welcome to Upstate Region", "Join the game (Upstate, NY).", "1,300,640", "obtainable"),
    ("Completed Tutorial", "Official text: tutorial disabled, badge unobtainable.", "18,741", "unobtainable"),
    ("Heres a present!", "Gift someone a game pass.", "536", "obtainable"),
    ("Completed 1st Route", "Finish your first in-game route.", "72,106", "obtainable"),
    ("Completed 5th Route", "Finish 5 in-game routes.", "14,163", "obtainable"),
    ("Completed 10th Route", "Finish 10 in-game routes.", "6,779", "obtainable"),
    ("Completed 25th Route", "Finish 25 in-game routes.", "1,892", "obtainable"),
    ("[LIVE EVENT] the tunnels", "Live event on August 3, 2025, 5 PM EST.", "163", "unobtainable"),
    ("Corn Maze 2025", "Completed the corn maze in October 2025.", "1,630", "unobtainable"),
    ("Corn Maze 2026", "Complete the corn maze during October 2026.", "0", "upcoming"),
]

# apis.roblox.com/game-passes/v1/universes/10453366727/game-passes, checked 2026-10-01
PASSES = [
    ("Microbird G5", "bus", 99),
    ("International AE", "bus", 99),
    ("Handicap Vision (Shorty)", "bus", 149),
    ("Bluebird D3FE", "bus", 249),
    ("O.C.T | Vision", "bus", 249),
    ("Electric LionC", "bus", 299),
    ("Premium Bluebird Vision", "bus", 499),
    ("Premium International CE", "bus", 499),
    ("Teleport To Bus", "utility", 24),
    ("x1.5 Cash", "utility", 150),
    ("Booster Premium Fee", "assignment", 750),
    ("Premium Assignment Fee", "assignment", 1000),
    ("Spawn Anywhere", "utility", None),  # off sale
]

CODES_WORKING = []   # none found on 2026-10-01; see ops research log
CODES_EXPIRED = []

VIDEOS = {
    "fall": ("ROBLOX | Regional School Bus Co | FALL IS HERE!", "ShayArson", "late September 2026", "https://www.youtube.com/watch?v=fwB2SwxE11Y"),
    "summer": ("ROBLOX | Regional School Bus Co | 2026 Summer Update Review", "ShayArson", "summer 2026", "https://www.youtube.com/watch?v=n1KAiM_fw-I"),
}
