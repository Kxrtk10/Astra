import json
import re
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET


WIKIPEDIA_SUMMARY_URL = "https://en.wikipedia.org/api/rest_v1/page/summary/"
GOOGLE_NEWS_RSS_URL = "https://news.google.com/rss/search?q={query}&hl=en-IN&gl=IN&ceid=IN:en"

CURRENT_TOPIC_HINTS = [
    "today",
    "latest",
    "recent",
    "news",
    "happening",
    "currently",
    "tournament",
    "match",
    "election",
    "score",
    "result",
    "winner",
]


def should_fetch_live_context(user_input):
    text = (user_input or "").strip().lower()
    if not text:
        return False

    study_prefixes = (
        "explain ",
        "generate quiz",
        "what should i study",
        "create study plan",
        "show weekly plan",
        "show my points",
    )
    if text.startswith(study_prefixes):
        return False

    if any(hint in text for hint in CURRENT_TOPIC_HINTS):
        return True

    return bool(
        re.search(
            r"\b(who is|what is happening|tell me about|what do you know about|updates on)\b",
            text,
            re.IGNORECASE,
        )
    )


def _fetch_url(url):
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "AdaptiveLearningTutor/1.0",
            "Accept": "application/json, application/xml, text/xml;q=0.9, */*;q=0.8",
        },
    )
    with urllib.request.urlopen(request, timeout=8) as response:
        return response.read()


def _fetch_wikipedia_summary(query):
    slug = urllib.parse.quote(query.replace(" ", "_"))
    try:
        payload = _fetch_url(f"{WIKIPEDIA_SUMMARY_URL}{slug}")
        data = json.loads(payload.decode("utf-8"))
        extract = (data.get("extract") or "").strip()
        title = (data.get("title") or "").strip()
        if not extract:
            return None
        return {"title": title or query, "summary": extract}
    except Exception:
        return None


def _fetch_news_rss(query, limit=3):
    encoded_query = urllib.parse.quote(query)
    try:
        payload = _fetch_url(GOOGLE_NEWS_RSS_URL.format(query=encoded_query))
        root = ET.fromstring(payload)
    except Exception:
        return []

    items = []
    channel = root.find("channel")
    if channel is None:
        return items

    for item in channel.findall("item")[:limit]:
        title = (item.findtext("title") or "").strip()
        link = (item.findtext("link") or "").strip()
        pub_date = (item.findtext("pubDate") or "").strip()
        if title:
            items.append({"title": title, "link": link, "pub_date": pub_date})
    return items


def build_live_context_bundle(user_input):
    query = (user_input or "").strip()
    if not query:
        return {"text": "", "sources": []}

    wiki = _fetch_wikipedia_summary(query)
    news_items = _fetch_news_rss(query)

    lines = []
    sources = []
    if wiki:
        lines.append("Reference background:")
        lines.append(f"- {wiki['title']}: {wiki['summary']}")
        sources.append(
            {
                "label": wiki["title"],
                "url": f"https://en.wikipedia.org/wiki/{urllib.parse.quote(wiki['title'].replace(' ', '_'))}",
                "kind": "background",
            }
        )

    if news_items:
        lines.append("Recent live context:")
        for item in news_items:
            lines.append(f"- {item['title']} ({item['pub_date']})")
            if item["link"]:
                lines.append(f"  Source: {item['link']}")
            sources.append(
                {
                    "label": item["title"],
                    "url": item["link"],
                    "kind": "news",
                }
            )

    return {"text": "\n".join(lines), "sources": sources}


def build_live_context(user_input):
    return build_live_context_bundle(user_input)["text"]
