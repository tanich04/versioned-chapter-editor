import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import os

from human_loop.db_manager import save_version, get_all_versions, generate_new_version_id

class BookAutomationGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("📚 Book Automation GUI")
        self.root.geometry("700x600")

        # --- File upload and info ---
        self.filename_label = tk.Label(root, text="No file selected")
        self.filename_label.pack(pady=10)

        self.upload_button = tk.Button(root, text="📂 Upload Chapter", command=self.upload_file)
        self.upload_button.pack()

        # --- Editable Text Area ---
        self.text_area = scrolledtext.ScrolledText(root, width=80, height=20)
        self.text_area.pack(pady=10)

        # --- Tags Entry ---
        self.tags_entry = tk.Entry(root, width=50)
        self.tags_entry.pack()
        self.tags_entry.insert(0, "Enter comma-separated tags")

        # --- Save Version ---
        self.save_button = tk.Button(root, text="💾 Save Version", command=self.save_version)
        self.save_button.pack(pady=10)

        # --- View Version History ---
        self.view_history_button = tk.Button(root, text="🕘 View All Versions", command=self.view_versions)
        self.view_history_button.pack()
        self.search_button = tk.Button(root, text="🔍 Search by Tag", command=self.search_by_tag)
        self.search_button.pack(pady=5)
        self.current_file_path = None

    def upload_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            self.current_file_path = file_path
            self.filename_label.config(text=f"📄 {os.path.basename(file_path)}")
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(tk.END, content)

    def save_version(self):
        if not self.current_file_path:
            messagebox.showwarning("No file", "Please upload a chapter file first.")
            return

        content = self.text_area.get("1.0", tk.END).strip()
        if not content:
            messagebox.showerror("Empty content", "The chapter content is empty.")
            return

        tags = self.tags_entry.get().split(",")
        filename = os.path.basename(self.current_file_path)
        version_id = generate_new_version_id(filename)

        save_version(version_id, content, tags)
        messagebox.showinfo("Success", f"Version saved as {version_id}")

    def view_versions(self):
        versions_data = get_all_versions()
        version_ids = versions_data.get("ids", [])
        metadatas = versions_data.get("metadatas", [])

        version_window = tk.Toplevel(self.root)
        version_window.title("📜 Version History")
        version_window.geometry("500x400")

        listbox = tk.Listbox(version_window, width=80, height=20)
        for i, vid in enumerate(version_ids):
            tags = metadatas[i].get("tags", "")
            listbox.insert(tk.END, f"{vid} | Tags: {tags}")
        listbox.pack(pady=20)
    def search_by_tag(self):
        tag = self.tags_entry.get().strip()
        if not tag:
            messagebox.showwarning("Empty Tag", "Please enter a tag to search.")
            return

        data = get_all_versions()
        version_ids = data["ids"]
        metadatas = data["metadatas"]
        documents = data["documents"]

        matched_versions = []
        for i, meta in enumerate(metadatas):
            tags = meta.get("tags", [])
            if tag in tags:
                matched_versions.append((version_ids[i], documents[i]))

        if not matched_versions:
            messagebox.showinfo("No Matches", f"No versions found with tag: {tag}")
            return

        # Create popup window
        search_window = tk.Toplevel(self.root)
        search_window.title(f"🔍 Versions with tag: {tag}")
        search_window.geometry("600x400")

        listbox = tk.Listbox(search_window, width=80, height=15)
        listbox.pack(pady=10)

        preview_box = scrolledtext.ScrolledText(search_window, width=70, height=10)
        preview_box.pack()
        export_button = tk.Button(search_window, text="⬇ Export Selected Version", command=export_selected_version)
        export_button.pack(pady=10)

        def show_content(event):
            selection = listbox.curselection()
            if selection:
                index = selection[0]
                content = matched_versions[index][1]
                preview_box.delete(1.0, tk.END)
                preview_box.insert(tk.END, content)

        for vid, _ in matched_versions:
            listbox.insert(tk.END, vid)
        listbox.bind("<<ListboxSelect>>", show_content)

        def export_selected_version():
            selection = listbox.curselection()
            if not selection:
                messagebox.showwarning("No Selection", "Select a version to export.")
                return
            index = selection[0]
            version_id, content = matched_versions[index]

            # Ask where to save the file
            filename = filedialog.asksaveasfilename(
                defaultextension=".txt",
                initialfile=version_id,
                filetypes=[("Text files", "*.txt")]
            )
            if filename:
                try:
                    with open(filename, "w", encoding="utf-8") as f:
                        f.write(content)
                    messagebox.showinfo("Export Successful", f"Version exported to {filename}")
                except Exception as e:
                    messagebox.showerror("Export Failed", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = BookAutomationGUI(root)
    root.mainloop()
