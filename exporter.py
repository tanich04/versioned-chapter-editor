# test_writer_reviewer.py

from ai_agents.writer import spin_chapter_text
from ai_agents.reviewer import review_and_improve

with open("chapter1.txt", "r", encoding="utf-8") as f:
    raw_text = f.read()

spun = spin_chapter_text(raw_text)
with open("chapter1_spun.txt", "w", encoding="utf-8") as f:
    f.write(spun)

reviewed = review_and_improve(spun)
with open("chapter1_final.txt", "w", encoding="utf-8") as f:
    f.write(reviewed)

print("✅ Spinning & reviewing complete using Gemini!")