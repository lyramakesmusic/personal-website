"""generate feed.xml from posts/index.json. run after adding a post, commit the result.
dates come from git (first commit that added each post's md), so index.json stays freeform.
the feed is plumbing for email (buttondown etc. watch it) - nobody needs to read it directly."""
import json, re, subprocess, html
from email.utils import format_datetime
from datetime import datetime, timezone

SITE = "https://lyraaaa.dev"
posts = json.load(open("posts/index.json", encoding="utf-8"))

LINK_RE = re.compile(r"\[([^\]]+)\]\([^)]+\)")
FRONT_RE = re.compile(r"^---\n[\s\S]*?\n---\n")


def first_para(md):
    body = FRONT_RE.sub("", md)
    for block in body.split("\n\n"):
        b = block.strip()
        if b and not b.startswith(("#", "!", ">", "-", "|", "```")):
            b = LINK_RE.sub(r"\1", b)        # [text](url) -> text
            b = re.sub(r"[*`]", "", b)       # emphasis / code markers (leave _ alone, it's in identifiers)
            return re.sub(r"\s+", " ", b)
    return ""


def git_date(path):
    out = subprocess.run(["git", "log", "--diff-filter=A", "--format=%aI", "--", path],
                         capture_output=True, text=True).stdout.strip().splitlines()
    return datetime.fromisoformat(out[-1]) if out else datetime.now(timezone.utc)


items = []
for p in posts:
    path = f"posts/{p['slug']}.md"
    md = open(path, encoding="utf-8").read()
    url = f"{SITE}/blog/{p['slug']}/"
    items.append(
        "    <item>\n"
        f"      <title>{html.escape(p['title'])}</title>\n"
        f"      <link>{url}</link>\n"
        f"      <guid isPermaLink=\"true\">{url}</guid>\n"
        f"      <pubDate>{format_datetime(git_date(path))}</pubDate>\n"
        f"      <description>{html.escape(first_para(md))}</description>\n"
        "    </item>"
    )

feed = (
    '<?xml version="1.0" encoding="UTF-8"?>\n'
    '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">\n'
    "  <channel>\n"
    "    <title>lyra</title>\n"
    f"    <link>{SITE}/</link>\n"
    f'    <atom:link href="{SITE}/feed.xml" rel="self" type="application/rss+xml"/>\n'
    "    <description>i like poking at things to see how they work.</description>\n"
    "    <language>en</language>\n"
    f"    <lastBuildDate>{format_datetime(datetime.now(timezone.utc))}</lastBuildDate>\n"
    + "\n".join(items) + "\n"
    "  </channel>\n"
    "</rss>\n"
)
open("feed.xml", "w", encoding="utf-8").write(feed)
print(f"wrote feed.xml with {len(items)} items")
