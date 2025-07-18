# score_versions.py

from human_loop.reward_scorer import score_version, view_scored_versions

def score_ui():
    print("\n🎯 RL-STYLE REWARD SCORING")
    print("────────────────────────────")

    view_scored_versions()

    version_id = input("\n🔍 Enter the version ID to score: ").strip()
    reward = int(input("⭐ Enter reward score (-1 to 5): ").strip())
    comment = input("💬 Optional comment: ").strip()

    score_version(version_id, reward, comment)

if __name__ == "__main__":
    score_ui()