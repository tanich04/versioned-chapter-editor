# human_loop/review_editor.py

import os
from human_loop.db_manager import save_version
from human_loop.voice_input import capture_voice_note
from datetime import datetime

def load_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def save_file(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def human_review_cli():
    # Load the reviewed file
    reviewed = load_file("chapter1_final.txt")

    print("\n📝 HUMAN-IN-THE-LOOP REVIEW TOOL")
    print("────────────────────────────────────")
    print("\n✅ Loaded reviewed chapter.")
    print("📖 Preview (first 500 characters):\n")
    print(reviewed[:500], "...\n")

    # Optional voice note
    choice = input("🎙️ Add a voice comment? (y/n): ").strip().lower()
    if choice == 'y':
        voice_note = capture_voice_note()
        if voice_note:
            reviewed += f"\n\n🗣️ Voice Note: {voice_note}"
        else:
            print("⚠️ No voice note added.")

    # Get version metadata
    version_name = input("\n📁 Enter a version name (e.g. 'chapter1_final_v2'): ").strip()
    tags = input("🏷️ Add tags (comma-separated, e.g. 'final, reviewed, human'): ").strip().split(',')

    # Save file and log to vector DB
    save_file(f"{version_name}.txt", reviewed)
    save_version(version_name, reviewed, tags)

    print(f"\n✅ Saved: {version_name}.txt")
    print(f"📚 Version stored in ChromaDB with tags: {tags}\n")
def edit_chapter(filename):
    # Read original content
    with open(filename, "r", encoding="utf-8") as f:
        original = f.read()

    print("\n--- ORIGINAL TEXT (read-only preview) ---\n")
    print(original[:500] + "...\n" if len(original) > 500 else original)
    print("\n--- END OF PREVIEW ---")

    print("\n✍️ Now enter your edited version below (or paste it in):\n")
    edited = input(">>> ")

    if not edited.strip():
        print("⚠️ No changes made.")
        return filename

    # Create new versioned filename
    base = filename.replace(".txt", "")
    version_num = 1
    while os.path.exists(f"{base}_v{version_num}.txt"):
        version_num += 1
    new_filename = f"{base}_v{version_num}.txt"

    # Save edited version
    with open(new_filename, "w", encoding="utf-8") as f:
        f.write(edited)

    print(f"✅ Edited version saved as {new_filename}")
    return new_filename
if __name__ == "__main__":
    human_review_cli()