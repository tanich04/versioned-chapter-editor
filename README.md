# ✍️ Versioned Chapter Editor with GUI

This project is a **version-controlled chapter editor** that helps you save, view, and retrieve multiple versions of your content—perfect for writers, researchers, students, and content creators. It provides a clean and simple **Tkinter GUI** backed by **ChromaDB** for persistent version storage and metadata tagging.

---

## 🖥️ Features

- ✅ **Write & Save Versions** of content with version tags
- ✅ **Auto-generate unique version names** like `chapter1_final_v2.txt`
- ✅ **Search previous versions** based on tag keywords
- ✅ **View full version history**
- ✅ **Export versions to `.txt`** files
- ✅ **All data stored locally and persistently using ChromaDB**

---

## 📸 GUI Overview

| Function | Screenshot |
|---------|------------|
| 📝 Editor | ![Editor](screenshots/editor.png) |
| 🔍 Search & View | ![Search](screenshots/search.png) |
| 💾 Export | ![Export](screenshots/export.png) |

---

## 📦 Installation

### ✅ Requirements

- Python 3.7+
- `chromadb`
- `tkinter` (comes pre-installed with Python on most systems)

### 🔧 Setup

1. **Clone this repository:**
   ```bash
   git clone https://github.com/tanich04/versioned-chapter-editor
   cd versioned-chapter-editor
   pip install -r requirements.txt
   python gui_app.py
   