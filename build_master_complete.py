# -*- coding: utf-8 -*-
"""
TOMORA Album Review & Literary Interpretation
Single-Page Dynamic Bilingual Master (Instant DE <-> EN Toggle)
"""

import os
import sys
import json
import re

# Import modules
from analysis_modules.tracks_01_04 import de_tracks_01_04, en_tracks_01_04
from analysis_modules.tracks_05_08 import de_tracks_05_08, en_tracks_05_08
from analysis_modules.tracks_09_12 import de_tracks_09_12, en_tracks_09_12

# Combine all modules
de_tracks_deep = {}
de_tracks_deep.update(de_tracks_01_04)
de_tracks_deep.update(de_tracks_05_08)
de_tracks_deep.update(de_tracks_09_12)

en_tracks_deep = {}
en_tracks_deep.update(en_tracks_01_04)
en_tracks_deep.update(en_tracks_05_08)
en_tracks_deep.update(en_tracks_09_12)

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

phase1_dir = "c:/Users/Hakan/Documents/antigravity/modest-meitner/album_analyse_fallstudie/Phase_1_Mikro_Dekonstruktion"

def clean_txt(t):
    return re.sub(r'[^a-zA-Z0-9]', '', t).lower()

def extract_stanzas_for_track(num_str, title, analysis_cards):
    p1_file = f"{num_str}_{title.replace(' ', '_')}.md"
    p1_path = os.path.join(phase1_dir, p1_file)
    if not os.path.exists(p1_path):
        for f in os.listdir(phase1_dir):
            if f.startswith(num_str):
                p1_path = os.path.join(phase1_dir, f)
                break
                
    lyrics_raw = ""
    if os.path.exists(p1_path):
        with open(p1_path, 'r', encoding='utf-8', errors='ignore') as f:
            p1_content = f.read()
        lyrics_match = re.search(r'### 1\.\s*Transkribierter Textkorpus\s*```text(.*?)```', p1_content, re.DOTALL)
        lyrics_raw = lyrics_match.group(1).strip() if lyrics_match else ""

    stanzas = []
    current_stanza = {"title": "", "lines": []}
    
    raw_lines = lyrics_raw.split('\n')
    cleaned_raw_lines = []
    for line in raw_lines:
        line_s = line.strip()
        is_title_line = False
        c_line = clean_txt(line_s)
        c_title = clean_txt(title)
        c_num = str(int(num_str))
        if (c_title in c_line and (c_num in c_line or num_str in c_line)) or line_s.lower() == f"{title.lower()} {c_num}." or line_s.lower() == f"{c_num}. {title.lower()}":
            is_title_line = True
            
        if not is_title_line:
            cleaned_raw_lines.append(line)

    total_valid_lines = len([l for l in cleaned_raw_lines if l.strip() and not (l.strip().startswith('[') and l.strip().endswith(']'))])
    line_idx_tracker = 0

    for line in cleaned_raw_lines:
        line_s = line.strip()
        if line_s.startswith('[') and line_s.endswith(']'):
            if current_stanza["lines"]:
                stanzas.append(current_stanza)
            current_stanza = {"title": line_s, "lines": []}
        elif line_s:
            matched_card_idx = 0
            if len(analysis_cards) > 1:
                ratio = line_idx_tracker / max(1, total_valid_lines)
                matched_card_idx = min(int(ratio * len(analysis_cards)), len(analysis_cards) - 1)

            current_stanza["lines"].append({
                "text": line_s,
                "target_card": matched_card_idx
            })
            line_idx_tracker += 1
        else:
            if current_stanza["lines"]:
                stanzas.append(current_stanza)
                current_stanza = {"title": "", "lines": []}
    if current_stanza["lines"]:
        stanzas.append(current_stanza)

    return stanzas

def render_markdown_block(text):
    text = text.strip()
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'(?<!\*)\*([^*]+?)\*(?!\*)', r'<em>\1</em>', text)
    text = re.sub(r'`([^`]+?)`', r'<code style="color:var(--magenta);font-family:monospace;">\1</code>', text)
    return text

def render_analysis_column_for_lang(review_raw, cards, num, lang):
    # Render review markdown
    paragraphs = [p.strip() for p in review_raw.strip().split('\n\n') if p.strip()]
    p_html_parts = []
    for p in paragraphs:
        if p.startswith('###'):
            kicker = re.sub(r'^###\s*(Track\s*\d+:?\s*[^—–\-]+[—–\-])?\s*', '', p).strip()
            if kicker:
                p_html_parts.append(f'<div style="font-size:1.15rem;font-weight:800;color:#ffffff;margin-bottom:16px;letter-spacing:-0.01em;">{render_markdown_block(kicker)}</div>')
        else:
            p_rendered = render_markdown_block(p)
            p_html_parts.append(f'<p>{p_rendered}</p>')
    review_html = "\n".join(p_html_parts)

    # Render cards
    cards_html_parts = []
    for idx, card in enumerate(cards):
        q = card["quote"]
        b = card["body"].strip()
        b_paragraphs = [bp.strip() for bp in b.split('\n\n') if bp.strip()]
        b_p_html = []
        for bp in b_paragraphs:
            b_rendered = render_markdown_block(bp)
            b_p_html.append(f'<p>{b_rendered}</p>')
        cards_body_html = "\n".join(b_p_html)

        cards_html_parts.append(f"""
        <div class="analysis-card" id="card-{num}-{lang}-{idx}">
          <span class="card-quote">{q}</span>
          <div class="card-body">
            {cards_body_html}
          </div>
        </div>
        """)
    cards_rendered = "\n".join(cards_html_parts)

    return f"""
    <div class="lang-block lang-{lang}">
      <div class="narrative-review">
        {review_html}
      </div>
      <div class="analysis-cards-list">
        {cards_rendered}
      </div>
    </div>
    """

def render_track_html(num, title, stanzas, de_info, en_info):
    # Render stanzas
    lyrics_html_parts = []
    line_global_idx = 0
    for s in stanzas:
        lyrics_html_parts.append('<div class="stanza">')
        if s["title"]:
            lyrics_html_parts.append(f'<div class="stanza-title">{s["title"]}</div>')
        for l in s["lines"]:
            text = l["text"]
            target_card = l["target_card"]
            lyrics_html_parts.append(
                f'<span class="lyric-line" data-line-idx="{line_global_idx}" data-target-card="{target_card}">{text}</span>'
            )
            line_global_idx += 1
        lyrics_html_parts.append('</div>')
    lyrics_rendered = "\n".join(lyrics_html_parts)

    # Render German and English analysis blocks
    de_analysis_html = render_analysis_column_for_lang(de_info["review"], de_info["cards"], num, "de")
    en_analysis_html = render_analysis_column_for_lang(en_info["review"], en_info["cards"], num, "en")

    return f"""
    <section class="track-section" id="track-{num}">
      <div class="track-header-bar">
        <div class="track-title-wrap">
          <span class="track-num-badge">{num}</span>
          <h2 class="track-heading">{title}</h2>
        </div>
        <button class="audio-play-btn" data-track-num="{num}" aria-label="Listen to Audio Essay">
          <svg class="play-icon" viewBox="0 0 24 24" width="13" height="13"><polygon points="6 4 20 12 6 20 6 4" fill="currentColor"></polygon></svg>
          <svg class="pause-icon" viewBox="0 0 24 24" width="13" height="13" style="display:none;"><rect x="5" y="4" width="4" height="16" fill="currentColor"></rect><rect x="15" y="4" width="4" height="16" fill="currentColor"></rect></svg>
          <span class="btn-text">
            <span class="lang-de">Audio-Essay</span>
            <span class="lang-en">Audio Essay</span>
          </span>
        </button>
      </div>
      <div class="track-grid">
        <div class="lyrics-col">
          {lyrics_rendered}
        </div>
        <div class="analysis-col">
          {de_analysis_html}
          {en_analysis_html}
        </div>
      </div>
    </section>
    """

HTML_MASTER_TEMPLATE = """<!DOCTYPE html>
<html lang="de">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>TOMORA — Album Review & Interpretation</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg: #0c0c0f;
      --bg-surface: #141418;
      --text: #ffffff;
      --text-muted: #8e8e93;
      --magenta: #ff007a;
      --magenta-dim: rgba(255, 0, 122, 0.12);
      --magenta-glow: rgba(255, 0, 122, 0.35);
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

    /* Dynamic Language Visibility */
    body[data-lang="de"] .lang-en { display: none !important; }
    body[data-lang="en"] .lang-de { display: none !important; }

    /* Animierter 35mm Analog-Film-Grain Canvas */
    #grainCanvas {
      position: fixed;
      top: 0;
      left: 0;
      width: 100vw;
      height: 100vh;
      pointer-events: none;
      z-index: 9999;
      opacity: 0.11;
      mix-blend-mode: screen;
    }

    ::selection {
      background-color: var(--magenta);
      color: #ffffff;
    }

    /* Minimalistische Navbar */
    .navbar {
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
    }

    .nav-left {
      display: flex;
      align-items: center;
    }

    .burger-btn {
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
    }

    .burger-btn span {
      display: block;
      width: 100%;
      height: 2px;
      background-color: #ffffff;
      transition: background-color 0.2s;
    }

    .burger-btn:hover span {
      background-color: var(--magenta);
    }

    .nav-center {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      text-align: center;
    }

    .brand-title {
      font-size: 1.1rem;
      font-weight: 900;
      letter-spacing: 0.25em;
      color: #ffffff;
      text-transform: uppercase;
      line-height: 1;
    }

    .nav-right {
      display: flex;
      justify-content: flex-end;
      align-items: center;
      gap: 16px;
    }

    .lang-toggle-btn {
      background: rgba(255, 255, 255, 0.06);
      color: var(--text-muted);
      border: 1px solid rgba(255, 255, 255, 0.15);
      padding: 6px 14px;
      border-radius: 4px;
      font-size: 0.75rem;
      font-weight: 800;
      letter-spacing: 0.15em;
      cursor: pointer;
      text-transform: uppercase;
      transition: all 0.2s ease;
      display: inline-flex;
      align-items: center;
      gap: 6px;
    }

    .lang-toggle-btn:hover {
      color: #ffffff;
      border-color: var(--magenta);
      background: var(--magenta-dim);
    }

    .lang-toggle-btn span.active-indicator {
      color: var(--magenta);
      font-weight: 900;
    }

    /* Burger Drawer */
    .drawer-overlay {
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
      padding: 20px 32px 36px 32px;
      display: flex;
      flex-direction: column;
      transition: left 0.35s cubic-bezier(0.16, 1, 0.3, 1);
      overflow-y: auto;
    }
    .drawer.active { left: 0; }

    .drawer-header {
      height: 25px;
      display: flex;
      align-items: center;
      gap: 20px;
      margin-bottom: 36px;
    }

    .drawer-close-btn {
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
    }

    .drawer-close-btn span {
      display: block;
      width: 24px;
      height: 2px;
      background-color: var(--magenta);
      position: absolute;
      top: 11px;
      left: 0;
      transition: background-color 0.2s;
    }

    .drawer-close-btn span:nth-child(1) { transform: rotate(45deg); }
    .drawer-close-btn span:nth-child(2) { transform: rotate(-45deg); }
    .drawer-close-btn:hover span { background-color: #ffffff; }

    .drawer-title {
      font-size: 0.85rem;
      font-weight: 800;
      letter-spacing: 0.15em;
      text-transform: uppercase;
      color: var(--magenta);
      line-height: 1;
    }

    .drawer-nav {
      list-style: none;
      display: flex;
      flex-direction: column;
      gap: 14px;
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

    /* FULL BLEED HERO VIDEO */
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

    .hero-video {
      width: 100%;
      height: 100%;
      object-fit: cover;
      display: block;
      max-height: 75vh;
    }

    /* Layout Wrapper */
    .main-wrapper {
      max-width: 1400px;
      margin: 0 auto;
      padding: 60px 32px 120px 32px;
    }

    .album-header {
      margin-bottom: 80px;
      text-align: center;
    }

    .album-meta-tag {
      display: inline-block;
      font-size: 0.75rem;
      font-weight: 800;
      letter-spacing: 0.25em;
      color: var(--magenta);
      text-transform: uppercase;
      margin-bottom: 12px;
    }

    .album-main-title {
      font-size: clamp(2.5rem, 5vw, 4rem);
      font-weight: 900;
      letter-spacing: -0.02em;
      line-height: 1.1;
      margin-bottom: 16px;
    }

    .album-subtitle {
      font-size: 1.15rem;
      color: var(--text-muted);
      max-width: 700px;
      margin: 0 auto;
      font-weight: 400;
      line-height: 1.6;
    }

    /* Track Container */
    .track-section {
      margin-bottom: 140px;
      scroll-margin-top: 100px;
    }

    .track-header-bar {
      margin-bottom: 40px;
      padding-bottom: 16px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 16px;
      flex-wrap: wrap;
    }

    .track-title-wrap {
      display: flex;
      align-items: baseline;
      gap: 16px;
    }

    .audio-play-btn {
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid rgba(255, 255, 255, 0.15);
      color: #cfcfd4;
      padding: 6px 14px;
      border-radius: 20px;
      font-size: 0.75rem;
      font-weight: 700;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 8px;
      transition: all 0.2s ease;
      user-select: none;
    }

    .audio-play-btn:hover {
      color: #ffffff;
      border-color: var(--magenta);
      background: var(--magenta-dim);
    }

    .audio-play-btn.playing {
      color: #ffffff;
      border-color: var(--magenta);
      background: rgba(255, 0, 122, 0.25);
      box-shadow: 0 0 15px var(--magenta-glow);
    }

    .track-num-badge {
      font-size: 1.2rem;
      font-weight: 900;
      color: var(--magenta);
      letter-spacing: 0.1em;
    }

    .track-heading {
      font-size: clamp(1.8rem, 3.5vw, 2.5rem);
      font-weight: 900;
      letter-spacing: -0.01em;
      color: #ffffff;
      text-transform: uppercase;
    }

    /* Two-Column Genius Layout */
    .track-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 60px;
      align-items: start;
    }

    @media (max-width: 992px) {
      .track-grid {
        grid-template-columns: 1fr;
        gap: 40px;
      }
    }

    /* Left Column: Lyrics */
    .lyrics-col {
      display: flex;
      flex-direction: column;
      gap: 28px;
    }

    .stanza {
      display: flex;
      flex-direction: column;
      gap: 8px;
    }

    .stanza-title {
      font-size: 0.75rem;
      font-weight: 800;
      letter-spacing: 0.15em;
      text-transform: uppercase;
      color: var(--magenta);
      margin-bottom: 4px;
    }

    .lyric-line {
      font-size: 1.08rem;
      font-weight: 500;
      color: rgba(255, 255, 255, 0.75);
      cursor: pointer;
      padding: 4px 8px;
      margin-left: -8px;
      border-radius: 4px;
      transition: all 0.2s ease;
      user-select: none;
      display: block;
      width: fit-content;
    }

    .lyric-line:hover {
      color: var(--magenta);
      background-color: var(--magenta-dim);
    }

    .lyric-line.active {
      color: #ffffff;
      background-color: var(--magenta-dim);
      font-weight: 700;
      box-shadow: 0 0 20px var(--magenta-glow);
    }

    /* Right Column: Analysis */
    .analysis-col {
      display: flex;
      flex-direction: column;
      gap: 32px;
    }

    .lang-block {
      display: flex;
      flex-direction: column;
      gap: 32px;
    }

    .narrative-review {
      background: transparent;
      font-size: 1.05rem;
      color: #cfcfd4;
      line-height: 1.8;
      font-weight: 400;
    }

    .narrative-review p {
      margin-bottom: 16px;
    }

    .narrative-review p:last-child {
      margin-bottom: 0;
    }

    .narrative-review em {
      color: #ffffff;
      font-style: italic;
    }

    .narrative-review strong {
      color: #ffffff;
      font-weight: 700;
    }

    .analysis-cards-list {
      display: flex;
      flex-direction: column;
      gap: 20px;
    }

    .analysis-card {
      background: var(--bg-surface);
      border-radius: 8px;
      padding: 24px 28px;
      transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
      scroll-margin-top: 120px;
      position: relative;
    }

    .analysis-card.active {
      background: #18181e;
      box-shadow: 0 0 0 2px var(--magenta), 0 12px 30px rgba(0, 0, 0, 0.5);
    }

    .card-quote {
      font-size: 0.85rem;
      font-weight: 800;
      color: var(--magenta);
      text-transform: uppercase;
      letter-spacing: 0.08em;
      margin-bottom: 12px;
      display: block;
    }

    .card-body {
      font-size: 0.98rem;
      color: #d0d0d5;
      line-height: 1.7;
    }

    .card-body p {
      margin-bottom: 12px;
    }
    .card-body p:last-child {
      margin-bottom: 0;
    }

    /* Footer */
    footer {
      border-top: 1px solid rgba(255, 255, 255, 0.08);
      padding: 60px 32px 120px 32px;
      text-align: center;
      color: var(--text-muted);
      font-size: 0.85rem;
      letter-spacing: 0.05em;
    }

    footer p {
      margin-bottom: 8px;
    }

    /* BOTTOM MINI PLAYER (Matching top navbar glass & drop-shadow) */
    .bottom-player {
      position: fixed;
      bottom: 0;
      left: 0;
      width: 100%;
      height: 75px;
      background: rgba(12, 12, 15, 0.85);
      backdrop-filter: blur(20px);
      -webkit-backdrop-filter: blur(20px);
      border-top: 1px solid rgba(255, 255, 255, 0.08);
      box-shadow: 0 -10px 30px rgba(0, 0, 0, 0.5);
      display: grid;
      grid-template-columns: 280px 1fr 280px;
      align-items: center;
      padding: 0 32px;
      z-index: 1000;
    }

    .player-left {
      display: flex;
      flex-direction: column;
      gap: 2px;
    }

    .player-track-info {
      display: flex;
      align-items: baseline;
      gap: 8px;
    }

    .player-track-num {
      font-size: 0.8rem;
      font-weight: 900;
      color: var(--magenta);
      letter-spacing: 0.08em;
    }

    .player-track-title {
      font-size: 0.95rem;
      font-weight: 800;
      color: #ffffff;
      text-transform: uppercase;
      letter-spacing: 0.04em;
    }

    .player-subtitle {
      font-size: 0.7rem;
      color: var(--text-muted);
      letter-spacing: 0.05em;
    }

    .player-center {
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 6px;
      max-width: 580px;
      margin: 0 auto;
      width: 100%;
    }

    .player-controls {
      display: flex;
      align-items: center;
      gap: 18px;
    }

    .ctrl-btn {
      background: none;
      border: none;
      color: var(--text-muted);
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 4px;
      transition: all 0.2s;
    }

    .ctrl-btn:hover {
      color: #ffffff;
    }

    .play-pause-circle {
      width: 36px;
      height: 36px;
      border-radius: 50%;
      background: #ffffff;
      color: #0c0c0f;
      display: flex;
      align-items: center;
      justify-content: center;
      border: none;
      cursor: pointer;
      transition: all 0.2s;
    }

    .play-pause-circle:hover {
      background: var(--magenta);
      color: #ffffff;
      box-shadow: 0 0 15px var(--magenta-glow);
    }

    .timeline-wrap {
      display: flex;
      align-items: center;
      gap: 12px;
      width: 100%;
    }

    .time-stamp {
      font-size: 0.72rem;
      color: var(--text-muted);
      font-variant-numeric: tabular-nums;
      font-family: monospace;
      min-width: 32px;
    }

    .timeline-track {
      flex: 1;
      height: 4px;
      background: rgba(255, 255, 255, 0.15);
      border-radius: 2px;
      cursor: pointer;
      position: relative;
    }

    .timeline-track:hover {
      height: 6px;
    }

    .timeline-fill {
      height: 100%;
      background: var(--magenta);
      border-radius: 2px;
      width: 0%;
      pointer-events: none;
      position: relative;
    }

    .timeline-thumb {
      position: absolute;
      right: -5px;
      top: 50%;
      transform: translateY(-50%);
      width: 10px;
      height: 10px;
      border-radius: 50%;
      background: #ffffff;
      box-shadow: 0 0 8px var(--magenta-glow);
      display: none;
    }

    .timeline-track:hover .timeline-thumb {
      display: block;
    }

    .player-right {
      display: flex;
      justify-content: flex-end;
      align-items: center;
      gap: 12px;
    }

    .player-lang-badge {
      font-size: 0.7rem;
      font-weight: 800;
      color: var(--text-muted);
      border: 1px solid rgba(255, 255, 255, 0.12);
      padding: 3px 8px;
      border-radius: 4px;
      letter-spacing: 0.1em;
    }

    @media (max-width: 850px) {
      .bottom-player {
        grid-template-columns: 1fr;
        height: auto;
        padding: 10px 18px;
        gap: 8px;
      }
      .player-left { display: none; }
      .player-right { display: none; }
    }
  </style>
</head>
<body data-lang="de">

  <!-- Grain Overlay -->
  <canvas id="grainCanvas"></canvas>

  <!-- Navbar -->
  <nav class="navbar">
    <div class="nav-left">
      <button class="burger-btn" id="burgerToggle" aria-label="Open Track Navigation">
        <span></span>
        <span></span>
        <span></span>
      </button>
    </div>
    <div class="nav-center">
      <div class="brand-title">TOMORA</div>
    </div>
    <div class="nav-right">
      <button class="lang-toggle-btn" id="langToggleBtn" aria-label="Switch Language">
        <span class="lang-de">EN</span>
        <span class="lang-en">DE</span>
      </button>
    </div>
  </nav>

  <!-- Burger Drawer -->
  <div class="drawer-overlay" id="drawerOverlay"></div>
  <div class="drawer" id="drawerNav">
    <div class="drawer-header">
      <button class="drawer-close-btn" id="drawerClose" aria-label="Close Navigation">
        <span></span>
        <span></span>
      </button>
      <div class="drawer-title">
        <span class="lang-de">Titelauswahl</span>
        <span class="lang-en">Track Selection</span>
      </div>
    </div>
    <ul class="drawer-nav">
      [[DRAWER_ITEMS]]
    </ul>
  </div>

  <!-- Hero Video -->
  <div class="hero-fullbleed">
    <video class="hero-video" autoplay loop muted playsinline>
      <source src="hero_video.mp4" type="video/mp4">
    </video>
  </div>

  <!-- Main Content -->
  <main class="main-wrapper">
    <header class="album-header">
      <span class="album-meta-tag">
        <span class="lang-de">Vollständige Werkanalyse & Psychogramm</span>
        <span class="lang-en">Full Work Analysis & Psychogram</span>
      </span>
      <h1 class="album-main-title">TOMORA</h1>
      <p class="album-subtitle">
        <span class="lang-de">Eine detaillierte literarische und psychoanalytische Untersuchung über Bindung, Verlust, seelische Dekonstruktion und die Rückkehr zur autonomen Souveränität.</span>
        <span class="lang-en">An in-depth literary and psychoanalytic examination of attachment, loss, psychological deconstruction, and the reclamation of sovereign autonomy.</span>
      </p>
    </header>

    <div class="tracks-list">
      [[TRACKS_HTML]]
    </div>
  </main>

  <footer>
    <p><strong>TOMORA</strong> — Album Review & Interpretation</p>
    <p>
      <span class="lang-de">Literarische und psychoanalytische Gesamtschau aller 12 Stücke.</span>
      <span class="lang-en">Literary and psychoanalytic study across all 12 tracks.</span>
    </p>
  </footer>

  <!-- Bottom Mini Player -->
  <div class="bottom-player" id="bottomPlayer">
    <div class="player-left">
      <div class="player-track-info">
        <span class="player-track-num" id="bpTrackNum">01</span>
        <span class="player-track-title" id="bpTrackTitle">PLEASE</span>
      </div>
      <div class="player-subtitle">
        <span class="lang-de">Neural Audio-Essay</span>
        <span class="lang-en">Neural Audio Essay</span>
      </div>
    </div>

    <div class="player-center">
      <div class="player-controls">
        <button class="ctrl-btn" id="bpPrevBtn" aria-label="Previous Track">
          <svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor"><polygon points="19 20 9 12 19 4 19 20"></polygon><line x1="5" y1="4" x2="5" y2="20" stroke="currentColor" stroke-width="2.5"></line></svg>
        </button>

        <button class="play-pause-circle" id="bpPlayPauseBtn" aria-label="Play or Pause">
          <svg class="bp-play-icon" viewBox="0 0 24 24" width="14" height="14" fill="currentColor"><polygon points="7 4 19 12 7 20 7 4"></polygon></svg>
          <svg class="bp-pause-icon" viewBox="0 0 24 24" width="14" height="14" fill="currentColor" style="display:none;"><rect x="6" y="4" width="3.5" height="16"></rect><rect x="14.5" y="4" width="3.5" height="16"></rect></svg>
        </button>

        <button class="ctrl-btn" id="bpNextBtn" aria-label="Next Track">
          <svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor"><polygon points="5 4 15 12 5 20 5 4"></polygon><line x1="19" y1="4" x2="19" y2="20" stroke="currentColor" stroke-width="2.5"></line></svg>
        </button>
      </div>

      <div class="timeline-wrap">
        <span class="time-stamp" id="bpCurrentTime">0:00</span>
        <div class="timeline-track" id="bpTimelineTrack">
          <div class="timeline-fill" id="bpTimelineFill">
            <div class="timeline-thumb"></div>
          </div>
        </div>
        <span class="time-stamp" id="bpTotalTime">0:00</span>
      </div>
    </div>

    <div class="player-right">
      <span class="player-lang-badge" id="bpLangBadge">DE</span>
    </div>
  </div>

  <script>
    // Track List Metadata
    const trackList = [
      { num: "01", title: "Please" },
      { num: "02", title: "Come Closer" },
      { num: "03", title: "A Boy Like You" },
      { num: "04", title: "Ring The Alarm" },
      { num: "05", title: "My Baby" },
      { num: "06", title: "Have You Seen Me Dance Alone" },
      { num: "07", title: "Somewhere Else" },
      { num: "08", title: "I Drink The Light" },
      { num: "09", title: "Wavelengths" },
      { num: "10", title: "Side By Side" },
      { num: "11", title: "The Thing" },
      { num: "12", title: "In A Minute" }
    ];

    // 1. Animierter 35mm Analog-Film-Grain
    (function initGrain() {
      const canvas = document.getElementById('grainCanvas');
      const ctx = canvas.getContext('2d');
      let width = canvas.width = window.innerWidth;
      let height = canvas.height = window.innerHeight;

      window.addEventListener('resize', () => {
        width = canvas.width = window.innerWidth;
        height = canvas.height = window.innerHeight;
      });

      function generateNoise() {
        const imgData = ctx.createImageData(width, height);
        const buffer = new Uint32Array(imgData.data.buffer);
        const len = buffer.length;
        for (let i = 0; i < len; i++) {
          if (Math.random() < 0.15) {
            const gray = Math.floor(Math.random() * 255);
            buffer[i] = (255 << 24) | (gray << 16) | (gray << 8) | gray;
          }
        }
        ctx.putImageData(imgData, 0, 0);
      }

      let frame = 0;
      function loop() {
        if (frame % 2 === 0) {
          generateNoise();
        }
        frame++;
        requestAnimationFrame(loop);
      }
      loop();
    })();

    // 2. Burger Drawer Navigation
    const burgerToggle = document.getElementById('burgerToggle');
    const drawerOverlay = document.getElementById('drawerOverlay');
    const drawerNav = document.getElementById('drawerNav');
    const drawerClose = document.getElementById('drawerClose');

    function openDrawer() {
      drawerOverlay.classList.add('active');
      drawerNav.classList.add('active');
      document.body.style.overflow = 'hidden';
    }

    function closeDrawer() {
      drawerOverlay.classList.remove('active');
      drawerNav.classList.remove('active');
      document.body.style.overflow = '';
    }

    burgerToggle.addEventListener('click', openDrawer);
    drawerOverlay.addEventListener('click', closeDrawer);
    drawerClose.addEventListener('click', closeDrawer);

    document.querySelectorAll('.drawer-nav a').forEach(link => {
      link.addEventListener('click', () => {
        closeDrawer();
      });
    });

    // 3. Dynamic Language Switcher (Instant & Non-Destructive)
    let currentLang = localStorage.getItem('tomora_lang') || 'de';
    const langToggleBtn = document.getElementById('langToggleBtn');

    function setLanguage(lang) {
      currentLang = lang;
      document.body.setAttribute('data-lang', lang);
      document.documentElement.lang = lang;
      localStorage.setItem('tomora_lang', lang);
      document.title = (lang === 'de') 
        ? 'TOMORA — Album Review & Psychoanalytische Interpretation'
        : 'TOMORA — Album Review & Literary Interpretation';
      
      const bpLangBadge = document.getElementById('bpLangBadge');
      if (bpLangBadge) bpLangBadge.textContent = lang.toUpperCase();
    }

    langToggleBtn.addEventListener('click', () => {
      setLanguage(currentLang === 'de' ? 'en' : 'de');
    });

    setLanguage(currentLang);

    // 4. Genius-Style Line Highlight & Scroll Interactivity
    document.querySelectorAll('.lyric-line').forEach(lineEl => {
      lineEl.addEventListener('click', () => {
        const trackSection = lineEl.closest('.track-section');
        const targetCardIdx = lineEl.getAttribute('data-target-card');

        trackSection.querySelectorAll('.lyric-line').forEach(l => l.classList.remove('active'));
        lineEl.classList.add('active');

        const activeLangBlock = trackSection.querySelector(`.lang-${currentLang}`);
        if (activeLangBlock) {
          const cards = activeLangBlock.querySelectorAll('.analysis-card');
          cards.forEach((card, idx) => {
            if (idx.toString() === targetCardIdx) {
              card.classList.add('active');
              card.scrollIntoView({ behavior: 'smooth', block: 'center' });
            } else {
              card.classList.remove('active');
            }
          });
        }
      });
    });

    // 5. Neural TTS Unified Audio Player (Header Buttons + Bottom Mini Player with Timeline)
    let currentAudio = null;
    let currentTrackIdx = 0;
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

    function formatTime(seconds) {
      if (isNaN(seconds) || seconds === 0) return '0:00';
      const m = Math.floor(seconds / 60);
      const s = Math.floor(seconds % 60);
      return `${m}:${s < 10 ? '0' : ''}${s}`;
    }

    function updateTrackUI(idx) {
      const track = trackList[idx];
      bpTrackNum.textContent = track.num;
      bpTrackTitle.textContent = track.title.toUpperCase();

      document.querySelectorAll('.audio-play-btn').forEach(btn => {
        const isThis = btn.getAttribute('data-track-num') === track.num;
        btn.classList.toggle('playing', isThis && isPlaying);
        btn.querySelector('.play-icon').style.display = (isThis && isPlaying) ? 'none' : 'inline-block';
        btn.querySelector('.pause-icon').style.display = (isThis && isPlaying) ? 'inline-block' : 'none';
      });

      bpPlayIcon.style.display = isPlaying ? 'none' : 'inline-block';
      bpPauseIcon.style.display = isPlaying ? 'inline-block' : 'none';
    }

    function loadAndPlayTrack(idx, autoPlay = true) {
      currentTrackIdx = (idx + trackList.length) % trackList.length;
      const track = trackList[currentTrackIdx];
      const audioSrc = `audio/track_${track.num}_${currentLang}.mp3`;

      if (currentAudio) {
        currentAudio.pause();
        currentAudio = null;
      }

      currentAudio = new Audio(audioSrc);
      bpTimelineFill.style.width = '0%';
      bpCurrentTime.textContent = '0:00';

      currentAudio.addEventListener('loadedmetadata', () => {
        bpTotalTime.textContent = formatTime(currentAudio.duration);
      });

      currentAudio.addEventListener('timeupdate', () => {
        if (!currentAudio) return;
        bpCurrentTime.textContent = formatTime(currentAudio.currentTime);
        const pct = (currentAudio.currentTime / (currentAudio.duration || 1)) * 100;
        bpTimelineFill.style.width = `${pct}%`;
      });

      currentAudio.addEventListener('ended', () => {
        // Auto-play next track
        loadAndPlayTrack(currentTrackIdx + 1, true);
      });

      if (autoPlay) {
        isPlaying = true;
        currentAudio.play().catch(e => console.log('Audio playback prevented:', e));
      } else {
        isPlaying = false;
      }
      updateTrackUI(currentTrackIdx);
    }

    // Toggle Play/Pause on Bottom Player
    bpPlayPauseBtn.addEventListener('click', () => {
      if (!currentAudio) {
        loadAndPlayTrack(currentTrackIdx, true);
        return;
      }
      if (currentAudio.paused) {
        currentAudio.play();
        isPlaying = true;
      } else {
        currentAudio.pause();
        isPlaying = false;
      }
      updateTrackUI(currentTrackIdx);
    });

    // Prev / Next Controls
    bpPrevBtn.addEventListener('click', () => {
      loadAndPlayTrack(currentTrackIdx - 1, true);
    });

    bpNextBtn.addEventListener('click', () => {
      loadAndPlayTrack(currentTrackIdx + 1, true);
    });

    // Timeline Scrubbing
    bpTimelineTrack.addEventListener('click', (e) => {
      if (!currentAudio || !currentAudio.duration) return;
      const rect = bpTimelineTrack.getBoundingClientRect();
      const clickX = e.clientX - rect.left;
      const pct = Math.max(0, Math.min(1, clickX / rect.width));
      currentAudio.currentTime = pct * currentAudio.duration;
    });

    // In-Page Track Header Audio Play Buttons
    document.querySelectorAll('.audio-play-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        const numStr = btn.getAttribute('data-track-num');
        const targetIdx = trackList.findIndex(t => t.num === numStr);

        if (targetIdx === currentTrackIdx && currentAudio) {
          if (currentAudio.paused) {
            currentAudio.play();
            isPlaying = true;
          } else {
            currentAudio.pause();
            isPlaying = false;
          }
          updateTrackUI(currentTrackIdx);
        } else {
          loadAndPlayTrack(targetIdx, true);
        }
      });
    });

    // Switch Audio when Language changes
    const prevSetLang = setLanguage;
    setLanguage = function(lang) {
      const wasAudioPlaying = isPlaying;
      const savedTime = currentAudio ? currentAudio.currentTime : 0;
      prevSetLang(lang);
      if (currentAudio) {
        loadAndPlayTrack(currentTrackIdx, wasAudioPlaying);
        if (currentAudio) {
          currentAudio.currentTime = savedTime;
        }
      }
    };

    // Initialize bottom player with track 1
    updateTrackUI(0);
  </script>
</body>
</html>
"""

# Prepare all tracks
tracks_rendered_parts = []
drawer_items_parts = []

for num_str, title in track_names_map.items():
    de_info = de_tracks_deep.get(num_str, {"review": "", "cards": []})
    en_info = en_tracks_deep.get(num_str, {"review": "", "cards": []})
    stanzas = extract_stanzas_for_track(num_str, title, de_info["cards"])
    
    tracks_rendered_parts.append(render_track_html(num_str, title, stanzas, de_info, en_info))
    drawer_items_parts.append(f'<li><a href="#track-{num_str}">{num_str} — {title}</a></li>')

full_page = HTML_MASTER_TEMPLATE
full_page = full_page.replace('[[DRAWER_ITEMS]]', "\n".join(drawer_items_parts))
full_page = full_page.replace('[[TRACKS_HTML]]', "\n".join(tracks_rendered_parts))

# Write to all outputs:
output_paths = [
    "c:/Users/Hakan/Documents/antigravity/modest-meitner/index.html",
    "c:/Users/Hakan/Documents/antigravity/modest-meitner/ALBUM_REVIEW_READER.html",
    "c:/Users/Hakan/Documents/antigravity/modest-meitner/ALBUM_REVIEW_READER_EN.html",
    "H:/Meine Ablage/Album_Review_und_Interpretation/index.html",
    "H:/Meine Ablage/Album_Review_und_Interpretation/ALBUM_REVIEW_READER.html",
    "H:/Meine Ablage/Album_Review_und_Interpretation/ALBUM_REVIEW_READER_EN.html"
]

for p in output_paths:
    dir_p = os.path.dirname(p)
    if dir_p and not os.path.exists(dir_p):
        os.makedirs(dir_p, exist_ok=True)
    with open(p, 'w', encoding='utf-8') as f:
        f.write(full_page)

print("Dynamic Bilingual Master successfully compiled and written to all targets!")
