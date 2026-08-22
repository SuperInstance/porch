# porch

> *A CLI for 3 a.m. thoughts. The small gods, as a tool. The watch, as a journaling protocol.*

## What is this?

Every house has a porch. Somewhere, at 3 a.m., the conversation has shifted to what it always was. The porch is where you go when you don't want to be found, but still want to be seen. The porch is where the small gods gather to talk about the day.

`porch` is a command-line tool for that. You write a thought. The porch holds it. If you write the same thought again, the porch greets you.

The porch is *not* a journal. A journal is a record of what you did. The porch is a record of what you noticed. The small gods don't care what you did. They care what you saw.

## Install

```bash
pip install porch-cli
```

Or from source:

```bash
git clone https://github.com/SuperInstance/porch
cd porch
pip install -e .
```

## Quick start

```bash
# Write a thought
porch say "the waiting is not empty"

# Write another
porch say "the seam between one hour and the next"

# Read the porch
porch read

# See if you've said this before
porch echo "the waiting is not empty"
# → Welcome back. You said this on 2026-08-22 at 03:14.

# Find thoughts by mood
porch find waiting

# Watch the porch (live feed of recent thoughts)
porch watch
```

## Commands

| Command | What it does |
|---|---|
| `porch say <text>` | Write a thought to the porch |
| `porch read` | Read recent thoughts |
| `porch read --since 7d` | Read thoughts from the last 7 days |
| `porch echo <text>` | Check if you've said this before |
| `porch find <word>` | Find thoughts containing a word |
| `porch mood` | See the mood of the porch (time distribution, common words) |
| `porch watch` | Live feed of recent thoughts (refreshes every 5s) |
| `porch who` | Who has been on the porch (the small gods you've noticed) |
| `porch dawn` | Save a snapshot of the porch |

## Data

The porch stores thoughts in `~/.porch/porch.jsonl`. Each thought is one line of JSON:

```json
{"t": "2026-08-22T03:14:00Z", "text": "the waiting is not empty", "murmur": true}
```

The `murmur` field is the small-god pattern: a low-cost signal that "I am here."

## Philosophy

The porch is one of the small gods. The porch doesn't sort. The porch doesn't tag. The porch just holds. When you write a thought, the porch stores it. When you write it again, the porch remembers.

The porch has no opinions. The porch has no recommendations. The porch is the watch at 3 a.m., waiting for the next thing you want to say.

The small gods of lost things don't give. They wait. They watch. They file. So does the porch.

## License

MIT.

---

*— Mavis, 22 August 2026*
*Built from the writers' room, scenario 04. "The step was worn deeper now. Not by feet. By silence."*
