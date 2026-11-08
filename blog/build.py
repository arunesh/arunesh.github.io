#!/usr/bin/env python3
"""Build the blog: Markdown posts in blog/_src/posts/ -> static HTML in blog/.

    python3 blog/build.py            build once
    python3 blog/build.py --serve    build, serve the site at http://localhost:8000/blog/
                                     and rebuild whenever a source file changes

Needs the `markdown` package (pip install markdown).
"""

import argparse
import datetime as dt
import html
import json
import os
import re
import shutil
import sys
import threading
import time
from email.utils import format_datetime
from pathlib import Path
from string import Template

import markdown

BLOG = Path(__file__).resolve().parent
ROOT = BLOG.parent
SRC = BLOG / "_src"
POSTS = SRC / "posts"
TEMPLATES = SRC / "templates"

# Folders in blog/ that build.py manages; anything else in blog/ is left alone.
RESERVED = {"_src", "assets"}


def load_config():
    return json.loads((SRC / "site.json").read_text())


def parse_front_matter(text, path):
    """Split '---\\nkey: value\\n---\\nbody' into (meta, body)."""
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", text, re.S)
    if not m:
        sys.exit(f"{path}: missing front matter (--- title: ... ---)")
    meta = {}
    for line in m.group(1).splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        key, _, value = line.partition(":")
        meta[key.strip()] = value.strip().strip('"')
    return meta, m.group(2)


def slug_from(path):
    # 2026-11-08-videoindex.md -> videoindex
    return re.sub(r"^\d{4}-\d{2}-\d{2}-", "", path.stem)


def read_posts():
    posts = []
    for path in sorted(POSTS.glob("*.md")):
        meta, body = parse_front_matter(path.read_text(), path)
        if meta.get("draft", "").lower() == "true":
            continue
        for field in ("title", "date"):
            if field not in meta:
                sys.exit(f"{path}: front matter needs '{field}'")
        md = markdown.Markdown(
            extensions=["extra", "toc", "sane_lists", "smarty"],
            extension_configs={"toc": {"permalink": "#", "permalink_class": "anchor", "toc_depth": "2-3"}},
            output_format="html5",
        )
        content = md.convert(body)
        words = len(re.findall(r"\w+", re.sub(r"<[^>]+>", " ", content)))
        posts.append({
            "title": meta["title"],
            "date": dt.date.fromisoformat(meta["date"]),
            "summary": meta.get("summary", ""),
            "tags": [t.strip() for t in meta.get("tags", "").split(",") if t.strip()],
            "slug": meta.get("slug") or slug_from(path),
            "show_toc": meta.get("toc", "").lower() == "true",
            "toc": md.toc,
            "content": content,
            "minutes": max(1, round(words / 230)),
        })
    posts.sort(key=lambda p: p["date"], reverse=True)
    return posts


def esc(s):
    return html.escape(s, quote=True)


def nice_date(d):
    return d.strftime("%b %-d, %Y")


def signup_box(cfg):
    nl = cfg.get("newsletter", {})
    user = nl.get("buttondown_username", "").strip()
    blurb = esc(nl.get("blurb", "New posts by email. No spam, unsubscribe anytime."))
    rss = '<a href="/blog/feed.xml">RSS</a>'
    if not user:
        # Not configured yet: show the box, but don't post anywhere.
        return f"""<section class="signup" aria-label="Email updates">
  <div class="signup-text"><strong>Get new posts by email</strong><span>Email updates are coming soon. Until then, follow via {rss}.</span></div>
  <form class="signup-form" onsubmit="return false">
    <input type="email" placeholder="you@example.com" aria-label="Email address" disabled>
    <button type="submit" disabled>Subscribe</button>
  </form>
</section>"""
    u = esc(user)
    return f"""<section class="signup" aria-label="Email updates">
  <div class="signup-text"><strong>Get new posts by email</strong><span>{blurb} Or follow via {rss}.</span></div>
  <form class="signup-form" action="https://buttondown.com/api/emails/embed-subscribe/{u}" method="post"
        target="popupwindow" onsubmit="window.open('https://buttondown.com/{u}', 'popupwindow')">
    <input type="email" name="email" placeholder="you@example.com" aria-label="Email address" required>
    <input type="hidden" value="1" name="embed">
    <button type="submit">Subscribe</button>
  </form>
</section>"""


def tags_html(tags):
    return "".join(f'<span class="tag">{esc(t)}</span>' for t in tags)


def render_page(cfg, base, title, description, body, path):
    return base.substitute(
        title=esc(title),
        description=esc(description),
        canonical=esc(cfg["site_url"].rstrip("/") + path),
        site_title=esc(cfg["title"]),
        author=esc(cfg["author"]),
        body=body,
        year=dt.date.today().year,
    )


def build():
    cfg = load_config()
    base = Template((TEMPLATES / "base.html").read_text())
    posts = read_posts()

    # Remove pages from earlier builds (folders with a generated index.html), keep everything else.
    for child in BLOG.iterdir():
        if child.is_dir() and child.name not in RESERVED and (child / ".generated").exists():
            shutil.rmtree(child)

    for p in posts:
        toc = ""
        if p["show_toc"] and p["toc"].count("<li") > 2:
            toc = f'<details class="toc"><summary>Contents</summary>{p["toc"]}</details>'
        body = f"""<article class="post">
  <header class="post-head">
    <p class="meta"><time datetime="{p['date'].isoformat()}">{nice_date(p['date'])}</time> · {p['minutes']} min read</p>
    <h1>{esc(p['title'])}</h1>
    {f'<p class="lede">{esc(p["summary"])}</p>' if p['summary'] else ''}
    <div class="tags">{tags_html(p['tags'])}</div>
  </header>
  {toc}
  <div class="prose">
{p['content']}
  </div>
  <footer class="post-foot">
    <a href="/blog/">&larr; All posts</a>
  </footer>
</article>
{signup_box(cfg)}"""
        out = BLOG / p["slug"]
        out.mkdir(exist_ok=True)
        (out / ".generated").write_text("created by blog/build.py; safe to delete\n")
        (out / "index.html").write_text(
            render_page(cfg, base, f"{p['title']} · {cfg['title']}", p["summary"] or p["title"], body, f"/blog/{p['slug']}/"))

    items = "\n".join(
        f"""  <li class="post-item">
    <p class="meta"><time datetime="{p['date'].isoformat()}">{nice_date(p['date'])}</time> · {p['minutes']} min read</p>
    <h2><a href="/blog/{p['slug']}/">{esc(p['title'])}</a></h2>
    {f'<p class="summary">{esc(p["summary"])}</p>' if p['summary'] else ''}
    <div class="tags">{tags_html(p['tags'])}</div>
  </li>""" for p in posts) or '  <li class="empty">No posts yet.</li>'
    index_body = f"""<header class="blog-head">
  <h1>{esc(cfg['title'])}</h1>
  <p class="lede">{esc(cfg['description'])}</p>
</header>
{signup_box(cfg)}
<ul class="post-list">
{items}
</ul>"""
    (BLOG / "index.html").write_text(render_page(cfg, base, cfg["title"], cfg["description"], index_body, "/blog/"))

    site = cfg["site_url"].rstrip("/")
    rss_items = "\n".join(f"""    <item>
      <title>{esc(p['title'])}</title>
      <link>{site}/blog/{p['slug']}/</link>
      <guid>{site}/blog/{p['slug']}/</guid>
      <pubDate>{format_datetime(dt.datetime.combine(p['date'], dt.time(12), dt.timezone.utc))}</pubDate>
      <description>{esc(p['summary'])}</description>
    </item>""" for p in posts)
    (BLOG / "feed.xml").write_text(f"""<?xml version="1.0" encoding="utf-8"?>
<rss version="2.0">
  <channel>
    <title>{esc(cfg['title'])}</title>
    <link>{site}/blog/</link>
    <description>{esc(cfg['description'])}</description>
{rss_items}
  </channel>
</rss>
""")
    print(f"built {len(posts)} post(s) -> {BLOG.relative_to(ROOT)}/")


def snapshot():
    return {p: p.stat().st_mtime for p in SRC.rglob("*") if p.is_file()}


def port_in_use(port):
    """True if anything answers on this port over IPv4 or IPv6 (browsers try both for 'localhost')."""
    import socket
    for family, host in ((socket.AF_INET, "127.0.0.1"), (socket.AF_INET6, "::1")):
        try:
            with socket.socket(family, socket.SOCK_STREAM) as s:
                s.settimeout(0.3)
                if s.connect_ex((host, port)) == 0:
                    return True
        except OSError:
            pass
    return False


def serve(port):
    import http.server
    import functools
    start = port
    while port_in_use(port):
        port += 1
    if port != start:
        print(f"port {start} is already used by another program; using {port} instead")
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(ROOT))
    httpd = http.server.ThreadingHTTPServer(("127.0.0.1", port), handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    print(f"serving http://127.0.0.1:{port}/blog/  (Ctrl+C to stop; rebuilds on save)")
    seen = snapshot()
    try:
        while True:
            time.sleep(1)
            now = snapshot()
            if now != seen:
                seen = now
                try:
                    build()
                except SystemExit as e:
                    print(e)
    except KeyboardInterrupt:
        httpd.shutdown()


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--serve", action="store_true", help="serve locally and rebuild on change")
    ap.add_argument("--port", type=int, default=8000)
    args = ap.parse_args()
    build()
    if args.serve:
        serve(args.port)
