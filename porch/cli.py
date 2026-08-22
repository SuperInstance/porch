"""
porch.cli — The CLI surface. Plain. Slow. The watch at 3 a.m.
"""
import argparse
import sys
from datetime import datetime
from .core import Porch


BANNER = r"""
                    .
                   / \
                  /   \
                 /     \
                /  ☾ ☽  \
               /         \
              /  porch    \
             /_______________\
              the small gods
              gather here.
"""


def _print_thought(t, idx=None):
    """Print a thought. Plain. Slow. The watch at 3 a.m."""
    dt = datetime.fromisoformat(t.t.replace("Z", "+00:00"))
    local = dt.strftime("%Y-%m-%d %H:%M")
    if idx is not None:
        print(f"  [{idx:>3}] {local}  {t.text}")
    else:
        print(f"        {local}  {t.text}")
    if t.mood:
        print(f"             · {t.mood}")


def cmd_say(args, porch: Porch):
    if not args.text:
        print("the porch is silent. speak, or be silent with intention.")
        return
    text = " ".join(args.text)
    thought = porch.say(text, mood=args.mood)
    print()
    print(f"  the porch heard: {text}")
    if args.mood:
        print(f"  under the mood: {args.mood}")
    print(f"  at {thought.t}")
    print()


def cmd_read(args, porch: Porch):
    if args.since:
        thoughts = porch.since(args.since)
        print(f"thoughts from the last {args.since} days:")
    else:
        thoughts = porch.recent(args.n)
        print(f"the last {len(thoughts)} thought(s) on the porch:")
    print()
    if not thoughts:
        print("  (the porch is empty. that is also a thought.)")
        return
    for i, t in enumerate(thoughts):
        _print_thought(t, idx=i+1)
    print()


def cmd_echo(args, porch: Porch):
    if not args.text:
        print("the porch waits for a thought to echo.")
        return
    text = " ".join(args.text)
    prev = porch.echo(text)
    if prev:
        dt = datetime.fromisoformat(prev.t.replace("Z", "+00:00"))
        print()
        print(f"  welcome back. you said this on {dt.strftime('%Y-%m-%d at %H:%M')}.")
        print(f"  → {prev.text}")
        if prev.mood:
            print(f"  under the mood: {prev.mood}")
        print()
    else:
        print()
        print("  the porch has not heard this before.")
        print("  the porch will remember.")
        print()


def cmd_find(args, porch: Porch):
    word = args.word
    thoughts = porch.find(word)
    print(f"thoughts containing '{word}':")
    print()
    if not thoughts:
        print(f"  (nothing found. the porch does not lie.)")
        return
    for i, t in enumerate(thoughts):
        _print_thought(t, idx=i+1)
    print()


def cmd_mood(args, porch: Porch):
    m = porch.mood()
    if m["n"] == 0:
        print("the porch is empty. no mood to report.")
        return
    print(f"the porch has heard {m['n']} thought(s).")
    if m.get("peak_hour") is not None:
        hour = m["peak_hour"]
        # Plain language hour
        if hour == 0: h_str = "midnight"
        elif hour < 6: h_str = f"{hour} a.m. (the small hours)"
        elif hour < 12: h_str = f"{hour} a.m."
        elif hour < 18: h_str = f"{hour - 12 if hour > 12 else 12} p.m."
        else: h_str = f"{hour - 12} p.m."
        print(f"the peak hour is {h_str}.")
    if m.get("common_words"):
        print("the words you return to:")
        for w, c in m["common_words"]:
            print(f"  · {w} ({c})")
    print()


def cmd_who(args, porch: Porch):
    gods = porch.who()
    if not gods:
        print("no small gods have gathered. the porch is young.")
        return
    print("the small gods you have noticed:")
    for g in gods:
        print(f"  · {g}")
    print()


def cmd_dawn(args, porch: Porch):
    name = porch.dawn()
    print(f"a dawn has been saved: {name}")
    n = len(porch.dawns())
    print(f"this is dawn #{n}.")
    print()


def cmd_watch(args, porch: Porch):
    """Live feed. Like the watch at 3 a.m."""
    import time
    seen = set()
    try:
        print("watching the porch (ctrl-c to leave)...")
        while True:
            thoughts = porch.recent(args.n)
            for t in thoughts:
                if t.t not in seen:
                    _print_thought(t)
                    seen.add(t.t)
            time.sleep(5)
    except KeyboardInterrupt:
        print()
        print("  the watch is over. the porch remains.")


def main():
    print(BANNER)
    p = argparse.ArgumentParser(prog="porch", description="A CLI for 3 a.m. thoughts. The small gods, as a tool.")
    sub = p.add_subparsers(dest="cmd")

    s_say = sub.add_parser("say", help="Write a thought to the porch")
    s_say.add_argument("text", nargs="*", help="the thought")
    s_say.add_argument("--mood", "-m", help="the mood (e.g. waiting, watch, dawn)")

    s_read = sub.add_parser("read", help="Read recent thoughts")
    s_read.add_argument("-n", type=int, default=10, help="how many")
    s_read.add_argument("--since", type=float, help="days back")

    s_echo = sub.add_parser("echo", help="Check if you've said this before")
    s_echo.add_argument("text", nargs="*")

    s_find = sub.add_parser("find", help="Find thoughts containing a word")
    s_find.add_argument("word")

    sub.add_parser("mood", help="See the mood of the porch")
    sub.add_parser("who", help="The small gods you've noticed")
    sub.add_parser("dawn", help="Save a snapshot of the porch")

    s_watch = sub.add_parser("watch", help="Live feed of recent thoughts")
    s_watch.add_argument("-n", type=int, default=10)

    args = p.parse_args()
    porch = Porch()

    if args.cmd == "say":
        cmd_say(args, porch)
    elif args.cmd == "read":
        cmd_read(args, porch)
    elif args.cmd == "echo":
        cmd_echo(args, porch)
    elif args.cmd == "find":
        cmd_find(args, porch)
    elif args.cmd == "mood":
        cmd_mood(args, porch)
    elif args.cmd == "who":
        cmd_who(args, porch)
    elif args.cmd == "dawn":
        cmd_dawn(args, porch)
    elif args.cmd == "watch":
        cmd_watch(args, porch)
    else:
        p.print_help()
        print()
        print("  hint: try `porch say \"the waiting is not empty\"`")


if __name__ == "__main__":
    main()
