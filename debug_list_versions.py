from human_loop.db_manager import get_all_versions

def list_versions():
    results = get_all_versions()
    print("\n📚 Available Versions in ChromaDB:")
    for vid in results['ids']:
        print("•", vid)

if __name__ == "__main__":
    list_versions()
