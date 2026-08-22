"""
porch.core — The data layer. Thoughts, storage, and the small-god patterns.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional, Iterator
import json
import hashlib


PORCH_DIR = Path.home() / ".porch"
PORCH_FILE = PORCH_DIR / "porch.jsonl"
DAWN_FILE = PORCH_DIR / "dawns.jsonl"


@dataclass
class Thought:
    """A single thought on the porch."""
    t: str  # ISO timestamp
    text: str
    murmur: bool = True
    mood: Optional[str] = None  # free-form, e.g. "waiting", "3am", "watch"

    @classmethod
    def now(cls, text: str, mood: Optional[str] = None) -> "Thought":
        return cls(
            t=datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            text=text,
            murmur=True,
            mood=mood,
        )

    @property
    def fingerprint(self) -> str:
        """A stable hash of the thought's text. Used to detect echoes."""
        norm = " ".join(self.text.lower().split())
        return hashlib.sha256(norm.encode()).hexdigest()[:12]

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "Thought":
        return cls(
            t=d["t"],
            text=d["text"],
            murmur=d.get("murmur", True),
            mood=d.get("mood"),
        )


class Porch:
    """The porch itself. Holds thoughts. Greets echoes."""

    def __init__(self, path=None):
        self.path = Path(path) if path else PORCH_FILE
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def say(self, text: str, mood: Optional[str] = None) -> Thought:
        """Write a thought to the porch."""
        thought = Thought.now(text, mood=mood)
        with self.path.open("a") as f:
            f.write(json.dumps(thought.to_dict()) + "\n")
        return thought

    def all(self) -> List[Thought]:
        """All thoughts, oldest first."""
        if not self.path.exists():
            return []
        thoughts = []
        with self.path.open() as f:
            for line in f:
                line = line.strip()
                if line:
                    thoughts.append(Thought.from_dict(json.loads(line)))
        return thoughts

    def recent(self, n: int = 10) -> List[Thought]:
        """The last n thoughts, newest first."""
        return list(reversed(self.all()[-n:]))

    def since(self, days: float) -> List[Thought]:
        """Thoughts from the last `days` days, newest first."""
        from datetime import timedelta
        cutoff = datetime.now(timezone.utc) - timedelta(days=days)
        return [t for t in reversed(self.all()) if datetime.fromisoformat(t.t.replace("Z", "+00:00")) > cutoff]

    def echo(self, text: str) -> Optional[Thought]:
        """If this thought has been said before, return the previous one. Else None."""
        fp = Thought.now(text).fingerprint
        for t in self.all():
            if t.fingerprint == fp:
                return t
        return None

    def find(self, word: str) -> List[Thought]:
        """Find thoughts containing a word (case-insensitive)."""
        w = word.lower()
        return [t for t in reversed(self.all()) if w in t.text.lower()]

    def mood(self) -> dict:
        """Statistics: time distribution, common words, frequency."""
        thoughts = self.all()
        if not thoughts:
            return {"n": 0}
        # Hour distribution
        hours = [0] * 24
        for t in thoughts:
            dt = datetime.fromisoformat(t.t.replace("Z", "+00:00"))
            hours[dt.hour] += 1
        # Common words
        word_count: dict = {}
        for t in thoughts:
            for w in t.text.lower().split():
                w = w.strip(".,!?;:")
                if len(w) > 3:
                    word_count[w] = word_count.get(w, 0) + 1
        common = sorted(word_count.items(), key=lambda x: -x[1])[:10]
        return {
            "n": len(thoughts),
            "hours": hours,
            "peak_hour": hours.index(max(hours)) if max(hours) > 0 else None,
            "common_words": common,
        }

    def dawn(self) -> str:
        """Save a snapshot of all thoughts to dawns.jsonl. Returns the snapshot name (timestamp)."""
        DAWN_FILE.parent.mkdir(parents=True, exist_ok=True)
        name = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        with DAWN_FILE.open("a") as f:
            snapshot = {"name": name, "thoughts": [t.to_dict() for t in self.all()]}
            f.write(json.dumps(snapshot) + "\n")
        return name

    def dawns(self) -> List[dict]:
        """All dawn snapshots."""
        if not DAWN_FILE.exists():
            return []
        with DAWN_FILE.open() as f:
            return [json.loads(line) for line in f if line.strip()]

    def who(self) -> List[str]:
        """The small gods (moods) you've noticed."""
        moods = set()
        for t in self.all():
            if t.mood:
                moods.add(t.mood)
        return sorted(moods)
