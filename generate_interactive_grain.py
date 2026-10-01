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
                
    lyrics_raw = ""
    micro_analysis = ""
    if os.path.exists(p1_path):
        with open(p1_path, 'r', encoding='utf-8', errors='ignore') as f:
            p1_content = f.read()
        lyrics_match = re.search(r'### 1\.\s*Transkribierter Textkorpus\s*```text(.*?)```', p1_content, re.DOTALL)
        lyrics_raw = lyrics_match.group(1).strip() if lyrics_match else ""
        analysis_parts = re.split(r'### 2\.\s*Zeile-f[^\n]*\n', p1_content)
        micro_analysis = analysis_parts[1].strip() if len(analysis_parts) > 1 else ""

    review_content = ""
    for rf in os.listdir(review_dir):
        if rf.startswith(num_str) and rf.endswith('.md'):
            with open(os.path.join(review_dir, rf), 'r', encoding='utf-8', errors='ignore') as f:
                review_content = f.read()
            break

    # Structure Lyrics into interactive Stanzas
    stanzas = []
    current_stanza = {"title": "", "lines": []}
    for line in lyrics_raw.split('\n'):
        line_s = line.strip()
        if line_s.startswith('[') and line_s.endswith(']'):
            if current_stanza["lines"]:
                stanzas.append(current_stanza)
            current_stanza = {"title": line_s, "lines": []}
        elif line_s:
            current_stanza["lines"].append(line_s)
        else:
            if current_stanza["lines"]:
                stanzas.append(current_stanza)
                current_stanza = {"title": "", "lines": []}
    if current_stanza["lines"]:
        stanzas.append(current_stanza)

    # Structure Micro Analysis into separate line-by-line cards
    analysis_cards = []
    blocks = re.split(r'\n(?=####\s+)', micro_analysis)
    for b in blocks:
        b = b.strip()
        if not b:
            continue
        title_m = re.match(r'####\s+`?([^`\n]+)`?', b)
        card_title = title_m.group(1).strip() if title_m else ""
        body = re.sub(r'####\s+[^\n]+\n', '', b).strip()
        if card_title or body:
            analysis_cards.append({
                "quote": card_title,
                "body": body
            })

    tracks.append({
        "num": num_str,
        "title": title,
        "stanzas": stanzas,
        "review": review_content,
        "analysis_cards": analysis_cards
    })

html_template = r"""<!DOCTYPE html>
<html lang="de">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>TOMORA — Lyrics & Analysis</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
  <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
  <style>
    :root {
      --bg: #0d0d10;
      --bg-surface: #141418;
      --text: #ffffff;
      --text-muted: #8e8e93;
      --magenta: #ff007a;
      --magenta-dim: rgba(255, 0, 122, 0.12);
      --magenta-glow: rgba(255, 0, 122, 0.3);
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
      line-height: 1.65;
      overflow-x: hidden;
      position: relative;
    }

    /* Subtiler analoger Film-Noise Overlay für organische Tiefe */
    body::before {
      content: "";
      position: fixed;
      inset: 0;
      width: 100vw;
      height: 100vh;
      pointer-events: none;
      z-index: 9999;
      opacity: 0.035;
      background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)'/%3E%3C/svg%3E");
    }

    ::selection {
      background-color: var(--magenta);
      color: #ffffff;
    }

    /* Minimalistische Navbar ohne harte Striche */
    .navbar {
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 65px;
      background: rgba(13, 13, 16, 0.85);
      backdrop-filter: blur(20px);
      -webkit-backdrop-filter: blur(20px);
      display: grid;
      grid-template-columns: 1fr auto 1fr;
      align-items: center;
      padding: 0 32px;
      z-index: 1000;
    }

    .burger-icon {
      cursor: pointer;
      display: flex;
      flex-direction: column;
      gap: 6px;
      width: 24px;
      padding: 4px 0;
      background: none;
      border: none;
    }

    .burger-icon span {
      display: block;
      width: 100%;
      height: 2px;
      background-color: #ffffff;
      transition: all 0.2s;
    }

    .burger-icon:hover span {
      background-color: var(--magenta);
    }

    .nav-brand {
      font-size: 1.4rem;
      font-weight: 900;
      letter-spacing: 0.25em;
      text-transform: uppercase;
      color: var(--magenta);
      text-decoration: none;
      text-align: center;
    }

    .nav-spacer { width: 24px; }

    /* Inhaltsverzeichnis (Drawer) */
    .drawer-overlay {
      position: fixed;
      inset: 0;
      background: rgba(0, 0, 0, 0.75);
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
      left: -340px;
      width: min(320px, 85vw);
      height: 100vh;
      background-color: #111115;
      z-index: 1200;
      padding: 36px 28px;
      display: flex;
      flex-direction: column;
      transition: left 0.35s cubic-bezier(0.16, 1, 0.3, 1);
      overflow-y: auto;
    }
    .drawer.active { left: 0; }

    .drawer-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 30px;
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
      color: #ffffff;
      font-size: 1.6rem;
      cursor: pointer;
      line-height: 1;
    }

    .drawer-nav {
      list-style: none;
      display: flex;
      flex-direction: column;
      gap: 12px;
    }

    .drawer-nav a {
      color: var(--text-muted);
      text-decoration: none;
      font-size: 1rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      display: block;
      padding: 4px 0;
      transition: all 0.2s;
    }

    .drawer-nav a:hover {
      color: #ffffff;
      padding-left: 6px;
    }

    /* FULL BLEED HERO ARTWORK (Kantenbündig) */
    .hero-fullbleed {
      margin-top: 65px;
      width: 100%;
      max-height: 75vh;
      overflow: hidden;
      display: flex;
      justify-content: center;
      align-items: center;
      background-color: #000000;
    }

    .hero-fullbleed img {
      width: 100%;
      height: 100%;
      max-height: 75vh;
      object-fit: cover;
      object-position: center 25%;
      display: block;
    }

    /* Content Area */
    .page-container {
      max-width: 1380px;
      margin: 0 auto;
      padding: 80px 32px 140px 32px;
    }

    /* Track Block */
    .track-block {
      margin-bottom: 160px;
      scroll-margin-top: 90px;
    }

    .track-heading {
      font-size: clamp(2.4rem, 5.5vw, 3.8rem);
      font-weight: 900;
      text-transform: uppercase;
      letter-spacing: 0.04em;
      margin-bottom: 48px;
      color: var(--magenta);
      display: flex;
      align-items: baseline;
      gap: 16px;
    }

    .track-heading .num {
      color: #ffffff;
      font-size: 0.75em;
    }

    /* 2 Spalten: Links Songtext, Rechts Analyse */
    .track-grid {
      display: grid;
      grid-template-columns: 1fr 1.35fr;
      gap: 70px;
      align-items: start;
    }

    /* Songtext Spalte (Klickbare Zeilen) */
    .lyrics-col {
      padding-right: 20px;
    }

    .col-header {
      font-size: 0.85rem;
      font-weight: 900;
      letter-spacing: 0.2em;
      text-transform: uppercase;
      color: var(--magenta);
      margin-bottom: 24px;
    }

    .stanza-block {
      margin-bottom: 32px;
    }

    .stanza-title {
      font-size: 0.8rem;
      font-weight: 800;
      color: var(--magenta);
      text-transform: uppercase;
      letter-spacing: 0.12em;
      margin-bottom: 10px;
      opacity: 0.85;
    }

    .lyric-line {
      font-size: 1.18rem;
      line-height: 1.9;
      color: #f4f4f5;
      padding: 3px 8px;
      margin: 2px -8px;
      border-radius: 4px;
      cursor: pointer;
      transition: all 0.2s ease;
    }

    .lyric-line:hover {
      background: rgba(255, 0, 122, 0.15);
      color: #ffffff;
    }

    .lyric-line.active-line {
      background: var(--magenta);
      color: #ffffff;
      font-weight: 600;
    }

    /* Analyse Spalte */
    .analysis-col {
      display: flex;
      flex-direction: column;
      gap: 28px;
    }

    .review-intro-box {
      font-size: 1.06rem;
      line-height: 1.8;
      color: #d1d1d6;
      margin-bottom: 16px;
    }

    .review-intro-box h1, .review-intro-box h2 {
      display: none; /* Überschrift steht schon drüber */
    }

    .review-intro-box p {
      margin-bottom: 18px;
    }

    .review-intro-box strong {
      color: #ffffff;
    }

    /* Einzelne Analyse Cards */
    .analysis-card {
      background: var(--bg-surface);
      border-radius: 6px;
      padding: 24px 28px;
      transition: all 0.3s ease;
      border-left: 3px solid transparent;
    }

    .analysis-card:hover {
      background: #18181e;
    }

    .analysis-card.highlighted {
      background: #1e1520;
      border-left-color: var(--magenta);
      box-shadow: 0 4px 24px rgba(255, 0, 122, 0.15);
    }

    .card-quote {
      font-size: 1.15rem;
      font-weight: 800;
      color: var(--magenta);
      margin-bottom: 16px;
      letter-spacing: 0.02em;
    }

    .card-body {
      font-size: 1.02rem;
      line-height: 1.75;
      color: #c4c4cc;
    }

    .card-body p {
      margin-bottom: 14px;
    }
    .card-body p:last-child {
      margin-bottom: 0;
    }

    .card-body strong {
      color: #ffffff;
      font-weight: 600;
    }

    .card-body ul {
      margin: 12px 0 12px 18px;
    }

    .card-body li {
      margin-bottom: 10px;
    }

    /* Responsive */
    @media (max-width: 960px) {
      .track-grid {
        grid-template-columns: 1fr;
        gap: 50px;
      }
      .page-container {
        padding: 40px 20px 100px 20px;
      }
      .navbar {
        padding: 0 20px;
      }
    }
  </style>
</head>
<body>

  <!-- Minimalistische Navbar -->
  <nav class="navbar">
    <button class="burger-icon" onclick="toggleDrawer()" aria-label="Menü">
      <span></span>
      <span></span>
      <span></span>
    </button>
    
    <a href="#" class="nav-brand">TOMORA</a>
    
    <div class="nav-spacer"></div>
  </nav>

  <!-- Inhaltsverzeichnis (Burger Drawer) -->
  <div class="drawer-overlay" id="drawerOverlay" onclick="toggleDrawer()"></div>
  <aside class="drawer" id="drawer">
    <div class="drawer-header">
      <div class="drawer-title">12 TRACKS</div>
      <button class="drawer-close" onclick="toggleDrawer()">&times;</button>
    </div>
    <ul class="drawer-nav" id="drawerTrackLinks">
      <!-- Tracks injected via JS -->
    </ul>
  </aside>

  <!-- Full-Bleed Artwork Banner -->
  <header class="hero-fullbleed">
    <img src="[[HERO_IMG]]" alt="TOMORA Artwork">
  </header>

  <!-- Main Content: Alle 12 Tracks -->
  <main class="page-container" id="tracksContainer">
    <!-- Tracks injected via JS -->
  </main>

  <script>
    const tracks = [[TRACKS_DATA]];

    function toggleDrawer() {
      document.getElementById('drawer').classList.toggle('active');
      document.getElementById('drawerOverlay').classList.toggle('active');
    }

    function renderMarkdown(md) {
      if (window.marked && typeof window.marked.parse === 'function') {
        return window.marked.parse(md);
      }
      return md
        .replace(/^### (.*$)/gim, '<h3>$1</h3>')
        .replace(/^## (.*$)/gim, '<h2>$1</h2>')
        .replace(/^# (.*$)/gim, '<h1>$1</h1>')
        .replace(/\*\*(.*)\*\*/gim, '<strong>$1</strong>')
        .replace(/\*(.*)\*/gim, '<em>$1</em>')
        .replace(/\n\n/gim, '</p><p>');
    }

    // Interaktives Highlighting beim Klick auf Lyrics
    function handleLyricClick(trackIdx, lineText, cardIdx = null) {
      // Un-highlight all in this track
      const trackSec = document.getElementById('track-' + tracks[trackIdx].num);
      trackSec.querySelectorAll('.lyric-line').forEach(el => el.classList.remove('active-line'));
      trackSec.querySelectorAll('.analysis-card').forEach(el => el.classList.remove('highlighted'));

      // Highlight clicked line
      event.currentTarget.classList.add('active-line');

      // Find matching card or use index
      const cards = trackSec.querySelectorAll('.analysis-card');
      let targetCard = null;

      if (cardIdx !== null && cards[cardIdx]) {
        targetCard = cards[cardIdx];
      } else {
        // Find by text match
        const cleanSearch = lineText.toLowerCase().replace(/[^a-z0-9]/g, '');
        for (let c of cards) {
          const qText = c.querySelector('.card-quote')?.innerText.toLowerCase().replace(/[^a-z0-9]/g, '') || '';
          if (qText.includes(cleanSearch) || cleanSearch.includes(qText)) {
            targetCard = c;
            break;
          }
        }
      }

      if (!targetCard && cards.length > 0) {
        targetCard = cards[0];
      }

      if (targetCard) {
        targetCard.classList.add('highlighted');
        const offset = 100;
        const bodyRect = document.body.getBoundingClientRect().top;
        const elementRect = targetCard.getBoundingClientRect().top;
        const elementPosition = elementRect - bodyRect;
        const offsetPosition = elementPosition - offset;

        window.scrollTo({
          top: offsetPosition,
          behavior: 'smooth'
        });
      }
    }

    const container = document.getElementById('tracksContainer');
    const drawerLinks = document.getElementById('drawerTrackLinks');

    tracks.forEach((track, tIdx) => {
      // Drawer Link
      const li = document.createElement('li');
      li.innerHTML = `<a href="#track-${track.num}" onclick="toggleDrawer()">${track.num}. ${track.title}</a>`;
      drawerLinks.appendChild(li);

      // Track Section
      const sec = document.createElement('section');
      sec.className = 'track-block';
      sec.id = 'track-' + track.num;

      // Build Stanzas HTML
      let lyricsHtml = '';
      let lineCounter = 0;
      track.stanzas.forEach((stanza) => {
        lyricsHtml += `<div class="stanza-block">`;
        if (stanza.title) {
          lyricsHtml += `<div class="stanza-title">${stanza.title}</div>`;
        }
        stanza.lines.forEach((line) => {
          const cardIdx = Math.min(lineCounter, Math.max(0, track.analysis_cards.length - 1));
          lyricsHtml += `<div class="lyric-line" onclick="handleLyricClick(${tIdx}, '${line.replace(/'/g, "\\'")}', ${cardIdx})">${line}</div>`;
          lineCounter++;
        });
        lyricsHtml += `</div>`;
      });

      // Build Analysis Cards HTML
      let analysisCardsHtml = '';
      track.analysis_cards.forEach((card, cIdx) => {
        analysisCardsHtml += `
          <div class="analysis-card" id="card-${tIdx}-${cIdx}">
            ${card.quote ? `<div class="card-quote">${card.quote}</div>` : ''}
            <div class="card-body">${renderMarkdown(card.body)}</div>
          </div>
        `;
      });

      sec.innerHTML = `
        <h2 class="track-heading">
          <span class="num">${track.num}.</span> ${track.title}
        </h2>
        <div class="track-grid">
          <!-- Links: Songtext (Klickbar) -->
          <div class="lyrics-col">
            <div class="col-header">Songtext / Lyrics</div>
            <div class="lyrics-wrapper">${lyricsHtml}</div>
          </div>
          <!-- Rechts: Interpretation & Analyse -->
          <div class="analysis-col">
            <div class="col-header">Interpretation & Dekonstruktion</div>
            ${track.review ? `<div class="review-intro-box">${renderMarkdown(track.review)}</div>` : ''}
            ${analysisCardsHtml}
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

print("Dynamic interactive grain reader successfully generated!")
