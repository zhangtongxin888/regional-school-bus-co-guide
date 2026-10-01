#!/usr/bin/env python3
"""Content contract tests."""
import os, re, sys, unittest
sys.path.insert(0, os.path.dirname(__file__))
import site_data as D
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
def read(p): return open(os.path.join(ROOT, p), encoding="utf-8").read()
PAGES = ["index.html"] + [f"{d}/index.html" for d in ["beginner-guide","fall-update","buses","core-loop","progression","common-mistakes","faq","sources"]]
class T(unittest.TestCase):
    def test_codes_need_three_sources(self):
        for c in D.CODES_WORKING:
            self.assertGreaterEqual(len(c.get("sources", [])), 3, c)
    def test_no_code_tables_without_codes(self):
        if not D.CODES_WORKING:
            for p in PAGES:
                self.assertNotRegex(read(p), r"(?i)working codes?:\s*<", p)
    def test_play_links_current_place(self):
        for p in PAGES:
            for href in re.findall(r'href="(https://www\.roblox\.com/games/[^"]+)"', read(p)):
                self.assertIn(str(D.GAME["place_id"]), href, p)
    def test_moved_answer_visible(self):
        for p in ["index.html", "faq/index.html", "beginner-guide/index.html", "common-mistakes/index.html"]:
            s = read(p); self.assertIn(str(D.GAME["place_id"]), s); self.assertIn(str(D.OLD_GAME["place_id"]), s)
    def test_pass_prices_rendered(self):
        s = read("buses/index.html")
        for name, kind, price in D.PASSES:
            self.assertIn(name.replace("&", "&amp;"), s)
            if price: self.assertIn(f"{price} Robux", s)
    def test_badges_rendered(self):
        s = read("progression/index.html")
        for b in D.BADGES: self.assertIn(b[0], s)
    def test_sitemap_lastmod(self):
        sm = read("sitemap.xml")
        self.assertEqual(sm.count(f"<lastmod>{D.CHECKED}</lastmod>"), sm.count("<loc>"))
        for p in ["fall-update", "buses"]: self.assertIn(f"/{p}/</loc>", sm)
    def test_no_next_runtime(self):
        for p in PAGES: self.assertNotIn("self.__next_f", read(p))
if __name__ == "__main__":
    unittest.main(verbosity=2)
