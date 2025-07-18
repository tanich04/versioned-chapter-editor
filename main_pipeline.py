import os
import time
from human_loop import review_editor, voice_input, reward_scorer, db_manager

def main():
    print("\n📘 AI Book Authoring Assistant - Interactive Pipeline")

    # Step 1: Select chapter and load existing version
    chapter = input("\n📄 Enter chapter name (e.g., chapter1_final): ")
    filepath = f"{chapter}.txt"
    if not os.path.exists(filepath):
        print("❌ File not found.")
        return

    # Step 2: Launch review + edit loop
    print("\n✏️  Opening editor for human-in-the-loop revision...")
    reviewed_path = review_editor.edit_text_file(filepath)

    # Step 3: Capture voice feedback (optional)
    voice_comment = input("\n🎙️ Do you want to add voice feedback? (y/n): ").strip().lower()
    if voice_comment == 'y':
        transcript = voice_input.capture_voice_comment()
        print("\n📝 Transcribed voice note:", transcript)
    else:
        transcript = ""

    # Step 4: Score the version
    score = input("\n⭐ Rate the updated version (-1 to 5): ")
    comment = input("💬 Add comment for this version: ")
    version_name = os.path.splitext(os.path.basename(reviewed_path))[0]
    db_manager.store_version_score(version_name, score, f"{comment}. {transcript}")

    print("\n✅ Full pipeline completed successfully.")

if __name__ == "__main__":
    main()
