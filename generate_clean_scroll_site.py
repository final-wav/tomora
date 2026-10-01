import json
import base64
import os
import re

# 1. Load User Magenta Artwork Image
img_path = r"C:\Users\Hakan\.gemini\antigravity\brain\5e6e588d-8195-4b9c-a574-5d026ae3847a\.user_uploaded\media_1790875455821.jpg"
with open(img_path, "rb") as f:
    img_b64 = base64.b64encode(f.read()).decode('utf-8')
img_src = f"data:image/jpeg;base64,{img_b64}"

# 2. Extract Phase 1 (Lyrics + Deep Analysis) & Reviews
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
    # Read Phase 1
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

    # Read Editorial Review
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

# 3. Read Essays
def read_file(path):
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    return ""

essay_content = read_file('album_review_und_interpretation/00_ALBUM_ESSAY_Gesamtreview.md')
epilog_content = read_file('album_review_und_interpretation/13_Epilog_Thematische_Querschnitte.md')
p2_1 = read_file('album_analyse_fallstudie/Phase_2_Makro_Systemarchitektur/01_Narrativer_Bogen_Zusammenbruch_Rekonstruktion.md')
p2_2 = read_file('album_analyse_fallstudie/Phase_2_Makro_Systemarchitektur/02_Systemische_Bruchstellen_und_Zwischenraeume.md')
p3_1 = read_file('album_analyse_fallstudie/Phase_3_Psychologische_Spiegelung_Resonanzraum/01_Analytische_Schutzpanzerung_und_Hypervigilanz.md')
p3_2 = read_file('album_analyse_fallstudie/Phase_3_Psychologische_Spiegelung_Resonanzraum/02_Der_Preis_des_Systems_und_Autonomer_Wiederaufbau.md')

data_payload = {
    "tracks": tracks,
    "essay": essay_content,
    "epilog": epilog_content,
    "p2_1": p2_1,
    "p2_2": p2_2,
    "p3_1": p3_1,
    "p3_2": p3_2
}

html_template = r"""<!DOCTYPE html>
<html lang="de">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>TOMORA — Album Review & Lyrics</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
  <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
  <style>
    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      -webkit-font-smoothing: antialiased;
    }

    html {
      scroll-behavior: smooth;
      background-color: #000000;
    }

    body {
      background-color: #000000;
      color: #ffffff;
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      line-height: 1.7;
      overflow-x: hidden;
    }

    ::selection {
      background-color: #ff007a;
      color: #ffffff;
    }

    /* Feste, flache Navbar */
    .navbar {
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 65px;
      background-color: #000000;
      border-bottom: 1px solid rgba(255, 255, 255, 0.1);
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
      background-color: #ffffff;
      transition: background-color 0.2s;
    }

    .burger-icon:hover span {
      background-color: #ff007a;
    }

    .nav-brand {
      font-size: 1.35rem;
      font-weight: 900;
      letter-spacing: 0.18em;
      text-transform: uppercase;
      color: #ffffff;
      text-decoration: none;
      text-align: center;
    }

    .nav-spacer {
      width: 26px;
    }

    /* Schlichte Drawer-Navigation (Inhaltsverzeichnis) */
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
      left: -360px;
      width: min(340px, 85vw);
      height: 100vh;
      background-color: #000000;
      border-right: 1px solid rgba(255, 255, 255, 0.12);
      z-index: 1200;
      padding: 30px 24px;
      display: flex;
      flex-direction: column;
      transition: left 0.3s ease;
      overflow-y: auto;
    }

    .drawer.active {
      left: 0;
    }

    .drawer-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 24px;
      padding-bottom: 12px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    }

    .drawer-title {
      font-size: 0.85rem;
      font-weight: 800;
      letter-spacing: 0.12em;
      text-transform: uppercase;
      color: #a1a1aa;
    }

    .drawer-close {
      background: none;
      border: none;
      color: #ffffff;
      font-size: 1.5rem;
      cursor: pointer;
      line-height: 1;
    }

    .drawer-nav {
      list-style: none;
      display: flex;
      flex-direction: column;
      gap: 8px;
    }

    .drawer-nav a {
      color: #a1a1aa;
      text-decoration: none;
      font-size: 0.95rem;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.04em;
      display: block;
      padding: 6px 0;
      transition: color 0.2s;
    }

    .drawer-nav a:hover {
      color: #ff007a;
    }

    .drawer-nav .section-tag {
      font-size: 0.72rem;
      font-weight: 800;
      color: #ff007a;
      letter-spacing: 0.15em;
      margin: 20px 0 6px 0;
      text-transform: uppercase;
    }

    /* Hero Section (Großes Titelbild) */
    .hero-wrap {
      margin-top: 65px;
      width: 100%;
      padding: 40px 24px 60px 24px;
      display: flex;
      flex-direction: column;
      align-items: center;
      text-align: center;
      border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    }

    .hero-img-container {
      width: min(580px, 92vw);
      margin-bottom: 30px;
    }

    .hero-img-container img {
      width: 100%;
      height: auto;
      display: block;
    }

    .hero-title {
      font-size: clamp(2.5rem, 6vw, 4.5rem);
      font-weight: 900;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      line-height: 1;
      margin-bottom: 12px;
    }

    .hero-subtitle {
      font-size: clamp(1rem, 2vw, 1.25rem);
      font-weight: 500;
      color: #ff007a;
      text-transform: uppercase;
      letter-spacing: 0.12em;
    }

    /* Content Layout */
    .page-container {
      max-width: 1300px;
      margin: 0 auto;
      padding: 60px 24px 140px 24px;
    }

    /* Einzelner Textabschnitt (Essay / Macro) */
    .text-section {
      max-width: 860px;
      margin: 0 auto 100px auto;
      padding-bottom: 80px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.1);
      scroll-margin-top: 90px;
    }

    /* Track Block: 2 Spalten (Links Songtext, Rechts Analyse) */
    .track-block {
      margin-bottom: 120px;
      padding-bottom: 100px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.1);
      scroll-margin-top: 90px;
    }

    .track-heading {
      font-size: clamp(2rem, 4vw, 3rem);
      font-weight: 900;
      text-transform: uppercase;
      letter-spacing: 0.04em;
      margin-bottom: 40px;
      color: #ffffff;
    }

    .track-heading span {
      color: #ff007a;
    }

    .track-grid {
      display: grid;
      grid-template-columns: 1fr 1.3fr;
      gap: 60px;
      align-items: start;
    }

    /* Songtext Spalte (Links) */
    .lyrics-col {
      border-right: 1px solid rgba(255, 255, 255, 0.1);
      padding-right: 40px;
    }

    .col-header {
      font-size: 0.85rem;
      font-weight: 800;
      letter-spacing: 0.15em;
      text-transform: uppercase;
      color: #ff007a;
      margin-bottom: 24px;
      padding-bottom: 8px;
      border-bottom: 1px solid rgba(255, 0, 122, 0.4);
    }

    .lyrics-content {
      font-size: 1.15rem;
      line-height: 2.1;
      color: #f4f4f5;
      white-space: pre-line;
      font-weight: 400;
    }

    .lyrics-content .verse-header {
      font-size: 0.82rem;
      font-weight: 700;
      color: #ff007a;
      margin: 28px 0 8px 0;
      display: block;
      text-transform: uppercase;
      letter-spacing: 0.08em;
    }

    /* Analyse Spalte (Rechts) */
    .analysis-col {
      color: #d4d4d8;
    }

    /* Typografie für Markdown Inhalte */
    .md-text h1 {
      font-size: 2rem;
      font-weight: 900;
      text-transform: uppercase;
      letter-spacing: -0.01em;
      color: #ffffff;
      margin-bottom: 24px;
    }

    .md-text h2 {
      font-size: 1.35rem;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.02em;
      color: #ffffff;
      margin: 40px 0 16px 0;
      border-left: 3px solid #ff007a;
      padding-left: 12px;
    }

    .md-text h3 {
      font-size: 1.1rem;
      font-weight: 700;
      text-transform: uppercase;
      color: #ff007a;
      margin: 30px 0 12px 0;
    }

    .md-text h4 {
      font-size: 0.95rem;
      font-weight: 700;
      color: #ffffff;
      text-transform: uppercase;
      margin: 24px 0 8px 0;
    }

    .md-text p {
      font-size: 1.05rem;
      line-height: 1.8;
      color: #d4d4d8;
      margin-bottom: 20px;
    }

    .md-text strong {
      color: #ffffff;
      font-weight: 700;
    }

    .md-text em {
      color: #ffffff;
      font-style: italic;
    }

    .md-text blockquote {
      border-left: 2px solid #ff007a;
      padding: 12px 0 12px 20px;
      margin: 24px 0;
      font-size: 1.15rem;
      font-style: italic;
      color: #ffffff;
    }

    .md-text ul, .md-text ol {
      margin: 16px 0 24px 20px;
      color: #d4d4d8;
    }

    .md-text li {
      margin-bottom: 8px;
      line-height: 1.7;
    }

    .md-text hr {
      border: 0;
      height: 1px;
      background: rgba(255, 255, 255, 0.1);
      margin: 40px 0;
    }

    /* Responsive */
    @media (max-width: 900px) {
      .track-grid {
        grid-template-columns: 1fr;
        gap: 40px;
      }
      .lyrics-col {
        border-right: none;
        padding-right: 0;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        padding-bottom: 40px;
      }
      .navbar {
        padding: 0 18px;
      }
      .page-container {
        padding: 40px 16px 100px 16px;
      }
    }
  </style>
</head>
<body>

  <!-- Feste Navbar -->
  <nav class="navbar">
    <button class="burger-icon" onclick="toggleDrawer()" aria-label="Inhaltsverzeichnis">
      <span></span>
      <span></span>
      <span></span>
    </button>
    
    <a href="#" class="nav-brand">TOMORA</a>
    
    <div class="nav-spacer"></div>
  </nav>

  <!-- Inhaltsverzeichnis (Burger Menü) -->
  <div class="drawer-overlay" id="drawerOverlay" onclick="toggleDrawer()"></div>
  <aside class="drawer" id="drawer">
    <div class="drawer-header">
      <div class="drawer-title">Inhaltsverzeichnis</div>
      <button class="drawer-close" onclick="toggleDrawer()">&times;</button>
    </div>
    
    <ul class="drawer-nav">
      <div class="section-tag">Allgemein</div>
      <li><a href="#essay" onclick="toggleDrawer()">00. Album Essay</a></li>
      <li><a href="#makro-1" onclick="toggleDrawer()">M1. Der Narrative Bogen</a></li>
      <li><a href="#makro-2" onclick="toggleDrawer()">M2. Systemische Bruchstellen</a></li>
      <li><a href="#resonanz-1" onclick="toggleDrawer()">M3. Analytische Schutzpanzerung</a></li>
      <li><a href="#resonanz-2" onclick="toggleDrawer()">M4. Autonomer Wiederaufbau</a></li>

      <div class="section-tag">Tracks (Lyrics & Analyse)</div>
      <!-- Injected via JS -->
      <div id="drawerTrackLinks"></div>

      <div class="section-tag">Abschluss</div>
      <li><a href="#epilog" onclick="toggleDrawer()">13. Epilog & Querschnitte</a></li>
    </ul>
  </aside>

  <!-- Hero Section -->
  <header class="hero-wrap">
    <div class="hero-img-container">
      <img src="[[HERO_IMG]]" alt="TOMORA Cover">
    </div>
    <h1 class="hero-title">TOMORA</h1>
    <div class="hero-subtitle">Anatomie eines Zusammenbruchs & Wiederaufbaus</div>
  </header>

  <!-- Haupt-Inhalt: Straight nach unten durchscrollen -->
  <main class="page-container">

    <!-- 1. Gesamtreview / Album Essay -->
    <section class="text-section" id="essay">
      <div class="col-header">00 // ALBUM ESSAY & GESAMTREVIEW</div>
      <div class="md-text" id="essayContainer"></div>
    </section>

    <!-- 2. Makro-Systemarchitektur: Narrativer Bogen & Bruchstellen -->
    <section class="text-section" id="makro-1">
      <div class="col-header">MAKRO // DER NARRATIVE BOGEN</div>
      <div class="md-text" id="makro1Container"></div>
    </section>

    <section class="text-section" id="makro-2">
      <div class="col-header">MAKRO // SYSTEMISCHE BRUCHSTELLEN</div>
      <div class="md-text" id="makro2Container"></div>
    </section>

    <section class="text-section" id="resonanz-1">
      <div class="col-header">PSYCHOLOGISCHE SPIEGELUNG // SCHUTZPANZERUNG & HYPERVIGILANZ</div>
      <div class="md-text" id="resonanz1Container"></div>
    </section>

    <section class="text-section" id="resonanz-2">
      <div class="col-header">PSYCHOLOGISCHE SPIEGELUNG // AUTONOMER WIEDERAUFBAU</div>
      <div class="md-text" id="resonanz2Container"></div>
    </section>

    <!-- 3. Alle 12 Tracks hintereinander weg (Split 2 Spalten) -->
    <div id="tracksContainer">
      <!-- Injected via JS -->
    </div>

    <!-- 4. Epilog -->
    <section class="text-section" id="epilog" style="border-bottom: none;">
      <div class="col-header">13 // EPILOG & THEMATISCHE QUERSCHNITTE</div>
      <div class="md-text" id="epilogContainer"></div>
    </section>

  </main>

  <script>
    const data = [[DATA_PAYLOAD]];

    function toggleDrawer() {
      document.getElementById('drawer').classList.toggle('active');
      document.getElementById('drawerOverlay').classList.toggle('active');
    }

    function formatLyrics(rawLyrics) {
      if (!rawLyrics) return '<p style="color: #71717a;">Kein Textkorpus vorhanden.</p>';
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

    // Populate Essays
    document.getElementById('essayContainer').innerHTML = renderMarkdown(data.essay);
    document.getElementById('makro1Container').innerHTML = renderMarkdown(data.p2_1);
    document.getElementById('makro2Container').innerHTML = renderMarkdown(data.p2_2);
    document.getElementById('resonanz1Container').innerHTML = renderMarkdown(data.p3_1);
    document.getElementById('resonanz2Container').innerHTML = renderMarkdown(data.p3_2);
    document.getElementById('epilogContainer').innerHTML = renderMarkdown(data.epilog);

    // Populate Tracks
    const tracksContainer = document.getElementById('tracksContainer');
    const drawerTrackLinks = document.getElementById('drawerTrackLinks');

    data.tracks.forEach(track => {
      // Add to drawer
      const li = document.createElement('li');
      li.innerHTML = `<a href="#track-${track.num}" onclick="toggleDrawer()">${track.num}. ${track.title}</a>`;
      drawerTrackLinks.appendChild(li);

      // Add Track Section
      const sec = document.createElement('section');
      sec.className = 'track-block';
      sec.id = 'track-' + track.num;

      sec.innerHTML = `
        <h2 class="track-heading"><span>${track.num}.</span> ${track.title}</h2>
        <div class="track-grid">
          <!-- Links: Songtext -->
          <div class="lyrics-col">
            <div class="col-header">Songtext / Lyrics</div>
            <div class="lyrics-content">${formatLyrics(track.lyrics)}</div>
          </div>
          <!-- Rechts: Analyse -->
          <div class="analysis-col">
            <div class="col-header">Review & Tiefenanalyse</div>
            <div class="md-text">
              ${renderMarkdown(track.review)}
              ${track.analysis ? '<hr/>' + renderMarkdown(track.analysis) : ''}
            </div>
          </div>
        </div>
      `;

      tracksContainer.appendChild(sec);
    });
  </script>
</body>
</html>
"""

html_final = html_template.replace('[[HERO_IMG]]', img_src)
html_final = html_final.replace('[[DATA_PAYLOAD]]', json.dumps(data_payload))

# Write files
with open('c:/Users/Hakan/Documents/antigravity/modest-meitner/ALBUM_REVIEW_READER.html', 'w', encoding='utf-8') as f:
    f.write(html_final)

with open('c:/Users/Hakan/Documents/antigravity/modest-meitner/album_review_und_interpretation/index.html', 'w', encoding='utf-8') as f:
    f.write(html_final)

print("Perfekt generiert!")
