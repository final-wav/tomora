# -*- coding: utf-8 -*-
"""
TOMORA Album Review & Literary Interpretation
Horizontal Carousel Reader (Track-by-Track, Modern < / > Navigation)
Preserves 100% of Typography, Palette, Pink Highlights, Grain & Audio/YouTube Engine.
Supports Bilingual DE / EN Toggle without reloading, preserving active slide & playback.
"""

import os
import re
import json

p1_de_dir = 'album_analyse_fallstudie/Phase_1_Mikro_Dekonstruktion'
p1_en_dir = 'album_analyse_fallstudie/Phase_1_Mikro_Dekonstruktion_EN'

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

youtube_ids = {
    "01": "z7fX1YvK2gQ",
    "02": "Q9jC7L6qB4E",
    "03": "kJQP7kiw5Fk",
    "04": "L_u8L5_bW4Y",
    "05": "3q2bT5yQz8g",
    "06": "8jT_V2qL5rQ",
    "07": "yN6Rz7L_Q8g",
    "08": "z7L_Q8gyN6R",
    "09": "V2qL5rQ8jT_",
    "10": "Qz8g3q2bT5y",
    "11": "bW4YL_u8L5_",
    "12": "kiw5FkkJQP7"
}

def clean_txt(t):
    return re.sub(r'[^a-zA-Z0-9]', '', t).lower()

def render_md(text):
    text = text.strip()
    text = re.sub(r'„([^“\n]+?)“', r'QQSTART\1QQEND', text)
    text = re.sub(r'"([^"\n]+?)"', r'QQSTART\1QQEND', text)
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'(?<!\*)\*([^*]+?)\*(?!\*)', r'<span class="lyric-quote-highlight">\1</span>', text)
    text = re.sub(r'`([^`]+?)`', r'<code style="color:var(--magenta);font-family:monospace;">\1</code>', text)
    text = text.replace('QQSTART', '<span class="lyric-quote-highlight">“').replace('QQEND', '”</span>')
    return text

def parse_phase1(dir_path, num_str):
    filepath = None
    for f in os.listdir(dir_path):
        if f.startswith(num_str) and f.endswith('.md'):
            filepath = os.path.join(dir_path, f)
            break
    if not filepath:
        return "", [], "", [], ""

    with open(filepath, 'r', encoding='utf-8') as fp:
        raw = fp.read()

    # Subtitle
    sub_m = re.search(r'## (.+?)\n', raw)
    subtitle = sub_m.group(1).strip() if sub_m else ''

    # Lyrics
    lyr_m = re.search(r'```text(.*?)```', raw, re.DOTALL)
    lyrics_raw = lyr_m.group(1).strip() if lyr_m else ''

    # Parse stanzas
    stanzas = []
    current_stanza = {"title": "", "lines": []}
    lines = lyrics_raw.split('\n')
    for line in lines:
        l_s = line.strip()
        if not l_s:
            if current_stanza["lines"]:
                stanzas.append(current_stanza)
                current_stanza = {"title": "", "lines": []}
            continue
        c_ls = clean_txt(l_s)
        c_title = clean_txt(track_names_map[num_str])
        if c_ls == c_title or c_ls == f"{c_title}{int(num_str)}" or c_ls == f"{int(num_str)}{c_title}" or re.match(r'^\d+\.\s+.*', l_s):
            continue
        if l_s.startswith('[') and l_s.endswith(']'):
            if current_stanza["lines"]:
                stanzas.append(current_stanza)
            current_stanza = {"title": l_s, "lines": []}
        else:
            current_stanza["lines"].append(l_s)
    if current_stanza["lines"]:
        stanzas.append(current_stanza)

    # Dramaturgie / Context
    dram_m = re.search(r'### I\.\s*(?:Album-Dramaturgie|Album Dramaturgy):[^\n]*\n(.*?)(?=### II\.)', raw, re.DOTALL)
    if not dram_m:
        dram_m = re.search(r'### 2\.\s*Textanalyse im Albumkontext\n(.*?)(?=####)', raw, re.DOTALL)
    if not dram_m:
        dram_m = re.search(r'### II\.\s*Textanalyse im Albumkontext\n(.*?)(?=####)', raw, re.DOTALL)
    dramaturgie = dram_m.group(1).strip() if dram_m else ''

    # Points or Sections
    points = []
    pts = re.findall(r'#### ([^\n]+)\n(.*?)(?=(?:####|###|\n---\s*\n|\Z))', raw, re.DOTALL)
    for title, body in pts:
        points.append({'title': title.strip(), 'body': body.strip()})

    # Synthesis / Finale
    syn_m = re.search(r'### IV\.\s*(?:Synthese|Synthesis):[^\n]*\n(.*?)(?=\Z)', raw, re.DOTALL)
    if not syn_m:
        syn_m = re.search(r'### Die eigentliche Funktion[^\n]*\n(.*?)(?=\Z)', raw, re.DOTALL)
    if not syn_m:
        syn_m = re.search(r'### Die eigentliche Bewegung[^\n]*\n(.*?)(?=\Z)', raw, re.DOTALL)
    if not syn_m:
        syn_m = re.search(r'### V\.\s*Schluss:[^\n]*\n(.*?)(?=\Z)', raw, re.DOTALL)
    synthesis = syn_m.group(1).strip() if syn_m else ''

    return subtitle, stanzas, dramaturgie, points, synthesis

def render_content_blocks(dramaturgie, points, synthesis, lang_code):
    # Render Dramaturgie
    dram_p = [p.strip() for p in dramaturgie.split('\n\n') if p.strip()]
    dram_rendered = "\n".join([f'<p>{render_md(p)}</p>' for p in dram_p])

    # Render Points
    pts_html = []
    for idx, pt in enumerate(points):
        p_title = pt["title"]
        p_body = pt["body"]
        body_p = [bp.strip() for bp in p_body.split('\n\n') if bp.strip()]
        body_rendered = "\n".join([f'<p>{render_md(bp)}</p>' for bp in body_p])
        pts_html.append(f'''
        <div class="analysis-point-card">
          <div class="point-header">
            <span class="point-num-tag">{idx+1:02d}</span>
            <h4 class="point-title">{render_md(p_title)}</h4>
          </div>
          <div class="point-body">
            {body_rendered}
          </div>
        </div>
        ''')
    pts_block = "\n".join(pts_html)

    # Render Synthesis
    syn_p = [p.strip() for p in synthesis.split('\n\n') if p.strip()]
    syn_rendered = "\n".join([f'<p>{render_md(p)}</p>' for p in syn_p])

    tag_dram = "I. Album-Dramaturgie & Kontext" if lang_code == "de" else "I. Album Dramaturgy & Context"
    tag_pts = f"Erschöpfende Lektüre ({len(points)} Analyse-Punkte)" if lang_code == "de" else f"Exhaustive Reading ({len(points)} Analysis Points)"
    tag_syn = "Synthese & Dramaturgische Sollbruchstelle" if lang_code == "de" else "Synthesis & Dramaturgical Fault Line"
    tag_kicker = "Monolithische Tiefenanalyse" if lang_code == "de" else "Monolithic Deep Analysis"

    return f'''
    <div class="lang-content lang-{lang_code}" data-lang="{lang_code}">
      <div class="analysis-section-kicker">{tag_kicker}</div>
      {f"""
      <div class="dramaturgy-box">
        <div class="dramaturgy-tag">{tag_dram}</div>
        <div class="dramaturgy-content">
          {dram_rendered}
        </div>
      </div>
      """ if dram_rendered else ""}

      <div class="points-grid-container">
        <div class="points-section-title">{tag_pts}</div>
        <div class="points-list">
          {pts_block}
        </div>
      </div>

      {f"""
      <div class="synthesis-box">
        <div class="synthesis-tag">{tag_syn}</div>
        <div class="synthesis-content">
          {syn_rendered}
        </div>
      </div>
      """ if syn_rendered else ""}
    </div>
    '''

def render_track_slide(num_str, title, data_de, data_en, is_active):
    active_cls = " active" if is_active else ""
    sub_de, stanzas_de, dram_de, pts_de, syn_de = data_de
    sub_en, stanzas_en, dram_en, pts_en, syn_en = data_en

    # Lyrics Block (English original text is identical across both languages)
    stanzas = stanzas_de if stanzas_de else stanzas_en
    stanzas_html = []
    for s in stanzas:
        lines_html = []
        for l in s["lines"]:
            lines_html.append(f'<div class="lyric-line-hero"><span class="lyric-hero-text">{render_md(l)}</span></div>')
        lines_str = "\n".join(lines_html)
        title_str = f'<div class="stanza-hero-tag">{s["title"]}</div>' if s["title"] else ''
        stanzas_html.append(f'<div class="stanza-hero-wrap">{title_str}\n{lines_str}</div>')
    lyrics_block = "\n".join(stanzas_html)

    content_de = render_content_blocks(dram_de, pts_de, syn_de, "de")
    content_en = render_content_blocks(dram_en, pts_en, syn_en, "en")

    return f'''
    <article class="track-slide{active_cls}" id="slide-{num_str}" data-track-num="{num_str}" data-track-title="{title}">
      <!-- Slide Track Header -->
      <div class="slide-header">
        <div class="slide-header-left">
          <span class="slide-num-badge">{num_str}</span>
          <div class="slide-title-wrap">
            <h2 class="slide-title">{title}</h2>
            <div class="slide-subtitle lang-de" data-lang="de">{sub_de}</div>
            <div class="slide-subtitle lang-en" data-lang="en" style="display:none;">{sub_en}</div>
          </div>
        </div>
        <div class="slide-header-right">
          <button class="song-round-play-btn" data-track-num="{num_str}" aria-label="Play Original Song">
            <svg class="play-icon" viewBox="0 0 24 24" width="13" height="13" fill="currentColor"><polygon points="7 4 19 12 7 20 7 4"></polygon></svg>
            <svg class="pause-icon" viewBox="0 0 24 24" width="13" height="13" fill="currentColor" style="display:none;"><rect x="6" y="4" width="3.5" height="16"></rect><rect x="14.5" y="4" width="3.5" height="16"></rect></svg>
          </button>
          <button class="audio-play-btn" data-track-num="{num_str}" aria-label="Listen to Audio Essay">
            <svg class="play-icon" viewBox="0 0 24 24" width="13" height="13"><polygon points="6 4 20 12 6 20 6 4" fill="currentColor"></polygon></svg>
            <svg class="pause-icon" viewBox="0 0 24 24" width="13" height="13" style="display:none;"><rect x="5" y="4" width="4" height="16" fill="currentColor"></rect><rect x="15" y="4" width="4" height="16" fill="currentColor"></rect></svg>
            <span class="btn-text">Audio-Essay</span>
          </button>
        </div>
      </div>

      <!-- Centered Hero Lyrics Column -->
      <div class="hero-lyrics-section">
        <div class="hero-lyrics-kicker">
          <span class="lang-de" data-lang="de">Songtext</span>
          <span class="lang-en" data-lang="en" style="display:none;">Lyrics</span>
        </div>
        <div class="hero-lyrics-container">
          {lyrics_block}
        </div>
      </div>

      <!-- In-Depth Analysis Below Lyrics -->
      <div class="hero-analysis-section">
        {content_de}
        {content_en}
      </div>
    </article>
    '''

def build_carousel_html():
    slides_html_list = []
    drawer_nav_list = []
    track_meta_list = []

    for num in range(1, 13):
        num_str = f"{num:02d}"
        title = track_names_map[num_str]
        data_de = parse_phase1(p1_de_dir, num_str)
        data_en = parse_phase1(p1_en_dir, num_str)
        is_active = (num == 1)
        slide_markup = render_track_slide(num_str, title, data_de, data_en, is_active)
        slides_html_list.append(slide_markup)
        
        drawer_nav_list.append(f'<li><a href="javascript:void(0)" onclick="goToTrack({num-1})">{num_str} — {title}</a></li>')
        track_meta_list.append({
            "num": num_str,
            "title": title,
            "ytId": youtube_ids[num_str]
        })

    slides_rendered = "\n".join(slides_html_list)
    drawer_nav_rendered = "\n".join(drawer_nav_list)
    track_list_json = json.dumps(track_meta_list, indent=2)

    full_html = f'''<!DOCTYPE html>
<html lang="de">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>TOMORA — Album Review & Monolithische Tiefenanalyse</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
  <script src="https://www.youtube.com/iframe_api"></script>
  <style>
    :root {{
      --bg: #0c0c0f;
      --bg-surface: #141418;
      --bg-card: rgba(20, 20, 24, 0.75);
      --text: #ffffff;
      --text-muted: #8e8e93;
      --magenta: #ff007a;
      --magenta-dim: rgba(255, 0, 122, 0.12);
      --magenta-glow: rgba(255, 0, 122, 0.35);
    }}

    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      -webkit-font-smoothing: antialiased;
    }}

    html {{
      scroll-behavior: smooth;
      background-color: var(--bg);
    }}

    body {{
      background-color: var(--bg);
      color: var(--text);
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
      line-height: 1.65;
      overflow-x: hidden;
      position: relative;
    }}

    /* Animierter 35mm Analog-Film-Grain Canvas */
    #grainCanvas {{
      position: fixed;
      top: 0;
      left: 0;
      width: 100vw;
      height: 100vh;
      pointer-events: none;
      z-index: 9999;
      opacity: 0.11;
      mix-blend-mode: screen;
    }}

    ::selection {{
      background-color: var(--magenta);
      color: #ffffff;
    }}

    /* Minimalistische Navbar */
    .navbar {{
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 65px;
      background: rgba(12, 12, 15, 0.85);
      backdrop-filter: blur(20px);
      -webkit-backdrop-filter: blur(20px);
      display: grid;
      grid-template-columns: 1fr auto 1fr;
      align-items: center;
      padding: 0 32px;
      z-index: 1000;
      border-bottom: 1px solid rgba(255, 255, 255, 0.06);
    }}

    .nav-left {{
      display: flex;
      align-items: center;
      gap: 16px;
    }}

    .burger-btn {{
      background: none;
      border: none;
      cursor: pointer;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      width: 24px;
      height: 16px;
      padding: 0;
      position: relative;
    }}

    .burger-btn span {{
      display: block;
      width: 100%;
      height: 2px;
      background-color: #ffffff;
      transition: background-color 0.2s;
    }}

    .burger-btn:hover span {{
      background-color: var(--magenta);
    }}

    .nav-track-indicator {{
      font-size: 0.8rem;
      font-weight: 800;
      letter-spacing: 0.15em;
      color: var(--text-muted);
      text-transform: uppercase;
    }}
    .nav-track-indicator span {{
      color: var(--magenta);
    }}

    .nav-center {{
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      text-align: center;
    }}

    .brand-title {{
      font-size: 1.1rem;
      font-weight: 900;
      letter-spacing: 0.25em;
      color: #ffffff;
      text-transform: uppercase;
      line-height: 1;
    }}

    .nav-right {{
      display: flex;
      justify-content: flex-end;
      align-items: center;
      gap: 16px;
    }}

    /* Sleek Language Switch Toggle */
    .lang-toggle-wrap {{
      display: inline-flex;
      align-items: center;
      background: rgba(255, 255, 255, 0.06);
      border: 1px solid rgba(255, 255, 255, 0.15);
      border-radius: 20px;
      padding: 2px;
      gap: 2px;
    }}

    .lang-btn {{
      background: none;
      border: none;
      color: var(--text-muted);
      font-family: inherit;
      font-size: 0.72rem;
      font-weight: 800;
      letter-spacing: 0.1em;
      padding: 4px 10px;
      border-radius: 16px;
      cursor: pointer;
      transition: all 0.2s ease;
    }}

    .lang-btn.active {{
      background: var(--magenta);
      color: #ffffff;
      box-shadow: 0 0 10px var(--magenta-glow);
    }}

    .lang-btn:hover:not(.active) {{
      color: #ffffff;
    }}

    /* Burger Drawer */
    .drawer-overlay {{
      position: fixed;
      top: 0;
      left: 0;
      width: 100vw;
      height: 100vh;
      background: rgba(0, 0, 0, 0.7);
      backdrop-filter: blur(8px);
      z-index: 1100;
      opacity: 0;
      pointer-events: none;
      transition: opacity 0.3s;
    }}
    .drawer-overlay.active {{
      opacity: 1;
      pointer-events: auto;
    }}

    .drawer {{
      position: fixed;
      top: 0;
      left: -340px;
      width: min(320px, 85vw);
      height: 100vh;
      background-color: #111115;
      z-index: 1200;
      padding: 20px 32px 36px 32px;
      display: flex;
      flex-direction: column;
      transition: left 0.35s cubic-bezier(0.16, 1, 0.3, 1);
      overflow-y: auto;
    }}
    .drawer.active {{ left: 0; }}

    .drawer-header {{
      height: 25px;
      display: flex;
      align-items: center;
      gap: 20px;
      margin-bottom: 36px;
    }}

    .drawer-close-btn {{
      background: none;
      border: none;
      cursor: pointer;
      display: flex;
      flex-direction: column;
      justify-content: center;
      width: 24px;
      height: 24px;
      padding: 0;
      position: relative;
    }}

    .drawer-close-btn span {{
      display: block;
      width: 24px;
      height: 2px;
      background-color: var(--magenta);
      position: absolute;
      top: 11px;
      left: 0;
      transition: background-color 0.2s;
    }}

    .drawer-close-btn span:nth-child(1) {{ transform: rotate(45deg); }}
    .drawer-close-btn span:nth-child(2) {{ transform: rotate(-45deg); }}
    .drawer-close-btn:hover span {{ background-color: #ffffff; }}

    .drawer-title {{
      font-size: 0.85rem;
      font-weight: 800;
      letter-spacing: 0.15em;
      text-transform: uppercase;
      color: var(--magenta);
      line-height: 1;
    }}

    .drawer-nav {{
      list-style: none;
      display: flex;
      flex-direction: column;
      gap: 14px;
    }}

    .drawer-nav a {{
      color: var(--text-muted);
      text-decoration: none;
      font-size: 1rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      display: block;
      padding: 4px 0;
      transition: all 0.2s;
    }}

    .drawer-nav a:hover {{
      color: #ffffff;
      padding-left: 6px;
    }}

    /* FULL BLEED HERO VIDEO */
    .hero-fullbleed {{
      margin-top: 65px;
      width: 100%;
      max-height: 45vh;
      overflow: hidden;
      display: flex;
      justify-content: center;
      align-items: center;
      background-color: #000000;
      position: relative;
    }}

    .hero-video {{
      width: 100%;
      height: 100%;
      object-fit: cover;
      display: block;
      max-height: 45vh;
      filter: brightness(0.75);
    }}

    .hero-overlay-text {{
      position: absolute;
      text-align: center;
      z-index: 10;
      pointer-events: none;
      padding: 0 20px;
    }}
    .hero-kicker {{
      font-size: 0.75rem;
      font-weight: 800;
      letter-spacing: 0.3em;
      color: var(--magenta);
      text-transform: uppercase;
      margin-bottom: 8px;
    }}
    .hero-title {{
      font-size: clamp(2.2rem, 5vw, 3.8rem);
      font-weight: 900;
      letter-spacing: -0.02em;
      color: #ffffff;
      line-height: 1.1;
    }}

    /* CAROUSEL WRAPPER & CONTROLS */
    .carousel-outer {{
      position: relative;
      max-width: 1300px;
      margin: 0 auto;
      padding: 40px 24px 140px 24px;
    }}

    /* GROSSE MODERNE PFEILE LINKS / RECHTS */
    .nav-arrow {{
      position: fixed;
      top: 50%;
      transform: translateY(-50%);
      width: 68px;
      height: 68px;
      border-radius: 50%;
      background: rgba(12, 12, 15, 0.65);
      backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
      border: 1px solid rgba(255, 255, 255, 0.15);
      color: #ffffff;
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      z-index: 900;
      transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
      box-shadow: 0 8px 30px rgba(0, 0, 0, 0.5);
      user-select: none;
    }}

    .nav-arrow:hover {{
      background: var(--magenta);
      border-color: var(--magenta);
      color: #ffffff;
      box-shadow: 0 0 25px var(--magenta-glow);
      transform: translateY(-50%) scale(1.08);
    }}

    .nav-arrow:active {{
      transform: translateY(-50%) scale(0.96);
    }}

    .nav-arrow-left {{
      left: 24px;
    }}

    .nav-arrow-right {{
      right: 24px;
    }}

    @media (max-width: 1400px) {{
      .nav-arrow {{
        position: absolute;
        top: 24px;
        transform: none;
        width: 48px;
        height: 48px;
      }}
      .nav-arrow:hover {{
        transform: scale(1.06);
      }}
      .nav-arrow-left {{ left: 24px; }}
      .nav-arrow-right {{ right: 24px; }}
    }}

    /* TRACK SLIDE (EINZELNER SONG) */
    .track-slide {{
      display: none;
      opacity: 0;
      transition: opacity 0.35s ease;
    }}

    .track-slide.active {{
      display: block;
      opacity: 1;
      animation: fadeInSlide 0.4s ease forwards;
    }}

    @keyframes fadeInSlide {{
      from {{ opacity: 0; transform: translateY(12px); }}
      to {{ opacity: 1; transform: translateY(0); }}
    }}

    /* SLIDE HEADER */
    .slide-header {{
      display: flex;
      justify-content: space-between;
      align-items: flex-end;
      padding-bottom: 24px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.08);
      margin-bottom: 48px;
      gap: 20px;
    }}

    .slide-header-left {{
      display: flex;
      align-items: baseline;
      gap: 20px;
      flex-wrap: wrap;
    }}

    .slide-num-badge {{
      font-size: clamp(2rem, 4vw, 3rem);
      font-weight: 900;
      color: var(--magenta);
      line-height: 1;
      letter-spacing: -0.02em;
    }}

    .slide-title-wrap {{
      display: flex;
      flex-direction: column;
      gap: 4px;
    }}

    .slide-title {{
      font-size: clamp(1.8rem, 3.5vw, 2.6rem);
      font-weight: 800;
      letter-spacing: -0.01em;
      color: #ffffff;
      line-height: 1.1;
    }}

    .slide-subtitle {{
      font-size: clamp(0.95rem, 1.4vw, 1.15rem);
      color: var(--text-muted);
      font-weight: 500;
      max-width: 800px;
      line-height: 1.4;
    }}

    .slide-header-right {{
      display: flex;
      align-items: center;
      gap: 12px;
      flex-shrink: 0;
    }}

    /* Header Action Buttons */
    .song-round-play-btn {{
      width: 44px;
      height: 44px;
      border-radius: 50%;
      background: rgba(255, 255, 255, 0.06);
      border: 1px solid rgba(255, 255, 255, 0.15);
      color: #ffffff;
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      transition: all 0.2s;
    }}

    .song-round-play-btn:hover {{
      background: var(--magenta);
      border-color: var(--magenta);
      transform: scale(1.06);
      box-shadow: 0 0 15px var(--magenta-glow);
    }}

    .song-round-play-btn.playing {{
      background: var(--magenta);
      border-color: var(--magenta);
      box-shadow: 0 0 15px var(--magenta-glow);
    }}

    .audio-play-btn {{
      display: flex;
      align-items: center;
      gap: 8px;
      height: 44px;
      padding: 0 18px;
      border-radius: 22px;
      background: rgba(255, 255, 255, 0.06);
      border: 1px solid rgba(255, 255, 255, 0.15);
      color: #ffffff;
      font-family: inherit;
      font-size: 0.8rem;
      font-weight: 700;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      cursor: pointer;
      transition: all 0.2s;
    }}

    .audio-play-btn:hover {{
      background: var(--magenta);
      border-color: var(--magenta);
      transform: scale(1.04);
      box-shadow: 0 0 15px var(--magenta-glow);
    }}

    .audio-play-btn.playing {{
      background: var(--magenta);
      border-color: var(--magenta);
      box-shadow: 0 0 15px var(--magenta-glow);
    }}

    /* HERO LYRICS SECTION */
    .hero-lyrics-section {{
      display: flex;
      flex-direction: column;
      align-items: center;
      text-align: center;
      padding: 60px 20px;
      margin-bottom: 70px;
      background: radial-gradient(circle at 50% 30%, rgba(255, 0, 122, 0.04) 0%, transparent 70%);
      border-radius: 12px;
      border: 1px solid rgba(255, 255, 255, 0.03);
    }}

    .hero-lyrics-kicker {{
      font-size: 0.75rem;
      font-weight: 800;
      letter-spacing: 0.25em;
      color: var(--magenta);
      text-transform: uppercase;
      margin-bottom: 32px;
    }}

    .hero-lyrics-container {{
      max-width: 760px;
      width: 100%;
      display: flex;
      flex-direction: column;
      gap: 36px;
    }}

    .stanza-hero-wrap {{
      display: flex;
      flex-direction: column;
      gap: 10px;
    }}

    .stanza-hero-tag {{
      font-size: 0.72rem;
      font-weight: 800;
      letter-spacing: 0.18em;
      color: var(--text-muted);
      text-transform: uppercase;
      margin-bottom: 8px;
    }}

    .lyric-line-hero {{
      font-size: clamp(1.2rem, 2.5vw, 1.55rem);
      font-weight: 600;
      line-height: 1.6;
      color: rgba(255, 255, 255, 0.92);
      letter-spacing: -0.01em;
    }}

    /* PINK HIGHLIGHTING */
    .lyric-quote-highlight {{
      color: var(--magenta);
      background: rgba(255, 0, 122, 0.12);
      padding: 2px 8px;
      border-radius: 4px;
      font-weight: 700;
      border: 1px solid rgba(255, 0, 122, 0.3);
      box-decoration-break: clone;
      -webkit-box-decoration-break: clone;
    }}

    /* DEEP DIVE ANALYSIS SECTION */
    .hero-analysis-section {{
      display: flex;
      flex-direction: column;
      gap: 48px;
    }}

    .analysis-section-kicker {{
      font-size: 0.85rem;
      font-weight: 900;
      letter-spacing: 0.2em;
      color: var(--magenta);
      text-transform: uppercase;
      border-left: 3px solid var(--magenta);
      padding-left: 12px;
    }}

    /* Dramaturgie Box */
    .dramaturgy-box {{
      background: rgba(255, 255, 255, 0.02);
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 10px;
      padding: 32px;
    }}
    .dramaturgy-tag {{
      font-size: 0.8rem;
      font-weight: 800;
      letter-spacing: 0.15em;
      color: #ffffff;
      text-transform: uppercase;
      margin-bottom: 16px;
    }}
    .dramaturgy-content p {{
      font-size: 1.08rem;
      color: #d0d0d5;
      line-height: 1.8;
      margin-bottom: 16px;
    }}
    .dramaturgy-content p:last-child {{ margin-bottom: 0; }}

    /* Points Grid */
    .points-grid-container {{
      display: flex;
      flex-direction: column;
      gap: 24px;
    }}
    .points-section-title {{
      font-size: 1.25rem;
      font-weight: 800;
      letter-spacing: -0.01em;
      color: #ffffff;
      padding-bottom: 12px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    }}
    .points-list {{
      display: flex;
      flex-direction: column;
      gap: 20px;
    }}
    .analysis-point-card {{
      background: var(--bg-card);
      border: 1px solid rgba(255, 255, 255, 0.07);
      border-radius: 8px;
      padding: 28px;
      transition: border-color 0.2s, background-color 0.2s;
    }}
    .analysis-point-card:hover {{
      background-color: rgba(26, 26, 32, 0.85);
      border-color: rgba(255, 0, 122, 0.35);
    }}
    .point-header {{
      display: flex;
      align-items: baseline;
      gap: 14px;
      margin-bottom: 14px;
    }}
    .point-num-tag {{
      font-size: 0.8rem;
      font-weight: 900;
      color: var(--magenta);
      letter-spacing: 0.1em;
      flex-shrink: 0;
    }}
    .point-title {{
      font-size: 1.15rem;
      font-weight: 700;
      color: #ffffff;
      line-height: 1.4;
    }}
    .point-body p {{
      font-size: 1.04rem;
      color: #c4c4cc;
      line-height: 1.8;
      margin-bottom: 14px;
    }}
    .point-body p:last-child {{ margin-bottom: 0; }}

    /* Synthesis Box */
    .synthesis-box {{
      background: linear-gradient(180deg, rgba(255, 0, 122, 0.04) 0%, rgba(20, 20, 24, 0.8) 100%);
      border: 1px solid rgba(255, 0, 122, 0.25);
      border-radius: 10px;
      padding: 32px;
    }}
    .synthesis-tag {{
      font-size: 0.8rem;
      font-weight: 800;
      letter-spacing: 0.15em;
      color: var(--magenta);
      text-transform: uppercase;
      margin-bottom: 16px;
    }}
    .synthesis-content p {{
      font-size: 1.08rem;
      color: #e0e0e5;
      line-height: 1.8;
      margin-bottom: 16px;
    }}
    .synthesis-content p:last-child {{ margin-bottom: 0; }}

    /* FLOATING BOTTOM MINI PLAYER */
    .bottom-player {{
      position: fixed;
      bottom: 24px;
      left: 50%;
      transform: translateX(-50%);
      width: min(840px, calc(100vw - 32px));
      height: 68px;
      background: rgba(12, 12, 15, 0.88);
      backdrop-filter: blur(20px);
      -webkit-backdrop-filter: blur(20px);
      border: 1px solid rgba(255, 255, 255, 0.12);
      border-radius: 8px;
      box-shadow: 0 16px 40px rgba(0, 0, 0, 0.65), 0 0 1px rgba(255, 255, 255, 0.15);
      display: grid;
      grid-template-columns: 1fr auto 1fr;
      align-items: center;
      padding: 0 24px;
      z-index: 1000;
    }}

    .player-left {{
      display: flex;
      flex-direction: column;
      gap: 2px;
      overflow: hidden;
      justify-content: center;
    }}

    .player-track-info {{
      display: flex;
      align-items: baseline;
      gap: 8px;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }}

    .player-track-num {{
      font-size: 0.75rem;
      font-weight: 900;
      color: var(--magenta);
      letter-spacing: 0.1em;
    }}

    .player-track-title {{
      font-size: 0.85rem;
      font-weight: 700;
      color: #ffffff;
      letter-spacing: 0.05em;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }}

    .player-mode-tag {{
      font-size: 0.65rem;
      font-weight: 700;
      color: var(--text-muted);
      letter-spacing: 0.08em;
      text-transform: uppercase;
    }}

    .player-center {{
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 4px;
    }}

    .player-controls {{
      display: flex;
      align-items: center;
      gap: 16px;
    }}

    .ctrl-btn {{
      background: none;
      border: none;
      color: var(--text-muted);
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 4px;
      transition: color 0.2s, transform 0.1s;
    }}
    .ctrl-btn:hover {{
      color: #ffffff;
      transform: scale(1.1);
    }}

    .play-pause-circle {{
      width: 36px;
      height: 36px;
      border-radius: 50%;
      background: #ffffff;
      border: none;
      color: #0c0c0f;
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      transition: transform 0.15s, background-color 0.2s;
    }}
    .play-pause-circle:hover {{
      transform: scale(1.08);
      background-color: var(--magenta);
      color: #ffffff;
    }}

    .timeline-wrap {{
      display: flex;
      align-items: center;
      gap: 10px;
      width: min(280px, 35vw);
    }}

    .time-stamp {{
      font-size: 0.65rem;
      font-weight: 600;
      color: var(--text-muted);
      font-variant-numeric: tabular-nums;
      min-width: 28px;
    }}

    .timeline-track {{
      flex: 1;
      height: 3px;
      background: rgba(255, 255, 255, 0.15);
      border-radius: 2px;
      position: relative;
      cursor: pointer;
    }}

    .timeline-fill {{
      height: 100%;
      background: var(--magenta);
      border-radius: 2px;
      width: 0%;
      position: relative;
    }}

    .player-right {{
      display: flex;
      justify-content: flex-end;
      align-items: center;
      gap: 12px;
    }}

    @media (max-width: 768px) {{
      .bottom-player {{
        bottom: 16px;
        width: calc(100vw - 24px);
        grid-template-columns: 1fr;
        height: auto;
        padding: 10px 14px;
        gap: 6px;
        border-radius: 8px;
      }}
      .player-left {{ display: none; }}
      .player-right {{ display: none; }}
      .player-center {{ width: 100%; }}
    }}
  </style>
</head>
<body>

  <!-- Film Grain Overlay -->
  <canvas id="grainCanvas"></canvas>

  <!-- Navbar -->
  <nav class="navbar">
    <div class="nav-left">
      <button class="burger-btn" id="burgerToggle" aria-label="Titelauswahl">
        <span></span>
        <span></span>
        <span></span>
      </button>
      <div class="nav-track-indicator">
        Track <span id="navTrackCurrent">01</span> / 12
      </div>
    </div>
    <div class="nav-center">
      <div class="brand-title">TOMORA</div>
    </div>
    <div class="nav-right">
      <!-- Dynamic Language Switcher Toggle -->
      <div class="lang-toggle-wrap">
        <button class="lang-btn active" id="langBtnDE" onclick="setLanguage('de')">DE</button>
        <button class="lang-btn" id="langBtnEN" onclick="setLanguage('en')">EN</button>
      </div>
    </div>
  </nav>

  <!-- Burger Drawer -->
  <div class="drawer-overlay" id="drawerOverlay"></div>
  <div class="drawer" id="drawerNav">
    <div class="drawer-header">
      <button class="drawer-close-btn" id="drawerClose" aria-label="Schließen">
        <span></span>
        <span></span>
      </button>
      <div class="drawer-title">Titelauswahl (01 - 12)</div>
    </div>
    <ul class="drawer-nav">
      {drawer_nav_rendered}
    </ul>
  </div>

  <!-- Hero Video Background -->
  <div class="hero-fullbleed">
    <video class="hero-video" autoplay loop muted playsinline>
      <source src="hero_video.mp4" type="video/mp4">
    </video>
    <div class="hero-overlay-text">
      <div class="hero-kicker">
        <span class="lang-de" data-lang="de">Das Meisterwerk im Detail</span>
        <span class="lang-en" data-lang="en" style="display:none;">The Masterpiece in Close-Up</span>
      </div>
      <h1 class="hero-title">TOMORA</h1>
    </div>
  </div>

  <!-- Carousel Navigation Arrows (Links / Rechts) -->
  <button class="nav-arrow nav-arrow-left" id="prevSlideBtn" aria-label="Vorheriger Track">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><polyline points="15 18 9 12 15 6"></polyline></svg>
  </button>
  <button class="nav-arrow nav-arrow-right" id="nextSlideBtn" aria-label="Nächster Track">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><polyline points="9 18 15 12 9 6"></polyline></svg>
  </button>

  <!-- Main Slides Container -->
  <main class="carousel-outer">
    {slides_rendered}
  </main>

  <!-- Floating Bottom Mini Player -->
  <div class="bottom-player">
    <div class="player-left">
      <div class="player-track-info">
        <span class="player-track-num" id="bpTrackNum">01</span>
        <span class="player-track-title" id="bpTrackTitle">PLEASE</span>
      </div>
      <span class="player-mode-tag">
        <span class="sub-mode-song">Track Audio (Original)</span>
        <span class="sub-mode-essay" style="display:none;">
          <span class="lang-de" data-lang="de">Neural TTS Audio-Essay</span>
          <span class="lang-en" data-lang="en" style="display:none;">Neural TTS Audio Essay</span>
        </span>
      </span>
    </div>

    <div class="player-center">
      <div class="player-controls">
        <button class="ctrl-btn" id="bpPrevBtn" aria-label="Vorheriger Song">
          <svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor"><polygon points="19 20 9 12 19 4 19 20"></polygon><line x1="5" y1="19" x2="5" y2="5" stroke="currentColor" stroke-width="2.5"></line></svg>
        </button>
        <button class="play-pause-circle" id="bpPlayPauseBtn" aria-label="Play/Pause">
          <svg class="bp-play-icon" viewBox="0 0 24 24" width="15" height="15" fill="currentColor"><polygon points="7 4 19 12 7 20 7 4"></polygon></svg>
          <svg class="bp-pause-icon" viewBox="0 0 24 24" width="15" height="15" fill="currentColor" style="display:none;"><rect x="6" y="4" width="3.5" height="16"></rect><rect x="14.5" y="4" width="3.5" height="16"></rect></svg>
        </button>
        <button class="ctrl-btn" id="bpNextBtn" aria-label="Nächster Song">
          <svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor"><polygon points="5 4 15 12 5 20 5 4"></polygon><line x1="19" y1="5" x2="19" y2="19" stroke="currentColor" stroke-width="2.5"></line></svg>
        </button>
      </div>
      <div class="timeline-wrap">
        <span class="time-stamp" id="bpCurrentTime">0:00</span>
        <div class="timeline-track" id="bpTimelineTrack">
          <div class="timeline-fill" id="bpTimelineFill"></div>
        </div>
        <span class="time-stamp" id="bpTotalTime">0:00</span>
      </div>
    </div>

    <div class="player-right">
      <span id="playerBadgeEssay" style="font-size:0.7rem;font-weight:800;color:var(--text-muted);letter-spacing:0.1em;">DE ESSAY</span>
    </div>
  </div>

  <!-- Hidden YouTube Player Container -->
  <div style="position: absolute; top: -9999px; left: -9999px; visibility: hidden;">
    <div id="ytPlayer"></div>
  </div>

  <!-- JavaScript Engine -->
  <script>
    // 1. Film Grain Animation
    const canvas = document.getElementById('grainCanvas');
    const ctx = canvas.getContext('2d');
    function resizeGrain() {{
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
    }}
    window.addEventListener('resize', resizeGrain);
    resizeGrain();

    function renderGrain() {{
      const w = canvas.width;
      const h = canvas.height;
      if (w > 0 && h > 0) {{
        const idata = ctx.createImageData(w, h);
        const b32 = new Uint32Array(idata.data.buffer);
        const len = b32.length;
        for (let i = 0; i < len; i++) {{
          if (Math.random() < 0.12) {{
            b32[i] = 0x22ffffff;
          }}
        }}
        ctx.putImageData(idata, 0, 0);
      }}
      requestAnimationFrame(renderGrain);
    }}
    requestAnimationFrame(renderGrain);

    // 2. Burger Drawer Logic
    const burgerToggle = document.getElementById('burgerToggle');
    const drawerNav = document.getElementById('drawerNav');
    const drawerOverlay = document.getElementById('drawerOverlay');
    const drawerClose = document.getElementById('drawerClose');

    function openDrawer() {{
      drawerNav.classList.add('active');
      drawerOverlay.classList.add('active');
    }}
    function closeDrawer() {{
      drawerNav.classList.remove('active');
      drawerOverlay.classList.remove('active');
    }}

    burgerToggle.addEventListener('click', openDrawer);
    drawerClose.addEventListener('click', closeDrawer);
    drawerOverlay.addEventListener('click', closeDrawer);

    // 3. Track List & Navigation State
    const trackList = {track_list_json};
    let currentTrackIdx = 0;
    let currentLanguage = 'de'; // 'de' | 'en'
    const navTrackCurrent = document.getElementById('navTrackCurrent');

    function setLanguage(lang) {{
      if (lang !== 'de' && lang !== 'en') return;
      currentLanguage = lang;
      
      document.getElementById('langBtnDE').classList.toggle('active', lang === 'de');
      document.getElementById('langBtnEN').classList.toggle('active', lang === 'en');
      
      document.querySelectorAll('.lang-de').forEach(el => {{
        el.style.display = (lang === 'de') ? '' : 'none';
      }});
      document.querySelectorAll('.lang-en').forEach(el => {{
        el.style.display = (lang === 'en') ? '' : 'none';
      }});
      
      const badge = document.getElementById('playerBadgeEssay');
      if (badge) badge.textContent = (lang === 'de') ? 'DE ESSAY' : 'EN ESSAY';
      
      // If audio essay is currently playing, switch source to chosen language seamlessly
      if (currentMode === 'essay' && currentAudio) {{
        const wasPlaying = !currentAudio.paused;
        const curTime = currentAudio.currentTime;
        playEssay(currentTrackIdx, wasPlaying);
      }}
    }}

    function goToTrack(idx) {{
      if (idx < 0) idx = trackList.length - 1;
      if (idx >= trackList.length) idx = 0;
      currentTrackIdx = idx;

      // Update slides
      document.querySelectorAll('.track-slide').forEach((slide, sIdx) => {{
        slide.classList.toggle('active', sIdx === currentTrackIdx);
      }});

      // Update navbar counter
      navTrackCurrent.textContent = trackList[currentTrackIdx].num;

      // Close drawer if open
      closeDrawer();

      // Scroll to slide header smoothly
      const activeSlide = document.getElementById('slide-' + trackList[currentTrackIdx].num);
      if (activeSlide) {{
        window.scrollTo({{
          top: activeSlide.offsetTop - 80,
          behavior: 'smooth'
        }});
      }}

      updateTrackUI(currentTrackIdx);
    }}

    document.getElementById('prevSlideBtn').addEventListener('click', () => {{
      goToTrack(currentTrackIdx - 1);
    }});
    document.getElementById('nextSlideBtn').addEventListener('click', () => {{
      goToTrack(currentTrackIdx + 1);
    }});

    // Keyboard Arrow Navigation
    window.addEventListener('keydown', (e) => {{
      if (e.key === 'ArrowLeft') goToTrack(currentTrackIdx - 1);
      if (e.key === 'ArrowRight') goToTrack(currentTrackIdx + 1);
    }});

    // 4. Media Audio Engine (YouTube + Neural TTS Audio Essay)
    let ytPlayer = null;
    let ytReady = false;
    let queuedVideoId = null;
    let currentMode = 'song'; // 'song' | 'essay'
    let currentAudio = null;
    let isPlaying = false;

    const bpTrackNum = document.getElementById('bpTrackNum');
    const bpTrackTitle = document.getElementById('bpTrackTitle');
    const bpPlayPauseBtn = document.getElementById('bpPlayPauseBtn');
    const bpPlayIcon = bpPlayPauseBtn.querySelector('.bp-play-icon');
    const bpPauseIcon = bpPlayPauseBtn.querySelector('.bp-pause-icon');
    const bpPrevBtn = document.getElementById('bpPrevBtn');
    const bpNextBtn = document.getElementById('bpNextBtn');
    const bpCurrentTime = document.getElementById('bpCurrentTime');
    const bpTotalTime = document.getElementById('bpTotalTime');
    const bpTimelineTrack = document.getElementById('bpTimelineTrack');
    const bpTimelineFill = document.getElementById('bpTimelineFill');

    function formatTime(seconds) {{
      if (isNaN(seconds) || seconds === 0) return '0:00';
      const m = Math.floor(seconds / 60);
      const s = Math.floor(seconds % 60);
      return `${{m}}:${{s < 10 ? '0' : ''}}${{s}}`;
    }}

    window.onYouTubeIframeAPIReady = function() {{
      ytPlayer = new YT.Player('ytPlayer', {{
        height: '200',
        width: '200',
        videoId: trackList[0].ytId,
        playerVars: {{ playsinline: 1, controls: 0, disablekb: 1, rel: 0 }},
        events: {{
          onReady: () => {{
            ytReady = true;
            if (queuedVideoId) {{
              ytPlayer.loadVideoById(queuedVideoId);
              if (isPlaying) ytPlayer.playVideo();
              queuedVideoId = null;
            }}
          }},
          onStateChange: (event) => {{
            if (currentMode !== 'song') return;
            if (event.data === YT.PlayerState.PLAYING) {{
              isPlaying = true;
              updateTrackUI(currentTrackIdx);
            }} else if (event.data === YT.PlayerState.PAUSED) {{
              isPlaying = false;
              updateTrackUI(currentTrackIdx);
            }} else if (event.data === YT.PlayerState.ENDED) {{
              // Automatischer Übergang zum Audio-Essay nach dem Song
              playEssay(currentTrackIdx, true);
            }}
          }}
        }}
      }});
    }};

    function updateTrackUI(idx) {{
      const track = trackList[idx];
      bpTrackNum.textContent = track.num;
      bpTrackTitle.textContent = track.title.toUpperCase();

      const songSub = document.querySelector('.sub-mode-song');
      const essaySub = document.querySelector('.sub-mode-essay');
      if (songSub && essaySub) {{
        songSub.style.display = currentMode === 'song' ? 'inline' : 'none';
        essaySub.style.display = currentMode === 'essay' ? 'inline' : 'none';
      }}

      document.querySelectorAll('.song-round-play-btn').forEach(btn => {{
        const isThis = (btn.getAttribute('data-track-num') === track.num) && (currentMode === 'song');
        btn.classList.toggle('playing', isThis && isPlaying);
        btn.querySelector('.play-icon').style.display = (isThis && isPlaying) ? 'none' : 'inline-block';
        btn.querySelector('.pause-icon').style.display = (isThis && isPlaying) ? 'inline-block' : 'none';
      }});

      document.querySelectorAll('.audio-play-btn').forEach(btn => {{
        const isThis = (btn.getAttribute('data-track-num') === track.num) && (currentMode === 'essay');
        btn.classList.toggle('playing', isThis && isPlaying);
        btn.querySelector('.play-icon').style.display = (isThis && isPlaying) ? 'none' : 'inline-block';
        btn.querySelector('.pause-icon').style.display = (isThis && isPlaying) ? 'inline-block' : 'none';
      }});

      bpPlayIcon.style.display = isPlaying ? 'none' : 'inline-block';
      bpPauseIcon.style.display = isPlaying ? 'inline-block' : 'none';
    }}

    function playSong(idx, autoPlay = true) {{
      currentMode = 'song';
      currentTrackIdx = (idx + trackList.length) % trackList.length;
      const track = trackList[currentTrackIdx];

      if (currentAudio) {{
        currentAudio.pause();
        currentAudio.currentTime = 0;
      }}

      bpTimelineFill.style.width = '0%';
      bpCurrentTime.textContent = '0:00';

      if (ytReady && ytPlayer && typeof ytPlayer.loadVideoById === 'function') {{
        ytPlayer.loadVideoById(track.ytId);
        if (autoPlay) {{
          ytPlayer.playVideo();
          isPlaying = true;
        }} else {{
          ytPlayer.pauseVideo();
          isPlaying = false;
        }}
      }} else {{
        queuedVideoId = track.ytId;
        isPlaying = autoPlay;
      }}
      updateTrackUI(currentTrackIdx);
    }}

    function playEssay(idx, autoPlay = true) {{
      currentMode = 'essay';
      currentTrackIdx = (idx + trackList.length) % trackList.length;
      const track = trackList[currentTrackIdx];

      if (ytReady && ytPlayer && typeof ytPlayer.pauseVideo === 'function') {{
        ytPlayer.pauseVideo();
      }}

      const langSuffix = (currentLanguage === 'en') ? 'en' : 'de';
      const audioSrc = `audio/track_${{track.num}}_${{langSuffix}}.mp3`;
      if (currentAudio) {{
        currentAudio.pause();
        currentAudio = null;
      }}

      currentAudio = new Audio(audioSrc);
      bpTimelineFill.style.width = '0%';
      bpCurrentTime.textContent = '0:00';

      currentAudio.addEventListener('loadedmetadata', () => {{
        bpTotalTime.textContent = formatTime(currentAudio.duration);
      }});

      currentAudio.addEventListener('timeupdate', () => {{
        if (!currentAudio || currentMode !== 'essay') return;
        bpCurrentTime.textContent = formatTime(currentAudio.currentTime);
        const pct = (currentAudio.currentTime / (currentAudio.duration || 1)) * 100;
        bpTimelineFill.style.width = `${{pct}}%`;
      }});

      currentAudio.addEventListener('ended', () => {{
        const nextIdx = (currentTrackIdx + 1) % trackList.length;
        goToTrack(nextIdx);
        playEssay(nextIdx, true);
      }});

      if (autoPlay) {{
        isPlaying = true;
        currentAudio.play().catch(e => console.log('Audio playback prevented:', e));
      }} else {{
        isPlaying = false;
      }}
      updateTrackUI(currentTrackIdx);
    }}

    // Play/Pause Bottom Player Toggle
    bpPlayPauseBtn.addEventListener('click', () => {{
      if (currentMode === 'song') {{
        if (ytReady && ytPlayer && typeof ytPlayer.getPlayerState === 'function') {{
          const state = ytPlayer.getPlayerState();
          if (state === YT.PlayerState.PLAYING) {{
            ytPlayer.pauseVideo();
            isPlaying = false;
          }} else {{
            ytPlayer.playVideo();
            isPlaying = true;
          }}
        }} else {{
          playSong(currentTrackIdx, true);
        }}
      }} else {{
        if (!currentAudio) {{
          playEssay(currentTrackIdx, true);
          return;
        }}
        if (currentAudio.paused) {{
          currentAudio.play();
          isPlaying = true;
        }} else {{
          currentAudio.pause();
          isPlaying = false;
        }}
      }}
      updateTrackUI(currentTrackIdx);
    }});

    // Player Prev / Next
    bpPrevBtn.addEventListener('click', () => {{
      goToTrack(currentTrackIdx - 1);
      if (currentMode === 'song') playSong(currentTrackIdx, true);
      else playEssay(currentTrackIdx, true);
    }});
    bpNextBtn.addEventListener('click', () => {{
      goToTrack(currentTrackIdx + 1);
      if (currentMode === 'song') playSong(currentTrackIdx, true);
      else playEssay(currentTrackIdx, true);
    }});

    // Timeline Scrubbing
    bpTimelineTrack.addEventListener('click', (e) => {{
      const rect = bpTimelineTrack.getBoundingClientRect();
      const clickX = e.clientX - rect.left;
      const pct = Math.max(0, Math.min(1, clickX / rect.width));

      if (currentMode === 'song' && ytReady && ytPlayer && typeof ytPlayer.getDuration === 'function') {{
        const dur = ytPlayer.getDuration() || 0;
        ytPlayer.seekTo(pct * dur, true);
      }} else if (currentMode === 'essay' && currentAudio && currentAudio.duration) {{
        currentAudio.currentTime = pct * currentAudio.duration;
      }}
    }});

    // YouTube Progress Poller
    setInterval(() => {{
      if (currentMode === 'song' && ytReady && ytPlayer && typeof ytPlayer.getCurrentTime === 'function' && typeof ytPlayer.getDuration === 'function') {{
        const cur = ytPlayer.getCurrentTime() || 0;
        const dur = ytPlayer.getDuration() || 0;
        bpCurrentTime.textContent = formatTime(cur);
        if (dur > 0) {{
          bpTotalTime.textContent = formatTime(dur);
          const pct = (cur / dur) * 100;
          bpTimelineFill.style.width = `${{pct}}%`;
        }}
      }}
    }}, 250);

    // In-Slide Buttons
    document.querySelectorAll('.song-round-play-btn').forEach(btn => {{
      btn.addEventListener('click', () => {{
        const numStr = btn.getAttribute('data-track-num');
        const targetIdx = trackList.findIndex(t => t.num === numStr);
        if (targetIdx === currentTrackIdx && currentMode === 'song') {{
          if (isPlaying) {{
            if (ytReady && ytPlayer) ytPlayer.pauseVideo();
            isPlaying = false;
          }} else {{
            if (ytReady && ytPlayer) ytPlayer.playVideo();
            isPlaying = true;
          }}
          updateTrackUI(currentTrackIdx);
        }} else {{
          playSong(targetIdx, true);
        }}
      }});
    }});

    document.querySelectorAll('.audio-play-btn').forEach(btn => {{
      btn.addEventListener('click', () => {{
        const numStr = btn.getAttribute('data-track-num');
        const targetIdx = trackList.findIndex(t => t.num === numStr);
        if (targetIdx === currentTrackIdx && currentMode === 'essay' && currentAudio) {{
          if (currentAudio.paused) {{
            currentAudio.play();
            isPlaying = true;
          }} else {{
            currentAudio.pause();
            isPlaying = false;
          }}
          updateTrackUI(currentTrackIdx);
        }} else {{
          playEssay(targetIdx, true);
        }}
      }});
    }});

    // Initialize Language to DE by default
    setLanguage('de');
    updateTrackUI(0);
  </script>
</body>
</html>
'''
    return full_html

if __name__ == "__main__":
    html_output = build_carousel_html()
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html_output)
    print("Carousel HTML generated successfully into index.html!")
