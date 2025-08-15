# ai_images_gallery_generator
Organize your AI-generated images and prompts into a versioned, searchable offline HTML gallery

# AI Images Gallery Generator

`generate_gallery.py` is a Python script that scans a local `images/` folder, reads prompt text files, matches them with image files, and generates a **self-contained HTML gallery** with search, favorites, folder filtering, dark mode.

## ✨ Features

- **Automatic image & prompt pairing** — Matches `<index>_prompt.txt` with image files sharing the same `<index>` prefix.
- **Multiple formats supported** — `.jpg`, `.jpeg`, `.png`, `.webp`, `.gif`.
- **Interactive HTML gallery**:
  - Search by prompt text or index number.
  - **Folder filter** dropdown to show only images from a selected subfolder.
  - Favorites 💖 saved in `localStorage` for persistence.
  - Copy Prompt button to quickly copy prompt text.
  - Dark Mode toggle.
  - Pagination controls.
  - Responsive grid layout with lazy-loaded images.
- **Offline & portable** — The generated HTML file works locally without a server.

## 📂 Folder Structure

Your working directory should look like this:
  
  project-root/
  ├─ generate_gallery.py
  ├─ images/
  │ ├─ folder1/
  │ │ ├─ 001_prompt.txt
  │ │ ├─ 001.jpg
  │ │ ├─ 002_prompt.txt
  │ │ └─ 002.png
  │ └─ folder2/
  │ ├─ 003_prompt.txt
  │ ├─ 003.webp
  │ └─ ...

- `images/` can contain multiple subfolders.
- Each `_prompt.txt` should have a matching image file starting with the same index number.

## 🛠 Usage

1. **Place your images and prompt files** inside the `images/` folder, keeping them organized in subfolders if needed.
2. **Run the script**:
   ```bash
   python generate_gallery.py
3. **This will create**:
   images_gallery.html
4. Open the HTML file in your web browser.

## 🔍 Matching Logic

A prompt file 123_prompt.txt will match the first image file in the same folder whose name starts with 123, optionally followed by space, hyphen, or underscore.
Matching is case-insensitive.
Only the first match is used.

##📜 License

This project is released under the MIT License. See LICENSE for details.
