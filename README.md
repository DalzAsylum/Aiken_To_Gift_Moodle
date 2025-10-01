# AIKEN → GIFT (Single-answer MCQ)

**Simple converter** from AIKEN `.txt` to GIFT `.txt` for Moodle import.

## Why (my own problem)
This project is more than just a script — it’s a tiny but powerful example of how AI can support pedagogy without alienating teachers or forcing them into rigid workflows.
I started with a simple problem:
I was using the AIKEN format for Moodle quizzes because it’s easy to write in plain text. But AIKEN has a big limitation: it doesn’t allow relative grading out of the box. For example, I wanted a fair scoring system like:

+1 for the correct answer
−1/(N−1) for each wrong answer

This is impossible to achieve with a standard AIKEN import in Moodle.
So, instead of giving up or switching to a complex tool, I decided to integrate AI into my workflow. I worked with Copilot to design and build this script step by step. It was a real co-creation process: I brought the teaching context and constraints, Copilot brought the coding power. Together, we iterated, tested, and refined until it worked.
And it worked so well that I thought:
Why keep it for myself?

I’m sharing it so other educators can benefit, adapt, and improve it. This is open source because pedagogy should be open, collaborative, and empowering.

💡 Key idea: AI should augment teachers, not lock them into bubbles or alien workflows. This tool respects existing practices (plain-text AIKEN) and makes them better with minimal friction.

- **Scope**: single-correct-answer MCQ (AIKEN standard)
- **Auto titles**: `::Q###_first_5_words::`
- **Relative marking**: each wrong choice = `-100/(N-1)%`
- **Encodings**: UTF‑8 (BOM) then Latin‑1 fallback
- **Comments**: lines starting with `//` or `#` are ignored

## Usage (Windows / CLI)
- Put `convert_aiken_to_gift.py` and `convert_aiken_to_gift.bat` next to your `quiz.txt` (AIKEN)
- Double‑click the BAT, or run: `python convert_aiken_to_gift.py quiz.txt`
- Output: `quiz_gift.txt`

## Credits
- My thanks to Grenoble Ecole de Management for the time I could spend on this and for providing me access to Copilot  

## License
This project is released under **GNU GPL v3.0 or later**. See `LICENSE`.
