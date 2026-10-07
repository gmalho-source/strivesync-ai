#!/usr/bin/env python3
"""Snapshot WordPress content into content/ via the REST API.

With WP_USER + WP_APP_PASSWORD set, uses context=edit to capture the raw
content (WPBakery shortcodes) plus drafts/private items. Without them, only
public items with rendered HTML are saved.

Usage:
    WP_URL=https://strivesync.ai WP_USER=... WP_APP_PASSWORD=... python3 scripts/wp_snapshot.py
"""

import base64
import json
import os
import pathlib
import sys
import urllib.error
import urllib.request

WP_URL = os.environ.get("WP_URL", "https://strivesync.ai").rstrip("/")
WP_USER = os.environ.get("WP_USER")
WP_APP_PASSWORD = os.environ.get("WP_APP_PASSWORD")
OUT = pathlib.Path(__file__).resolve().parent.parent / "content"

AUTHED = bool(WP_USER and WP_APP_PASSWORD)
TYPES = ["pages", "posts", "categories", "tags", "media"]
if AUTHED:
    TYPES += ["menus", "menu-items", "blocks"]


def get(path, params):
    query = "&".join(f"{k}={v}" for k, v in params.items())
    req = urllib.request.Request(f"{WP_URL}/wp-json/wp/v2/{path}?{query}")
    if AUTHED:
        token = base64.b64encode(f"{WP_USER}:{WP_APP_PASSWORD}".encode()).decode()
        req.add_header("Authorization", f"Basic {token}")
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.load(resp), int(resp.headers.get("X-WP-TotalPages", "1"))


def fetch_all(path):
    params = {"per_page": 100, "context": "edit" if AUTHED else "view"}
    if AUTHED and path in ("pages", "posts", "blocks"):
        params["status"] = "publish,draft,pending,private,future"
    items, page, total = [], 1, 1
    while page <= total:
        batch, total = get(path, {**params, "page": page})
        items.extend(batch)
        page += 1
    return items


def main():
    print(f"Snapshot {WP_URL} ({'authenticated' if AUTHED else 'public only'})")
    for t in TYPES:
        try:
            items = fetch_all(t)
        except urllib.error.HTTPError as e:
            print(f"  {t}: skipped (HTTP {e.code})", file=sys.stderr)
            continue
        folder = OUT / t
        folder.mkdir(parents=True, exist_ok=True)
        for old in folder.glob("*.json"):
            old.unlink()
        for item in items:
            name = f"{item['id']}-{item.get('slug') or 'item'}.json"
            (folder / name).write_text(
                json.dumps(item, indent=2, ensure_ascii=False, sort_keys=True) + "\n"
            )
        print(f"  {t}: {len(items)}")


if __name__ == "__main__":
    main()
