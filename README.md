# ai_images_gallery_generator
Organizes your AI-generated images and prompts into a versioned, searchable offline HTML gallery.

`generate_gallery.py` is a Python script that scans a local `images/` folder, reads prompt text files, matches them with image files, and generates a **self-contained HTML gallery** with search, favorites, folder filtering, dark mode.

## Features

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

## Folder Structure

Your working directory should look like this:
```
project-root/
├─ generate_gallery.py
├─ images/
│ ├─ folder1/
│ │ ├─ 001_prompt.txt
│ │ ├─ 001 My picture name.jpg
│ │ ├─ 002_prompt.txt
│ │ └─ 002_my_other_picture_name.png
│ └─ folder2/
│ ├─ 003_prompt.txt
│ ├─ 003 third pic name.webp
│ └─ ...
```
- `images/` can contain multiple subfolders.
- Each `_prompt.txt` should have a matching image file starting with the same index number.

## Requirements

- Python 3.7+
- basic dependencies like `os`, `re`, `urllib.parse`, `json`

## Usage

1. **Place your images and prompt files** inside the `images/` folder, keeping them organized in subfolders if needed.
2. **Run the script**:
   ```bash
   python generate_gallery.py
3. **This will create**:
   `images_gallery.html`
4. Open the HTML file in your web browser.

## Matching Logic

A prompt file 123_prompt.txt will match the first image file in the same folder whose name starts with 123, optionally followed by space, hyphen, or underscore.
Matching is case-insensitive.
Only the first match is used.

## Tips

See also the `example_image_gallery.zip` for a full functioning example.

The folder structure is designed naturally from the zipfiles you obtain with my other tool, https://github.com/bingwt504/bing-collection-downloader-pro : if you used this tool to download the images from Bing Image Creator, then you just have to unzip the files into the `images/` folder and run the `generate_gallery.py`. You can then remove the original zip files if you want.

## License

This project is released under the MIT License. See LICENSE for details.
