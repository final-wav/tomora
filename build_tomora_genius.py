import json
import base64
import os
import re

# 1. Load Artwork as Base64
img_path = r"C:\Users\Hakan\.gemini\antigravity\brain\5e6e588d-8195-4b9c-a574-5d026ae3847a\.user_uploaded\media_1790875455821.jpg"
with open(img_path, "rb") as f:
    img_b64 = base64.b64encode(f.read()).decode('utf-8')
img_src = f"data:image/jpeg;base64,{img_b64}"

# 2. Extract Phase 1 (Lyrics + Deep Analysis)
phase1_dir = 'album_analyse_fallstudie/Phase_1_Mikro_Dekonstruktion'
review_dir = 'album_review_und_interpretation'

track_files = sorted(os.listdir(phase1_dir))
tracks_data = []

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

for tf in track_files:
    num_match = re.match(r'^(\d+)', tf)
    if not num_match:
        continue
    num_str = num_match.group(1)
    
    # Read Phase 1
    p1_path = os.path.join(phase1_dir, tf)
    with open(p1_path, 'r', encoding='utf-8', errors='ignore') as f:
        p1_content = f.read()
    
    # Extract Lyrics
    lyrics_match = re.search(r'### 1\.\s*Transkribierter Textkorpus\s*```text(.*?)```', p1_content, re.DOTALL)
    lyrics = lyrics_match.group(1).strip() if lyrics_match else ""
    
    # Extract Line-by-Line analysis
    analysis_parts = re.split(r'### 2\.\s*Zeile-f[^\n]*\n', p1_content)
    micro_analysis = analysis_parts[1].strip() if len(analysis_parts) > 1 else ""
    
    # Read Review from review_dir if exists
    review_content = ""
    for rf in os.listdir(review_dir):
        if rf.startswith(num_str) and rf.endswith('.md'):
            with open(os.path.join(review_dir, rf), 'r', encoding='utf-8', errors='ignore') as f:
                review_content = f.read()
            break
            
    track_title = track_names_map.get(num_str, tf.replace('.md', ''))
    
    tracks_data.append({
        "num": num_str,
        "title": track_title,
        "lyrics": lyrics,
        "review": review_content,
        "micro_analysis": micro_analysis
    })

# 3. Read Essays & Macro Chapters
def read_md(path):
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    return ""

essay_content = read_md('album_review_und_interpretation/00_ALBUM_ESSAY_Gesamtreview.md')
epilog_content = read_md('album_review_und_interpretation/13_Epilog_Thematische_Querschnitte.md')
p2_1 = read_md('album_analyse_fallstudie/Phase_2_Makro_Systemarchitektur/01_Narrativer_Bogen_Zusammenbruch_Rekonstruktion.md')
p2_2 = read_md('album_analyse_fallstudie/Phase_2_Makro_Systemarchitektur/02_Systemische_Bruchstellen_und_Zwischenraeume.md')
p3_1 = read_md('album_analyse_fallstudie/Phase_3_Psychologische_Spiegelung_Resonanzraum/01_Analytische_Schutzpanzerung_und_Hypervigilanz.md')
p3_2 = read_md('album_analyse_fallstudie/Phase_3_Psychologische_Spiegelung_Resonanzraum/02_Der_Preis_des_Systems_und_Autonomer_Wiederaufbau.md')

macro_data = {
    "essay": essay_content,
    "epilog": epilog_content,
    "p2_1": p2_1,
    "p2_2": p2_2,
    "p3_1": p3_1,
    "p3_2": p3_2
}

all_app_data = {
    "tracks": tracks_data,
    "macro": macro_data
}

# 4. Generate the Modern Genius-Style HTML Web App
html_code = r"""<!DOCTYPE html>
<html lang="de">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>TOMORA — Album Review & Lyrics Deconstruction</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
  <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
  <style>
    :root {
      --bg: #000000;
      --surface: #0a0a0c;
      --surface-elevated: #111115;
      --surface-card: #141418;
      --magenta: #ff007a;
      --magenta-light: #ff3399;
      --magenta-glow: rgba(255, 0, 122, 0.25);
      --magenta-dim: rgba(255, 0, 122, 0.08);
      --text: #f5f5f7;
      --text-muted: #8e8e93;
      --text-dim: #48484a;
      --border: rgba(255, 255, 255, 0.08);
      --border-light: rgba(255, 255, 255, 0.14);
      --border-magenta: rgba(255, 0, 122, 0.4);
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      -webkit-font-smoothing: antialiased;
    }

    html {
      scroll-behavior: smooth;
    }

    body {
      background-color: var(--bg);
      color: var(--text);
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
      line-height: 1.65;
      overflow-x: hidden;
    }

    ::selection {
      background-color: var(--magenta);
      color: #fff;
    }

    /* Fixed Clean Navbar with Perfect Center */
    .navbar {
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 64px;
      display: grid;
      grid-template-columns: 1fr auto 1fr;
      align-items: center;
      padding: 0 28px;
      background: rgba(0, 0, 0, 0.92);
      backdrop-filter: blur(20px);
      -webkit-backdrop-filter: blur(20px);
      border-bottom: 1px solid var(--border);
      z-index: 1000;
    }

    .nav-left {
      display: flex;
      align-items: center;
      gap: 16px;
    }

    .burger-btn {
      background: none;
      border: none;
      cursor: pointer;
      display: flex;
      flex-direction: column;
      justify-content: center;
      gap: 5px;
      width: 32px;
      height: 32px;
      padding: 4px;
    }

    .burger-btn span {
      display: block;
      height: 2px;
      background: #ffffff;
      transition: all 0.25s ease;
    }

    .burger-btn span:nth-child(1) { width: 22px; }
    .burger-btn span:nth-child(2) { width: 16px; }
    .burger-btn span:nth-child(3) { width: 22px; }

    .burger-btn:hover span {
      background: var(--magenta);
    }
    .burger-btn:hover span:nth-child(2) {
      width: 22px;
    }

    .nav-brand {
      font-weight: 800;
      font-size: 1.15rem;
      letter-spacing: 0.22em;
      text-transform: uppercase;
      color: #ffffff;
      text-decoration: none;
      text-align: center;
      user-select: none;
      display: flex;
      align-items: center;
      gap: 8px;
      justify-self: center;
    }

    .nav-brand span.dot {
      width: 6px;
      height: 6px;
      background: var(--magenta);
      border-radius: 50%;
      display: inline-block;
      box-shadow: 0 0 8px var(--magenta);
    }

    .nav-right {
      display: flex;
      justify-content: flex-end;
      align-items: center;
      gap: 12px;
    }

    .nav-pill {
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.75rem;
      font-weight: 500;
      text-transform: uppercase;
      padding: 6px 14px;
      border: 1px solid var(--border);
      background: var(--surface);
      border-radius: 100px;
      color: var(--text-muted);
      cursor: pointer;
      transition: all 0.2s ease;
    }

    .nav-pill:hover {
      border-color: var(--magenta);
      color: #ffffff;
    }

    /* Drawer Sidebar */
    .drawer-overlay {
      position: fixed;
      inset: 0;
      background: rgba(0, 0, 0, 0.8);
      backdrop-filter: blur(8px);
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
      left: -380px;
      width: min(360px, 85vw);
      height: 100vh;
      background: var(--surface);
      border-right: 1px solid var(--border);
      z-index: 1200;
      padding: 28px 24px;
      display: flex;
      flex-direction: column;
      transition: left 0.35s cubic-bezier(0.16, 1, 0.3, 1);
      overflow-y: auto;
    }

    .drawer.active {
      left: 0;
    }

    .drawer-top {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 24px;
      padding-bottom: 16px;
      border-bottom: 1px solid var(--border);
    }

    .drawer-title {
      font-size: 0.85rem;
      font-weight: 700;
      letter-spacing: 0.15em;
      text-transform: uppercase;
      color: var(--text-muted);
    }

    .drawer-close {
      background: none;
      border: none;
      font-size: 1.5rem;
      color: var(--text-muted);
      cursor: pointer;
      line-height: 1;
    }

    .drawer-close:hover {
      color: var(--magenta);
    }

    .drawer-menu-list {
      list-style: none;
      display: flex;
      flex-direction: column;
      gap: 4px;
    }

    .drawer-item a {
      display: flex;
      align-items: center;
      gap: 12px;
      padding: 10px 14px;
      border-radius: 6px;
      color: var(--text-muted);
      text-decoration: none;
      font-size: 0.92rem;
      font-weight: 500;
      transition: all 0.15s ease;
      cursor: pointer;
    }

    .drawer-item a .index-num {
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.75rem;
      color: var(--text-dim);
      min-width: 22px;
    }

    .drawer-item a:hover, .drawer-item.active a {
      background: var(--surface-card);
      color: #ffffff;
    }

    .drawer-item.active a {
      border-left: 2px solid var(--magenta);
    }

    .drawer-item a:hover .index-num, .drawer-item.active a .index-num {
      color: var(--magenta);
    }

    /* Hero Section */
    .hero {
      margin-top: 64px;
      padding: 48px 24px 40px;
      display: flex;
      flex-direction: column;
      align-items: center;
      text-align: center;
      border-bottom: 1px solid var(--border);
      background: radial-gradient(circle at 50% 20%, rgba(255, 0, 122, 0.07) 0%, transparent 60%);
    }

    .hero-artwork {
      width: min(340px, 80vw);
      aspect-ratio: 1 / 1;
      border-radius: 8px;
      overflow: hidden;
      margin-bottom: 28px;
      box-shadow: 0 16px 40px rgba(0, 0, 0, 0.9), 0 0 30px var(--magenta-glow);
      border: 1px solid var(--border-magenta);
    }

    .hero-artwork img {
      width: 100%;
      height: 100%;
      object-fit: cover;
      display: block;
    }

    .hero-pretitle {
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.75rem;
      font-weight: 600;
      letter-spacing: 0.2em;
      text-transform: uppercase;
      color: var(--magenta);
      margin-bottom: 8px;
    }

    .hero-title {
      font-size: clamp(2rem, 4.5vw, 3.2rem);
      font-weight: 900;
      letter-spacing: 0.04em;
      text-transform: uppercase;
      line-height: 1.1;
      margin-bottom: 12px;
    }

    .hero-subtitle {
      font-size: 1.05rem;
      color: var(--text-muted);
      max-width: 600px;
      margin-bottom: 28px;
    }

    /* Navigation Bar for Views */
    .view-selector {
      display: flex;
      gap: 10px;
      justify-content: center;
      flex-wrap: wrap;
      margin-bottom: 10px;
    }

    .view-btn {
      background: var(--surface);
      border: 1px solid var(--border);
      color: var(--text-muted);
      padding: 10px 22px;
      border-radius: 100px;
      font-size: 0.88rem;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.2s ease;
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .view-btn:hover {
      color: #fff;
      border-color: var(--border-light);
    }

    .view-btn.active {
      background: #ffffff;
      color: #000000;
      border-color: #ffffff;
    }

    /* Track Navigation Bar */
    .track-strip-wrap {
      position: sticky;
      top: 64px;
      background: rgba(0, 0, 0, 0.95);
      backdrop-filter: blur(16px);
      border-bottom: 1px solid var(--border);
      z-index: 900;
      padding: 12px 20px;
      overflow-x: auto;
      white-space: nowrap;
    }

    .track-strip {
      display: inline-flex;
      gap: 8px;
      max-width: 1300px;
      margin: 0 auto;
    }

    .track-pill {
      background: var(--surface);
      border: 1px solid var(--border);
      color: var(--text-muted);
      padding: 8px 16px;
      border-radius: 100px;
      font-size: 0.82rem;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.2s ease;
      display: inline-flex;
      align-items: center;
      gap: 8px;
      text-transform: uppercase;
    }

    .track-pill .p-num {
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.72rem;
      color: var(--text-dim);
    }

    .track-pill:hover {
      color: #fff;
      border-color: var(--border-light);
    }

    .track-pill.active {
      background: var(--magenta);
      border-color: var(--magenta);
      color: #ffffff;
    }
    .track-pill.active .p-num {
      color: rgba(255, 255, 255, 0.7);
    }

    /* Main Container */
    .main-wrapper {
      max-width: 1400px;
      margin: 0 auto;
      padding: 40px 24px 120px;
    }

    /* GENIUS STYLE SPLIT VIEW */
    .genius-layout {
      display: grid;
      grid-template-columns: 1fr 1.2fr;
      gap: 40px;
      align-items: start;
    }

    .column-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding-bottom: 14px;
      margin-bottom: 24px;
      border-bottom: 2px solid var(--border);
    }

    .column-title {
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.82rem;
      letter-spacing: 0.14em;
      text-transform: uppercase;
      font-weight: 700;
      color: var(--magenta);
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .column-badge {
      font-size: 0.75rem;
      color: var(--text-dim);
      font-family: 'JetBrains Mono', monospace;
    }

    /* LYRICS COLUMN (LEFT) */
    .lyrics-card {
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 32px 28px;
    }

    .lyrics-body {
      font-size: 1.15rem;
      line-height: 2.1;
      color: var(--text);
      font-weight: 400;
      white-space: pre-line;
      letter-spacing: 0.01em;
    }

    .lyrics-body .section-marker {
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.78rem;
      font-weight: 700;
      text-transform: uppercase;
      color: var(--magenta);
      margin: 28px 0 10px 0;
      display: block;
      letter-spacing: 0.1em;
      border-bottom: 1px solid rgba(255, 0, 122, 0.2);
      padding-bottom: 4px;
    }

    /* ANALYSIS COLUMN (RIGHT) */
    .analysis-card {
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 32px 32px;
    }

    .track-meta-title {
      font-size: 1.8rem;
      font-weight: 900;
      text-transform: uppercase;
      letter-spacing: 0.02em;
      margin-bottom: 20px;
      color: #ffffff;
      display: flex;
      align-items: center;
      gap: 12px;
    }

    .md-render h1 {
      font-size: 1.6rem;
      font-weight: 800;
      margin: 32px 0 16px;
      color: #fff;
    }

    .md-render h2 {
      font-size: 1.25rem;
      font-weight: 700;
      margin: 36px 0 16px;
      color: #fff;
      display: flex;
      align-items: center;
      gap: 10px;
    }

    .md-render h2::before {
      content: '';
      display: inline-block;
      width: 4px;
      height: 1.1em;
      background: var(--magenta);
      border-radius: 2px;
    }

    .md-render h3 {
      font-size: 1.05rem;
      font-weight: 700;
      color: var(--magenta);
      margin: 28px 0 12px;
    }

    .md-render h4 {
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.9rem;
      font-weight: 700;
      color: var(--magenta-light);
      margin: 24px 0 8px;
      padding: 6px 12px;
      background: var(--magenta-dim);
      border-radius: 4px;
      display: inline-block;
    }

    .md-render p {
      font-size: 1.04rem;
      color: #d1d1d6;
      line-height: 1.8;
      margin-bottom: 20px;
    }

    .md-render strong {
      color: #ffffff;
      font-weight: 700;
    }

    .md-render em {
      color: #e5e5ea;
      font-style: italic;
    }

    .md-render blockquote {
      background: var(--surface-card);
      border-left: 3px solid var(--magenta);
      padding: 16px 20px;
      margin: 24px 0;
      font-size: 1.08rem;
      font-style: italic;
      color: #ffffff;
      border-radius: 0 6px 6px 0;
    }

    .md-render ul, .md-render ol {
      margin: 16px 0 24px 20px;
      color: #d1d1d6;
    }

    .md-render li {
      margin-bottom: 10px;
      line-height: 1.7;
    }

    .md-render hr {
      border: 0;
      height: 1px;
      background: var(--border);
      margin: 40px 0;
    }

    /* FULL ARTICLE VIEW (FOR ESSAY / MACRO CHAPTERS) */
    .article-view-wrap {
      max-width: 820px;
      margin: 0 auto;
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 48px 40px;
    }

    /* Responsive Design */
    @media (max-width: 1024px) {
      .genius-layout {
        grid-template-columns: 1fr;
        gap: 32px;
      }
      .main-wrapper {
        padding: 24px 16px 80px;
      }
      .lyrics-card, .analysis-card, .article-view-wrap {
        padding: 24px 20px;
      }
    }

    @media (max-width: 768px) {
      .navbar { padding: 0 16px; }
      .nav-right { display: none; }
      .hero { padding: 32px 16px 32px; }
      .hero-artwork { width: 240px; }
    }
  </style>
</head>
<body>

  <!-- Top Navbar -->
  <nav class="navbar">
    <div class="nav-left">
      <button class="burger-btn" onclick="toggleDrawer()" aria-label="Menü">
        <span></span>
        <span></span>
        <span></span>
      </button>
    </div>
    
    <a href="#" class="nav-brand" onclick="showView('track', 0)">
      <span>TOMORA</span>
      <span class="dot"></span>
    </a>
    
    <div class="nav-right">
      <button class="nav-pill" onclick="showView('essay', 0)">Gesamtreview</button>
      <button class="nav-pill" onclick="toggleDrawer()">12 Tracks</button>
    </div>
  </nav>

  <!-- Side Drawer Menu -->
  <div class="drawer-overlay" id="drawerOverlay" onclick="toggleDrawer()"></div>
  <aside class="drawer" id="drawer">
    <div class="drawer-top">
      <div class="drawer-title">TOMORA — ALBUM GUIDE</div>
      <button class="drawer-close" onclick="toggleDrawer()">&times;</button>
    </div>
    
    <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; color: var(--magenta); margin-bottom: 8px; font-weight: 700; text-transform: uppercase;">
      KAPITEL & ESSAYS
    </div>
    <ul class="drawer-menu-list" style="margin-bottom: 24px;">
      <li class="drawer-item" id="menu-essay"><a onclick="showView('essay', 0); toggleDrawer();"><span class="index-num">00</span> Album Essay & Gesamtreview</a></li>
      <li class="drawer-item" id="menu-p2-1"><a onclick="showView('p2_1', 0); toggleDrawer();"><span class="index-num">M1</span> Makro: Der Narrative Bogen</a></li>
      <li class="drawer-item" id="menu-p2-2"><a onclick="showView('p2_2', 0); toggleDrawer();"><span class="index-num">M2</span> Makro: Systemische Bruchstellen</a></li>
      <li class="drawer-item" id="menu-p3-1"><a onclick="showView('p3_1', 0); toggleDrawer();"><span class="index-num">M3</span> Resonanz: Analytische Schutzpanzerung</a></li>
      <li class="drawer-item" id="menu-p3-2"><a onclick="showView('p3_2', 0); toggleDrawer();"><span class="index-num">M4</span> Resonanz: Autonomer Wiederaufbau</a></li>
      <li class="drawer-item" id="menu-epilog"><a onclick="showView('epilog', 0); toggleDrawer();"><span class="index-num">13</span> Epilog & Thematische Querschnitte</a></li>
    </ul>

    <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; color: var(--magenta); margin-bottom: 8px; font-weight: 700; text-transform: uppercase;">
      TRACK-BY-TRACK (LYRICS & REVIEW)
    </div>
    <ul class="drawer-menu-list" id="drawerTrackList">
      <!-- Tracks injected via JS -->
    </ul>
  </aside>

  <!-- Hero Section -->
  <header class="hero">
    <div class="hero-artwork">
      <img src="[[HERO_IMG_SRC]]" alt="TOMORA Cover">
    </div>
    <div class="hero-pretitle">Tiefenpsychologische Fallstudie & Lyrics-Dekonstruktion</div>
    <h1 class="hero-title">TOMORA</h1>
    <p class="hero-subtitle">Anatomie eines Zusammenbruchs, der infantilen Regressionsfalle und des autonomen Wiederaufbaus.</p>
    
    <div class="view-selector">
      <button class="view-btn active" id="btn-mode-tracks" onclick="showView('track', currentTrackIndex)">🎧 Track-by-Track (Genius Split)</button>
      <button class="view-btn" id="btn-mode-essay" onclick="showView('essay', 0)">📄 Album Essay</button>
      <button class="view-btn" id="btn-mode-epilog" onclick="showView('epilog', 0)">🔬 Epilog & Systemanalyse</button>
    </div>
  </header>

  <!-- Sticky Track Strip (Only for track mode) -->
  <div class="track-strip-wrap" id="trackStripWrap">
    <div class="track-strip" id="trackStrip">
      <!-- Track pills injected via JS -->
    </div>
  </div>

  <!-- Main Content Area -->
  <main class="main-wrapper" id="mainApp">
    <!-- Dynamic View Injected Here -->
  </main>

  <script>
    const appData = [[APP_DATA_JSON]];
    let currentView = 'track';
    let currentTrackIndex = 0;

    function toggleDrawer() {
      document.getElementById('drawer').classList.toggle('active');
      document.getElementById('drawerOverlay').classList.toggle('active');
    }

    function formatLyrics(rawLyrics) {
      if (!rawLyrics) return '<p style="color: var(--text-muted)">Kein transkribierter Songtext vorhanden.</p>';
      
      const lines = rawLyrics.split('\n');
      let html = '';
      
      lines.forEach(line => {
        const trimmed = line.trim();
        if (trimmed.startsWith('[') && trimmed.endsWith(']')) {
          html += `<span class="section-marker">${trimmed}</span>`;
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

    function initNavigation() {
      const drawerList = document.getElementById('drawerTrackList');
      const trackStrip = document.getElementById('trackStrip');

      drawerList.innerHTML = '';
      trackStrip.innerHTML = '';

      appData.tracks.forEach((t, idx) => {
        // Drawer Item
        const li = document.createElement('li');
        li.className = 'drawer-item';
        li.id = 'track-menu-' + idx;
        li.innerHTML = `<a onclick="showView('track', ${idx}); toggleDrawer();"><span class="index-num">${t.num}</span> ${t.title}</a>`;
        drawerList.appendChild(li);

        // Strip Pill
        const pill = document.createElement('button');
        pill.className = 'track-pill' + (idx === 0 ? ' active' : '');
        pill.id = 'track-pill-' + idx;
        pill.innerHTML = `<span class="p-num">${t.num}</span> ${t.title}`;
        pill.onclick = () => showView('track', idx);
        trackStrip.appendChild(pill);
      });
    }

    function showView(viewType, trackIdx = 0) {
      currentView = viewType;
      currentTrackIndex = trackIdx;
      const main = document.getElementById('mainApp');
      const stripWrap = document.getElementById('trackStripWrap');
      
      // Update Button states
      document.querySelectorAll('.view-btn').forEach(b => b.classList.remove('active'));
      document.querySelectorAll('.drawer-item').forEach(b => b.classList.remove('active'));

      if (viewType === 'track') {
        stripWrap.style.display = 'block';
        document.getElementById('btn-mode-tracks').classList.add('active');
        
        // Update pills
        document.querySelectorAll('.track-pill').forEach((p, i) => {
          if (i === trackIdx) p.classList.add('active');
          else p.classList.remove('active');
        });

        const curItem = document.getElementById('track-menu-' + trackIdx);
        if (curItem) curItem.classList.add('active');

        const track = appData.tracks[trackIdx];

        main.innerHTML = `
          <div class="genius-layout">
            <!-- Left: Lyrics -->
            <section class="lyrics-column">
              <div class="column-header">
                <div class="column-title"><span>🎵</span> SONGTEXT / LYRICS</div>
                <div class="column-badge">TRACK ${track.num}</div>
              </div>
              <div class="lyrics-card">
                <div class="lyrics-body">${formatLyrics(track.lyrics)}</div>
              </div>
            </section>

            <!-- Right: Review & Deep Analysis -->
            <section class="analysis-column">
              <div class="column-header">
                <div class="column-title"><span>🧠</span> REVIEW & TIEFENANALYSE</div>
                <div class="column-badge">PSYCHODYNAMISCHE DEKONSTRUKTION</div>
              </div>
              <div class="analysis-card">
                <div class="track-meta-title">${track.num}. ${track.title}</div>
                <div class="md-render">
                  ${renderMarkdown(track.review)}
                  ${track.micro_analysis ? '<hr/>' + renderMarkdown(track.micro_analysis) : ''}
                </div>
              </div>
            </section>
          </div>
        `;
      } else {
        // Essay / Macro views
        stripWrap.style.display = 'none';

        let mdContent = '';
        let titleBadge = '';

        if (viewType === 'essay') {
          document.getElementById('btn-mode-essay').classList.add('active');
          document.getElementById('menu-essay').classList.add('active');
          mdContent = appData.macro.essay;
          titleBadge = 'ALBUM ESSAY // GESAMTREVIEW';
        } else if (viewType === 'epilog') {
          document.getElementById('btn-mode-epilog').classList.add('active');
          document.getElementById('menu-epilog').classList.add('active');
          mdContent = appData.macro.epilog;
          titleBadge = 'EPILOG // THEMATISCHE QUERSCHNITTE';
        } else if (viewType === 'p2_1') {
          document.getElementById('menu-p2-1').classList.add('active');
          mdContent = appData.macro.p2_1;
          titleBadge = 'MAKRO // NARRATIVER BOGEN';
        } else if (viewType === 'p2_2') {
          document.getElementById('menu-p2-2').classList.add('active');
          mdContent = appData.macro.p2_2;
          titleBadge = 'MAKRO // SYSTEMISCHE BRUCHSTELLEN';
        } else if (viewType === 'p3_1') {
          document.getElementById('menu-p3-1').classList.add('active');
          mdContent = appData.macro.p3_1;
          titleBadge = 'PSYCHOLOGISCHE SPIEGELUNG // SCHUTZPANZERUNG';
        } else if (viewType === 'p3_2') {
          document.getElementById('menu-p3-2').classList.add('active');
          mdContent = appData.macro.p3_2;
          titleBadge = 'PSYCHOLOGISCHE SPIEGELUNG // AUTONOMER WIEDERAUFBAU';
        }

        main.innerHTML = `
          <div class="article-view-wrap">
            <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; color: var(--magenta); margin-bottom: 20px; font-weight: 700; letter-spacing: 0.15em;">
              ${titleBadge}
            </div>
            <div class="md-render">
              ${renderMarkdown(mdContent)}
            </div>
          </div>
        `;
      }

      // Scroll to content top
      const targetPos = document.getElementById('mainApp').getBoundingClientRect().top + window.pageYOffset - 140;
      window.scrollTo({ top: Math.max(0, targetPos), behavior: 'smooth' });
    }

    initNavigation();
    showView('track', 0);
  </script>
</body>
</html>
"""

# Replace placeholders safely
html_final = html_code.replace('[[HERO_IMG_SRC]]', img_src)
html_final = html_final.replace('[[APP_DATA_JSON]]', json.dumps(all_app_data))

# Save local files
out_path1 = 'c:/Users/Hakan/Documents/antigravity/modest-meitner/ALBUM_REVIEW_READER.html'
out_path2 = 'c:/Users/Hakan/Documents/antigravity/modest-meitner/album_review_und_interpretation/index.html'

with open(out_path1, 'w', encoding='utf-8') as f:
    f.write(html_final)

with open(out_path2, 'w', encoding='utf-8') as f:
    f.write(html_final)

print("TOMORA Genius-Style Web App erfolgreich generiert!")
