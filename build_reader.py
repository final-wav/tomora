import json
import os
import glob

base_dir = os.path.abspath('album_review_und_interpretation')

ordered_files = [
    '00_ALBUM_ESSAY_Gesamtreview.md',
    'Track_Reviews/01_Please_Review.md',
    'Track_Reviews/02_Come_Closer_Review.md',
    'Track_Reviews/03_A_Boy_Like_You_Review.md',
    'Track_Reviews/04_Ring_The_Alarm_Review.md',
    'Track_Reviews/05_My_Baby_Review.md',
    'Track_Reviews/06_Have_You_Seen_Me_Dance_Alone_Review.md',
    'Track_Reviews/07_Somewhere_Else_Review.md',
    'Track_Reviews/08_I_Drink_The_Light_Review.md',
    'Track_Reviews/09_Wavelengths_Review.md',
    'Track_Reviews/10_Side_By_Side_Review.md',
    'Track_Reviews/11_The_Thing_Review.md',
    'Track_Reviews/12_In_A_Minute_Review.md',
    '13_Epilog_Thematische_Querschnitte.md'
]

review_data = []
for rel in ordered_files:
    full_path = os.path.join(base_dir, rel.replace('/', os.sep))
    if os.path.exists(full_path):
        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()
        review_data.append({
            'file': rel,
            'name': os.path.basename(rel),
            'content': content
        })

html_template = f'''<!DOCTYPE html>
<html lang="de">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Album Review & Song Interpretation — Komplettausgabe</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,600;1,6..72,400&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
  <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
  <style>
    :root {{
      --bg-body: #0a0c10;
      --bg-sidebar: #10131a;
      --bg-card: #151922;
      --bg-card-hover: #1c2230;
      --border-color: #232a3b;
      --text-main: #e2e8f0;
      --text-muted: #94a3b8;
      --text-dim: #64748b;
      --accent: #f59e0b;
      --accent-glow: rgba(245, 158, 11, 0.15);
      --accent-blue: #38bdf8;
      --sidebar-width: 340px;
    }}

    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: 'Plus Jakarta Sans', sans-serif;
      background-color: var(--bg-body);
      color: var(--text-main);
      display: flex;
      height: 100vh;
      overflow: hidden;
      -webkit-font-smoothing: antialiased;
    }}

    /* Sidebar Navigation */
    aside {{
      width: var(--sidebar-width);
      background-color: var(--bg-sidebar);
      border-right: 1px solid var(--border-color);
      display: flex;
      flex-direction: column;
      flex-shrink: 0;
      height: 100%;
    }}

    .brand-header {{
      padding: 22px 18px;
      border-bottom: 1px solid var(--border-color);
      background: linear-gradient(180deg, rgba(245,158,11,0.06) 0%, transparent 100%);
    }}

    .brand-tag {{
      font-size: 0.68rem;
      text-transform: uppercase;
      letter-spacing: 0.14em;
      color: var(--accent);
      font-weight: 700;
      margin-bottom: 4px;
    }}

    .brand-title {{
      font-size: 1.12rem;
      font-weight: 800;
      color: #fff;
      letter-spacing: -0.02em;
    }}

    .view-mode-tabs {{
      display: flex;
      padding: 8px 12px;
      gap: 6px;
      background: rgba(0,0,0,0.25);
      border-bottom: 1px solid var(--border-color);
    }}

    .tab-btn {{
      flex: 1;
      background: transparent;
      border: 1px solid var(--border-color);
      color: var(--text-muted);
      padding: 7px 10px;
      border-radius: 6px;
      font-size: 0.75rem;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.2s;
    }}

    .tab-btn.active {{
      background: var(--accent);
      color: #000;
      border-color: var(--accent);
    }}

    .search-box {{
      padding: 10px 14px;
      border-bottom: 1px solid var(--border-color);
    }}

    .search-box input {{
      width: 100%;
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      color: #fff;
      padding: 8px 12px;
      border-radius: 6px;
      font-size: 0.82rem;
      outline: none;
      transition: all 0.2s;
    }}

    .search-box input:focus {{
      border-color: var(--accent);
      box-shadow: 0 0 0 2px var(--accent-glow);
    }}

    .nav-list {{
      list-style: none;
      overflow-y: auto;
      flex-grow: 1;
      padding: 10px 8px;
    }}

    .nav-item {{
      display: flex;
      align-items: center;
      gap: 10px;
      padding: 9px 12px;
      border-radius: 6px;
      cursor: pointer;
      color: var(--text-muted);
      font-size: 0.84rem;
      margin-bottom: 2px;
      text-decoration: none;
      transition: all 0.15s;
    }}

    .nav-item:hover {{
      background-color: var(--bg-card-hover);
      color: #fff;
    }}

    .nav-item.active {{
      background-color: var(--bg-card);
      color: var(--accent);
      font-weight: 600;
      border-left: 3px solid var(--accent);
    }}

    .nav-num {{
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.72rem;
      opacity: 0.6;
      width: 22px;
    }}

    /* Main Scroll Area */
    main {{
      flex-grow: 1;
      overflow-y: auto;
      height: 100%;
      padding: 48px 64px 96px;
      display: flex;
      justify-content: center;
      scroll-behavior: smooth;
    }}

    .content-wrapper {{
      max-width: 860px;
      width: 100%;
    }}

    .section-card {{
      margin-bottom: 72px;
      padding-bottom: 56px;
      border-bottom: 1px solid var(--border-color);
    }}

    .section-card:last-child {{
      border-bottom: none;
    }}

    .file-source-badge {{
      display: inline-block;
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.72rem;
      padding: 3px 8px;
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: 4px;
      color: var(--accent-blue);
      margin-bottom: 16px;
    }}

    /* Markdown Render Styling */
    .md-rendered {{
      font-family: 'Newsreader', serif;
      font-size: 1.18rem;
      line-height: 1.8;
      color: #cbd5e1;
    }}

    .md-rendered h1 {{
      font-family: 'Plus Jakarta Sans', sans-serif;
      font-size: 2.2rem;
      font-weight: 800;
      color: #fff;
      margin-bottom: 12px;
      letter-spacing: -0.025em;
      line-height: 1.2;
    }}

    .md-rendered h2 {{
      font-family: 'Plus Jakarta Sans', sans-serif;
      font-size: 1.38rem;
      font-weight: 700;
      color: #f8fafc;
      margin: 36px 0 16px;
      letter-spacing: -0.015em;
    }}

    .md-rendered h3 {{
      font-family: 'Plus Jakarta Sans', sans-serif;
      font-size: 1.1rem;
      font-weight: 600;
      color: var(--accent);
      margin: 28px 0 12px;
    }}

    .md-rendered p {{
      margin-bottom: 20px;
    }}

    .md-rendered blockquote {{
      background: var(--bg-card);
      border-left: 3px solid var(--accent);
      padding: 16px 20px;
      margin: 24px 0;
      border-radius: 0 8px 8px 0;
      font-family: 'Plus Jakarta Sans', sans-serif;
      font-size: 0.95rem;
      line-height: 1.65;
      color: #f8fafc;
    }}

    .md-rendered hr {{
      border: 0;
      height: 1px;
      background: var(--border-color);
      margin: 36px 0;
    }}

    .md-rendered table {{
      width: 100%;
      border-collapse: collapse;
      margin: 28px 0;
      font-family: 'Plus Jakarta Sans', sans-serif;
      font-size: 0.88rem;
    }}

    .md-rendered th, .md-rendered td {{
      border: 1px solid var(--border-color);
      padding: 12px 16px;
      text-align: left;
    }}

    .md-rendered th {{
      background: var(--bg-card);
      color: var(--accent);
      font-weight: 700;
    }}

    .md-rendered ul, .md-rendered ol {{
      margin: 16px 0 16px 28px;
    }}

    .md-rendered li {{
      margin-bottom: 8px;
    }}

    .md-rendered strong {{
      color: #fff;
      font-weight: 600;
    }}

    ::-webkit-scrollbar {{ width: 6px; }}
    ::-webkit-scrollbar-track {{ background: transparent; }}
    ::-webkit-scrollbar-thumb {{ background: var(--border-color); border-radius: 3px; }}
  </style>
</head>
<body>

  <aside>
    <div class="brand-header">
      <div class="brand-tag">● Komplettausgabe</div>
      <div class="brand-title">Album Review & Interpretation</div>
    </div>
    
    <div class="view-mode-tabs">
      <button class="tab-btn active" id="btnModeContinuous" onclick="setMode('continuous')">Alle am Stück</button>
      <button class="tab-btn" id="btnModeSingle" onclick="setMode('single')">Kapitelweise</button>
    </div>

    <div class="search-box">
      <input type="text" id="searchInput" placeholder="Volltextsuche in allen Tracks..." oninput="handleSearch(this.value)">
    </div>

    <ul class="nav-list" id="navList"></ul>
  </aside>

  <main id="mainScrollArea">
    <div class="content-wrapper" id="contentContainer"></div>
  </main>

  <script>
    const reviewFiles = {json.dumps(review_data)};
    let currentMode = 'continuous';
    let currentSingleIndex = 0;

    function renderMarkdown(text) {{
      if (window.marked && typeof window.marked.parse === 'function') {{
        return window.marked.parse(text);
      }}
      return text
        .replace(/^### (.*$)/gim, '<h3>$1</h3>')
        .replace(/^## (.*$)/gim, '<h2>$1</h2>')
        .replace(/^# (.*$)/gim, '<h1>$1</h1>')
        .replace(/^\\> (.*$)/gim, '<blockquote>$1</blockquote>')
        .replace(/\\*\\*(.*)\\*\\*/gim, '<strong>$1</strong>')
        .replace(/\\*(.*)\\*/gim, '<em>$1</em>')
        .replace(/\\n$/gim, '<br />')
        .split('\\n\\n').map(p => '<p>' + p + '</p>').join('');
    }}

    function renderNav() {{
      const navList = document.getElementById('navList');
      navList.innerHTML = '';

      reviewFiles.forEach((item, index) => {{
        const titleMatch = item.content.match(/^#\\s+(.*)/m);
        const title = titleMatch ? titleMatch[1].replace(/#+/g, '').trim() : item.name.replace('.md', '');
        
        const li = document.createElement('li');
        li.className = `nav-item ${{currentMode === 'single' && index === currentSingleIndex ? 'active' : ''}}`;
        li.id = `nav-item-${{index}}`;
        li.onclick = () => {{
          if (currentMode === 'continuous') {{
            const targetEl = document.getElementById(`doc-sec-${{index}}`);
            if (targetEl) targetEl.scrollIntoView({{ behavior: 'smooth' }});
          }} else {{
            currentSingleIndex = index;
            renderNav();
            renderContent();
            document.getElementById('mainScrollArea').scrollTop = 0;
          }}
        }};

        const numStr = (index === 0) ? '00' : (index === reviewFiles.length - 1 ? '13' : (index < 10 ? '0' + index : '' + index));

        li.innerHTML = `
          <span class="nav-num">${{numStr}}</span>
          <span style="overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">${{title}}</span>
        `;
        navList.appendChild(li);
      }});
    }}

    function setMode(mode) {{
      currentMode = mode;
      document.getElementById('btnModeContinuous').className = `tab-btn ${{mode === 'continuous' ? 'active' : ''}}`;
      document.getElementById('btnModeSingle').className = `tab-btn ${{mode === 'single' ? 'active' : ''}}`;
      renderNav();
      renderContent();
    }}

    function renderContent() {{
      const container = document.getElementById('contentContainer');
      container.innerHTML = '';

      if (currentMode === 'continuous') {{
        reviewFiles.forEach((item, index) => {{
          const section = document.createElement('div');
          section.className = 'section-card';
          section.id = `doc-sec-${{index}}`;
          section.innerHTML = `
            <div class="file-source-badge">📄 ${{item.file}}</div>
            <div class="md-rendered">${{renderMarkdown(item.content)}}</div>
          `;
          container.appendChild(section);
        }});
      }} else {{
        const item = reviewFiles[currentSingleIndex];
        const section = document.createElement('div');
        section.className = 'section-card';
        section.innerHTML = `
          <div class="file-source-badge">📄 ${{item.file}}</div>
          <div class="md-rendered">${{renderMarkdown(item.content)}}</div>
        `;
        container.appendChild(section);
      }}
    }}

    function handleSearch(q) {{
      const term = q.toLowerCase().trim();
      const navItems = document.querySelectorAll('.nav-item');
      reviewFiles.forEach((item, idx) => {{
        const match = item.name.toLowerCase().includes(term) || item.content.toLowerCase().includes(term);
        navItems[idx].style.display = match ? 'flex' : 'none';
      }});
    }}

    renderNav();
    renderContent();
  </script>
</body>
</html>'''

with open('album_review_und_interpretation/index.html', 'w', encoding='utf-8') as f:
    f.write(html_template)

with open('ALBUM_REVIEW_READER.html', 'w', encoding='utf-8') as f:
    f.write(html_template)

print('Done! Clean file generated.')
