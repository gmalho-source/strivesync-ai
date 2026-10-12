#!/usr/bin/env python3
"""AI Systems repositioning (content/proposals/2026-10-ai-systems-repositioning.md).

Applies the approved copy to the WPBakery `content.raw` of each page, text only.
Every replacement must match exactly once (or the stated count), otherwise the
script aborts before writing anything.

    python3 scripts/repositioning_2026_10.py check          # dry run against content/ snapshot
    python3 scripts/repositioning_2026_10.py drafts         # create/update draft copies

Go-live is deliberately not implemented here: on approval, the approved raw is
copied into the original page IDs so URLs, Salient page settings and SEO history stay.
"""

import base64
import json
import os
import pathlib
import re
import sys
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
STATE = ROOT / "content/proposals/2026-10-ai-systems-repositioning.drafts.json"
WP_URL = os.environ.get("WP_URL", "https://strivesync.ai").rstrip("/")


def sub(raw, old, new, count=1):
    found = raw.count(old)
    if found != count:
        raise SystemExit(f"expected {count}x, found {found}x: {old[:90]!r}")
    return raw.replace(old, new)


def home(r):
    r = sub(r, "We help ambitious businesses across the UAE unlock their full potential, combining cutting-edge artificial intelligence with proven marketing strategies to drive real, measurable growth.",
            "We design, build and run AI systems for ambitious businesses across the UAE: agents that sell, serve and qualify, wired into the tools your team already uses.")
    r = sub(r, "Between wasted Ad spend, scattered content, and AI you can’t figure out how to use… It feels like you’re running in place.",
            "Leads that wait hours for a reply. A CRM nobody updates. Ten AI tools, zero systems. It feels like you’re running in place.")
    r = sub(r, "From intelligent AI agents that automate your workflows to performance campaigns that fill your pipeline — we’re here to make your marketing work harder, so you don’t have to.",
            "We replace manual, fragile processes with AI agents and automations that work around the clock — so your pipeline moves even when your team doesn’t.")
    r = sub(r, "Whether you’re just starting out or scaling to the next level, we’re here to support your growth every step of the way.",
            "We don’t sell software licences or hours. We install infrastructure that keeps producing long after the project ends.")
    r = sub(r, "<h3>Acquire. Convert. Automate.</h3>", "<h3>Capture. Qualify. Convert. Automate.</h3>")
    r = sub(r, "We drive qualified leads to your business with data-driven campaigns — then implement AI agents across your marketing, sales, and customer service to turn that pipeline into predictable revenue.",
            "We connect every step between a first click and a signed deal — AI agents, CRM, WhatsApp and your website working as one system that turns demand into predictable revenue.")
    r = sub(r, "<h2>Field of expertise</h2>", "<h2>One system. Three building blocks.</h2>")
    # Card 1
    r = sub(r, 'font_line_height="1"]Technology[', 'font_line_height="1"]AI Systems · 01[')
    r = sub(r, "<h2>Artificial Intelligence</h2>", "<h2>AI Agents</h2>")
    r = sub(r, "Deploy custom AI agents across your business — from smart customer service bots to automated lead qualification, sales assistants, and operational workflows. We make AI practical and accessible for businesses of every size.",
            "Custom AI agents for sales, customer service and lead qualification. They answer in seconds, in your tone, in Arabic and English, 24/7, and hand over to your team at the right moment.")
    # Card 2
    r = sub(r, 'font_line_height="1"]Marketing[', 'font_line_height="1"]AI Systems · 02[')
    r = sub(r, "<h2>Performance Marketing</h2>", "<h2>Automation &amp; Integrations</h2>")
    r = sub(r, "Data-driven campaigns on Google, Meta, LinkedIn, and TikTok designed to do one thing: generate qualified leads and drive online sales. Every dirham spent is tracked, optimised, and accountable.",
            "CRM, WhatsApp and lead-management flows that run themselves. Every lead captured, scored, routed and followed up — no spreadsheets, no leads lost between tools.")
    r = sub(r, 'url="https://strivesync.ai/services/performance-marketing/"', 'url="/services/artificial-intelligence-for-business/#automation"')
    # Card 3
    r = sub(r, 'font_line_height="1"]Development[', 'font_line_height="1"]AI Systems · 03[')
    r = sub(r, "<h2>Websites &amp; eCommerce</h2>", "<h2>AI-Ready Websites</h2>")
    r = sub(r, "Beautiful, high-performing websites built for conversion. From landing pages to full e-commerce platforms, we design digital experiences that look great and deliver results.",
            "Websites and stores built as the front door of your system: fast, conversion-focused and connected to your AI agents and CRM from day one.")
    r = sub(r, 'url="/website-development/"', 'url="/services/website-development/"')
    # Vision
    r = sub(r, "Imagine waking up to a pipeline full of qualified leads that came in while you slept. Your AI assistant already handled overnight customer enquiries. Your social media is growing consistently, your campaigns are profitable, and your brand is turning heads.",
            "Imagine waking up to a pipeline that worked overnight. Every enquiry answered. Every lead qualified and in your CRM. The hot ones already booked into your sales team’s calendar.")
    r = sub(r, "That’s not a dream — that’s what happens when you have the right growth partner by your side.",
            "That’s not a dream — that’s what a well-built system does.")
    return r


def services(r):
    r = sub(r, "<h2>How can we help you today?</h2>",
            "<h2>AI Systems, built around your business.</h2>\r\n<p>Every Strivesync project is one system with three building blocks. Most clients start with one and grow into all three.</p>")
    r = sub(r, "<h2>Artificial Intelligence</h2>\r\n<h5>For high performing businesses</h5>",
            "<h2>AI Agents</h2>\r\n<h5>Sell, serve and qualify — 24/7.</h5>")
    r = sub(r, 'link_screen_reader="Artificial Intelligence page"', 'link_screen_reader="AI Agents page"')
    r = sub(r, "<h2>Performance Marketing</h2>\r\n<h5>Leads. Sales. Growth. Measured to the last dirham.</h5>",
            "<h2>Automation &amp; Integrations</h2>\r\n<h5>Your CRM, WhatsApp and workflows, running on their own.</h5>")
    r = sub(r, 'link_url="https://strivesync.ai/services/performance-marketing/"',
            'link_url="https://strivesync.ai/services/artificial-intelligence-for-business/#automation"')
    r = sub(r, 'link_screen_reader="Performance Marketing (Paid Media) Page"', 'link_screen_reader="Automation and Integrations page"')
    r = sub(r, "<h2>Web Development</h2>\r\n<h5>Beautiful design. Seamless experience. Built for conversion.</h5>",
            "<h2>AI-Ready Websites</h2>\r\n<h5>The front door of your system. Built to convert.</h5>")
    r = sub(r, 'link_screen_reader="Website development page"', 'link_screen_reader="AI-Ready Websites page"')
    # Remove the Brand Strategy card (its whole inner column) and re-split 4 -> 3 columns.
    cols = re.findall(r"\[vc_column_inner [^\]]*\].*?\[/vc_column_inner\]", r, flags=re.S)
    brand = [c for c in cols if "services/brand-strategy/" in c]
    if len(brand) != 1:
        raise SystemExit(f"expected 1 Brand Strategy column, found {len(brand)}")
    r = sub(r, brand[0], "")
    r = sub(r, 'width="1/4"', 'width="1/3"', count=3)
    return r


def ai_business(r):
    r = sub(r, 'text_content="Artificial Intelligence for Businesses"', 'text_content="AI Systems for Businesses That Want to Scale"')
    r = sub(r, "Artificial intelligence isn’t just for tech giants anymore. At StriveSync, we help businesses of all sizes implement practical, powerful AI solutions that save time, reduce costs, and unlock new growth opportunities.",
            "AI isn’t a tool you subscribe to. It’s infrastructure you build. Strivesync designs, builds and runs AI systems that save time, cut costs and turn more of your demand into revenue.")
    r = sub(r, "Whether you need an AI-powered chatbot, an intelligent lead scoring system, or automated workflows that free your team to focus on what they do best — we design, build, and deploy AI agents tailored to your specific needs.",
            "From AI agents that answer and qualify every lead, to automations that keep your CRM, WhatsApp and team in sync — we build around your goals, your data and your existing tools.")
    r = sub(r, "providing data-driven recommendations that accelerate your sales cycle.",
            "providing data-driven recommendations that accelerate your sales cycle. Integrated with your CRM and calendar, so qualified leads land as booked meetings, not tasks.")
    r = sub(r, "<b>AI for Marketing &amp; Lead Generation</b>", "<b>AI Lead Capture &amp; Qualification</b>")
    r = sub(r, "Let AI do the heavy lifting. From predictive audience targeting to automated email sequences and smart content recommendations, our AI marketing tools help you reach the right people with the right message — at scale.",
            "Every lead from your website, ads, WhatsApp or social inbox is captured, enriched and scored by AI in seconds — then routed to the right person with the context they need to close.")
    r = sub(r, "Deliver exceptional customer experiences while reducing support costs.",
            "Deliver exceptional customer experiences while reducing support costs. In Arabic and English, across WhatsApp, web chat and email.")
    r = sub(r, "<b>Operational Automation</b>", '<span id="automation"></span><b>Automation &amp; Integrations</b>')
    r = sub(r, "Streamline your business operations with AI-driven workflows. From data entry and reporting to inventory management and process optimisation — we identify the repetitive tasks that slow you down and automate them intelligently.",
            "We connect your CRM, WhatsApp, forms, email and internal tools into workflows that run themselves — lead routing, follow-ups, reporting, onboarding. We find the repetitive work that slows your team down and remove it.")
    r = sub(r, "Building systems is more <em>achievable</em>\xa0than ever before.", "Discover. Design. Deploy. Improve.")
    return r


def website(r):
    r = sub(r, 'text_content="Websites That Work as Hard as You Do"', 'text_content="AI-Ready Websites: The Front Door of Your System"')
    r = sub(r, "Your website is your most important digital asset. It’s where first impressions are formed, where trust is built, and where visitors become customers. At StriveSync, we design and build websites that look stunning and perform brilliantly.",
            "Your website is where your system meets your customer. We build it AI-assisted, fast and conversion-focused — and connected from day one to the agents and automations behind it.")
    r = sub(r, "we create digital experiences that reflect your brand and deliver measurable results.",
            "we build websites that capture, qualify and route every visitor into your sales system — connected to your CRM and AI agents from day one.")
    r = sub(r, "high-impact landing pages for your campaigns —", "high-impact landing pages built to capture and qualify leads —")
    r = sub(r, "<h2>We've been doing websites for the last 20 years</h2>", "<h2>We've been building websites for over 20 years.</h2>")
    # AI Integration moves to first place. Rotate the contents of the 4 service
    # columns, keeping each [vc_column] wrapper (padding/background) where it is.
    pat = re.compile(r"(\[vc_column [^\]]*\])(\[nectar_icon .*?)(\[/vc_column\])", re.S)
    blocks = [m for m in pat.finditer(r) if "Let's Talk" in m.group(2)]
    titles = ["Website Design", "Website Development", "E-Commerce Solutions", "AI Integration"]
    if len(blocks) != 4 or [t for t in titles if t in blocks[titles.index(t)].group(2)] != titles:
        raise SystemExit("service columns not in the expected order")
    inner = [m.group(2) for m in blocks]
    rotated = inner[3:] + inner[:3]
    out, pos = [], 0
    for m, body in zip(blocks, rotated):
        out += [r[pos:m.start(2)], body]
        pos = m.end(2)
    out.append(r[pos:])
    return "".join(out)


def about(r):
    r = sub(r, "Based in Dubai, we’re an AI-powered marketing agency that combines the latest in artificial intelligence with deep marketing expertise to help businesses grow smarter, faster, and more efficiently.",
            "Based in Dubai, we’re an AI systems company. We combine hands-on AI engineering with two decades of sales and marketing experience to help businesses grow smarter, faster and with less friction.")
    r = sub(r, "To make AI-powered marketing accessible, practical, and results-driven for growing businesses in the UAE and beyond.",
            "To make AI systems accessible, practical and results-driven for growing businesses in the UAE and beyond.")
    r = sub(r, "To be the most trusted AI marketing partner for SMEs and startups in the Middle East — helping businesses compete and win in the digital age, regardless of their size.",
            "To be the most trusted AI systems partner for SMEs and startups in the Middle East — helping businesses compete and win, regardless of their size.")
    return r


PAGES = {
    10: ("10-strivesync", home,
         "Strivesync builds AI-native sales and marketing systems for UAE businesses: custom AI agents, CRM and WhatsApp automation, and AI-ready websites. Based in Dubai."),
    1549: ("1549-services", services,
           "AI agents, automation & integrations and AI-ready websites — the three building blocks of every Strivesync system. See what we build for UAE businesses."),
    1597: ("1597-artificial-intelligence-for-business", ai_business,
           "Custom AI agents, lead qualification and CRM & WhatsApp automation for UAE businesses. Strivesync designs, builds and runs AI systems that scale without adding headcount."),
    1706: ("1706-website-development", website, None),
    1466: ("1466-about-strivesync", about, None),
}


def api(method, path, body=None):
    token = base64.b64encode(f"{os.environ['WP_USER']}:{os.environ['WP_APP_PASSWORD']}".encode()).decode()
    req = urllib.request.Request(f"{WP_URL}/wp-json/{path}", method=method,
                                 data=json.dumps(body).encode() if body is not None else None)
    req.add_header("Authorization", f"Basic {token}")
    req.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.load(resp)


def transformed(pid):
    name, fn, _ = PAGES[pid]
    page = json.load(open(ROOT / f"content/pages/{name}.json"))
    raw = page["content"]["raw"]
    new = fn(raw)
    if "StriveSync" in new:
        raise SystemExit(f"{pid}: 'StriveSync' spelling left in page")
    if new.count("[") != new.count("]"):
        raise SystemExit(f"{pid}: unbalanced shortcode brackets")
    return page, new


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "check"
    results = {pid: transformed(pid) for pid in PAGES}  # all-or-nothing validation
    if mode == "check":
        for pid, (page, new) in results.items():
            print(f"{pid} {page['slug']}: ok ({len(page['content']['raw'])} -> {len(new)} chars)")
        return
    if mode != "drafts":
        raise SystemExit("usage: repositioning_2026_10.py [check|drafts]")
    state = json.loads(STATE.read_text()) if STATE.exists() else {}
    for pid, (page, new) in results.items():
        body = {
            "title": page["title"]["raw"],
            "content": new,
            "status": "draft",
            "parent": page["parent"],
            "menu_order": page["menu_order"],
            "template": page["template"],
            "featured_media": page["featured_media"],
            "slug": f"{page['slug']}-ai-systems-draft",
        }
        draft_id = state.get(str(pid))
        if draft_id:
            current = api("GET", f"wp/v2/pages/{draft_id}?context=edit")
            if current["status"] != "draft":
                raise SystemExit(f"copy {draft_id} is no longer a draft, refusing to touch it")
            saved = api("POST", f"wp/v2/pages/{draft_id}", body)
        else:
            saved = api("POST", "wp/v2/pages", body)
        assert saved["status"] == "draft"
        state[str(pid)] = saved["id"]
        STATE.write_text(json.dumps(state, indent=2) + "\n")
        print(f"{pid} {page['slug']} -> draft {saved['id']}")


if __name__ == "__main__":
    main()
