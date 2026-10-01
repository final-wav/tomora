import json
import base64
import os
import re

# 1. Load User Magenta Artwork Image
img_path = r"C:\Users\Hakan\.gemini\antigravity\brain\5e6e588d-8195-4b9c-a574-5d026ae3847a\.user_uploaded\media_1790875455821.jpg"
with open(img_path, "rb") as f:
    img_b64 = base64.b64encode(f.read()).decode('utf-8')
img_src = f"data:image/jpeg;base64,{img_b64}"

# 2. Extract Phase 1 (Lyrics + Deep Analysis) & Reviews for all 12 Tracks
phase1_dir = 'album_analyse_fallstudie/Phase_1_Mikro_Dekonstruktion'
review_dir = 'album_review_und_interpretation'

track_names_map = {
    "01": "Please",
    "02": "Come Closer",
    "03": "A Boy Like You",
    "04": "Ring The Alarm",
    "05": "My Baby",
    "06": "Have You Seen Me Dance Alone",
    "07": "Somewhere Else",
    "08": "I Drink The Light",
    "09": "Wavelengths",
    "10": "Side By Side",
    "11": "The Thing",
    "12": "In A Minute"
}

tracks = []
for num_str, title in track_names_map.items():
    p1_file = f"{num_str}_{title.replace(' ', '_')}.md"
    p1_path = os.path.join(phase1_dir, p1_file)
    if not os.path.exists(p1_path):
        for f in os.listdir(phase1_dir):
            if f.startswith(num_str):
                p1_path = os.path.join(phase1_dir, f)
                break
                
    lyrics = ""
    micro_analysis = ""
    if os.path.exists(p1_path):
        with open(p1_path, 'r', encoding='utf-8', errors='ignore') as f:
            p1_content = f.read()
        lyrics_match = re.search(r'### 1\.\s*Transkribierter Textkorpus\s*```text(.*?)```', p1_content, re.DOTALL)
        lyrics = lyrics_match.group(1).strip() if lyrics_match else ""
        analysis_parts = re.split(r'### 2\.\s*Zeile-f[^\n]*\n', p1_content)
        micro_analysis = analysis_parts[1].strip() if len(analysis_parts) > 1 else ""

    review_content = ""
    for rf in os.listdir(review_dir):
        if rf.startswith(num_str) and rf.endswith('.md'):
            with open(os.path.join(review_dir, rf), 'r', encoding='utf-8', errors='ignore') as f:
                review_content = f.read()
            break

    tracks.append({
        "num": num_str,
        "title": title,
        "lyrics": lyrics,
        "review": review_content,
        "analysis": micro_analysis
    })

html_template = r"""<!DOCTYPE html>
<html lang="de">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>TOMORA — Tracks & Lyrics</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
  <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
  <style>
    :root {
      --bg: #111114; /* Dunkles Anthrazit statt 100% Schwarz */
      --bg-header: rgba(17, 17, 20, 0.95);
      --text: #ffffff;
      --text-muted: #a1a1aa;
      --magenta: #ff007a;
      --magenta-light: #ff3399;
      --border: rgba(255, 0, 122, 0.2);
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      -webkit-font-smoothing: antialiased;
    }

    html {
      scroll-behavior: smooth;
      background-color: var(--bg);
    }

    body {
      background-color: var(--bg);
      color: var(--text);
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
      line-height: 1.7;
      overflow-x: hidden;
    }

    ::selection {
      background-color: var(--magenta);
      color: #ffffff;
    }

    /* Fixed Navbar */
    .navbar {
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 65px;
      background-color: var(--bg-header);
      backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
      border-bottom: 2px solid var(--magenta);
      display: grid;
      grid-template-columns: 1fr auto 1fr;
      align-items: center;
      padding: 0 30px;
      z-index: 1000;
    }

    .burger-icon {
      cursor: pointer;
      display: flex;
      flex-direction: column;
      gap: 5px;
      width: 26px;
      padding: 4px 0;
      background: none;
      border: none;
    }

    .burger-icon span {
      display: block;
      width: 100%;
      height: 2px;
      background-color: var(--magenta);
    }

    .nav-brand {
      font-size: 1.4rem;
      font-weight: 900;
      letter-spacing: 0.2em;
      text-transform: uppercase;
      color: var(--magenta);
      text-decoration: none;
      text-align: center;
    }

    .nav-spacer { width: 26px; }

    /* Drawer */
    .drawer-overlay {
      position: fixed;
      inset: 0;
      background: rgba(0, 0, 0, 0.7);
      z-index: 1100;
      opacity: 0;
      pointer-events: none;
      transition: opacity 0.3s ease;
    }
    .drawer-overlay.active {
      opacity: 1;
      pointer-events: auto;
    }

    .drawer {
      position: fixed;
      top: 0;
      left: -340px;
      width: min(320px, 85vw);
      height: 100vh;
      background-color: #141418;
      border-right: 2px solid var(--magenta);
      z-index: 1200;
      padding: 30px 24px;
      display: flex;
      flex-direction: column;
      transition: left 0.3s ease;
      overflow-y: auto;
    }
    .drawer.active { left: 0; }

    .drawer-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 24px;
      padding-bottom: 12px;
      border-bottom: 1px solid var(--border);
    }

    .drawer-title {
      font-size: 0.85rem;
      font-weight: 800;
      letter-spacing: 0.15em;
      text-transform: uppercase;
      color: var(--magenta);
    }

    .drawer-close {
      background: none;
      border: none;
      color: var(--magenta);
      font-size: 1.6rem;
      cursor: pointer;
      line-height: 1;
    }

    .drawer-nav {
      list-style: none;
      display: flex;
      flex-direction: column;
      gap: 10px;
    }

    .drawer-nav a {
      color: #ffffff;
      text-decoration: none;
      font-size: 1rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.04em;
      display: block;
      padding: 6px 0;
      transition: color 0.2s;
    }

    .drawer-nav a:hover {
      color: var(--magenta);
    }

    /* FULL BLEED HERO COVER (Geht komplett an die Ränder) */
    .hero-fullbleed {
      margin-top: 65px;
      width: 100%;
      max-height: 80vh;
      overflow: hidden;
      display: flex;
      justify-content: center;
      align-items: center;
      background-color: #000;
      border-bottom: 3px solid var(--magenta);
    }

    .hero-fullbleed img {
      width: 100%;
      height: 100%;
      max-height: 80vh;
      object-fit: cover;
      object-position: center 30%;
      display: block;
    }

    /* Main Container (Fokus auf die 12 Tracks) */
    .page-container {
      max-width: 1350px;
      margin: 0 auto;
      padding: 70px 30px 140px 30px;
    }

    /* Track Block (2 Spalten: Links Songtext, Rechts Interpretation) */
    .track-block {
      margin-bottom: 140px;
      padding-bottom: 100px;
      border-bottom: 1px solid var(--border);
      scroll-margin-top: 90px;
    }

    .track-heading {
      font-size: clamp(2.2rem, 5vw, 3.5rem);
      font-weight: 900;
      text-transform: uppercase;
      letter-spacing: 0.04em;
      margin-bottom: 40px;
      color: var(--magenta);
      display: flex;
      align-items: baseline;
      gap: 16px;
    }

    .track-heading .num {
      color: #ffffff;
      font-size: 0.8em;
    }

    .track-grid {
      display: grid;
      grid-template-columns: 1fr 1.35fr;
      gap: 60px;
      align-items: start;
    }

    /* Linke Spalte: Songtext */
    .lyrics-col {
      border-right: 2px solid var(--border);
      padding-right: 45px;
    }

    .col-header {
      font-size: 0.9rem;
      font-weight: 900;
      letter-spacing: 0.18em;
      text-transform: uppercase;
      color: var(--magenta);
      margin-bottom: 28px;
      padding-bottom: 8px;
      border-bottom: 2px solid var(--magenta);
    }

    .lyrics-content {
      font-size: 1.18rem;
      line-height: 2.15;
      color: #ffffff;
      white-space: pre-line;
      font-weight: 400;
    }

    .lyrics-content .verse-header {
      font-size: 0.85rem;
      font-weight: 800;
      color: var(--magenta);
      margin: 32px 0 10px 0;
      display: block;
      text-transform: uppercase;
      letter-spacing: 0.1em;
    }

    /* Rechte Spalte: Interpretation & Analyse */
    .analysis-col {
      color: #e4e4e7;
    }

    /* Typography */
    .md-text h1 {
      font-size: 2rem;
      font-weight: 900;
      text-transform: uppercase;
      color: var(--magenta);
      margin-bottom: 24px;
    }

    .md-text h2 {
      font-size: 1.4rem;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.02em;
      color: #ffffff;
      margin: 40px 0 16px 0;
      border-left: 4px solid var(--magenta);
      padding-left: 14px;
    }

    .md-text h3 {
      font-size: 1.15rem;
      font-weight: 700;
      text-transform: uppercase;
      color: var(--magenta);
      margin: 32px 0 14px 0;
    }

    .md-text h4 {
      font-size: 1rem;
      font-weight: 700;
      color: #ffffff;
      text-transform: uppercase;
      margin: 24px 0 8px 0;
    }

    .md-text p {
      font-size: 1.08rem;
      line-height: 1.85;
      color: #e4e4e7;
      margin-bottom: 22px;
    }

    .md-text strong {
      color: #ffffff;
      font-weight: 700;
    }

    .md-text em {
      color: var(--magenta-light);
      font-style: italic;
    }

    .md-text blockquote {
      border-left: 3px solid var(--magenta);
      padding: 14px 0 14px 22px;
      margin: 28px 0;
      font-size: 1.2rem;
      font-style: italic;
      color: #ffffff;
      background: rgba(255, 0, 122, 0.05);
    }

    .md-text hr {
      border: 0;
      height: 1px;
      background: var(--border);
      margin: 48px 0;
    }

    /* Responsive */
    @media (max-width: 960px) {
      .track-grid {
        grid-template-columns: 1fr;
        gap: 45px;
      }
      .lyrics-col {
        border-right: none;
        padding-right: 0;
        border-bottom: 2px solid var(--border);
        padding-bottom: 45px;
      }
      .page-container {
        padding: 40px 18px 100px 18px;
      }
      .navbar {
        padding: 0 18px;
      }
    }
  </style>
</head>
<body>

  <!-- Top Navbar -->
  <nav class="navbar">
    <button class="burger-icon" onclick="toggleDrawer()" aria-label="Tracklist">
      <span></span>
      <span></span>
      <span></span>
    </button>
    
    <a href="#" class="nav-brand">TOMORA</a>
    
    <div class="nav-spacer"></div>
  </nav>

  <!-- Track Inhaltsverzeichnis (Burger Drawer) -->
  <div class="drawer-overlay" id="drawerOverlay" onclick="toggleDrawer()"></div>
  <aside class="drawer" id="drawer">
    <div class="drawer-header">
      <div class="drawer-title">12 TRACKS</div>
      <button class="drawer-close" onclick="toggleDrawer()">&times;</button>
    </div>
    <ul class="drawer-nav" id="drawerTrackLinks">
      <!-- Injected via JS -->
    </ul>
  </aside>

  <!-- Full-Bleed Cover Bild (Geht komplett an die Ränder) -->
  <header class="hero-fullbleed">
    <img src="[[HERO_IMG]]" alt="TOMORA Artwork">
  </header>

  <!-- Hauptbereich: Direkt die 12 Tracks hintereinander weg -->
  <main class="page-container" id="tracksContainer">
    <!-- Injected via JS -->
  </main>

  <script>
    const tracks = [[TRACKS_DATA]];

    function toggleDrawer() {
      document.getElementById('drawer').classList.toggle('active');
      document.getElementById('drawerOverlay').classList.toggle('active');
    }

    function formatLyrics(rawLyrics) {
      if (!rawLyrics) return '<p style="color: var(--text-muted);">Kein Songtext vorhanden.</p>';
      const lines = rawLyrics.split('\n');
      let html = '';
      lines.forEach(line => {
        const trimmed = line.trim();
        if (trimmed.startsWith('[') && trimmed.endsWith(']')) {
          html += `<span class="verse-header">${trimmed}</span>`;
        } else if (trimmed === '') {
          html += '<br/>';
        } else {
          html += `<div>${trimmed}</div>`;
        }
      });
      return html;
    }

    function renderMarkdown(md) {
      if (window.marked && typeof window.marked.parse === 'function') {
        return window.marked.parse(md);
      }
      return md
        .replace(/^### (.*$)/gim, '<h3>$1</h3>')
        .replace(/^## (.*$)/gim, '<h2>$1</h2>')
        .replace(/^# (.*$)/gim, '<h1>$1</h1>')
        .replace(/^\> (.*$)/gim, '<blockquote>$1</blockquote>')
        .replace(/\*\*(.*)\*\*/gim, '<strong>$1</strong>')
        .replace(/\*(.*)\*/gim, '<em>$1</em>')
        .replace(/\n\n/gim, '</p><p>');
    }

    const container = document.getElementById('tracksContainer');
    const drawerLinks = document.getElementById('drawerTrackLinks');

    tracks.forEach(track => {
      // Drawer Nav Link
      const li = document.createElement('li');
      li.innerHTML = `<a href="#track-${track.num}" onclick="toggleDrawer()">${track.num}. ${track.title}</a>`;
      drawerLinks.appendChild(li);

      // Track Section
      const sec = document.createElement('section');
      sec.className = 'track-block';
      sec.id = 'track-' + track.num;

      sec.innerHTML = `
        <h2 class="track-heading">
          <span class="num">${track.num}.</span> ${track.title}
        </h2>
        <div class="track-grid">
          <!-- Links: Songtext -->
          <div class="lyrics-col">
            <div class="col-header">Songtext / Lyrics</div>
            <div class="lyrics-content">${formatLyrics(track.lyrics)}</div>
          </div>
          <!-- Rechts: Interpretation & Analyse -->
          <div class="analysis-col">
            <div class="col-header">Interpretation & Tiefenanalyse</div>
            <div class="md-text">
              ${renderMarkdown(track.review)}
              ${track.analysis ? '<hr/>' + renderMarkdown(track.analysis) : ''}
            </div>
          </div>
        </div>
      `;

      container.appendChild(sec);
    });
  </script>
</body>
</html>
"""

html_final = html_template.replace('[[HERO_IMG]]', img_src)
html_final = html_final.replace('[[TRACKS_DATA]]', json.dumps(tracks))

with open('c:/Users/Hakan/Documents/antigravity/modest-meitner/ALBUM_REVIEW_READER.html', 'w', encoding='utf-8') as f:
    f.write(html_final)

with open('c:/Users/Hakan/Documents/antigravity/modest-meitner/album_review_und_interpretation/index.html', 'w', encoding='utf-8') as f:
    f.write(html_final)

print("Updated perfectly to user specifications!")
