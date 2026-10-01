import json
import base64
import os
import re

# Load and sort review data
with open('album_review_und_interpretation/all_md_data.json', 'r', encoding='utf-8-sig') as f:
    raw_data = json.load(f)

# Sort properly by prefix number (00, 01, ... 13)
def extract_num(item):
    match = re.match(r'^(\d+)', item['name'])
    return int(match.group(1)) if match else 99

review_data = sorted(raw_data, key=extract_num)

# Load user hero artwork image as base64
img_path = r"C:\Users\Hakan\.gemini\antigravity\brain\5e6e588d-8195-4b9c-a574-5d026ae3847a\.user_uploaded\media_1790875455821.jpg"
with open(img_path, "rb") as f:
    img_b64 = base64.b64encode(f.read()).decode('utf-8')
img_src = f"data:image/jpeg;base64,{img_b64}"

html_content = r"""<!DOCTYPE html>
<html lang="de">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>MODEST MEITNER — Album Review & Interpretation</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;1,400;1,600&family=Syne:wght@700;800;900&family=Space+Mono:ital,wght@0,400;0,700;1,400&display=swap" rel="stylesheet">
  <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
  <style>
    :root {
      --bg-black: #060608;
      --bg-surface: #0e0e12;
      --bg-elevated: #16161c;
      --magenta: #ff007a;
      --magenta-dim: rgba(255, 0, 122, 0.12);
      --magenta-glow: rgba(255, 0, 122, 0.25);
      --text-white: #fcfcfd;
      --text-muted: #8e8e9a;
      --text-dim: #52525e;
      --border: rgba(255, 255, 255, 0.08);
      --border-magenta: rgba(255, 0, 122, 0.3);
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      -webkit-font-smoothing: antialiased;
      -moz-osx-font-smoothing: grayscale;
    }

    html {
      scroll-behavior: smooth;
    }

    body {
      background-color: var(--bg-black);
      color: var(--text-white);
      font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
      overflow-x: hidden;
      line-height: 1.7;
    }

    /* Selection */
    ::selection {
      background: var(--magenta);
      color: #fff;
    }

    /* Top Sticky Navigation Bar */
    .nav {
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 72px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 32px;
      background: rgba(6, 6, 8, 0.88);
      backdrop-filter: blur(20px);
      -webkit-backdrop-filter: blur(20px);
      border-bottom: 1px solid var(--border);
      z-index: 1000;
      transition: all 0.3s ease;
    }

    .nav-left {
      display: flex;
      align-items: center;
      gap: 16px;
      width: 160px;
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
      background: var(--text-white);
      border-radius: 2px;
      transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    }

    .burger-btn span:nth-child(1) { width: 24px; }
    .burger-btn span:nth-child(2) { width: 18px; }
    .burger-btn span:nth-child(3) { width: 24px; }

    .burger-btn:hover span {
      background: var(--magenta);
    }

    .burger-btn:hover span:nth-child(2) {
      width: 24px;
    }

    .nav-brand {
      font-family: 'Syne', sans-serif;
      font-weight: 900;
      font-size: 1.25rem;
      letter-spacing: 0.12em;
      text-transform: uppercase;
      color: var(--text-white);
      text-decoration: none;
      text-align: center;
      flex: 1;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 10px;
    }

    .nav-brand .dot {
      width: 7px;
      height: 7px;
      background: var(--magenta);
      border-radius: 50%;
      box-shadow: 0 0 10px var(--magenta);
    }

    .nav-right {
      width: 160px;
      display: flex;
      justify-content: flex-end;
      align-items: center;
    }

    .nav-badge {
      font-family: 'Space Mono', monospace;
      font-size: 0.75rem;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      padding: 6px 14px;
      border: 1px solid var(--border);
      border-radius: 100px;
      color: var(--text-muted);
      background: var(--bg-surface);
    }

    /* Side Drawer / Menu */
    .drawer-overlay {
      position: fixed;
      inset: 0;
      background: rgba(0, 0, 0, 0.75);
      backdrop-filter: blur(8px);
      z-index: 1100;
      opacity: 0;
      pointer-events: none;
      transition: opacity 0.35s ease;
    }

    .drawer-overlay.active {
      opacity: 1;
      pointer-events: auto;
    }

    .drawer {
      position: fixed;
      top: 0;
      left: -420px;
      width: min(400px, 90vw);
      height: 100vh;
      background: var(--bg-surface);
      border-right: 1px solid var(--border);
      z-index: 1200;
      padding: 36px 28px;
      display: flex;
      flex-direction: column;
      transition: left 0.4s cubic-bezier(0.16, 1, 0.3, 1);
      overflow-y: auto;
    }

    .drawer.active {
      left: 0;
    }

    .drawer-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 32px;
      padding-bottom: 20px;
      border-bottom: 1px solid var(--border);
    }

    .drawer-title {
      font-family: 'Syne', sans-serif;
      font-weight: 800;
      font-size: 1.1rem;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      color: var(--text-white);
    }

    .drawer-close {
      background: none;
      border: none;
      color: var(--text-muted);
      font-size: 1.6rem;
      line-height: 1;
      cursor: pointer;
      padding: 4px;
      transition: color 0.2s;
    }

    .drawer-close:hover {
      color: var(--magenta);
    }

    .tracklist {
      list-style: none;
      display: flex;
      flex-direction: column;
      gap: 6px;
    }

    .track-item a {
      display: flex;
      align-items: baseline;
      gap: 14px;
      padding: 12px 14px;
      border-radius: 8px;
      text-decoration: none;
      color: var(--text-muted);
      font-size: 0.95rem;
      font-weight: 500;
      transition: all 0.2s ease;
    }

    .track-item a .num {
      font-family: 'Space Mono', monospace;
      font-size: 0.75rem;
      color: var(--text-dim);
      min-width: 24px;
    }

    .track-item a:hover {
      background: var(--magenta-dim);
      color: var(--text-white);
      transform: translateX(4px);
    }

    .track-item a:hover .num {
      color: var(--magenta);
    }

    /* Hero Section */
    .hero {
      margin-top: 72px;
      padding: 48px 24px 72px;
      display: flex;
      flex-direction: column;
      align-items: center;
      text-align: center;
      position: relative;
      background: radial-gradient(circle at 50% 30%, rgba(255, 0, 122, 0.08) 0%, transparent 70%);
      border-bottom: 1px solid var(--border);
    }

    .hero-artwork-wrap {
      position: relative;
      width: min(520px, 92vw);
      aspect-ratio: 1 / 1;
      margin: 0 auto 36px;
      border-radius: 12px;
      overflow: hidden;
      border: 1px solid var(--border);
      box-shadow: 0 20px 60px rgba(0, 0, 0, 0.8), 0 0 40px var(--magenta-dim);
    }

    .hero-artwork {
      width: 100%;
      height: 100%;
      object-fit: cover;
      display: block;
      filter: contrast(1.05) saturate(1.1);
      transition: transform 0.6s cubic-bezier(0.16, 1, 0.3, 1);
    }

    .hero-artwork-wrap:hover .hero-artwork {
      transform: scale(1.02);
    }

    .hero-tag {
      font-family: 'Space Mono', monospace;
      font-size: 0.8rem;
      text-transform: uppercase;
      letter-spacing: 0.2em;
      color: var(--magenta);
      margin-bottom: 14px;
    }

    .hero-heading {
      font-family: 'Syne', sans-serif;
      font-weight: 900;
      font-size: clamp(2.2rem, 5vw, 4rem);
      letter-spacing: -0.02em;
      line-height: 1.05;
      text-transform: uppercase;
      margin-bottom: 18px;
      max-width: 900px;
    }

    .hero-subheading {
      font-size: clamp(1.05rem, 2vw, 1.25rem);
      color: var(--text-muted);
      max-width: 640px;
      margin-bottom: 32px;
      font-weight: 400;
    }

    .hero-actions {
      display: flex;
      gap: 14px;
      justify-content: center;
      flex-wrap: wrap;
    }

    .btn-hero {
      display: inline-flex;
      align-items: center;
      gap: 10px;
      padding: 12px 28px;
      border-radius: 100px;
      font-size: 0.9rem;
      font-weight: 700;
      letter-spacing: 0.04em;
      text-decoration: none;
      cursor: pointer;
      transition: all 0.25s ease;
    }

    .btn-primary {
      background: var(--magenta);
      color: #fff;
      box-shadow: 0 4px 20px var(--magenta-glow);
    }

    .btn-primary:hover {
      background: #ff1f8f;
      transform: translateY(-2px);
      box-shadow: 0 8px 30px rgba(255, 0, 122, 0.4);
    }

    .btn-secondary {
      background: var(--bg-surface);
      border: 1px solid var(--border);
      color: var(--text-white);
    }

    .btn-secondary:hover {
      border-color: var(--text-muted);
      transform: translateY(-2px);
    }

    /* Main Container & Reader Content */
    .container {
      max-width: 840px;
      margin: 0 auto;
      padding: 72px 24px 140px;
    }

    /* Section Cards */
    .article-block {
      margin-bottom: 120px;
      scroll-margin-top: 100px;
    }

    .article-meta-badge {
      display: inline-block;
      font-family: 'Space Mono', monospace;
      font-size: 0.72rem;
      letter-spacing: 0.15em;
      text-transform: uppercase;
      color: var(--magenta);
      background: var(--magenta-dim);
      padding: 4px 12px;
      border-radius: 4px;
      margin-bottom: 16px;
    }

    /* Typography inside rendered markdown */
    .md-body h1 {
      font-family: 'Syne', sans-serif;
      font-weight: 800;
      font-size: clamp(2rem, 3.5vw, 2.75rem);
      line-height: 1.15;
      letter-spacing: -0.02em;
      color: var(--text-white);
      margin-bottom: 28px;
      padding-bottom: 20px;
      border-bottom: 1px solid var(--border);
    }

    .md-body h2 {
      font-family: 'Syne', sans-serif;
      font-weight: 700;
      font-size: 1.45rem;
      letter-spacing: -0.01em;
      color: var(--text-white);
      margin: 48px 0 18px;
      display: flex;
      align-items: center;
      gap: 12px;
    }

    .md-body h2::before {
      content: '';
      display: inline-block;
      width: 4px;
      height: 1.1em;
      background: var(--magenta);
      border-radius: 2px;
    }

    .md-body h3 {
      font-family: 'Plus Jakarta Sans', sans-serif;
      font-size: 1.15rem;
      font-weight: 700;
      color: var(--magenta);
      margin: 32px 0 14px;
    }

    .md-body p {
      font-size: 1.08rem;
      color: #c4c4cf;
      margin-bottom: 24px;
      line-height: 1.85;
      font-weight: 400;
    }

    .md-body strong {
      color: var(--text-white);
      font-weight: 700;
    }

    .md-body em {
      color: #e4e4e9;
      font-style: italic;
    }

    .md-body blockquote {
      position: relative;
      background: var(--bg-surface);
      border-left: 3px solid var(--magenta);
      padding: 20px 24px;
      margin: 32px 0;
      border-radius: 0 8px 8px 0;
      font-size: 1.12rem;
      font-style: italic;
      color: #f1f1f5;
    }

    .md-body blockquote p:last-child {
      margin-bottom: 0;
    }

    .md-body hr {
      border: 0;
      height: 1px;
      background: var(--border);
      margin: 64px 0;
    }

    .md-body ul, .md-body ol {
      margin: 20px 0 28px 24px;
      color: #c4c4cf;
    }

    .md-body li {
      margin-bottom: 10px;
      line-height: 1.7;
    }

    /* Track divider */
    .track-separator {
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 20px;
      margin: 80px 0;
      color: var(--text-dim);
      font-family: 'Space Mono', monospace;
      font-size: 0.8rem;
    }

    .track-separator::before,
    .track-separator::after {
      content: '';
      flex: 1;
      height: 1px;
      background: var(--border);
    }

    /* Footer */
    footer {
      border-top: 1px solid var(--border);
      padding: 60px 24px;
      text-align: center;
      color: var(--text-dim);
      font-size: 0.85rem;
      font-family: 'Space Mono', monospace;
    }

    footer .brand {
      font-family: 'Syne', sans-serif;
      font-weight: 900;
      font-size: 1.4rem;
      color: var(--text-white);
      margin-bottom: 8px;
    }

    /* Floating Quick Nav / Back to top */
    .floating-nav {
      position: fixed;
      bottom: 28px;
      right: 28px;
      display: flex;
      flex-direction: column;
      gap: 10px;
      z-index: 900;
    }

    .floating-btn {
      width: 44px;
      height: 44px;
      border-radius: 50%;
      background: var(--bg-surface);
      border: 1px solid var(--border);
      color: var(--text-white);
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      text-decoration: none;
      font-size: 1rem;
      transition: all 0.25s ease;
      box-shadow: 0 8px 24px rgba(0,0,0,0.5);
    }

    .floating-btn:hover {
      background: var(--magenta);
      border-color: var(--magenta);
      transform: translateY(-2px);
    }

    @media (max-width: 768px) {
      .nav { padding: 0 18px; }
      .nav-right { display: none; }
      .container { padding: 48px 18px 100px; }
      .hero { padding: 32px 18px 56px; }
      .hero-artwork-wrap { margin-bottom: 24px; }
      .floating-nav { bottom: 18px; right: 18px; }
    }
  </style>
</head>
<body>

  <!-- Top Navbar -->
  <nav class="nav">
    <div class="nav-left">
      <button class="burger-btn" onclick="toggleDrawer()" aria-label="Menü öffnen">
        <span></span>
        <span></span>
        <span></span>
      </button>
    </div>
    <a href="#" class="nav-brand">
      <span>MODEST MEITNER</span>
      <span class="dot"></span>
    </a>
    <div class="nav-right">
      <span class="nav-badge">12 TRACKS</span>
    </div>
  </nav>

  <!-- Side Drawer Navigation -->
  <div class="drawer-overlay" id="drawerOverlay" onclick="toggleDrawer()"></div>
  <aside class="drawer" id="drawer">
    <div class="drawer-header">
      <div class="drawer-title">Tracklist & Kapitel</div>
      <button class="drawer-close" onclick="toggleDrawer()">&times;</button>
    </div>
    <ul class="tracklist" id="tracklistNav">
      <!-- Injected via JS -->
    </ul>
  </aside>

  <!-- Hero Section -->
  <header class="hero">
    <div class="hero-artwork-wrap">
      <img src="[[HERO_IMG_PLACEHOLDER]]" alt="Modest Meitner Cover" class="hero-artwork">
    </div>
    <div class="hero-tag">Anatomie eines Zusammenbruchs</div>
    <h1 class="hero-heading">Album Review & Tiefenpsychologische Interpretation</h1>
    <p class="hero-subheading">Eine detaillierte Rekonstruktion über symbiotische Klammerhaltung, sensorischen Hunger, Ego-Tod und autonomen Wiederaufbau.</p>
    <div class="hero-actions">
      <a href="#section-0" class="btn-hero btn-primary">Gesamtreview lesen</a>
      <button onclick="toggleDrawer()" class="btn-hero btn-secondary">Tracklist öffnen</button>
    </div>
  </header>

  <!-- Main Content Container -->
  <main class="container" id="mainContainer">
    <!-- Articles injected here -->
  </main>

  <!-- Floating Navigation -->
  <div class="floating-nav">
    <button class="floating-btn" onclick="window.scrollTo({top: 0, behavior: 'smooth'})" title="Nach oben">↑</button>
    <button class="floating-btn" onclick="toggleDrawer()" title="Menü">☰</button>
  </div>

  <!-- Footer -->
  <footer>
    <div class="brand">MODEST MEITNER</div>
    <p>© 2026 • Psychodynamische Fallstudie & Literarische Dekonstruktion</p>
  </footer>

  <script>
    const reviewData = [[REVIEW_DATA_PLACEHOLDER]];

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
        .replace(/^\> (.*$)/gim, '<blockquote>$1</blockquote>')
        .replace(/\*\*(.*)\*\*/gim, '<strong>$1</strong>')
        .replace(/\*(.*)\*/gim, '<em>$1</em>')
        .replace(/\n\n/gim, '</p><p>');
    }

    function buildApp() {
      const navList = document.getElementById('tracklistNav');
      const container = document.getElementById('mainContainer');

      reviewData.forEach((item, index) => {
        // Parse Title
        const titleMatch = item.content.match(/^#\s+(.*)/m);
        let rawTitle = titleMatch ? titleMatch[1].replace(/#+/g, '').trim() : item.name.replace('.md', '');
        
        // Pretty title format
        let trackNumber = String(index).padStart(2, '0');
        let displayTitle = rawTitle;

        if (index === 0) {
          trackNumber = 'ESSAY';
        } else if (index === reviewData.length - 1) {
          trackNumber = 'EPILOG';
        }

        // Nav Item
        const li = document.createElement('li');
        li.className = 'track-item';
        li.innerHTML = `
          <a onclick="scrollToSection(${index}); toggleDrawer();">
            <span class="num">${trackNumber}</span>
            <span class="title">${displayTitle}</span>
          </a>
        `;
        navList.appendChild(li);

        // Section Content
        const article = document.createElement('article');
        article.className = 'article-block';
        article.id = 'section-' + index;

        let badgeText = `KAPITEL ${trackNumber}`;
        if (index === 0) badgeText = 'ALBUM ESSAY & GESAMTREVIEW';
        else if (index === reviewData.length - 1) badgeText = 'EPILOG & QUERSCHNITTE';
        else badgeText = `TRACK ${trackNumber} // DEEP DIVE`;

        article.innerHTML = `
          <span class="article-meta-badge">${badgeText}</span>
          <div class="md-body">
            ${renderMarkdown(item.content)}
          </div>
        `;

        container.appendChild(article);

        // Add stylish separator except on last item
        if (index < reviewData.length - 1) {
          const sep = document.createElement('div');
          sep.className = 'track-separator';
          sep.innerHTML = `<span>◆</span>`;
          container.appendChild(sep);
        }
      });
    }

    function scrollToSection(index) {
      const el = document.getElementById('section-' + index);
      if (el) {
        const offset = 90;
        const bodyRect = document.body.getBoundingClientRect().top;
        const elementRect = el.getBoundingClientRect().top;
        const elementPosition = elementRect - bodyRect;
        const offsetPosition = elementPosition - offset;

        window.scrollTo({
          top: offsetPosition,
          behavior: 'smooth'
        });
      }
    }

    buildApp();
  </script>
</body>
</html>
"""

# Replace placeholders safely
html_final = html_content.replace('[[HERO_IMG_PLACEHOLDER]]', img_src)
html_final = html_final.replace('[[REVIEW_DATA_PLACEHOLDER]]', json.dumps(review_data))

# Save files locally
with open('c:/Users/Hakan/Documents/antigravity/modest-meitner/ALBUM_REVIEW_READER.html', 'w', encoding='utf-8') as f:
    f.write(html_final)

with open('c:/Users/Hakan/Documents/antigravity/modest-meitner/album_review_und_interpretation/index.html', 'w', encoding='utf-8') as f:
    f.write(html_final)

print("HTML erfolgreich und modernisiert gebaut!")
