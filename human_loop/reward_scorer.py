# human_loop/reward_scorer.py

from human_loop.db_manager import collection

def score_version(version_id: str, reward: int, comment: str = ""):
    # Delete and re-add metadata with score (Chroma has no update)
    existing = collection.get(ids=[version_id])
    if not existing['ids']:
        print(f"❌ Version '{version_id}' not found.")
        return

    document = existing['documents'][0]
    metadata = existing['metadatas'][0]
    metadata.update({"reward": reward, "comment": comment})

    # Re-add with updated metadata
    collection.delete(ids=[version_id])
    collection.add(documents=[document], ids=[version_id], metadatas=[metadata])
    print(f"✅ Reward for '{version_id}' saved: {reward} ({comment})")

def view_scored_versions():
    results = collection.get()
    for idx, vid in enumerate(results['ids']):
        meta = results['metadatas'][idx]
        print(f"\n📄 Version: {vid}")
        print(f"🏷️ Tags: {meta.get('tags')}")
        print(f"⭐ Reward: {meta.get('reward', 'Not scored')}")
        if 'comment' in meta:
            print(f"💬 Comment: {meta['comment']}")