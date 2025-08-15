import os
import re
import urllib.parse
import json

root_dir = os.path.join(os.path.dirname(__file__), "images")
output_html_path = os.path.join(os.path.dirname(__file__), "images_gallery.html")

image_data = []
for dirpath, _, filenames in os.walk(root_dir):
    for file in filenames:
        if file.endswith("_prompt.txt"):
            prompt_number = file.split("_")[0]
            prompt_path = os.path.join(dirpath, file)
            try:
                with open(prompt_path, 'r', encoding='utf-8') as f:
                    prompt_text = f.read().strip()
            except:
                prompt_text = ""
            image = None
            for img_file in sorted(os.listdir(dirpath)):
                ext = os.path.splitext(img_file)[1].lower()
                if ext in ['.jpg', '.jpeg', '.png', '.webp', '.gif'] and re.match(
                    rf"^" + re.escape(prompt_number) + r"([\s_-].+)?" + re.escape(ext) + r"$",
                    img_file, re.IGNORECASE
                ):
                    image = os.path.join(dirpath, img_file)
                    break
            subfolder = os.path.basename(dirpath)
            image_data.append({
                'image': image,
                'prompt': prompt_text,
                'subfolder': subfolder,
                'index': prompt_number,
                'index_num': int(prompt_number.split('-')[0]) if prompt_number.split('-')[0].isdigit() else 999999
            })

html_parts = ['<!DOCTYPE html><html><head><meta charset="UTF-8"><title>AI Images Prompts Gallery</title>']
html_parts.append("""<style>
:root { --img-size: 300px; }
body {
  font-family: 'Segoe UI', sans-serif; margin: 0; padding: 0;
  background: #f5f5f5; color: #333;
}
body.dark {
  background: #121212; color: #eee;
}
header {
  padding: 0.5em; background: #333; color: white;
  text-align: center; font-size: 1.2em; position: relative;
}
#darkToggle {
  position: absolute; right: 1em; top: 0.5em;
}
.controls {
  padding: 1em; text-align: center;
  background: #fafafa; border-bottom: 1px solid #ddd;
}
body.dark .controls {
  background: #1e1e1e; border-color: #333;
}
.controls input, .controls button, .controls label {
  margin: 0.2em;
}
.gallery {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(var(--img-size), 1fr));
  gap: 15px; padding: 20px;
}
.card {
  border: 1px solid #ccc;
  padding: 10px; background: white;
  box-shadow: 2px 2px 6px rgba(0,0,0,0.1);
}
body.dark .card {
  background: #1e1e1e; color: #eee; border-color: #444;
}
.card img {
  width: 100%; height: auto;
  cursor: pointer; border-radius: 5px;
}
.favorite {
  font-size: 22px; cursor: pointer; margin-right: 5px;
}
.super-favorite {
  font-size: 22px; cursor: pointer; margin-right: 5px;
}
.favorite { color: #ccc; }
.favorite.active { color: red; }
.super-favorite { color: #ccc; }
.super-favorite.active { color: red; }
textarea {
  width: 100%; resize: vertical; margin-top: 5px; height: 8em;
  background-color: #f9f9f9; color: #333;
  border: 1px solid #ccc; overflow-y: auto;
  font-family: inherit;
}
body.dark textarea {
  background-color: #2a2a2a; color: #eee; border-color: #555;
}
textarea[readonly] { pointer-events: auto; }
.pagination-controls {
  text-align: center; margin: 1em;
}
.pagination-controls button {
  padding: 0.4em 0.8em; margin: 0.2em;
  border: none; border-radius: 4px;
  background-color: #eee; cursor: pointer; font-weight: bold;
}
body.dark .pagination-controls button {
  background-color: #444; color: #ccc;
}
body.dark .pagination-controls button.active {
  background-color: #007BFF; color: white;
}
.pagination-controls button.active {
  background-color: #007BFF; color: white;
}
</style>
<script>
let favorites = JSON.parse(localStorage.getItem('favorites') || '{}');
let superFavorites = JSON.parse(localStorage.getItem('superFavorites') || '{}');
let currentPage = 0;
let imagesPerPage = 200;
let allCards = [];

function copyText(text) {
  navigator.clipboard.writeText(text);
}
function toggleFavorite(id) {
  favorites[id] = !favorites[id];
  localStorage.setItem('favorites', JSON.stringify(favorites));
  renderGallery();
}
function toggleSuperFavorite(id) {
  const isActive = superFavorites[id] = !superFavorites[id];
  if (isActive) {
    favorites[id] = true;
    localStorage.setItem('favorites', JSON.stringify(favorites));
  }
  localStorage.setItem('superFavorites', JSON.stringify(superFavorites));
  renderGallery();
}
function toggleTheme() {
  document.body.classList.toggle('dark');
}
function setSize(size) {
  document.documentElement.style.setProperty('--img-size', size);
}
function filterGallery() {
  const search = document.getElementById('searchInput').value.toLowerCase();
  const onlySuperFav = document.getElementById('superFavToggle').checked;
  const folderVal = document.getElementById('folderFilter') ? document.getElementById('folderFilter').value : '';
  return allCards.filter(card => {
    const matchesSearch = card.prompt.toLowerCase().includes(search);
    const matchesSuperFav = !onlySuperFav || superFavorites[card.id];
    return matchesSearch && matchesSuperFav && (!folderVal || card.subfolder === folderVal);
  });
}
function renderPagination(pagination, totalPages) {
  pagination.innerHTML = '';
  for (let i = 0; i < totalPages; i++) {
    const btn = document.createElement('button');
    btn.textContent = i + 1;
    btn.className = (i === currentPage ? 'active' : '');
    btn.onclick = () => { currentPage = i; renderGallery(); };
    pagination.appendChild(btn);
  }
}
function renderGallery() {
  const gallery = document.querySelector('.gallery');
  const paginations = document.querySelectorAll('.pagination-controls');
  gallery.innerHTML = '';
  const filtered = filterGallery();
  const totalPages = Math.ceil(filtered.length / imagesPerPage);
  paginations.forEach(p => renderPagination(p, totalPages));
  const pageItems = filtered.slice(currentPage * imagesPerPage, (currentPage + 1) * imagesPerPage);
  for (const card of pageItems) {
    const div = document.createElement('div');
    div.className = 'card';
    div.setAttribute('data-id', card.id);
    div.setAttribute('data-prompt', card.prompt);
    const heartSymbol = superFavorites[card.id] ? '&#10084;' : '&#10084;';
    div.innerHTML = `
      ${card.imageHTML}
      <div><strong>folder:</strong> ${card.subfolder} (${card.index})</div>
      <textarea rows="4" readonly onfocus="this.select()">${card.prompt}</textarea>
      <button onclick="copyText(this.previousElementSibling.value)">Copy Prompt</button>
      <div>
        <span class="super-favorite ${superFavorites[card.id] ? 'active' : ''}" onclick="toggleSuperFavorite('${card.id}')">${heartSymbol}</span>
      </div>
    `;
    gallery.appendChild(div);
  }
}
document.addEventListener('DOMContentLoaded', () => {
  renderGallery();
});
</script>
</head><body>
<header>
  <h1>AI Images Prompts Gallery</h1>
  <button id="darkToggle" onclick="toggleTheme()">Toggle Dark Mode</button>
</header>
<div class="controls">
  <input id="searchInput" type="text" placeholder="Search prompts..." oninput="renderGallery()">
  <select id="folderFilter" onchange="renderGallery()"><option value="">All folders</option></select>
  <label><input type="checkbox" id="superFavToggle" onchange="renderGallery()">Favorites only</label>
  <div>
    <span>Show images as:</span>
    <button onclick="setSize('200px')">Small</button>
    <button onclick="setSize('300px')">Medium</button>
    <button onclick="setSize('400px')">Large</button>
  </div>
</div>
<div class="pagination-controls"></div>
<div class="gallery"></div>
<div class="pagination-controls"></div>
""")

html_parts.append('<script>\n')
cards = []
for i, data in enumerate(sorted(image_data, key=lambda x: (x['subfolder'].lower(), x['index_num']))):
    image = data['image']
    prompt = data['prompt']
    subfolder = data['subfolder']
    index = data['index']
    unique_id = f"{subfolder}_{os.path.basename(image)}" if image else f"{subfolder}_noimg_{i}"
    if image:
        rel_path = os.path.relpath(image, os.path.dirname(output_html_path)).replace("\\", "/")
        encoded_path = urllib.parse.quote(rel_path)
        image_html = f'<img src="{encoded_path}" onclick="window.open(\'{encoded_path}\')">'
    else:
        image_html = '<div style="width:100%;height:200px;border:1px dashed #aaa;"></div>'
    cards.append({"id": unique_id, "prompt": prompt, "subfolder": subfolder, "index": index, "imageHTML": image_html})

folders = sorted({d['subfolder'] for d in image_data})

html_parts.append('allCards = ' + json.dumps(cards, ensure_ascii=False).replace('</script>', '<\\/script>') + ';\n')
html_parts.append('const folders = ' + json.dumps(folders, ensure_ascii=False) + ';\n')
html_parts.append("const sel = document.getElementById('folderFilter'); if (sel) { folders.forEach(f => { const o=document.createElement('option'); o.value=f; o.textContent=f; sel.appendChild(o); }); }\n")
html_parts.append('renderGallery();</script></body></html>')

with open(output_html_path, 'w', encoding='utf-8') as f:
    f.write(''.join(html_parts))

print(f"HTML gallery created at: {output_html_path}")


with open(output_html_path, 'w', encoding='utf-8') as f:
    f.write(''.join(html_parts))

print(f"HTML gallery created at: {output_html_path}")
