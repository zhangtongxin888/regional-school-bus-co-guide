#!/usr/bin/env python3
"""SEO audit over the built HTML for every sitemap URL."""
import json, os, re, sys, html
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SITE = "https://regionalschoolbusco.wiki"
NEW_PLACE, OLD_PLACE = "93172673274529", "15937818410"
errs, rows = [], []
sm = open(os.path.join(ROOT, "sitemap.xml"), encoding="utf-8").read()
locs = re.findall(r"<loc>(.*?)</loc>", sm)
if len(re.findall(r"<lastmod>\d{4}-\d{2}-\d{2}</lastmod>", sm)) != len(locs): errs.append("sitemap: every url needs lastmod")
robots = open(os.path.join(ROOT, "robots.txt")).read()
if f"Sitemap: {SITE}/sitemap.xml" not in robots: errs.append("robots.txt missing sitemap")
def fpath(path):
    path = path.split("#")[0].split("?")[0]
    return os.path.join(ROOT, "index.html") if path in ("", "/") else os.path.join(ROOT, path.strip("/"), "index.html")
titles, inbound = {}, {l.replace(SITE, ""): 0 for l in locs}
for loc in locs:
    path = loc.replace(SITE, "")
    f = fpath(path)
    if not os.path.exists(f): errs.append(f"{path}: missing file"); continue
    s = open(f, encoding="utf-8").read()
    g = lambda r: (re.search(r, s, re.S) or [None, None])[1]
    title = html.unescape(g(r"<title>(.*?)</title>") or ""); desc = html.unescape(g(r'<meta name="description" content="(.*?)"') or "")
    canon = g(r'<link rel="canonical" href="(.*?)"'); h1s = re.findall(r"<h1[^>]*>(.*?)</h1>", s, re.S)
    h1 = re.sub(r"<[^>]+>", " ", h1s[0]) if h1s else ""
    if canon != loc: errs.append(f"{path}: canonical {canon} != {loc}")
    if not (20 <= len(title) <= 65): errs.append(f"{path}: title length {len(title)}")
    if not (70 <= len(desc) <= 170): errs.append(f"{path}: description length {len(desc)}")
    if len(h1s) != 1: errs.append(f"{path}: {len(h1s)} h1")
    if title in titles: errs.append(f"{path}: duplicate title with {titles[title]}")
    titles[title] = path
    for tag in ['property="og:title"', 'property="og:description"', 'property="og:url"', 'property="og:image"', 'name="twitter:card"', 'name="twitter:title"']:
        if tag not in s: errs.append(f"{path}: missing {tag}")
    if 'type="application/ld+json"' not in s: errs.append(f"{path}: no JSON-LD")
    if 'name="robots" content="noindex"' in s: errs.append(f"{path}: noindex on sitemap url")
    # exact-query ownership: only the homepage may target "<game> wiki"
    owns_wiki = "regional school bus co wiki" in (title + " " + h1).lower()
    if path == "/" and not owns_wiki: errs.append("/: homepage must own 'Regional School Bus Co Wiki' in title/H1")
    if path != "/" and owns_wiki: errs.append(f"{path}: competes with homepage for 'regional school bus co wiki'")
    # links
    for href in re.findall(r'href="([^"]+)"', s):
        if href.startswith("/") and not href.startswith("//"):
            if href.startswith(("/_next/", "/assets/", "/images/", "/manifest", "/og.png")):
                if not os.path.exists(os.path.join(ROOT, href.lstrip("/"))): errs.append(f"{path}: missing asset {href}")
                continue
            if not os.path.exists(fpath(href)): errs.append(f"{path}: broken internal link {href}")
            k = href.split("#")[0]
            if k in inbound and k != path: inbound[k] += 1
        if "roblox.com/games/" in href and NEW_PLACE not in href: errs.append(f"{path}: Roblox play link not pointing at current place: {href}")
    body = re.sub(r"<script.*?</script>", "", s, flags=re.S)
    rows.append({"path": path, "title": title, "titleLen": len(title), "descLen": len(desc), "h1": h1.strip(), "words": len(re.sub(r"<[^>]+>", " ", body).split())})
for k, v in inbound.items():
    if k != "/" and v == 0: errs.append(f"{k}: orphan (no inbound internal links)")
print(json.dumps(rows, indent=1, ensure_ascii=False))
print(f"seo audit: {len(locs)} sitemap urls, {len(errs)} problems")
for e in errs: print("  -", e)
sys.exit(1 if errs else 0)
