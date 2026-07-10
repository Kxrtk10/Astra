import json
import re
import time
import urllib.parse
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime

import httpx


NEWS_CACHE_TTL_SECONDS = 15 * 60
SPORTS_CACHE_TTL_SECONDS = 10 * 60

NEWS_FEEDS = [
    {
        "name": "NDTV",
        "url": "https://feeds.feedburner.com/ndtvnews-top-stories",
    },
    {
        "name": "BBC News",
        "url": "https://feeds.bbci.co.uk/news/world/rss.xml",
    },
    {
        "name": "Times of India",
        "url": "https://timesofindia.indiatimes.com/rssfeedstopstories.cms",
    },
]

SPORTSDB_BASE_URL = "https://www.thesportsdb.com/api/v1/json/3"
ESPN_FIFA_WORLD_SCOREBOARD_URL = "https://site.api.espn.com/apis/site/v2/sports/soccer/fifa.world/scoreboard"
FIFA_WORLD_CUP_2026_STAGE_DATES = {
    "Group Stage": "20260611-20260627",
    "Round of 32": "20260628-20260703",
    "Round of 16": "20260704-20260707",
    "Quarterfinals": "20260709-20260711",
    "Semifinals": "20260714-20260715",
    "Third-place Match": "20260718-20260718",
    "Final": "20260719-20260719",
}
SPORTS_KEYWORDS = {
    "score",
    "scores",
    "match",
    "fixture",
    "fixtures",
    "result",
    "results",
    "won",
    "winner",
    "world cup",
    "football",
    "soccer",
    "cricket",
    "ipl",
    "premier league",
    "champions league",
    "la liga",
    "nba",
    "tennis",
    "fifa",
}
NEWS_KEYWORDS = {
    "news",
    "headline",
    "headlines",
    "latest",
    "today",
    "current",
    "right now",
    "happening",
    "update",
    "updates",
    "breaking",
}
CURRENT_EVENT_KEYWORDS = SPORTS_KEYWORDS | NEWS_KEYWORDS

POPULAR_LEAGUES = {
    "ipl": "4464",
    "premier league": "4328",
    "champions league": "4480",
    "la liga": "4335",
    "nba": "4387",
}

SPORTS_FILLER_PHRASES = (
    'okay now give me',
    'ok now give me',
    'okay give me',
    'ok give me',
    'can you tell me',
    'could you tell me',
    'please tell me',
    'tell me about',
    'give me',
    'what about',
    'what are',
    'what were',
    'show me',
    'i want',
)

SPORTS_INTENT_WORDS = {
    'score', 'scores', 'result', 'results', 'fixture', 'fixtures',
    'match', 'matches', 'latest', 'today', 'current', 'right', 'now',
    'give', 'tell', 'show', 'please', 'me', 'the', 'of', 'for', 'in',
}

TOURNAMENT_ALIASES = (
    (re.compile(r'\b(fifa\s+wc|fifa\s+world\s+cup|world\s+cup)\b'), 'FIFA World Cup'),
    (re.compile(r'\bipl\b'), 'IPL'),
    (re.compile(r'\bnba\b'), 'NBA'),
    (re.compile(r'\bpremier\s+league\b'), 'Premier League'),
    (re.compile(r'\bchampions\s+league\b'), 'Champions League'),
    (re.compile(r'\bla\s+liga\b'), 'La Liga'),
)

_news_cache = {"expires_at": 0.0, "items": []}
_sports_cache = {}


def is_lounge_live_query(message: str) -> bool:
    text = _normalize(message)
    if not text:
        return False
    if any(keyword in text for keyword in CURRENT_EVENT_KEYWORDS):
        return True
    return bool(re.search(r"\b(who won|what happened|what is happening|what's happening)\b", text))


def build_lounge_live_context(message: str) -> dict:
    text = _normalize(message)
    if not is_lounge_live_query(text):
        return {"text": "", "sources": [], "intent": "none", "has_data": False, "deterministic_reply": ""}

    wants_sports = _is_sports_query(text)
    wants_news = _is_news_query(text) and (not wants_sports or any(word in text for word in ('news', 'headline', 'headlines', 'breaking', 'update', 'updates')))
    lines = []
    sources = []
    intent_parts = []

    if wants_sports:
        sports_query = _clean_sports_query(text)
        sports_items = _get_sports_items(sports_query)
        intent_parts.append("sports")
        if sports_items:
            lines.append("Latest available sports context from ESPN/TheSportsDB:")
            for item in sports_items[:6]:
                lines.append(_format_sports_item(item))
            sources.append({"label": "TheSportsDB", "url": "https://www.thesportsdb.com/", "kind": "sports"})

    if wants_news:
        news_items = _filter_news_items(_get_news_items(), text)
        intent_parts.append("news")
        if news_items:
            lines.append("Recent news headlines from cached RSS feeds:")
            for item in news_items[:6]:
                lines.append(_format_news_item(item))
                if item.get("url"):
                    sources.append({"label": item.get("title") or item.get("source"), "url": item["url"], "kind": "news"})

    if not lines:
        requested_label = _describe_live_request(text, wants_sports=wants_sports, wants_news=wants_news)
        return {
            'text': (
                'Lounge live-data request detected, but no matching cached news or sports data is available. '
                'Tell the student this plainly in one short sentence and do not guess.'
            ),
            'sources': [],
            'intent': '+'.join(intent_parts) or 'live',
            'has_data': False,
            'deterministic_reply': f'I don\'t have those {requested_label} in my live sources right now.',
        }

    context = "\n".join(lines)
    context += (
        "\n\nUse only the context above for live/current facts. "
        "If the student's exact team, match, or topic is not covered by the context, say that briefly and do not fabricate."
    )
    return {
        "text": context,
        "sources": _dedupe_sources(sources),
        "intent": "+".join(intent_parts) or "live",
        "has_data": True,
        "deterministic_reply": "",
    }


def _normalize(value: str) -> str:
    return re.sub(r"\s+", " ", str(value or "").strip().lower())


def _is_sports_query(text: str) -> bool:
    return any(keyword in text for keyword in SPORTS_KEYWORDS)


def _is_news_query(text: str) -> bool:
    return any(keyword in text for keyword in NEWS_KEYWORDS)


def _fetch_text(url: str, params: dict | None = None) -> str:
    with httpx.Client(timeout=8.0, follow_redirects=True) as client:
        response = client.get(
            url,
            params=params or {},
            headers={"User-Agent": "AstraLearningStudio/1.0"},
        )
        response.raise_for_status()
        return response.text or ""


def _get_news_items() -> list[dict]:
    now = time.time()
    if _news_cache["expires_at"] > now:
        return list(_news_cache["items"])

    items = []
    for feed in NEWS_FEEDS:
        try:
            xml_text = _fetch_text(feed["url"])
            items.extend(_parse_rss_items(xml_text, feed["name"]))
        except Exception:
            continue

    items.sort(key=lambda item: item.get("published_ts") or 0, reverse=True)
    _news_cache["items"] = items[:80]
    _news_cache["expires_at"] = now + NEWS_CACHE_TTL_SECONDS
    return list(_news_cache["items"])


def _parse_rss_items(xml_text: str, source: str) -> list[dict]:
    try:
        root = ET.fromstring(xml_text.encode("utf-8"))
    except Exception:
        return []

    channel = root.find("channel")
    raw_items = channel.findall("item") if channel is not None else root.findall(".//item")
    parsed = []
    for item in raw_items[:25]:
        title = _clean_xml_text(item.findtext("title"))
        summary = _clean_xml_text(item.findtext("description"))
        url = _clean_xml_text(item.findtext("link"))
        published = _clean_xml_text(item.findtext("pubDate"))
        if not title:
            continue
        parsed.append(
            {
                "title": title,
                "summary": summary,
                "url": url,
                "published": published,
                "published_ts": _parse_published_ts(published),
                "source": source,
            }
        )
    return parsed


def _clean_xml_text(value: str | None) -> str:
    text = re.sub(r"<[^>]+>", " ", str(value or ""))
    return re.sub(r"\s+", " ", text).strip()


def _parse_published_ts(value: str) -> float:
    try:
        parsed = parsedate_to_datetime(value)
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)
        return parsed.timestamp()
    except Exception:
        return 0.0


def _filter_news_items(items: list[dict], query: str) -> list[dict]:
    terms = _important_terms(query)
    if not terms:
        return items[:6]
    scored = []
    for item in items:
        haystack = _normalize(f"{item.get('title', '')} {item.get('summary', '')} {item.get('source', '')}")
        score = sum(1 for term in terms if term in haystack)
        if score:
            scored.append((score, item.get("published_ts") or 0, item))
    if scored:
        scored.sort(key=lambda row: (row[0], row[1]), reverse=True)
        return [row[2] for row in scored[:6]]
    return items[:6]


def _important_terms(query: str) -> list[str]:
    stop_words = {
        "what",
        "whats",
        "what's",
        "the",
        "with",
        "about",
        "today",
        "latest",
        "current",
        "right",
        "now",
        "score",
        "scores",
        "news",
        "match",
        "result",
        "results",
        "tell",
        "me",
    }
    words = re.findall(r"[a-z0-9]+", query.lower())
    return [word for word in words if len(word) > 2 and word not in stop_words][:8]


def _get_sports_items(query_info: dict) -> list[dict]:
    search_text = str(query_info.get('search_text') or '').strip()
    if not search_text:
        return []

    cache_key = f'sports:{search_text.lower()[:120]}'
    now = time.time()
    cached = _sports_cache.get(cache_key)
    if cached and cached['expires_at'] > now:
        return list(cached['items'])

    items = []
    if query_info.get('source') == 'espn_fifa_world':
        items.extend(_sports_by_espn_fifa_world(query_info))
    items.extend(_sports_by_event_search(search_text))
    items.extend(_sports_by_team_search(query_info))
    items.extend(_sports_by_known_league(search_text.lower()))
    items.extend(_sports_by_today(search_text.lower()))
    items = _dedupe_sports_items(items)
    _sports_cache[cache_key] = {'expires_at': now + SPORTS_CACHE_TTL_SECONDS, 'items': items[:12]}
    return list(_sports_cache[cache_key]['items'])


def _sports_get(path: str, params: dict) -> dict:
    try:
        text = _fetch_text(f"{SPORTSDB_BASE_URL}/{path}", params=params)
        return json.loads(text)
    except Exception:
        return {}


def _fetch_json(url: str, params: dict | None = None) -> dict:
    try:
        text = _fetch_text(url, params=params or {})
        parsed = json.loads(text)
        return parsed if isinstance(parsed, dict) else {}
    except Exception:
        return {}


def _sports_by_espn_fifa_world(query_info: dict) -> list[dict]:
    try:
        round_label = str(query_info.get("round_label") or "").strip()
        date_range = FIFA_WORLD_CUP_2026_STAGE_DATES.get(round_label)
        params = {"dates": date_range} if date_range else None
        data = _fetch_json(ESPN_FIFA_WORLD_SCOREBOARD_URL, params=params)
        events = data.get('events') or []
        items = _extract_espn_events(events)
        return _filter_espn_world_cup_items(items, query_info)
    except Exception:
        return []


def _sports_by_event_search(query: str) -> list[dict]:
    data = _sports_get("searchevents.php", {"e": query})
    return _extract_events(data.get("event") or [])


def _sports_by_team_search(query_info: dict) -> list[dict]:
    terms = list(query_info.get('team_candidates') or [])
    items = []
    for term in terms[:4]:
        data = _sports_get('searchteams.php', {'t': term})
        teams = data.get('teams') or []
        for team in teams[:2]:
            team_id = team.get('idTeam')
            if not team_id:
                continue
            last_events = _sports_get('eventslast.php', {'id': team_id}).get('results') or []
            next_events = _sports_get('eventsnext.php', {'id': team_id}).get('events') or []
            items.extend(_extract_events(last_events[:3] + next_events[:3]))
    return items


def _sports_by_known_league(query: str) -> list[dict]:
    items = []
    for keyword, league_id in POPULAR_LEAGUES.items():
        if keyword not in query:
            continue
        season = _guess_season()
        data = _sports_get("eventsseason.php", {"id": league_id, "s": season})
        events = data.get("events") or []
        items.extend(_nearby_events(events))
    return items


def _sports_by_today(query: str) -> list[dict]:
    if not any(word in query for word in ("today", "right now", "latest", "tonight")):
        return []
    items = []
    for sport in ("Soccer", "Cricket", "Basketball", "Tennis"):
        data = _sports_get("eventsday.php", {"d": datetime.now(timezone.utc).date().isoformat(), "s": sport})
        items.extend(_extract_events((data.get("events") or [])[:5]))
    return items


def _clean_sports_query(query: str) -> dict:
    cleaned = _normalize(query)
    for phrase in SPORTS_FILLER_PHRASES:
        cleaned = cleaned.replace(phrase, ' ')
    cleaned = re.sub(r'\bwc\b', 'world cup', cleaned)
    cleaned = re.sub(r'[^a-z0-9\s]', ' ', cleaned)
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()

    alias_label = ''
    for pattern, label in TOURNAMENT_ALIASES:
        if pattern.search(cleaned):
            alias_label = label
            break

    round_label = ''
    round_match = re.search(r'\bround\s+(?:of\s+)?(\d+)\b', cleaned)
    if round_match:
        round_label = f'Round of {round_match.group(1)}'

    elif "group stage" in cleaned or re.search(r"\bgroup\b", cleaned):
        round_label = "Group Stage"
    elif re.search(r"\bquarter[\s-]?finals?\b", cleaned) or re.search(r"\bqf\b", cleaned):
        round_label = "Quarterfinals"
    elif re.search(r"\bsemi[\s-]?finals?\b", cleaned) or re.search(r"\bsf\b", cleaned):
        round_label = "Semifinals"
    elif re.search(r"\bthird[\s-]?place\b", cleaned) or re.search(r"\b3rd[\s-]?place\b", cleaned):
        round_label = "Third-place Match"
    elif re.search(r"\bfinals?\b", cleaned):
        round_label = "Final"

    words = [word for word in cleaned.split() if len(word) > 1 and word not in SPORTS_INTENT_WORDS]
    if alias_label:
        search_text = ' '.join(part for part in [alias_label, round_label] if part).strip()
        competition_only = True
    else:
        search_text = ' '.join(words[:6]).strip()
        competition_only = any(word in cleaned for word in ('league', 'cup', 'tournament', 'qualifier'))

    return {
        'search_text': search_text,
        'label': ' '.join(part for part in [alias_label or search_text, round_label] if part).strip(),
        'source': 'espn_fifa_world' if alias_label == 'FIFA World Cup' else 'sportsdb',
        'round_label': round_label,
        'team_candidates': [] if competition_only else _sports_team_candidates_from_words(words),
    }


def _sports_team_candidates_from_words(words: list[str]) -> list[str]:
    candidates = []
    if words:
        candidates.append(' '.join(words[:4]))
    for size in (3, 2, 1):
        for index in range(0, max(0, len(words) - size + 1)):
            candidates.append(' '.join(words[index : index + size]))
    return [candidate for candidate in dict.fromkeys(candidates) if candidate]


def _describe_live_request(query: str, wants_sports: bool, wants_news: bool) -> str:
    if wants_sports:
        cleaned = _clean_sports_query(query)
        label = str(cleaned.get('label') or cleaned.get('search_text') or '').strip()
        if label:
            if any(word in query for word in ('score', 'scores')):
                return f'{label} scores'
            if any(word in query for word in ('fixture', 'fixtures')):
                return f'{label} fixtures'
            return f'{label} results'
        return 'sports results'
    if wants_news:
        terms = _important_terms(query)
        return (' '.join(terms[:4]) + ' updates').strip() if terms else 'current updates'
    return 'live updates'


def _guess_season() -> str:
    now = datetime.now(timezone.utc)
    if now.month >= 7:
        return f"{now.year}-{now.year + 1}"
    return f"{now.year - 1}-{now.year}"


def _nearby_events(events: list[dict]) -> list[dict]:
    today = datetime.now(timezone.utc).date()
    scored = []
    for event in events:
        event_date = _parse_event_date(event)
        if event_date is None:
            distance = 999
        else:
            distance = abs((event_date - today).days)
        scored.append((distance, event))
    scored.sort(key=lambda row: row[0])
    return _extract_events([row[1] for row in scored[:8]])


def _extract_events(events: list[dict]) -> list[dict]:
    parsed = []
    for event in events:
        if not isinstance(event, dict):
            continue
        home = event.get("strHomeTeam") or ""
        away = event.get("strAwayTeam") or ""
        name = event.get("strEvent") or " vs ".join(part for part in [home, away] if part)
        if not name:
            continue
        parsed.append(
            {
                "id": event.get("idEvent") or name,
                "event": name,
                "league": event.get("strLeague") or "",
                "date": event.get("dateEvent") or "",
                "time": event.get("strTime") or "",
                "home": home,
                "away": away,
                "home_score": event.get("intHomeScore"),
                "away_score": event.get("intAwayScore"),
                "status": event.get("strStatus") or "",
                "sport": event.get("strSport") or "",
            }
        )
    return parsed


def _extract_espn_events(events: list[dict]) -> list[dict]:
    parsed = []
    for event in events:
        if not isinstance(event, dict):
            continue
        competitions = event.get('competitions') or []
        competition = competitions[0] if competitions and isinstance(competitions[0], dict) else {}
        competitors = competition.get('competitors') or []
        home = {}
        away = {}
        for competitor in competitors:
            if not isinstance(competitor, dict):
                continue
            side = str(competitor.get('homeAway') or '').lower()
            if side == 'home':
                home = competitor
            elif side == 'away':
                away = competitor
        if not home and competitors:
            home = competitors[0] if isinstance(competitors[0], dict) else {}
        if not away and len(competitors) > 1:
            away = competitors[1] if isinstance(competitors[1], dict) else {}

        home_team = home.get('team') or {}
        away_team = away.get('team') or {}
        home_name = home_team.get('displayName') or home_team.get('shortDisplayName') or home_team.get('name') or ''
        away_name = away_team.get('displayName') or away_team.get('shortDisplayName') or away_team.get('name') or ''
        event_name = event.get('name') or event.get('shortName') or ' vs '.join(part for part in [away_name, home_name] if part)
        if not event_name:
            continue

        status_block = competition.get('status') or event.get('status') or {}
        status_type = status_block.get('type') or {}
        status = status_type.get('description') or status_type.get('name') or status_block.get('displayClock') or ''
        stage = _extract_espn_stage(event, competition)
        parsed.append({
            'id': event.get('id') or event_name,
            'event': event_name,
            'league': 'FIFA World Cup',
            'date': str(event.get('date') or '')[:10],
            'time': str(event.get('date') or '')[11:19],
            'home': home_name,
            'away': away_name,
            'home_score': home.get('score'),
            'away_score': away.get('score'),
            'status': status,
            'sport': 'Soccer',
            'stage': stage,
        })
    return parsed


def _extract_espn_stage(event: dict, competition: dict) -> str:
    notes = competition.get('notes') if isinstance(competition, dict) else []
    first_note = notes[0] if isinstance(notes, list) and notes and isinstance(notes[0], dict) else {}
    candidates = []
    for source, key in ((event.get('season'), 'slug'), (event.get('season'), 'displayName'), (event.get('week'), 'text'), (event.get('group'), 'name')):
        if isinstance(source, dict):
            candidates.append(source.get(key))
    candidates.extend([
        competition.get("altGameNote") if isinstance(competition, dict) else None,
        first_note.get("headline"),
        event.get("name"),
        event.get("shortName"),
    ])
    return re.sub(r'\s+', ' ', ' '.join(str(item or '') for item in candidates)).strip()


def _filter_espn_world_cup_items(items: list[dict], query_info: dict) -> list[dict]:
    round_label = _normalize(query_info.get('round_label') or '')
    if not round_label:
        return items
    round_label = round_label.replace("-", " ")
    round_number = "".join(re.findall(r"\d+", round_label))
    filtered = []
    for item in items:
        haystack = _normalize("{} {} {}".format(item.get("stage", ""), item.get("event", ""), item.get("status", ""))).replace("-", " ")
        number_match = bool(round_number) and (
            "round of {}".format(round_number) in haystack
            or "round {}".format(round_number) in haystack
        )
        if round_label in haystack or number_match:
            filtered.append(item)
    return filtered


def _parse_event_date(event: dict):
    try:
        value = event.get("dateEvent")
        return datetime.strptime(value, "%Y-%m-%d").date() if value else None
    except Exception:
        return None


def _dedupe_sports_items(items: list[dict]) -> list[dict]:
    seen = set()
    deduped = []
    for item in items:
        key = str(item.get("id") or item.get("event") or "").lower()
        if not key or key in seen:
            continue
        seen.add(key)
        deduped.append(item)
    return deduped


def _format_sports_item(item: dict) -> str:
    score = ""
    if item.get("home_score") is not None and item.get("away_score") is not None:
        score = f" Score: {item.get('home')} {item.get('home_score')} - {item.get('away_score')} {item.get('away')}."
    date_bits = " ".join(part for part in [item.get("date"), item.get("time")] if part).strip()
    status = f" Status: {item.get('status')}." if item.get("status") else ""
    league = f" [{item.get('league')}]" if item.get("league") else ""
    stage = f" {item.get('stage')}." if item.get("stage") else ""
    date_text = f" {date_bits}." if date_bits else ""
    return f"- {item.get('event')}{league}.{stage}{date_text}{score}{status}"


def _format_news_item(item: dict) -> str:
    summary = f" - {item.get('summary')}" if item.get("summary") else ""
    published = f" ({item.get('published')})" if item.get("published") else ""
    return f"- {item.get('title')} [{item.get('source')}]{published}{summary}"


def _dedupe_sources(sources: list[dict]) -> list[dict]:
    seen = set()
    deduped = []
    for source in sources:
        key = source.get("url") or source.get("label")
        if not key or key in seen:
            continue
        seen.add(key)
        deduped.append(source)
    return deduped[:8]
