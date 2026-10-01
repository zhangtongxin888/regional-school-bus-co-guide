#!/usr/bin/env python3
"""HTML lint: tag balance, duplicate ids, empty links, alt text, JSON-LD parses, no stale Next runtime."""
import glob, json, os, re, sys
from html.parser import HTMLParser
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
VOID = {"area","base","br","col","embed","hr","img","input","link","meta","source","track","wbr"}
errs = []
class P(HTMLParser):
    def __init__(s, f):
        super().__init__(); s.f=f; s.stack=[]; s.ids=set(); s.in_a=None
    def handle_starttag(s, t, attrs):
        a=dict(attrs)
        if "id" in a:
            if a["id"] in s.ids: errs.append(f"{s.f}: duplicate id {a['id']}")
            s.ids.add(a["id"])
        if t=="img" and not a.get("alt"): errs.append(f"{s.f}: img without alt")
        if t=="a" and not a.get("href"): errs.append(f"{s.f}: a without href")
        if t not in VOID: s.stack.append(t)
    def handle_endtag(s, t):
        if t in VOID: return
        if not s.stack or s.stack[-1]!=t:
            errs.append(f"{s.f}: unexpected </{t}> (open: {s.stack[-3:]})"); 
            if t in s.stack:
                while s.stack and s.stack.pop()!=t: pass
            return
        s.stack.pop()
files = [f for f in glob.glob(os.path.join(ROOT, "**/*.html"), recursive=True) if "/.git/" not in f]
for f in files:
    s = open(f, encoding="utf-8").read(); rel = os.path.relpath(f, ROOT)
    p = P(rel); p.feed(s); p.close()
    if p.stack: errs.append(f"{rel}: unclosed {p.stack}")
    if "/_next/static/chunks/" in s and re.search(r'<script[^>]+_next', s): errs.append(f"{rel}: stale Next.js runtime script")
    if "self.__next_f" in s: errs.append(f"{rel}: stale RSC payload")
    for m in re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
        try: json.loads(m)
        except Exception as e: errs.append(f"{rel}: bad JSON-LD {e}")
print(f"lint: {len(files)} html files, {len(errs)} problems")
for e in errs: print("  -", e)
sys.exit(1 if errs else 0)
