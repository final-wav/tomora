import json
import os

with open('album_review_und_interpretation/all_md_data.json', 'r', encoding='utf-8-sig') as f:
    review_data = json.load(f)

html_template = """<!DOCTYPE html>
<html lang="de">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Album Review & Interpretation</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;700;900&family=Playfair+Display:ital,wght@0,600;1,400&display=swap" rel="stylesheet">
  <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
  <style>
    :root {
      --bg-main: #0a0a0a;
      --text-main: #e5e5e5;
      --text-muted: #a3a3a3;
      --accent: #ff4500; /* Die "eine Farbe" - kraftvoll und modern */
      --nav-bg: rgba(10, 10, 10, 0.85);
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }
    
    body {
      font-family: 'Inter', sans-serif;
      background-color: var(--bg-main);
      color: var(--text-main);
      -webkit-font-smoothing: antialiased;
      overflow-x: hidden;
    }

    /* Navbar (Glatt, flach, blur) */
    .navbar {
      position: fixed;
      top: 0; left: 0; right: 0;
      height: 70px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 0 40px;
      background: var(--nav-bg);
      backdrop-filter: blur(12px);
      -webkit-backdrop-filter: blur(12px);
      z-index: 1000;
      border-bottom: 1px solid rgba(255,255,255,0.05);
    }

    .nav-brand {
      font-weight: 900;
      font-size: 1.2rem;
      letter-spacing: -0.04em;
      text-transform: uppercase;
    }

    .nav-brand span {
      color: var(--accent);
    }

    .burger-menu {
      cursor: pointer;
      display: flex;
      flex-direction: column;
      gap: 6px;
      padding: 10px;
    }
    
    .burger-menu span {
      display: block;
      width: 28px;
      height: 2px;
      background-color: #fff;
      transition: 0.3s;
    }

    /* Burger Drawer */
    .drawer-overlay {
      position: fixed;
      inset: 0;
      background: rgba(0,0,0,0.6);
      opacity: 0;
      pointer-events: none;
      transition: opacity 0.3s ease;
      z-index: 999;
    }
    .drawer-overlay.active {
      opacity: 1;
      pointer-events: all;
    }

    .drawer {
      position: fixed;
      top: 0; right: -400px;
      width: 100%;
      max-width: 380px;
      height: 100vh;
      background: #121212;
      z-index: 1001;
      transition: right 0.4s cubic-bezier(0.16, 1, 0.3, 1);
      padding: 80px 40px 40px;
      overflow-y: auto;
      border-left: 1px solid rgba(255,255,255,0.05);
    }
    .drawer.active {
      right: 0;
    }

    .close-btn {
      position: absolute;
      top: 25px; right: 40px;
      font-size: 2rem;
      font-weight: 300;
      cursor: pointer;
      color: var(--text-muted);
    }
    .close-btn:hover { color: #fff; }

    .nav-list {
      list-style: none;
    }
    .nav-list li {
      margin-bottom: 16px;
    }
    .nav-list a {
      color: var(--text-muted);
      text-decoration: none;
      font-size: 1rem;
      font-weight: 500;
      transition: color 0.2s;
      cursor: pointer;
      display: block;
    }
    .nav-list a:hover { color: #fff; }
    .nav-list a.active { color: var(--accent); }

    /* Hero Section (1 großes Titelbild) */
    .hero {
      position: relative;
      height: 80vh;
      min-height: 500px;
      background-image: url('https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?q=80&w=2564&auto=format&fit=crop');
      background-size: cover;
      background-position: center;
      display: flex;
      align-items: flex-end;
      padding: 60px 5%;
    }
    .hero::after {
      content: '';
      position: absolute;
      inset: 0;
      background: linear-gradient(to top, var(--bg-main) 0%, rgba(10,10,10,0.2) 100%);
    }
    .hero-content {
      position: relative;
      z-index: 10;
      max-width: 800px;
      margin: 0 auto;
      width: 100%;
    }
    .hero-title {
      font-size: clamp(2.5rem, 5vw, 4.5rem);
      font-weight: 900;
      letter-spacing: -0.03em;
      line-height: 1.1;
      margin-bottom: 16px;
    }
    .hero-subtitle {
      font-family: 'Playfair Display', serif;
      font-style: italic;
      font-size: clamp(1.2rem, 2vw, 1.8rem);
      color: var(--text-muted);
    }

    /* Content Area (Glatt, flach, lesbar) */
    main {
      max-width: 760px;
      margin: 0 auto;
      padding: 80px 20px 120px;
    }

    .article-section {
      margin-bottom: 100px;
    }

    /* Editorial Markdown Styling */
    .md-rendered {
      font-size: 1.15rem;
      line-height: 1.8;
      color: var(--text-muted);
    }
    .md-rendered h1 {
      font-size: 2.2rem;
      font-weight: 800;
      color: #fff;
      margin-bottom: 10px;
      letter-spacing: -0.02em;
    }
    .md-rendered h2 {
      font-size: 1.5rem;
      font-weight: 700;
      color: #fff;
      margin: 60px 0 20px;
    }
    .md-rendered h3 {
      font-size: 1.2rem;
      font-weight: 600;
      color: var(--accent);
      margin: 40px 0 16px;
    }
    .md-rendered p {
      margin-bottom: 24px;
    }
    .md-rendered blockquote {
      font-family: 'Playfair Display', serif;
      font-style: italic;
      font-size: 1.3rem;
      line-height: 1.6;
      color: #fff;
      border-left: 2px solid var(--accent);
      padding: 10px 0 10px 24px;
      margin: 40px 0;
    }
    .md-rendered hr {
      border: 0;
      height: 1px;
      background: rgba(255,255,255,0.1);
      margin: 60px 0;
    }
    .md-rendered strong {
      color: #fff;
      font-weight: 600;
    }

    /* Responsive */
    @media (max-width: 768px) {
      .navbar { padding: 0 20px; }
      .hero { height: 60vh; }
    }
  </style>
</head>
<body>

  <!-- Navbar -->
  <nav class="navbar">
    <div class="nav-brand">Modest<span>Meitner</span></div>
    <div class="burger-menu" onclick="toggleDrawer()">
      <span></span><span></span><span></span>
    </div>
  </nav>

  <!-- Drawer Menu -->
  <div class="drawer-overlay" id="drawerOverlay" onclick="toggleDrawer()"></div>
  <aside class="drawer" id="drawer">
    <div class="close-btn" onclick="toggleDrawer()">&times;</div>
    <ul class="nav-list" id="navList">
      <!-- Injected via JS -->
    </ul>
  </aside>

  <!-- Hero Section -->
  <header class="hero">
    <div class="hero-content">
      <h1 class="hero-title">Anatomie eines Zusammenbruchs</h1>
      <div class="hero-subtitle">Album Review & Tiefeninterpretation</div>
    </div>
  </header>

  <!-- Main Content -->
  <main id="contentContainer">
    <!-- Injected via JS -->
  </main>

  <script>
    const reviewFiles = """ + json.dumps(review_data) + """;

    function toggleDrawer() {
      document.getElementById('drawer').classList.toggle('active');
      document.getElementById('drawerOverlay').classList.toggle('active');
    }

    function renderMarkdown(text) {
      if (window.marked && typeof window.marked.parse === 'function') {
        return window.marked.parse(text);
      }
      // Simple fallback
      return text
        .replace(/^### (.*$)/gim, '<h3>$1</h3>')
        .replace(/^## (.*$)/gim, '<h2>$1</h2>')
        .replace(/^# (.*$)/gim, '<h1>$1</h1>')
        .replace(/^\> (.*$)/gim, '<blockquote>$1</blockquote>')
        .replace(/\*\*(.*)\*\*/gim, '<strong>$1</strong>')
        .replace(/\*(.*)\*/gim, '<em>$1</em>')
        .replace(/\n$/gim, '<br />')
        .split('\n\n').map(p => '<p>' + p + '</p>').join('');
    }

    function buildPage() {
      const navList = document.getElementById('navList');
      const container = document.getElementById('contentContainer');

      reviewFiles.forEach((item, index) => {
        // Extract Title
        const titleMatch = item.content.match(/^#\s+(.*)/m);
        const title = titleMatch ? titleMatch[1].replace(/#+/g, '').trim() : item.name.replace('.md', '');
        
        // Build Nav
        const li = document.createElement('li');
        li.innerHTML = `<a onclick="scrollToSection(${index}); toggleDrawer()">${title}</a>`;
        navList.appendChild(li);

        // Build Content Section
        const section = document.createElement('div');
        section.className = 'article-section';
        section.id = 'section-' + index;
        section.innerHTML = `<div class="md-rendered">${renderMarkdown(item.content)}</div>`;
        container.appendChild(section);
      });
    }

    function scrollToSection(index) {
      const el = document.getElementById('section-' + index);
      if (el) {
        // Offset for navbar
        const y = el.getBoundingClientRect().top + window.pageYOffset - 90;
        window.scrollTo({top: y, behavior: 'smooth'});
      }
    }

    buildPage();
  </script>
</body>
</html>"""

with open('album_review_und_interpretation/index.html', 'w', encoding='utf-8') as f:
    f.write(html_template)

with open('ALBUM_REVIEW_READER.html', 'w', encoding='utf-8') as f:
    f.write(html_template)

print('Neues Design erfolgreich angewendet!')
