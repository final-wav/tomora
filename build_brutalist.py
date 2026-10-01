import json
import base64
import os

img_path = r"C:\Users\Hakan\.gemini\antigravity\brain\5e6e588d-8195-4b9c-a574-5d026ae3847a\.user_uploaded\media_1790875455821.jpg"
with open(img_path, "rb") as f:
    img_b64 = base64.b64encode(f.read()).decode('utf-8')
img_src = f"data:image/jpeg;base64,{img_b64}"

with open('album_review_und_interpretation/all_md_data.json', 'r', encoding='utf-8-sig') as f:
    review_data = json.load(f)

html_template = """<!DOCTYPE html>
<html lang="de">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>MODEST MEITNER - ALBUM REVIEW</title>
  <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
  <style>
    :root {
      --bg: #000000;
      --text: #ffffff;
      --magenta: #ff00ff;
    }
    
    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }
    
    body {
      background-color: var(--bg);
      color: var(--text);
      font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
      -webkit-font-smoothing: antialiased;
    }

    /* Schlichte Navbar */
    .navbar {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 15px 30px;
      background-color: var(--bg);
      border-bottom: 2px solid var(--magenta);
      position: sticky;
      top: 0;
      z-index: 100;
    }

    .burger {
      cursor: pointer;
      display: flex;
      flex-direction: column;
      gap: 6px;
      width: 30px;
    }
    
    .burger span {
      display: block;
      width: 100%;
      height: 3px;
      background-color: var(--text);
    }
    
    .logo {
      font-family: "Times New Roman", Times, serif;
      font-weight: 900;
      font-size: 28px;
      letter-spacing: 2px;
      text-transform: uppercase;
      color: var(--magenta);
      text-align: center;
      flex-grow: 1;
    }
    
    .placeholder { width: 30px; }

    /* Burger Drawer */
    .drawer {
      position: fixed;
      top: 0; left: -100%;
      width: 100%;
      max-width: 350px;
      height: 100vh;
      background-color: var(--bg);
      border-right: 2px solid var(--magenta);
      z-index: 200;
      transition: left 0.3s ease;
      padding: 30px;
      overflow-y: auto;
    }
    .drawer.active { left: 0; }
    
    .close-btn {
      font-size: 40px;
      font-weight: bold;
      color: var(--magenta);
      cursor: pointer;
      text-align: right;
      margin-bottom: 30px;
      line-height: 1;
    }

    ul.nav-list { list-style: none; }
    ul.nav-list li { margin-bottom: 20px; }
    ul.nav-list a {
      color: var(--text);
      text-decoration: none;
      font-size: 16px;
      font-weight: bold;
      text-transform: uppercase;
      cursor: pointer;
    }
    ul.nav-list a:hover { color: var(--magenta); }

    /* Hero Bild */
    .hero {
      width: 100%;
      text-align: center;
      padding: 40px 20px;
      border-bottom: 2px solid var(--magenta);
    }
    .hero img {
      max-width: 100%;
      height: auto;
      max-height: 70vh;
      display: block;
      margin: 0 auto;
    }

    /* Content */
    main {
      max-width: 800px;
      margin: 0 auto;
      padding: 60px 20px 120px 20px;
    }

    .article-section { margin-bottom: 100px; }

    /* Markdown Styling - Stark & Schlicht */
    .md-rendered h1 {
      font-family: "Times New Roman", Times, serif;
      font-size: 2.5rem;
      text-transform: uppercase;
      color: var(--magenta);
      text-align: center;
      margin-bottom: 40px;
    }
    
    .md-rendered h2 {
      font-size: 1.5rem;
      text-transform: uppercase;
      color: var(--magenta);
      margin: 60px 0 20px 0;
      border-bottom: 1px solid var(--magenta);
      padding-bottom: 10px;
    }
    
    .md-rendered h3 {
      font-size: 1.2rem;
      text-transform: uppercase;
      color: var(--text);
      margin: 40px 0 15px 0;
    }
    
    .md-rendered p {
      font-size: 1.1rem;
      line-height: 1.6;
      margin-bottom: 25px;
    }
    
    .md-rendered blockquote {
      font-style: italic;
      color: var(--magenta);
      border-left: 3px solid var(--magenta);
      padding-left: 20px;
      margin: 30px 0;
      font-size: 1.2rem;
    }
    
    .md-rendered strong {
      color: var(--magenta);
    }
    
    .md-rendered hr {
      border: 0;
      height: 2px;
      background-color: var(--magenta);
      margin: 60px 0;
    }
  </style>
</head>
<body>

  <!-- Navbar -->
  <nav class="navbar">
    <div class="burger" onclick="toggleMenu()">
      <span></span><span></span><span></span>
    </div>
    <div class="logo">MODEST MEITNER</div>
    <div class="placeholder"></div>
  </nav>

  <!-- Sidebar / Drawer -->
  <aside class="drawer" id="drawer">
    <div class="close-btn" onclick="toggleMenu()">&times;</div>
    <ul class="nav-list" id="navList"></ul>
  </aside>

  <!-- Hero -->
  <div class="hero">
    <img src="[[IMG_SRC]]" alt="Album Artwork" />
  </div>

  <!-- Content -->
  <main id="contentContainer"></main>

  <script>
    const reviewFiles = [[JSON_DATA]];

    function toggleMenu() {
      document.getElementById('drawer').classList.toggle('active');
    }

    function renderMarkdown(text) {
      if (window.marked && typeof window.marked.parse === 'function') {
        return window.marked.parse(text);
      }
      return text;
    }

    function buildPage() {
      const navList = document.getElementById('navList');
      const container = document.getElementById('contentContainer');

      reviewFiles.forEach((item, index) => {
        const titleMatch = item.content.match(/^#\s+(.*)/m);
        const title = titleMatch ? titleMatch[1].replace(/#+/g, '').trim() : item.name.replace('.md', '');
        
        const li = document.createElement('li');
        li.innerHTML = `<a onclick="scrollToSection(${index}); toggleMenu()">${title}</a>`;
        navList.appendChild(li);

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
        const y = el.getBoundingClientRect().top + window.pageYOffset - 80;
        window.scrollTo({top: y, behavior: 'smooth'});
      }
    }

    buildPage();
  </script>
</body>
</html>"""

html_template = html_template.replace('[[IMG_SRC]]', img_src)
html_template = html_template.replace('[[JSON_DATA]]', json.dumps(review_data))

with open('album_review_und_interpretation/index.html', 'w', encoding='utf-8') as f:
    f.write(html_template)

with open('ALBUM_REVIEW_READER.html', 'w', encoding='utf-8') as f:
    f.write(html_template)

print('Repariert und generiert.')
