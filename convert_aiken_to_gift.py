# -*- coding: utf-8 -*-
"""
convert_aiken_to_gift.py — Simple AIKEN → GIFT converter (single-answer MCQ)

Copyright (C) 2025  Grenoble Ecole de Management &
Pierre DAL ZOTTO (aka "DalzAsylum")

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

Description
-----------
- Input: one AIKEN .txt file in the same folder as this script (or pass a path).
- Output: a <name>_gift.txt file.
- Scope: single-correct-answer MCQ only (AIKEN standard).
- Titles: auto `::Q###_first_5_words::`.
- Relative marking: each wrong choice gets `-100/(N-1)%`.
- Comments starting with // or # are ignored.

Usage
-----
  python convert_aiken_to_gift.py            # picks the single .txt in folder
  python convert_aiken_to_gift.py quiz.txt   # convert explicit file

Pedagogical intent
------------------
Part of a reflection on “how to use AI for pedagogy”: integrate into
actual teaching practices (plain‑text AIKEN) so people can do better
without being locked into alien workflows.
"""
from __future__ import annotations
import os
import re
import sys
from pathlib import Path
from typing import List, Tuple

# --- Regular expressions ---
CHOICE_RE = re.compile(r"^\s*([A-Z])\s*[\.)]\s*(.+\S)\s*$")
ANSWER_RE = re.compile(r"^\s*ANSWER\s*:\s*(.+?)\s*$", re.IGNORECASE)

GIFT_ESCAPE_MAP = {
    "\\": r"\\\\",
    "~": r"\~",
    "=": r"\=",
    "#": r"\#",
    "{": r"\{",
    "}": r"\}",
    ":": r"\:",
}

def gift_escape(s: str) -> str:
    """Escape GIFT special chars in a text segment."""
    return "".join(GIFT_ESCAPE_MAP.get(ch, ch) for ch in s)

def make_title(idx: int, question: str, n_words: int = 5) -> str:
    """Build ::Q###_firstNWords:: from the prompt."""
    words = re.findall(r"\w+", question, flags=re.UNICODE)
    slug = "_".join(words[:n_words]) if words else "Question"
    return f"::Q{idx:03}_{slug}::"

def parse_blocks(text: str) -> List[List[str]]:
    """Split AIKEN content into blocks separated by blank lines; skip comments."""
    lines = text.replace('\r\n', '\n').replace('\r', '\n').split('\n')
    blocks: List[List[str]] = []
    cur: List[str] = []
    for raw in lines:
        if raw.strip().startswith('//') or raw.strip().startswith('#'):
            continue
        if not raw.strip():
            if cur:
                blocks.append(cur)
                cur = []
            continue
        cur.append(raw.rstrip())
    if cur:
        blocks.append(cur)
    return blocks

def convert_block(idx: int, block: List[str]) -> str:
    """Convert a single AIKEN block to one GIFT MCQ (single correct answer)."""
    if not block:
        raise ValueError("Empty block")

    question = block[0].strip()
    choices: List[Tuple[str, str]] = []
    answer_raw: str | None = None

    for line in block[1:]:
        m_ans = ANSWER_RE.match(line)
        if m_ans:
            answer_raw = m_ans.group(1).strip()
            break
        m_choice = CHOICE_RE.match(line)
        if m_choice:
            letter, text = m_choice.group(1).upper(), m_choice.group(2).strip()
            choices.append((letter, text))
        else:
            question += "\n" + line.strip()

    if answer_raw is None:
        raise ValueError("Missing ANSWER: line")

    # Determine correct letter (letter or full-text mapping)
    correct = answer_raw.upper().strip()
    if not (len(correct) == 1 and correct.isalpha()):
        normalized = answer_raw.strip().lower()
        for lt, tx in choices:
            if tx.strip().lower() == normalized:
                correct = lt
                break

    letters = {lt for lt, _ in choices}
    if correct not in letters:
        raise ValueError(f"Invalid or not found ANSWER: '{answer_raw}'")

    n = len(choices)
    if n < 2:
        raise ValueError("At least 2 choices required")

    penalty = -100.0 / (n - 1)
    pct = f"{penalty:.6f}".rstrip('0').rstrip('.')

    title = make_title(idx, question)
    qtext = gift_escape(question)

    parts = []
    for lt, tx in choices:
        esc = gift_escape(tx)
        if lt == correct:
            parts.append(f"={esc}")
        else:
            parts.append(f"~%{pct}%{esc}")

    return f"{title} {qtext} {{\n" + "\n".join(parts) + "\n}"

def read_text_any(path: str) -> str:
    """Read as UTF‑8 (BOM ok) then Latin‑1 fallback."""
    try:
        return Path(path).read_text(encoding='utf-8-sig')
    except UnicodeDecodeError:
        return Path(path).read_text(encoding='latin-1')

def find_single_txt_in_cwd() -> str:
    """Return the only .txt (excluding *_gift.txt) in current folder or raise."""
    txts = [f for f in os.listdir('.') if f.lower().endswith('.txt') and not f.lower().endswith('_gift.txt')]
    if len(txts) == 0:
        raise FileNotFoundError("No .txt AIKEN file found in folder.")
    if len(txts) > 1:
        raise RuntimeError("Multiple .txt files found. Leave only your AIKEN file and retry.")
    return txts[0]

def main(argv: list[str] | None = None) -> None:
    argv = sys.argv[1:] if argv is None else argv

    # Resolve input file
    if argv:
        inpath = argv[0]
        if not os.path.isfile(inpath):
            print(f"[ERROR] File not found: {inpath}")
            sys.exit(1)
    else:
        try:
            inpath = find_single_txt_in_cwd()
        except Exception as e:
            print(f"[ERROR] {e}")
            sys.exit(1)

    # Read
    try:
        raw = read_text_any(inpath)
    except Exception as e:
        print(f"[ERROR] Cannot read: {e}")
        sys.exit(1)

    # Convert
    blocks = parse_blocks(raw)
    out_lines: List[str] = []
    errors: List[Tuple[int, str]] = []

    for i, blk in enumerate(blocks, 1):
        try:
            out_lines.append(convert_block(i, blk))
        except Exception as e:
            errors.append((i, str(e)))

    outpath = os.path.splitext(inpath)[0] + "_gift.txt"

    try:
        Path(outpath).write_text("\n\n".join(out_lines) + ("\n" if out_lines else ""), encoding='utf-8')
    except Exception as e:
        print(f"[ERROR] Cannot write output: {e}")
        sys.exit(1)

    # Report
    if errors:
        print(f"Done with warnings. Output: {outpath}")
        for i, msg in errors:
            print(f" - Q#{i}: {msg}")
    else:
        print(f"Done. Output: {outpath}")

if __name__ == '__main__':
    main()
