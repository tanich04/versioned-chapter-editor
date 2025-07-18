import os
from human_loop import db_manager

def display_file_preview(filepath, lines=20):
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            print("\n--- ORIGINAL TEXT (read-only preview) ---\n")
            for i in range(lines):
                line = file.readline()
                if not line:
                    break
                print(line.strip())
            print("\n--- END OF PREVIEW ---")
    except FileNotFoundError:
        print("❌ File not found.")
    except Exception as e:
        print(f"❌ Error reading file: {e}")

def view_version_history(chapter):
    print(f"\n📚 Version history for: {chapter}\n")
    versions = db_manager.get_all_versions()

    if not versions or not versions.get("ids"):
        print("⚠️ No versions found.")
        return

    filtered_versions = [
        {"id": v_id, "metadata": versions["metadatas"][i], "document": versions["documents"][i]}
        for i, v_id in enumerate(versions["ids"])
        if v_id.startswith(chapter)
    ]

    if not filtered_versions:
        print("⚠️ No version history found for this chapter.")
        return

    for version in filtered_versions:
        print(f"📄 Version ID: {version['id']}")
        print(f"🏷️ Tags: {version['metadata'].get('tags', '')}")
        print(f"📄 Content Preview:\n{version['document'][:300]}...\n")
        print("—" * 40)

def main():
    while True:
        print("\nChoose an option:")
        print("1. Review and score a chapter")
        print("2. View version history")
        print("3. Exit")

        choice = input("Enter your choice (1/2/3): ").strip()

        if choice == "1":
            chapter = input("\n📄 Enter the chapter filename (e.g., chapter1.txt): ").strip()

            if not os.path.isfile(chapter):
                print("❌ File does not exist.")
                continue

            display_file_preview(chapter)

            print("\n✍️ Now enter your edited version below (or paste it in):\n")
            user_edit = input(">>> ")

            if user_edit.lower() == "no":
                with open(chapter, "r", encoding="utf-8") as f:
                    user_edit = f.read()

            new_version_id = db_manager.generate_new_version_id(chapter)
            tags = input("🏷️ Enter tags (comma-separated): ").split(",")

            db_manager.save_version(new_version_id, user_edit, tags)
            print(f"✅ Edited version saved as {new_version_id}")

        elif choice == "2":
            chapter = input("\n🔍 Enter chapter filename to view version history: ").strip()
            view_version_history(chapter)

        elif choice == "3":
            print("👋 Exiting. Goodbye!")
            break
        else:
            print("❗ Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()
