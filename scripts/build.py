#!/usr/bin/env python3
"""Static builder for regionalschoolbusco.wiki.

The original Next.js source was never committed (the repo only held the static
export). From 2026-10-01 the pages are generated from this file plus
scripts/site_data.py into the repo root, which is what Vercel serves.
Run: python3 scripts/build.py
"""
import html, json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from site_data import *  # noqa

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
E = html.escape
CSS = "/_next/static/chunks/0ll9sp~e.ioxx.css"
BODY_CLASS = "geist_a71539c9-module__T19VSG__variable geist_mono_8d43a2aa-module__8Li5zG__variable"
PLAY = GAME["url"]
BRAND = "Regional School Bus Co Guide"

NAV = [("/beginner-guide/", "Start here"), ("/fall-update/", "Fall update"), ("/buses/", "Buses"),
       ("/progression/", "CDL &amp; progression"), ("/common-mistakes/", "Mistakes"), ("/faq/", "FAQ")]


def a(href, text, ext=False):
    rel = ' rel="noreferrer"' if ext else ""
    return f'<a href="{href}"{rel}>{text}</a>'


def head(p):
    t, d, url = E(p["title"]), E(p["description"]), SITE + p["path"]
    ld = "".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in p.get("jsonld", []))
    pre = '<link rel="preload" as="image" href="/images/regional-school-bus-fleet.webp"/>' if p["path"] == "/" else ""
    return f"""<!DOCTYPE html><html lang="en"><head><meta charSet="utf-8"/><meta name="viewport" content="width=device-width, initial-scale=1"/><link rel="preload" href="/_next/static/media/797e433ab948586e-s.p.08e28id.o-okb.woff2" as="font" crossorigin="" type="font/woff2"/><link rel="preload" href="/_next/static/media/caa3a2e1cccd8315-s.p.09~u27dqhyhd6.woff2" as="font" crossorigin="" type="font/woff2"/>{pre}<link rel="stylesheet" href="{CSS}"/><link rel="stylesheet" href="/assets/site-extra.css"/><meta name="theme-color" content="#f5bf26"/><meta name="color-scheme" content="light"/><title>{t}</title><meta name="description" content="{d}"/><meta name="application-name" content="{BRAND}"/><meta name="author" content="{BRAND}"/><link rel="manifest" href="/manifest.webmanifest"/><meta name="category" content="games"/>{'<meta name="robots" content="noindex"/>' if p.get("noindex") else f'<link rel="canonical" href="{url}"/>'}<meta property="og:title" content="{t}"/><meta property="og:description" content="{d}"/><meta property="og:url" content="{url}"/><meta property="og:site_name" content="{BRAND}"/><meta property="og:image" content="{SITE}/og.png"/><meta property="og:image:width" content="1731"/><meta property="og:image:height" content="909"/><meta property="og:image:alt" content="Regional School Bus Co guide — yellow school buses in Upstate Region"/><meta property="og:type" content="{'website' if p['path']=='/' else 'article'}"/><meta name="twitter:card" content="summary_large_image"/><meta name="twitter:title" content="{t}"/><meta name="twitter:description" content="{d}"/><meta name="twitter:image" content="{SITE}/og.png"/>{ld}</head>"""


def shell(p, main):
    nav = "".join(f'<a href="{h}"{" aria-current=\"page\"" if h == p["path"] else ""}>{x}</a>' for h, x in NAV)
    return head(p) + f"""<body class="{BODY_CLASS}"><div class="site-shell"><a class="skip-link" href="#main-content">Skip to main content</a><header class="site-header"><div class="header-inner"><a class="brand" aria-label="{BRAND} home" href="/"><span class="brand-mark" aria-hidden="true">R</span><span><strong>Regional School Bus Co</strong><small>Wiki &amp; Guide</small></span></a><nav class="main-nav" aria-label="Main navigation">{nav}</nav></div></header><main id="main-content">{main}</main><footer class="site-footer"><div class="footer-grid"><div><p class="footer-title">Learn the route, then improve it.</p><p>An independent, community-made guide. Not affiliated with Roblox, Regional Bus Community or Regional Bus Company. Facts last checked {CHECKED_HUMAN}.</p></div><nav aria-label="Footer navigation"><a href="/beginner-guide/">Beginner guide</a><a href="/core-loop/">Core loop</a><a href="/fall-update/">Fall Update 2026</a><a href="/buses/">Buses &amp; passes</a><a href="/progression/">CDL &amp; progression</a><a href="/common-mistakes/">Mistakes</a><a href="/faq/">FAQ</a><a href="/sources/">Sources</a><a href="{PLAY}" rel="noreferrer">Play on Roblox (current game) ↗</a></nav></div></footer></div></body></html>"""


def guide_page(p):
    toc = "".join(f'<li><a href="#{sid}">{h}</a></li>' for sid, h, _ in p["sections"])
    secs = "".join(f'<section id="{sid}"><h2>{h}</h2>{body}</section>' for sid, h, body in p["sections"])
    rel = "".join(f'<a class="related-card" href="{h}"><strong>{s}</strong><span>{d}</span><em>Open guide →</em></a>' for h, s, d in p["related"])
    notice = p.get("notice", "")
    main = f"""<section class="guide-hero"><div class="wide-container"><nav class="breadcrumbs" aria-label="Breadcrumb"><a href="/">Wiki home</a><span aria-hidden="true">/</span><span>{p['crumb']}</span></nav><p class="eyebrow">{p['eyebrow']}</p><h1>{p['h1']}</h1><p class="guide-deck">{p['deck']}</p><span class="reading-time">{p['reading']}</span><span class="updated-line">Updated {CHECKED_HUMAN}</span></div></section><div class="guide-layout wide-container"><aside class="contents-card" aria-label="On this page"><p>On this page</p><ol>{toc}</ol></aside><article class="guide-article">{notice}{secs}</article></div><section class="keep-reading"><div class="wide-container"><p class="eyebrow">Continue your route</p><h2>Keep reading</h2><div class="related-grid">{rel}</div></div></section>"""
    return shell(p, main)


def table(headers, rows):
    th = "".join(f"<th scope=\"col\">{h}</th>" for h in headers)
    tr = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f'<div class="table-wrap"><table class="data-table"><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table></div>'


def crumbs(name, path):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Regional School Bus Co Wiki", "item": SITE + "/"},
        {"@type": "ListItem", "position": 2, "name": name, "item": SITE + path}]}


def article(p):
    return {"@context": "https://schema.org", "@type": "Article", "headline": p["h1"], "description": p["description"],
            "datePublished": "2026-08-10", "dateModified": CHECKED, "mainEntityOfPage": SITE + p["path"],
            "author": {"@type": "Organization", "name": BRAND, "url": SITE + "/"},
            "publisher": {"@type": "Organization", "name": BRAND, "url": SITE + "/"},
            "about": {"@type": "VideoGame", "name": GAME["name"], "url": PLAY}}


MOVED_NOTICE = f"""<div class="notice-card" id="game-moved"><strong class="kicker">Game moved · checked {CHECKED_HUMAN}</strong><h2>Use the new Regional School Bus Co place</h2><p>The original place (ID {OLD_GAME['place_id']}) is now titled “{OLD_GAME['name']}” and shows {OLD_GAME['playing']} players; its last update was {OLD_GAME['last_updated']}. The live game is place <b>{GAME['place_id']}</b>, published by the <b>{GAME['creator']}</b> group (formerly {GAME['former_brand']}). Old favorites, bookmarks and video links that point to the old ID open the empty place.</p><a class="button button-primary" href="{PLAY}" rel="noreferrer">Open the current game on Roblox <span aria-hidden="true">↗</span></a></div>"""


def bus_rows():
    rows = []
    for name, kind, price in PASSES:
        if kind != "bus":
            continue
        rows.append([E(name), f"{price} Robux", '<span class="tag tag-ok">on sale</span>'])
    return rows


def util_rows():
    notes = {
        "Teleport To Bus": "Moves you to your spawned bus. Creator videos show a Teleport to bus button next to Spawn bus.",
        "x1.5 Cash": "Name says 1.5× cash. The in-game currency is shown as $ (a group-reward claim paid $175 in a Sept 2026 video).",
        "Booster Premium Fee": "Fee pass tied to the vehicle-assignment system. Benefits are not described on the pass.",
        "Premium Assignment Fee": "Fee pass tied to the vehicle-assignment system. Benefits are not described on the pass.",
        "Spawn Anywhere": "Off sale. Start from the Bus Yard instead.",
    }
    rows = []
    for name, kind, price in PASSES:
        if kind == "bus":
            continue
        status = '<span class="tag tag-off">off sale</span>' if price is None else '<span class="tag tag-ok">on sale</span>'
        rows.append([E(name), "—" if price is None else f"{price} Robux", status, notes.get(name, "")])
    return rows


def badge_rows():
    tag = {"obtainable": "tag-ok", "unobtainable": "tag-off", "upcoming": "tag-rep"}
    return [[E(n), E(d), c, f'<span class="tag {tag[s]}">{s}</span>'] for n, d, c, s in BADGES]


FV = VIDEOS["fall"]; SV = VIDEOS["summer"]

# ---------------------------------------------------------------- pages
PAGES = []

HOME_FAQ = [
    ("Where is Regional School Bus Co now?", f"It moved to a new Roblox place, ID {GAME['place_id']}, published by Regional Bus Community (formerly Regional Bus Company). The old place {OLD_GAME['place_id']} is titled “{OLD_GAME['name']}” and is empty."),
    ("Are there Regional School Bus Co codes?", f"No. As of {CHECKED_HUMAN} the game page, its badges, passes and the code sites we checked list no working codes. Code lists for School Bus Simulator 24 belong to a different game."),
    ("When is the Corn Maze 2026?", "The official Corn Maze 2026 badge says it unlocks by completing the corn maze during October 2026. In a late-September video the maze was still closed."),
]

home = {
    "path": "/", "title": "Regional School Bus Co Wiki (Roblox): New Link & Fall Update",
    "description": "Regional School Bus Co (formerly Regional Bus Company) moved to a new Roblox place. Get the working link, Fall Update 2026 and Corn Maze info, bus prices and route tips.",
}
home["jsonld"] = [
    {"@context": "https://schema.org", "@graph": [
        {"@type": "WebSite", "name": "Regional School Bus Co Wiki", "alternateName": BRAND, "url": SITE + "/", "inLanguage": "en"},
        {"@type": "VideoGame", "name": GAME["name"], "alternateName": [GAME["alt_name"], "Regional Bus Company school bus game"], "url": PLAY,
         "gamePlatform": ["Roblox", "PC", "Mobile", "Xbox", "PlayStation 5"], "publisher": {"@type": "Organization", "name": GAME["creator"]}}]},
    {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": ans}} for q, ans in HOME_FAQ]},
]
home_faq_html = "".join(f'<details{" open" if i == 0 else ""}><summary><span>{E(q)}</span><b aria-hidden="true">+</b></summary><div><p>{E(ans)}</p></div></details>' for i, (q, ans) in enumerate(HOME_FAQ))
home_main = f"""<section class="home-hero"><div class="hero-grid wide-container"><div class="hero-copy"><p class="eyebrow">Independent wiki · Updated {CHECKED_HUMAN}</p><h1><strong>Regional School Bus Co Wiki</strong><span>New game link, Fall Update and your first route.</span></h1><p class="hero-deck">Regional School Bus Co, also called {E(GAME['alt_name'])}, now runs on a new Roblox place from {GAME['creator']}. Start there, spawn a public bus, run an AM or PM route with the GPS line, and refuel before the next drive.</p><div class="hero-actions"><a class="button button-primary" href="{PLAY}" rel="noreferrer">Play the current game <span aria-hidden="true">↗</span></a><a class="text-link" href="/beginner-guide/">Start the beginner guide</a></div><ul class="stat-row" aria-label="Live game stats checked {CHECKED_HUMAN}"><li><b>{GAME['playing']}</b>playing</li><li><b>{GAME['visits']}</b>visits</li><li><b>{GAME['favorites']}</b>favorites</li><li><b>{GAME['max_players']}</b>max per server</li></ul></div><figure class="hero-visual"><div class="image-frame"><img alt="Regional School Bus Co official media showing a fleet of yellow school buses" width="768" height="432" decoding="async" style="color:transparent" src="/images/regional-school-bus-fleet.webp"/><div class="loop-stamp" aria-hidden="true"><span>DRIVE</span><b>→</b><span>TRANSPORT</span><b>→</b><span>REFUEL</span></div></div><figcaption>Official Roblox game media for Regional School Bus Co.</figcaption></figure></div></section>
<section class="home-notice"><div class="wide-container">{MOVED_NOTICE}</div></section>
<section class="route-section" aria-labelledby="latest-title"><div class="wide-container"><div class="section-heading"><p class="eyebrow">Latest in Regional School Bus Co</p><h2 id="latest-title">What changed this season</h2><p>Last game update on Roblox: {GAME['updated_utc']}. Dates and counts below were read on {CHECKED_HUMAN}.</p></div><div class="route-grid"><a class="route-card" href="/fall-update/"><div class="route-card-top"><span>01</span><em>Event</em></div><h3>Fall Update 2026 &amp; Corn Maze</h3><p>Pumpkin farm, Upstate Drive-In Theater, new buildings and plazas. The Corn Maze 2026 badge is for completing the maze during October 2026.</p><strong>See what’s new →</strong></a><a class="route-card" href="/buses/"><div class="route-card-top"><span>02</span><em>Lookup</em></div><h3>Buses &amp; game pass prices</h3><p>Eight bus passes from 99 to 499 Robux, plus Teleport To Bus (24) and x1.5 Cash (150). Spawn Anywhere is off sale.</p><strong>Compare buses →</strong></a><a class="route-card" href="/faq/#codes"><div class="route-card-top"><span>03</span><em>Status</em></div><h3>Codes: none right now</h3><p>No working Regional School Bus Co codes are listed anywhere we checked. Don’t use School Bus Simulator 24 codes; they belong to another game.</p><strong>Read the codes answer →</strong></a></div></div></section>
<section class="quickstart-section" aria-labelledby="quickstart-title"><div class="wide-container"><div class="section-heading split-heading"><div><p class="eyebrow">Quick start</p><h2 id="quickstart-title">Your first session in five steps</h2></div><p>Built from the official game description and creator gameplay videos. Exact buttons differ by device, so follow the on-screen labels.</p></div><ol class="loop-grid"><li><span>01</span><h3>Join the new place</h3><p>Open place {GAME['place_id']} by {GAME['creator']}. The old “MOVED” place is empty.</p></li><li><span>02</span><h3>Customize, then Spawn bus</h3><p>At the Bus Yard pick a standard public bus, set a bus number, adjust Customize options, then press Spawn bus. No CDL is needed for public buses.</p></li><li><span>03</span><h3>Start the bus and a route</h3><p>Sit in the driver seat, start the bus, then choose an AM or PM route. Starting a route turns on the GPS line.</p></li><li><span>04</span><h3>Follow the GPS line</h3><p>The GPS doesn’t reroute. If you miss a turn, go back to the main road. Use the minimap to find stops and places.</p></li><li><span>05</span><h3>Refuel and repeat</h3><p>Watch the fuel gauge and refuel when needed. Your 1st, 5th, 10th and 25th completed routes each award a badge.</p></li></ol><a class="inline-cta" href="/beginner-guide/">Open the full beginner guide <span>→</span></a></div></section>
<section class="route-section" aria-labelledby="route-title"><div class="wide-container"><div class="section-heading"><p class="eyebrow">Wiki chapters</p><h2 id="route-title">Everything on this site</h2><p>Each page answers one player question and links to the next step.</p></div><div class="route-grid"><a class="route-card" href="/core-loop/"><div class="route-card-top"><span>01</span><em>Repeatable play</em></div><h3>Core loop</h3><p>Bus Yard → bus and number → route and students → fuel → finish, then repeat.</p><strong>Open chapter →</strong></a><a class="route-card" href="/progression/"><div class="route-card-top"><span>02</span><em>Next goals</em></div><h3>CDL, badges &amp; progression</h3><p>Route badges, the Training Facility CDL path, assigned buses and BD Edition.</p><strong>Open chapter →</strong></a><a class="route-card" href="/common-mistakes/"><div class="route-card-top"><span>03</span><em>Troubleshooting</em></div><h3>Common mistakes</h3><p>Joining the old place, using another game’s codes, lag settings and GPS detours.</p><strong>Open chapter →</strong></a></div></div></section>
<section class="faq-page wide-container" aria-labelledby="home-faq-title"><div class="faq-intro"><p class="eyebrow">Quick answers</p><h2 id="home-faq-title">Regional School Bus Co questions</h2><p>More answers on the <a href="/faq/">FAQ page</a>; evidence is on the <a href="/sources/">sources page</a>.</p></div><div class="faq-list">{home_faq_html}</div></section>"""
home["html"] = shell(home, home_main)
PAGES.append(home)

# ---- beginner guide
bg = {"path": "/beginner-guide/", "crumb": "Beginner guide", "eyebrow": "Start here",
      "title": "How to Play Regional School Bus Co: Spawn a Bus & Start a Route",
      "description": "Regional School Bus Co beginner guide: join the new place, spawn a public bus, start an AM or PM route with GPS, pick up students, refuel and earn route badges.",
      "h1": "How to play Regional School Bus Co (beginner guide)",
      "deck": "From joining the right place to finishing your first AM or PM route. Steps follow the official game description and creator gameplay videos from 2026.",
      "reading": "6-minute quick start",
      "notice": MOVED_NOTICE.replace("<h2>", "<h3>").replace("</h2>", "</h3>")}
bg["sections"] = [
    ("join", "1. Join the current place", f"<p>Search Roblox for “Regional School Bus Co” and pick the one by <b>{GAME['creator']}</b> (place {GAME['place_id']}). The game warns it is not built for low-end devices. It supports {GAME['platforms']}, with up to {GAME['max_players']} players per server.</p><p>Joining awards the <b>Welcome to Upstate Region</b> badge. The <b>Completed Tutorial</b> badge’s official text says the tutorial is disabled, so there’s no forced tutorial. Use this page instead.</p>"),
    ("bus-yard", "2. Pick a public bus at the Bus Yard", "<p>Start at the Bus Yard. Standard public buses can be driven by anyone, so you don’t need a CDL. Choose an available bus and set your bus number in the interface. Creator videos show the bus list, a <b>Customize</b> menu (decor such as a jack-o’-lantern during fall) and a <b>Spawn bus</b> button.</p><p>If you own the <a href=\"/buses/\">Teleport To Bus pass</a>, the Teleport to bus button moves you to your spawned bus. Spawn Anywhere is off sale, so plan around the yard.</p><div class=\"field-note\"><strong>Field note</strong><p>Can’t get your bus out of a tight spot? In the September 2026 fall video the creator despawned and spawned again rather than driving out.</p></div>"),
    ("start-bus", "3. Start the bus", "<p>Sit in the driver seat and start the bus. The game simulates a real school bus, so expect a short start sequence; in one creator video air pressure had to build before driving. Take down the “empty bus” sign if your bus shows one. The exact keys differ between PC, mobile and console, so read the prompts on your screen.</p>"),
    ("route", "4. Start an AM or PM route and follow the GPS", "<ol class=\"steps\"><li>Open the route option and pick a route. Videos show AM and PM routes, and public route sessions are also hosted by the community.</li><li>Starting a route turns on the <b>GPS</b>: a guide line on the road and the <b>minimap</b>.</li><li>Follow the line to each stop and to the school. <b>The GPS does not reroute.</b> If you take a wrong turn, drive back to the main road until you’re on the line again.</li><li>At each stop, stop fully and turn on the red warning lights, as creators do in gameplay videos. The summer 2026 update added light reflections on stop signs.</li></ol><p>Route names, stop order and pay can change between updates. This guide doesn’t publish fixed numbers for them.</p>"),
    ("fuel", "5. Keep enough fuel", "<p>Refueling is part of the official game loop. Check the fuel gauge between stops and refuel before a long leg. Station locations and fuel prices aren’t published here because they aren’t stable public data.</p>"),
    ("badges", "6. Finish routes for badges", "<p>Each finished route counts toward the official route badges. Snapshot from Roblox’s badge API:</p>" + table(["Badge", "How to get it", "Players awarded"], [[E(b[0]), E(b[1]), b[2]] for b in BADGES if "Route" in b[0]]) + "<p>For the CDL, assigned buses and other badges, see <a href=\"/progression/\">CDL &amp; progression</a>.</p>"),
    ("settings", "7. Fix lag before you drive", "<p>In the summer 2026 update the settings menu gained <b>Clouds</b> and <b>realistic light glow</b> options, and the menu itself warned they can cause lag. Turn them off on weaker devices. A creator on a strong PC switched graphics from automatic to manual and maxed it; on weaker devices, go lower instead.</p>"),
    ("first-session-checklist", "First-session checklist", "<ul class=\"plain\"><li>Joined place " + str(GAME['place_id']) + " (not the old MOVED place).</li><li>Picked a public bus, set a number, pressed Spawn bus.</li><li>Started the bus and chose an AM or PM route.</li><li>Followed the GPS line and used the minimap. No reroute, so return to the main road after a wrong turn.</li><li>Checked fuel and refueled before it ran low.</li><li>Finished the route for the Completed 1st Route badge.</li></ul>"),
]
bg["related"] = [("/core-loop/", "Understand the core loop", "Turn your first route into a repeatable session."), ("/common-mistakes/", "Avoid early mistakes", "Old place links, wrong-game codes, GPS detours and lag."), ("/fall-update/", "Fall Update 2026", "Pumpkin farm, drive-in and the Corn Maze 2026 badge.")]
bg["jsonld"] = [article(bg), crumbs("Beginner guide", bg["path"]), {"@context": "https://schema.org", "@type": "HowTo", "name": "How to start your first route in Regional School Bus Co", "step": [
    {"@type": "HowToStep", "name": "Join the current place", "text": f"Open Regional School Bus Co by {GAME['creator']} (place {GAME['place_id']})."},
    {"@type": "HowToStep", "name": "Spawn a public bus", "text": "At the Bus Yard choose a standard public bus, set a bus number and press Spawn bus."},
    {"@type": "HowToStep", "name": "Start the bus", "text": "Sit in the driver seat and start the bus using the on-screen prompts."},
    {"@type": "HowToStep", "name": "Start a route", "text": "Choose an AM or PM route; the GPS line and minimap guide you to each stop. The GPS does not reroute."},
    {"@type": "HowToStep", "name": "Refuel and finish", "text": "Refuel when the gauge is low and finish the route to earn route badges."}]}]
bg["html"] = guide_page(bg)
PAGES.append(bg)

# ---- fall update (new)
fu = {"path": "/fall-update/", "crumb": "Fall Update 2026", "eyebrow": "Event · October 2026",
      "title": "Regional School Bus Co Fall Update 2026: Corn Maze & Pumpkins",
      "description": "What's in the Regional School Bus Co Fall Update 2026: pumpkin farm, Upstate Drive-In Theater, new buildings, and how the Corn Maze 2026 badge works in October 2026.",
      "h1": "Regional School Bus Co Fall Update 2026",
      "deck": "Part 1 of the fall update is live. Here’s what it added, where to find it, and what we know about the Corn Maze 2026 badge.",
      "reading": "4-minute read"}
fu["sections"] = [
    ("summary", "Quick answer", f"<p>The fall update (part 1) added a <b>pumpkin farm</b> with pumpkin-tossing and pumpkin-weighing areas, the <b>Upstate Drive-In Theater</b>, new buildings and plazas, map updates, fall lighting and foliage, plus bug fixes. That list comes from the in-game update log as read in the {E(FV[1])} video “{E(FV[0])}” ({FV[2]}). The same log says a <b>part 2</b> with Halloween content is still to come.</p><p>Roblox lists the game’s latest update as {GAME['updated_utc']}.</p>"),
    ("corn-maze", "Corn Maze 2026 badge", f"<p>The official badge <b>Corn Maze 2026</b> reads: “This badge was unlocked by completing the corn maze during October 2026.” Roblox’s badge API showed it awarded to <b>0 players</b> on {CHECKED_HUMAN}, so nobody has been able to finish the maze yet.</p>" + table(["Badge", "Official condition", "Status " + CHECKED], [["Corn Maze 2026", "Complete the corn maze during October 2026", '<span class="tag tag-rep">not yet awarded</span>'], ["Corn Maze 2025", "Completed the maze in October 2025", '<span class="tag tag-off">no longer obtainable</span>']]) + "<p>In the late-September video the maze entrance was <b>closed</b>, and the creator guessed it opens with part 2. Treat the opening date as unconfirmed until the maze is open in your server.</p>"),
    ("where", "Where to find the fall locations", "<ol class=\"steps\"><li>Spawn a bus at the Bus Yard (or walk).</li><li>Open the <b>minimap</b>. The pumpkin farm has its own marker, so use it to turn around if you take the wrong road.</li><li>The <b>Upstate Drive-In Theater</b> showed movie titles on its sign. In the video it came up shortly after the river area, so use the minimap if you can’t see it.</li><li>The pumpkin-weighing contest is a display of results (in the video it had already happened), not a minigame you play.</li></ol><div class=\"field-note\"><strong>Field note</strong><p>An NPC at the farm asks a riddle: “I am full of rows but have no seeds…” The answer that worked in the video was cornfield.</p></div>"),
    ("cash", "Free cash: the group reward", f"<p>In the same video, an in-game group-membership check for the <b>{GAME['creator']}</b> Roblox group paid <b>$175</b> in-game cash. That’s a single observation, so the amount may change. There are no redeem codes; see the <a href=\"/faq/#codes\">codes answer</a>.</p>"),
    ("lag", "Fall update lag", "<p>The fall video showed lag spikes of 15–20 seconds, assets loading late and floating terrain near the farm. The game page warns it’s not built for low-end devices. If you lag, turn off Clouds and realistic light glow, lower graphics, and rejoin a less busy server (max 8 players).</p>"),
    ("summer", "Earlier in 2026: the summer update", f"<p>The summer 2026 update (reviewed in “{E(SV[0])}”) added route <b>GPS</b>, a <b>minimap</b>, song radio, terrain grass, stop-sign light reflections, a new Vision drive sound, a construction site and a carnival field-trip spot with rides. The 2026 Next Gen in that log was a roster bus, and the log teased “free third gens for everyone” for a later update. Whether that arrived isn’t confirmed.</p>"),
]
fu["related"] = [("/beginner-guide/", "Beginner guide", "Spawn a bus and run your first GPS route."), ("/progression/", "Badges &amp; progression", "All 10 badges, including route milestones."), ("/faq/", "FAQ", "Moved game, codes, Discord and CDL answers.")]
fu["jsonld"] = [article(fu), crumbs("Fall Update 2026", fu["path"]), {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
    {"@type": "Question", "name": "What is in the Regional School Bus Co fall update?", "acceptedAnswer": {"@type": "Answer", "text": "Part 1 added a pumpkin farm with pumpkin tossing and weighing areas, the Upstate Drive-In Theater, new buildings and plazas, map updates, fall lighting and foliage, and bug fixes. Part 2 with Halloween content is listed as coming later."}},
    {"@type": "Question", "name": "How do you get the Corn Maze 2026 badge?", "acceptedAnswer": {"@type": "Answer", "text": "The official badge is earned by completing the corn maze during October 2026. On October 1, 2026 it had not been awarded to anyone yet, and the maze was closed in a late-September video."}}]}]
fu["html"] = guide_page(fu)
PAGES.append(fu)

# ---- buses (new)
bu = {"path": "/buses/", "crumb": "Buses &amp; game passes", "eyebrow": "Lookup",
      "title": "Regional School Bus Co Buses & Game Passes: Every Price in Robux",
      "description": f"Every Regional School Bus Co game pass and price, checked {CHECKED_HUMAN}: 8 bus passes (99–499 Robux), Teleport To Bus, x1.5 Cash, fee passes and free buses.",
      "h1": "Regional School Bus Co buses and game passes",
      "deck": "Every pass the current game sells, with Robux prices from Roblox’s own pass list, plus what you can drive for free.",
      "reading": "3-minute lookup"}
bu["sections"] = [
    ("free", "Do you need to buy a bus?", "<p>No. Standard public buses can be driven by anyone, and you need no pass or CDL to spawn one and run a route. The passes below unlock specific models or conveniences. Assigned buses come through the community CDL and assignment system, not just a purchase (see <a href=\"/progression/\">CDL &amp; progression</a>).</p>"),
    ("bus-passes", "Bus passes and prices", f"<p>From Roblox’s game-pass list for place {GAME['place_id']}, checked {CHECKED_HUMAN}. Cheapest first:</p>" + table(["Bus pass", "Price", "Status"], bus_rows()) + "<p>Pass pages don’t list stats such as seats, speed or fuel use, and we don’t invent them. “Premium” in a name is part of the official pass title.</p>"),
    ("utility", "Utility and fee passes", table(["Pass", "Price", "Status", "What it does"], util_rows()) + "<p>Gifting any game pass to another player earns the <b>Heres a present!</b> badge.</p>"),
    ("which", "Which pass is worth it?", "<ul class=\"plain\"><li><b>Just starting:</b> buy nothing. Learn the route loop on a public bus first.</li><li><b>Want a specific model cheaply:</b> Microbird G5 and International AE are the cheapest bus passes at 99 Robux each.</li><li><b>Tired of walking to your bus:</b> Teleport To Bus is the cheapest pass at 24 Robux.</li><li><b>Grinding cash:</b> x1.5 Cash (150 Robux) boosts earnings by the multiplier in its name. Payout per route isn’t published, so the real gain is unknown.</li><li><b>Fee passes (750 / 1,000 Robux):</b> they belong to the assignment system. Read the current assignment rules in the community before buying.</li></ul>"),
    ("models", "Buses seen in gameplay", "<p>Creator videos in 2026 also show models such as the ICRE, the Vision and a C2 in the bus list, and the summer update log listed a “2026 Next Gen” roster bus. Availability depends on your access level, so check the in-game list.</p>"),
]
bu["related"] = [("/beginner-guide/", "Spawn your first bus", "Customize, Spawn bus, start a route."), ("/progression/", "CDL &amp; assigned buses", "How the Training Facility path works."), ("/common-mistakes/", "Mistakes to avoid", "Including assuming every bus is public.")]
bu["jsonld"] = [article(bu), crumbs("Buses & game passes", bu["path"]), {"@context": "https://schema.org", "@type": "ItemList", "name": "Regional School Bus Co game passes", "itemListElement": [
    {"@type": "ListItem", "position": i + 1, "name": n + (f" ({p} Robux)" if p else " (off sale)")} for i, (n, k, p) in enumerate(PASSES)]}]
bu["html"] = guide_page(bu)
PAGES.append(bu)

# ---- core loop
cl = {"path": "/core-loop/", "crumb": "Core gameplay loop", "eyebrow": "Repeatable play",
      "title": "Regional School Bus Co Gameplay Loop: Routes, GPS & Fuel",
      "description": "The Regional School Bus Co gameplay loop: Bus Yard → spawn a bus → AM/PM route with GPS → pick up students → refuel → finish and repeat, with route badges along the way.",
      "h1": "Regional School Bus Co core gameplay loop",
      "deck": "One repeatable cycle: Bus Yard → bus and number → route with GPS → students → fuel → finish.",
      "reading": "4-minute overview"}
cl["sections"] = [
    ("loop-map", "Bus Yard → bus and number → route → fuel → finish", "<ol class=\"steps\"><li><b>Bus Yard:</b> choose a standard public bus, set a number, Customize, Spawn bus.</li><li><b>Route:</b> start the bus, pick an AM or PM route. The GPS line and minimap turn on.</li><li><b>Students:</b> stop at each marked stop with lights on, then continue to the school.</li><li><b>Fuel:</b> check the gauge between stops and refuel when needed.</li><li><b>Finish:</b> complete the route, then start another or join a hosted public route session.</li></ol>"),
    ("success-signal", "How you know a route counted", "<p>A finished route counts toward the official badges <b>Completed 1st, 5th, 10th and 25th Route</b>. When the 1st Route badge appears, your loop worked. Pay per route isn’t a published value, and the currency shows as $ in game.</p>"),
    ("gps", "GPS detours", "<p>The route GPS doesn’t reroute. Missing a turn means driving back to the main road and rejoining the line.</p>"),
    ("fuel", "Use fuel as a continuity check", "<p>Refueling is a confirmed part of the official loop. Treat the fuel gauge like a checkpoint between stops. Warning thresholds and fuel prices aren’t published here.</p>"),
]
cl["related"] = [("/beginner-guide/", "Return to the beginner guide", "Step-by-step first session."), ("/progression/", "Plan progression", "Badges, CDL, assigned buses and BD Edition.")]
cl["jsonld"] = [article(cl), crumbs("Core gameplay loop", cl["path"])]
cl["html"] = guide_page(cl)
PAGES.append(cl)

# ---- progression
pr = {"path": "/progression/", "crumb": "CDL &amp; progression", "eyebrow": "Next goals",
      "title": "Regional School Bus Co CDL, Badges & Assigned Bus Progression",
      "description": "Regional School Bus Co progression: all 10 badges with award counts, route milestones, the Training Facility CDL path, assigned buses and BD Edition.",
      "h1": "Regional School Bus Co CDL, badges and progression",
      "deck": "Route badges first, then the community CDL path toward an assigned bus, BD Edition and route permissions.",
      "reading": "5-minute plan"}
pr["sections"] = [
    ("badges", "All badges", f"<p>All 10 badges on the current place from Roblox’s badge API, checked {CHECKED_HUMAN}:</p>" + table(["Badge", "Condition (official text)", "Awarded", "Status"], badge_rows())),
    ("early", "Early game: route milestones", "<p>Aim for the 1st, 5th, 10th and 25th route badges. Few players reach 25 routes, so finishing routes reliably already puts you ahead. Learn the GPS and fuel loop on a public bus before chasing anything else.</p>"),
    ("cdl", "Advanced: CDL, assigned bus and BD Edition", "<p>The community’s own description says to go to the <b>Training Facility</b> for the official CDL. Passing unlocks an assigned bus, BD Edition, fleet assignment and route permissions, plus the chance to rank up. The creator’s assignment bulletin adds that Bus Driver+ members may qualify for assigned vehicles.</p><p>Training sessions, tests and applications run through the community. The Discord <b>Regional Bus Community</b> (discord.gg/regional, about 3,654 members on " + CHECKED_HUMAN + ") uses the same name as the new group. The original group description pointed players to the community’s communications server for development updates, operations and applications. Requirements and fees change, so check them there before you pay for <a href=\"/buses/\">Premium Assignment Fee or Booster Premium Fee</a>.</p>"),
    ("rename", "Regional Bus Company vs Regional Bus Community", f"<p>Same fleet and staff idea, new group. The original group <b>Regional Bus Company</b> (ID {OLD_GAME['group_id']}) still exists with its old “MOVED” place, while the live game is published by <b>{GAME['creator']}</b> (ID {GAME['creator_group_id']}, {GAME['group_members']} members on {CHECKED_HUMAN}). A late-September creator video suggests the old group was locked, which would explain the new group and place. The creator wasn’t certain.</p>"),
    ("device", "Use a high-performance device when possible", "<p>The official description says the game is not designed for low-end devices. Turn off Clouds and realistic light glow, lower graphics, and close background apps before assuming a mechanic is broken.</p>"),
]
pr["related"] = [("/buses/", "Buses &amp; passes", "Prices for every bus and fee pass."), ("/faq/", "Check the FAQ", "Moved game, codes, Discord and Corn Maze answers.")]
pr["jsonld"] = [article(pr), crumbs("CDL & progression", pr["path"])]
pr["html"] = guide_page(pr)
PAGES.append(pr)

# ---- mistakes
cm = {"path": "/common-mistakes/", "crumb": "Common mistakes", "eyebrow": "Troubleshooting",
      "title": "Regional School Bus Co Not Working? 8 Common Mistakes & Fixes",
      "description": "Fix common Regional School Bus Co problems: joining the old MOVED place, another game's codes, a GPS that won't reroute, lag from Clouds and light glow, and more.",
      "h1": "Common Regional School Bus Co mistakes",
      "deck": "Quick fixes for the problems new and returning drivers hit most often.",
      "reading": "5-minute checklist"}
cm["sections"] = [
    ("old-place", "Joining the old “MOVED” place", f"<p>If the game is empty or won’t update, check the place ID. {OLD_GAME['place_id']} is the old “{OLD_GAME['name']}” with 0 players. The live game is <a href=\"{PLAY}\" rel=\"noreferrer\">place {GAME['place_id']}</a> by {GAME['creator']}. Update your favorites.</p>"),
    ("wrong-codes", "Using another game’s codes", "<p>Regional School Bus Co has no working codes right now. Lists such as School Bus Simulator 24 codes are for a different Roblox game and won’t work here. Free cash came from the group reward in a 2026 video, not from a code.</p>"),
    ("gps", "Expecting the GPS to reroute", "<p>The route GPS line doesn’t recalculate. After a wrong turn, drive back to the main road until you’re on the line.</p>"),
    ("lag", "Leaving Clouds and light glow on", "<p>The settings menu itself flags Clouds and realistic light glow as lag sources. Turn them off on phones and older PCs, and lower graphics if the fall map loads slowly.</p>"),
    ("bus-yard", "Skipping the Bus Yard", "<p>Spawn Anywhere is off sale. Start from the Bus Yard, or use Teleport to bus after spawning if you own that pass.</p>"),
    ("public", "Assuming every bus is public", "<p>Standard public buses are free to drive, but pass buses and assigned buses have their own access. Check the <a href=\"/buses/\">bus pass list</a> before you think something’s broken.</p>"),
    ("cdl", "Thinking a beginner needs a CDL", "<p>You don’t. The CDL is the community path to an assigned bus and route permissions, not a requirement for public buses.</p>"),
    ("tutorial", "Waiting for a tutorial", "<p>The tutorial is disabled, and the official badge text says so. Follow the <a href=\"/beginner-guide/\">beginner guide</a> instead.</p>"),
]
cm["related"] = [("/beginner-guide/", "Follow the first-session route", "Join, spawn, route, refuel."), ("/sources/", "Review the evidence", "Where every fact on this site comes from.")]
cm["jsonld"] = [article(cm), crumbs("Common mistakes", cm["path"])]
cm["html"] = guide_page(cm)
PAGES.append(cm)

# ---- FAQ
FAQ = [
    ("moved", "Why can't I find Regional School Bus Co, or why is it empty?", f"The game moved. The old place {OLD_GAME['place_id']} is now called “{OLD_GAME['name']}” and has 0 players. Play place {GAME['place_id']} by {GAME['creator']} instead.", PLAY, "Open the current game ↗"),
    ("rbc", "Is Regional Bus Company the same as Regional School Bus Co?", f"Yes. Regional Bus Company was the original group. The game now runs under {GAME['creator']} (formerly Regional Bus Company), and the game is also called {GAME['alt_name']}.", "/progression/#rename", "Read about the rename →"),
    ("codes", "Are there any Regional School Bus Co codes?", f"No. On {CHECKED_HUMAN} there were no working codes on the official game page, and none on the code sites we checked. School Bus Simulator 24 codes are for another game. We’ll only list a code once three or more independent sources confirm it works.", "/common-mistakes/#wrong-codes", "Why other codes fail →"),
    ("corn-maze", "When does the Corn Maze 2026 open?", "The official Corn Maze 2026 badge is for completing the corn maze during October 2026. It had 0 awards on October 1, 2026, and the maze was closed in a late-September video. Part 2 of the fall update is expected to add Halloween content.", "/fall-update/#corn-maze", "Fall Update details →"),
    ("first", "What should I do first?", "Join the current place, pick a standard public bus at the Bus Yard, set a number, press Spawn bus, start the bus, choose an AM or PM route, follow the GPS line, refuel when needed and finish the route.", "/beginner-guide/", "Open the beginner guide →"),
    ("gps", "How does the route GPS work?", "Starting a route turns on a guide line and the minimap. The GPS does not reroute, so after a wrong turn go back to the main road.", "/core-loop/#gps", "Core loop →"),
    ("cdl", "Do beginners need a CDL?", "No. Standard public buses can be driven by anyone. The CDL from the Training Facility leads to an assigned bus, BD Edition, fleet assignment and route permissions.", "/progression/#cdl", "CDL path →"),
    ("buses", "How much do the buses cost?", "Eight bus passes cost 99 to 499 Robux (Microbird G5 and International AE are the cheapest). Teleport To Bus is 24 Robux, x1.5 Cash is 150, and Spawn Anywhere is off sale.", "/buses/", "Full price list →"),
    ("badges", "What badges can I get?", "Welcome to Upstate Region, Heres a present!, Completed 1st/5th/10th/25th Route, and Corn Maze 2026 in October 2026. Completed Tutorial, the Tunnels live event and Corn Maze 2025 can no longer be earned.", "/progression/#badges", "All badges →"),
    ("discord", "Is there a Regional School Bus Co Discord?", "The community Discord is Regional Bus Community at discord.gg/regional, about 3,654 members on October 1, 2026. The original group description pointed players to that communications server for updates and applications.", "/progression/#cdl", "How the community fits in →"),
    ("platforms", "Which platforms are supported?", "Mobile, PC, Xbox and PS5. The game recommends a high-end device, and servers hold up to 8 players.", "/common-mistakes/#lag", "Lag fixes →"),
    ("official", "Is this an official wiki?", "No. This is an independent, community-made guide, not affiliated with Roblox, Regional Bus Community or Regional Bus Company.", "/sources/", "Read the sources →"),
]
fq = {"path": "/faq/", "title": "Regional School Bus Co FAQ: Moved Game, Codes, Corn Maze & CDL",
      "description": "Answers to Regional School Bus Co questions: where the game moved, whether codes exist, when the Corn Maze 2026 opens, bus prices, badges, Discord and the CDL.",
      "h1": "Regional School Bus Co FAQ"}
fq["jsonld"] = [{"@context": "https://schema.org", "@type": "FAQPage", "url": SITE + "/faq/", "mainEntity": [
    {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": ans}} for _, q, ans, _, _ in FAQ]}, crumbs("FAQ", "/faq/")]
items = "".join(f'<details id="{i}"{" open" if n < 3 else ""}><summary><span>{E(q)}</span><b aria-hidden="true">+</b></summary><div><p>{E(ans)}</p><a href="{h}"{" rel=\"noreferrer\"" if h.startswith("http") else ""}>{lt}</a></div></details>' for n, (i, q, ans, h, lt) in enumerate(FAQ))
fq_main = f"""<section class="guide-hero compact-hero"><div class="wide-container"><nav class="breadcrumbs" aria-label="Breadcrumb"><a href="/">Wiki home</a><span aria-hidden="true">/</span><span>FAQ</span></nav><p class="eyebrow">Answers without guesswork</p><h1>Regional School Bus Co FAQ</h1><p class="guide-deck">The questions players ask most about the moved game, codes, the Corn Maze, buses and the CDL.</p><span class="updated-line">Updated {CHECKED_HUMAN}</span></div></section><section class="faq-page wide-container"><div class="faq-intro"><p class="eyebrow">Current status</p><h2>Short answers, sources linked.</h2><p>Live numbers are snapshots from Roblox’s public APIs on {CHECKED_HUMAN}. Single-source details are labeled on the linked pages.</p></div><div class="faq-list">{items}</div></section>"""
fq["html"] = shell(fq, fq_main)
PAGES.append(fq)

# ---- sources
SRC = [
    ("Official Roblox page", f"Regional School Bus Co · place {GAME['place_id']}", "Current game by Regional Bus Community: description, platforms, high-end-device warning, max players, live stats, last update time.", PLAY),
    ("Official Roblox API", "Badges for universe " + str(GAME['universe_id']), "All 10 badge names, official conditions and award counts, including Corn Maze 2026.", f"https://badges.roblox.com/v1/universes/{GAME['universe_id']}/badges?limit=50"),
    ("Official Roblox API", "Game passes for universe " + str(GAME['universe_id']), "Every pass name, Robux price and on-sale status used on the buses page.", f"https://apis.roblox.com/game-passes/v1/universes/{GAME['universe_id']}/game-passes?passView=Full&pageSize=50"),
    ("Official Roblox group", f"Regional Bus Community · group {GAME['creator_group_id']}", "Publisher of the current place, the rename note “formerly Regional Bus Company”, member count.", GAME['group_url']),
    ("Independent game record", f"Rolimon’s · old place {OLD_GAME['place_id']}", "Shows the original place renamed “MOVED Regional School Bus Co” with 0 players.", f"https://www.rolimons.com/game/{OLD_GAME['place_id']}"),
    ("Independent group record", f"Rolimon’s · Regional Bus Company {OLD_GAME['group_id']}", "Original group description: Training Facility CDL, assigned bus, BD Edition, fleet assignment, route permissions.", f"https://www.rolimons.com/group/{OLD_GAME['group_id']}"),
    ("Creator community bulletin", "Regional Bus Company Assignment Information", "Standard public buses can be driven by anyone, and Bus Driver+ members may qualify for assigned vehicles.", "https://devforum.roblox.com/t/regional-bus-company-assignment-information/2829899"),
    ("Creator video", f"{FV[1]} · {FV[0]}", "Fall update part 1 log (pumpkin farm, drive-in, buildings, part 2 Halloween), closed corn maze, $175 group reward, lag observations.", FV[3]),
    ("Creator video", f"{SV[1]} · {SV[0]}", "Summer 2026 update: GPS routes that don’t reroute, minimap, AM routes, settings that cause lag, carnival, roster bus note.", SV[3]),
]
src_items = "".join(f'<article><span>{i+1:02d}</span><div><em>{E(r)}</em><h3>{E(t)}</h3><p>{E(d)}</p></div><a href="{E(u)}" rel="noreferrer">Open source ↗</a></article>' for i, (r, t, d, u) in enumerate(SRC))
so = {"path": "/sources/", "title": "Sources & Verification | Regional School Bus Co Guide",
      "description": f"Official Roblox pages, APIs, group records and creator videos behind this Regional School Bus Co guide, last checked {CHECKED_HUMAN}."}
so["jsonld"] = [crumbs("Sources", "/sources/")]
so_main = f"""<section class="guide-hero compact-hero"><div class="wide-container"><nav class="breadcrumbs" aria-label="Breadcrumb"><a href="/">Wiki home</a><span aria-hidden="true">/</span><span>Sources</span></nav><p class="eyebrow">Evidence before advice</p><h1>Sources &amp; verification</h1><p class="guide-deck">Official Roblox data sets the facts. Creator videos fill in how things look in play, labeled as observations.</p><span class="updated-line">Checked {CHECKED_HUMAN}</span></div></section><section class="sources-page wide-container"><div class="source-list"><div class="source-list-heading"><p class="eyebrow">Source ledger</p><h2>Pages checked for this guide</h2></div>{src_items}</div><div class="source-policy"><div><p class="eyebrow">Publishing rule</p><h2>No source, no exact value.</h2></div><p>Prices, badge counts and player numbers come from Roblox’s public APIs and are dated. Route pay, fuel prices, bus stats and keybinds aren’t published until a stable public source shows them. Codes need three or more independent sources. Head back to the <a href="/beginner-guide/">beginner guide</a> to play.</p></div></section>"""
so["html"] = shell(so, so_main)
PAGES.append(so)

# ---- 404
nf = {"path": "/404", "noindex": True, "title": "Page not found | Regional School Bus Co Guide", "description": "This page does not exist on the Regional School Bus Co guide."}
nf["html"] = shell(nf, f'<section class="guide-hero compact-hero"><div class="wide-container"><p class="eyebrow">404</p><h1>Page not found</h1><p class="guide-deck">Try the <a href="/">wiki home</a>, the <a href="/beginner-guide/">beginner guide</a> or the <a href="/faq/">FAQ</a>. Looking for the game? <a href="{PLAY}" rel="noreferrer">Play the current place ↗</a></p></div></section>')

SITEMAP = [("/", "1.0", "weekly"), ("/beginner-guide/", "0.9", "weekly"), ("/fall-update/", "0.9", "weekly"), ("/buses/", "0.8", "monthly"),
           ("/core-loop/", "0.7", "monthly"), ("/progression/", "0.7", "monthly"), ("/common-mistakes/", "0.7", "monthly"), ("/faq/", "0.8", "weekly"), ("/sources/", "0.5", "monthly")]


def main():
    for p in PAGES:
        rel = "index.html" if p["path"] == "/" else p["path"].strip("/") + "/index.html"
        out = os.path.join(ROOT, rel)
        os.makedirs(os.path.dirname(out), exist_ok=True)
        with open(out, "w", encoding="utf-8") as f:
            f.write(p["html"])
    with open(os.path.join(ROOT, "404.html"), "w", encoding="utf-8") as f:
        f.write(nf["html"])
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for path, pri, cf in SITEMAP:
        sm.append(f"<url><loc>{SITE}{path}</loc><lastmod>{CHECKED}</lastmod><changefreq>{cf}</changefreq><priority>{pri}</priority></url>")
    sm.append("</urlset>")
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write("\n".join(sm) + "\n")
    print(f"built {len(PAGES)} pages + 404 + sitemap ({len(SITEMAP)} urls)")


if __name__ == "__main__":
    main()
