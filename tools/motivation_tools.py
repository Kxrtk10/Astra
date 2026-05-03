import json
import random
from datetime import date
from pathlib import Path


MOTIVATION_ROOT = Path("app_data") / "motivation"
QUOTES_PATH = MOTIVATION_ROOT / "quotes.json"
BOOSTS_PATH = MOTIVATION_ROOT / "boosts.json"
STORIES_PATH = MOTIVATION_ROOT / "stories.json"

DEFAULT_QUOTES = [
    "Consistency is the hidden chapter every JEE topper studies.",
    "A tough day is still a day of progress if you showed up.",
    "Small concepts mastered well become huge scores later.",
    "Focus on the next problem, not the entire mountain.",
    "Your pace matters less than your consistency.",
    "Revision is where confidence stops being a feeling and becomes a skill.",
    "A clear mind and one honest study block can change the day.",
    "The students who improve most are the ones who keep returning.",
    "One neat solution is worth ten rushed attempts.",
    "You do not need perfect energy to make real progress.",
    "The exam rewards the learner who stays steady under pressure.",
    "Every strong rank starts with ordinary days done well.",
    "Learn the concept once, then sharpen it again tomorrow.",
    "The habit of returning to work is a superpower.",
    "You are closer than yesterday because you are still here.",
    "Deep understanding beats noisy effort every time.",
    "Your preparation grows when you protect your attention.",
    "The most valuable study session is the one you actually complete.",
    "Momentum is built by repeating small wins with patience.",
    "One honest mistake corrected today becomes one less mistake tomorrow.",
    "Great prep is not dramatic; it is dependable.",
    "Let the hard problem teach you, not discourage you.",
    "Every formula becomes easier when the idea behind it is clear.",
    "A focused hour is better than a distracted afternoon.",
    "You can recover from a bad day with the next good decision.",
    "The path forward is built one solved doubt at a time.",
    "Calm effort often outruns panic.",
    "Astra believes in the student who keeps trying again.",
    "The next chapter starts whenever you do.",
    "The best comeback begins with one small restart.",
]

DEFAULT_BOOSTS = [
    "You studied today. That already makes you better than yesterday.",
    "One concept at a time.",
    "Every JEE topper was once exactly where you are.",
    "Consistency beats talent every single time.",
    "Do not chase perfection. Chase clarity.",
    "A short session still counts if you stay honest with it.",
    "The next improvement is always smaller than it feels.",
    "You do not need to feel ready to begin.",
    "Your brain learns best when you return after a pause.",
    "Tiny wins build big confidence.",
    "The first step is often the hardest one.",
    "Slow and clear beats fast and confused.",
    "One clean revision can save ten future mistakes.",
    "If today was messy, tomorrow can still be excellent.",
    "You are allowed to take your learning one block at a time.",
    "Progress is progress, even when it feels quiet.",
    "Every corrected doubt strengthens the next answer.",
    "The work you do now is still working for you later.",
    "A focused restart is powerful.",
    "Keep the pace gentle, but keep it moving.",
]

DEFAULT_STORIES = [
    {
        "title": "The Student Who Failed Two Mocks and Still Made It",
        "tags": ["failure", "comeback", "mocks"],
        "story": (
            "In the first half of the year, Riya looked like the kind of student who should already be thriving. "
            "Her notebooks were organized, her timetable was neat, and she never missed a class. Then mock test season arrived and the scores were brutal. "
            "Two papers in a row came back lower than she had ever imagined. The first reaction was embarrassment. The second was silence. "
            "She stopped posting updates, stopped talking about ranks, and almost convinced herself that maybe she was not built for this exam. "
            "What changed was not a miracle. A mentor helped her stop reading the score as a verdict and start reading it as data. "
            "She wrote down every wrong answer by topic, not by emotion. Projectile motion, electrostatics, and a few algebra sections kept appearing in the error log. "
            "Instead of doing more of everything, she did less but better. She revised one weak concept every day, solved fewer problems but checked each one properly, and rebuilt her confidence through small proofs of progress. "
            "Three months later the same student who feared the score report was calmly explaining her mistakes to a friend and lifting her average by a huge margin. "
            "The comeback was not loud. It was disciplined."
        ),
    },
    {
        "title": "The Student Managing Anxiety in Silence",
        "tags": ["mental health", "anxiety", "support"],
        "story": (
            "Arjun was the student who always said, 'I am fine.' He said it when he was behind on chapters, when his sleep was broken, and when he had not felt calm in weeks. "
            "From the outside he looked ordinary: a little tired, a little quiet, still showing up. Inside, the pressure had started to blur everything. "
            "He could read a physics solution and forget the first line by the second paragraph. He would open chemistry and feel his chest tighten for reasons he could not explain. "
            "One evening he admitted the truth to a senior: he was not lazy, he was overloaded. That sentence changed the way he studied. "
            "He stopped pretending he needed to work for ten hours straight. He built smaller blocks, added breaks on purpose, and began every session by writing one sentence: 'Today I only need to finish this one piece.' "
            "The result was not instant genius. It was relief. A lighter schedule made it easier to think, and better thinking made the score climb. "
            "He learned that mental health was not a side topic. It was part of exam preparation itself. Once he protected that, everything else became more possible."
        ),
    },
    {
        "title": "A Comeback After Financial Pressure",
        "tags": ["financial hardship", "support", "comeback"],
        "story": (
            "Meera's preparation did not happen in a perfectly supported home. Her family handled every rupee carefully, and every new book or test series felt like a decision, not a purchase. "
            "There were weeks when she shared a single old desk with her younger brother and studied under a lamp that flickered at night. She knew what it meant to worry about fees while also worrying about formulas. "
            "What made her story powerful was that she never turned hardship into a dramatic speech. She turned it into structure. She used free resources, borrowed notes when needed, and built a system that did not depend on expensive noise. "
            "She studied one chapter deeply instead of collecting ten half-finished ones. When she could not afford more mock tests, she repeated the same papers and analyzed them more carefully each time. "
            "That carefulness became her edge. While others chased endless material, she turned limited resources into high-quality revision. "
            "When her score finally rose, it was not because the road became easy. It was because she learned how to make small resources work hard. "
            "Her confidence came from proof that effort can be intelligent, not just intense."
        ),
    },
    {
        "title": "The Last-Minute Rescue Run",
        "tags": ["last minute", "revision", "focus"],
        "story": (
            "Soham had the kind of week every student fears. A family function, a missed revision block, two weak chapters, and a practice paper that looked worse than expected. "
            "He had less time than he wanted and more anxiety than he could comfortably hold. Instead of panicking, he made a rescue list. "
            "He did not try to revise everything. He selected only the highest-yield formulas, the most repeated concepts, and the one or two topics that showed up in his wrong-answer log again and again. "
            "Each morning started with a short recall test. Each evening ended with a one-page summary. He stopped chasing perfection and started chasing recall speed. "
            "The strange thing about last-minute prep is that when you become very clear about what matters, your brain can work better than expected. "
            "Soham's final test week was not magical, but it was disciplined. He entered the room with a smaller list and a calmer mind. "
            "The rescue did not come from cramming more. It came from cutting the noise and protecting the essentials."
        ),
    },
    {
        "title": "The Repeater Who Finally Found Rhythm",
        "tags": ["repeater", "growth", "rhythm"],
        "story": (
            "Kabir repeated the year, and he hated hearing that label attached to him. For a long time he believed that one difficult result had become his identity. "
            "The first months were uncomfortable because he kept comparing himself to batchmates who seemed faster, brighter, and more certain. That comparison made him rush, and rushing made him careless. "
            "A good teacher helped him replace shame with routine. He started studying at the same hour every day, revised the same mistakes every week, and tracked the chapters where he used to panic. "
            "The real turning point was that he stopped treating repetition as proof of failure. He started treating it as proof that he had another year to learn deeply. "
            "He became calmer in questions that once scared him. He also became kinder to himself when a day went badly. That kindness was not softness. It was stability. "
            "By the time test season arrived, he was not trying to prove he had never failed. He was proving he had learned how to recover. "
            "That mindset made all the difference."
        ),
    },
    {
        "title": "The Quiet Student Who Kept Improving",
        "tags": ["quiet progress", "discipline", "confidence"],
        "story": (
            "Nobody called Naina the brightest student in the room. She did not dominate discussions, and she rarely announced big goals. "
            "What she did have was an almost stubborn habit of returning to the work. She reviewed her errors, asked short questions, and refused to let a topic remain fuzzy for long. "
            "At first the progress felt invisible. Her friends talked about big jumps while her own improvement looked like a few marks here and there. "
            "Then the small gains started to stack. A formula sheet became easier to recall. A chemistry mechanism stopped feeling random. A calculus problem that once looked impossible began to feel manageable. "
            "Her confidence did not come from one dramatic score. It came from watching confusion get replaced by clarity again and again. "
            "By the end of the cycle, she had become the kind of student everyone trusts: steady, prepared, and hard to shake."
        ),
    },
    {
        "title": "The Student Who Recovered After Burnout",
        "tags": ["burnout", "recovery", "balance"],
        "story": (
            "At one point, Dev thought the only way to succeed was to push harder every single day. He kept adding hours, more practice sets, more notes, more pressure. "
            "For a while it looked productive, but eventually his attention cracked. He was reading without absorbing, solving without understanding, and sleeping with his phone still open to revision apps. "
            "When burnout hit, he did the uncomfortable thing: he paused. He reduced the noise, cut the least useful tasks, and rebuilt the day around a few honest priorities. "
            "He studied in smaller sessions, took real breaks, and started tracking energy along with marks. "
            "That new balance did not lower his ambition. It made his ambition sustainable. The next months were calmer, the answers were cleaner, and the revision actually stuck. "
            "He learned that recovery is not time wasted. Recovery is what lets the learning return."
        ),
    },
    {
        "title": "The Student Who Started Late and Still Caught Up",
        "tags": ["late start", "catch up", "hope"],
        "story": (
            "Aditi began seriously preparing later than most of her batch. For the first few weeks she felt like she was constantly behind, chasing a train that had already left. "
            "What saved her was honesty. She stopped pretending she had the same starting point and made a catch-up plan that was small enough to survive real life. "
            "Instead of trying to study every topic at once, she focused on the chapters with the highest score return. She learned the core ideas first, then the common question types, then the traps. "
            "She used short, repeated revision sessions and kept one weekly checkpoint for progress. Slowly the panic faded. The backlog was still there, but it no longer owned her. "
            "By the final stretch, she was no longer the student apologizing for being late. She was the student who had learned how to close gaps intelligently."
        ),
    },
]


def _load_json(path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default


def _write_json(path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def ensure_motivation_store():
    MOTIVATION_ROOT.mkdir(parents=True, exist_ok=True)
    if not QUOTES_PATH.exists():
        _write_json(QUOTES_PATH, {"quotes": list(DEFAULT_QUOTES)})
    if not BOOSTS_PATH.exists():
        _write_json(BOOSTS_PATH, {"boosts": list(DEFAULT_BOOSTS)})
    if not STORIES_PATH.exists():
        _write_json(STORIES_PATH, {"stories": list(DEFAULT_STORIES)})


def load_quotes():
    ensure_motivation_store()
    data = _load_json(QUOTES_PATH, {"quotes": list(DEFAULT_QUOTES)})
    quotes = data.get("quotes", [])
    return quotes if isinstance(quotes, list) and quotes else list(DEFAULT_QUOTES)


def load_boosts():
    ensure_motivation_store()
    data = _load_json(BOOSTS_PATH, {"boosts": list(DEFAULT_BOOSTS)})
    boosts = data.get("boosts", [])
    return boosts if isinstance(boosts, list) and boosts else list(DEFAULT_BOOSTS)


def load_stories():
    ensure_motivation_store()
    data = _load_json(STORIES_PATH, {"stories": list(DEFAULT_STORIES)})
    stories = data.get("stories", [])
    return stories if isinstance(stories, list) and stories else list(DEFAULT_STORIES)


def get_daily_motivation():
    quotes = load_quotes()
    boosts = load_boosts()
    today = date.today()
    seed = today.toordinal()
    quote = quotes[seed % len(quotes)] if quotes else ""
    randomizer = random.Random(seed ^ 0xA5A5A5A5)
    boost_tokens = randomizer.sample(boosts, k=min(3, len(boosts))) if boosts else []
    return {
        "date": today.isoformat(),
        "quote": quote,
        "boost_tokens": boost_tokens,
        "quote_index": seed % len(quotes) if quotes else 0,
    }


def get_all_stories():
    return load_stories()


def get_story_by_index(index):
    stories = load_stories()
    if not stories:
        return None
    if index < 0 or index >= len(stories):
        return None
    return stories[index]
