# AIKEN → GIFT (Single-answer MCQ)

**Simple converter** from AIKEN `.txt` to GIFT `.txt` for Moodle import.

- **Scope**: single-correct-answer MCQ (AIKEN standard)
- **Auto titles**: `::Q###_first_5_words::`
- **Relative marking**: each wrong choice = `-100/(N-1)%`
- **Encodings**: UTF‑8 (BOM) then Latin‑1 fallback
- **Comments**: lines starting with `//` or `#` are ignored

## Usage (Windows / CLI)
- Put `convert_aiken_to_gift.py` and `convert_aiken_to_gift.bat` next to your `quiz.txt` (AIKEN)
- Double‑click the BAT, or run: `python convert_aiken_to_gift.py quiz.txt`
- Output: `quiz_gift.txt`

## Why (pedagogical story)
A tiny example of **“how to use AI for pedagogy”**: integrate into **existing practices** (plain‑text AIKEN) so teachers can do better without being locked into new workflows.

## Credits
- Grenoble Ecole de Management  
- Pierre DAL ZOTTO (aka *DalzAsylum*)

## License
This project is released under **GNU GPL v3.0 or later**. See `LICENSE`.
