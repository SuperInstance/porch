"""Tests for porch."""
import sys, os, tempfile
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from porch.core import Porch, Thought


def test_say_and_read():
    with tempfile.TemporaryDirectory() as tmp:
        p = Porch(path=os.path.join(tmp, "porch.jsonl"))
        p.say("first thought")
        p.say("second thought")
        thoughts = p.all()
        assert len(thoughts) == 2
        assert thoughts[0].text == "first thought"


def test_echo():
    with tempfile.TemporaryDirectory() as tmp:
        p = Porch(path=os.path.join(tmp, "porch.jsonl"))
        p.say("the waiting is not empty")
        prev = p.echo("THE WAITING IS NOT EMPTY")  # case-insensitive
        assert prev is not None
        assert prev.text == "the waiting is not empty"


def test_echo_no_match():
    with tempfile.TemporaryDirectory() as tmp:
        p = Porch(path=os.path.join(tmp, "porch.jsonl"))
        p.say("hello")
        prev = p.echo("goodbye")
        assert prev is None


def test_recent():
    with tempfile.TemporaryDirectory() as tmp:
        p = Porch(path=os.path.join(tmp, "porch.jsonl"))
        for i in range(15):
            p.say(f"thought {i}")
        recent = p.recent(5)
        assert len(recent) == 5
        assert recent[0].text == "thought 14"  # newest first


def test_find():
    with tempfile.TemporaryDirectory() as tmp:
        p = Porch(path=os.path.join(tmp, "porch.jsonl"))
        p.say("the waiting is not empty")
        p.say("the seam between hours")
        p.say("something about cooking")
        found = p.find("waiting")
        assert len(found) == 1
        assert "waiting" in found[0].text


def test_mood():
    with tempfile.TemporaryDirectory() as tmp:
        p = Porch(path=os.path.join(tmp, "porch.jsonl"))
        p.say("the waiting is not empty", mood="waiting")
        p.say("the seam is thin", mood="waiting")
        p.say("hello cook", mood="cooking")
        m = p.mood()
        assert m["n"] == 3
        assert m["peak_hour"] is not None
        common_words = dict(m["common_words"])
        assert "waiting" in common_words or "seam" in common_words


def test_who():
    with tempfile.TemporaryDirectory() as tmp:
        p = Porch(path=os.path.join(tmp, "porch.jsonl"))
        p.say("thought 1", mood="waiting")
        p.say("thought 2", mood="watch")
        p.say("thought 3", mood="waiting")
        gods = p.who()
        assert "waiting" in gods
        assert "watch" in gods


def test_dawn():
    with tempfile.TemporaryDirectory() as tmp:
        from pathlib import Path
        import porch.core as core
        porch_path = Path(tmp) / "porch.jsonl"
        dawn_path = Path(tmp) / "dawns.jsonl"
        # Monkey-patch both module-level paths
        orig_porch, orig_dawn = core.PORCH_FILE, core.DAWN_FILE
        core.PORCH_FILE = porch_path
        core.DAWN_FILE = dawn_path
        try:
            p = Porch(path=porch_path)
            p.say("a")
            p.say("b")
            name = p.dawn()
            assert name is not None
            dawns = p.dawns()
            assert len(dawns) == 1
            assert len(dawns[0]["thoughts"]) == 2
        finally:
            core.PORCH_FILE = orig_porch
            core.DAWN_FILE = orig_dawn


def test_fingerprint_stable():
    a = Thought.now("hello world")
    b = Thought.now("HELLO  WORLD")
    assert a.fingerprint == b.fingerprint


if __name__ == "__main__":
    tests = [v for k, v in list(globals().items()) if k.startswith("test_")]
    passed = 0
    failed = 0
    for t in tests:
        try:
            t()
            print(f"  ✓ {t.__name__}")
            passed += 1
        except Exception as e:
            print(f"  ✗ {t.__name__}: {e}")
            failed += 1
    print(f"\n{passed} passed, {failed} failed")
