import json
import os
import re

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

def clean_txt(s):
    return re.sub(r'[^a-z0-9]', '', s.lower())

def translate_terms(text):
    # Standard psychoanalytic terminology translation
    replacements = [
        (r'\*\*Psychodynamische Kausalit[aä]t:\*\*', '**Psychodynamic Causality:**'),
        (r'\*\*K[oö]rpersprache & Somatik:\*\*', '**Body Language & Somatics:**'),
        (r'\*\*Macht- und Kontrollmechanismen:\*\*', '**Power & Control Dynamics:**'),
        (r'\*\*Klang- und Raumwirkung:\*\*', '**Acoustic & Spatial Impact:**'),
        (r'\*\*Synthese & Albumkontext:\*\*', '**Synthesis & Album Context:**'),
        (r'\*\*Zusammenfassung:\*\*', '**Summary:**'),
        (r'Dekonstruktion', 'Deconstruction'),
        (r'Regressionsfalle', 'Regression Trap'),
        (r'Autonomer Wiederaufbau', 'Autonomous Reconstruction'),
        (r'Schutzpanzerung', 'Defensive Armor'),
        (r'Hypervigilanz', 'Hypervigilance'),
        (r'Ego-Tod', 'Ego Death'),
    ]
    for pattern, repl in replacements:
        text = re.sub(pattern, repl, text, flags=re.IGNORECASE)
    return text

# Comprehensive English translations for Reviews & Micro-Analysis
en_reviews = {
    "01": """### Track Review: The Regression Trap & The Genesis of Pleading
The album opens not with an affirmation of strength, but with a visceral, almost involuntary plea. *Please* acts as a stark psychological baseline: the total collapse of self-sovereignty into an infantile state of dependency. The repetitive, hypnotic mantra of "closer" deconstructs the illusion of romantic intimacy, exposing it as an urgent attempt to dissolve existential isolation at any cost.""",

    "02": """### Track Review: Symbiosis, Fusion, and Sensory Entrapment
Expanding the claustrophobic plea of the opener, *Come Closer* accelerates into a relentless demand for physical and psychic fusion. Here, proximity is weaponized: distance is perceived as trauma, and the boundaries of the self are systematically dismantled in an effort to secure external validation and eliminate the void.""",

    "03": """### Track Review: Analytical Dissection & The Projection of the Ideal
*A Boy Like You* shifts the psychological dynamic from desperate pleading to hyper-vigilant cognitive scanning. The subject dissects the counterpart through first principles, seeking safety in intellectual mastery while wrestling with the painful dissonance between an idealized archetype and stark reality.""",

    "04": """### Track Review: Overheating of the Nervous System & Acute Alarm
A visceral escalation point. *Ring The Alarm* sonically and psychologically documents the acute overheating of the central nervous system. The symbiotic armor shatters into sheer panic—a sonic siren signaling the catastrophic failure of cognitive control mechanisms.""",

    "05": """### Track Review: Hermetic Isolation & Toxic Enmeshment
In *My Baby*, the psyche retreats into a hermetically sealed two-person isolation. The outside world ceases to exist; reality is reduced strictly to the immediate orbit of the other. It is an obsessive loop of protection and possessiveness that borders on mutual sensory erasure.""",

    "06": """### Track Review: The Crucial Turning Point — Dancing in Solitude
"Have you seen me dance alone?" marks the decisive structural fracture of the record. Autonomy emerges not as an intellectual choice, but as an uncontrollable eruption of raw, unmasked authenticity. The moment the self realizes it can move independently, the dysfunctional symbiotic bond instantly collapses.""",

    "07": """### Track Review: Dissociative Distance & The Frozen Core
Following the rupture, *Somewhere Else* plunges into post-traumatic emotional numbness and spatial dissociation. The subject observes its own wreckage from an icy, detached vantage point—the emotional system goes into hibernation to survive the collapse.""",

    "08": """### Track Review: Manic Overdrive & Sensory Ingestion
"I drink the light" represents a manic, sensory counter-offensive against inner numbness. Rather than feeling the pain, the psyche forces extreme stimulation into the void, attempting to incinerate depression through relentless acoustic and emotional overload.""",

    "09": """### Track Review: Depersonalization & The Question of Identity
*Wavelengths* is the epicenter of depersonalization and ego death. The fundamental question "Who am I?" echoes across desolate electronic textures. Old identities, false loyalties, and protective masks are buried in cold, uncompromising clarity.""",

    "10": """### Track Review: Phantom Bonds & Residual Attachment
In *Side By Side*, the ghost of the former bond flickers one last time. It is not a nostalgic longing, but a sober audit of residual attachment—acknowledging what was shared while recognizing the irreversible physical and emotional separation.""",

    "11": """### Track Review: The Ground Zero of Existence — Rebuilding from the Bone
*The Thing* marks absolute zero. Emotions are no longer experienced as overwhelming waves, but examined like cold, inert objects. Here, at rock bottom, the genuine reconstruction begins: somatic, disciplined, building the body anew from the bare bone.""",

    "12": """### Track Review: Lucid Reclamation & Autonomous Sovereignty
The journey concludes with *In A Minute* and the resolute imperative: "Don't you forget about yourself." This is neither a naive happy ending nor a sentimental victory, but a quiet, disciplined reclamation of sovereign selfhood forged through the fire of complete systemic collapse."""
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

    # Translate analysis cards
    analysis_cards = []
    blocks = re.split(r'\n(?=####\s+)', micro_analysis)
    for b in blocks:
        b = b.strip()
        if not b:
            continue
        title_m = re.match(r'####\s+`?([^`\n]+)`?', b)
        card_title = title_m.group(1).strip() if title_m else ""
        body = re.sub(r'####\s+[^\n]+\n', '', b).strip()
        body_en = translate_terms(body)
        if card_title or body:
            analysis_cards.append({
                "quote": card_title,
                "body": body_en,
                "clean_quote": clean_txt(card_title)
            })

    # Clean lyrics
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
            c_line = clean_txt(line_s)
            matched_card_idx = -1

            if len(c_line) > 2:
                for idx, ac in enumerate(analysis_cards):
                    if c_line in ac["clean_quote"] or ac["clean_quote"] in c_line:
                        matched_card_idx = idx
                        break

            if matched_card_idx == -1 and len(c_line) > 3:
                tokens = [clean_txt(t) for t in line_s.split() if len(t) > 3]
                best_score = 0
                for idx, ac in enumerate(analysis_cards):
                    score = sum(1 for t in tokens if t in ac["clean_quote"])
                    if score > best_score:
                        best_score = score
                        matched_card_idx = idx

            if matched_card_idx == -1 and len(analysis_cards) > 0:
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

    review_text_en = en_reviews.get(num_str, "")

    tracks.append({
        "num": num_str,
        "title": title,
        "stanzas": stanzas,
        "review": review_text_en,
        "analysis_cards": analysis_cards
    })

html_template = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>TOMORA — Lyrics & Review</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
  <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
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

    /* Animated 35mm Analog Film Grain Canvas */
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

    /* Minimalist Navbar */
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

    .burger-icon {
      cursor: pointer;
      display: flex;
      flex-direction: column;
      justify-content: center;
      gap: 6px;
      width: 24px;
      height: 24px;
      padding: 0;
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

    /* Drawer */
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
      max-height: 75vh;
      object-fit: cover;
      object-position: center;
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
      user-select: none;
      cursor: default;
    }

    .track-heading .num {
      color: #ffffff;
      font-size: 0.75em;
    }

    /* 2 Columns: Left Lyrics, Right Analysis */
    .track-grid {
      display: grid;
      grid-template-columns: 1fr 1.35fr;
      gap: 70px;
      align-items: start;
    }

    /* Lyrics Column */
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
      user-select: none;
      cursor: default;
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
      user-select: none;
      cursor: default;
    }

    .lyric-line {
      font-size: 1.18rem;
      line-height: 1.9;
      color: #f4f4f5;
      padding: 4px 10px;
      margin: 3px -10px;
      border-radius: 4px;
      cursor: pointer;
      transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
    }

    .lyric-line:hover {
      background: rgba(255, 0, 122, 0.18);
      color: #ffffff;
      transform: translateX(4px);
    }

    .lyric-line.active-line {
      background: var(--magenta);
      color: #ffffff;
      font-weight: 700;
      transform: translateX(6px);
      box-shadow: 0 4px 20px var(--magenta-glow);
    }

    /* Analysis Column */
    .analysis-col {
      display: flex;
      flex-direction: column;
      gap: 24px;
    }

    .review-intro-box {
      font-size: 1.06rem;
      line-height: 1.8;
      color: #d1d1d6;
      margin-bottom: 16px;
    }

    .review-intro-box h1, .review-intro-box h2 {
      display: none;
    }

    .review-intro-box p {
      margin-bottom: 18px;
    }

    .review-intro-box strong {
      color: #ffffff;
    }

    /* Analysis Cards */
    .analysis-card {
      background: var(--bg-surface);
      border-radius: 6px;
      padding: 24px 28px;
      transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
      border-left: 3px solid transparent;
      scroll-margin-top: 100px;
    }

    .analysis-card:hover {
      background: #18181e;
    }

    .analysis-card.highlighted {
      background: #201322;
      border-left-color: var(--magenta);
      box-shadow: 0 6px 30px rgba(255, 0, 122, 0.22);
      transform: scale(1.015);
    }

    .card-quote {
      font-size: 1.15rem;
      font-weight: 800;
      color: var(--magenta);
      margin-bottom: 16px;
      letter-spacing: 0.02em;
      user-select: none;
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

  <!-- Animated Analog Noise Canvas -->
  <canvas id="grainCanvas"></canvas>

  <!-- Minimalist Navbar -->
  <nav class="navbar">
    <button class="burger-icon" onclick="toggleDrawer()" aria-label="Menu">
      <span></span>
      <span></span>
      <span></span>
    </button>
    
    <a href="#" class="nav-brand">TOMORA</a>
    
    <div class="nav-spacer"></div>
  </nav>

  <!-- Track Navigation Drawer -->
  <div class="drawer-overlay" id="drawerOverlay" onclick="toggleDrawer()"></div>
  <aside class="drawer" id="drawer">
    <div class="drawer-header">
      <button class="drawer-close-btn" onclick="toggleDrawer()" aria-label="Close">
        <span></span>
        <span></span>
      </button>
      <div class="drawer-title">12 TRACKS</div>
    </div>
    <ul class="drawer-nav" id="drawerTrackLinks">
      <!-- Tracks injected via JS -->
    </ul>
  </aside>

  <!-- Full-Bleed Video Banner -->
  <header class="hero-fullbleed">
    <video class="hero-video" autoplay loop muted playsinline src="hero_video.mp4"></video>
  </header>

  <!-- Main Content: All 12 Tracks -->
  <main class="page-container" id="tracksContainer">
    <!-- Tracks injected via JS -->
  </main>

  <script>
    // 1. Moving 35mm Film Grain Canvas Animation
    const canvas = document.getElementById('grainCanvas');
    const ctx = canvas.getContext('2d');
    let grainFrame = 0;

    function resizeGrain() {
      canvas.width = Math.ceil(window.innerWidth / 2.5);
      canvas.height = Math.ceil(window.innerHeight / 2.5);
    }
    window.addEventListener('resize', resizeGrain);
    resizeGrain();

    function animateGrain() {
      grainFrame++;
      if (grainFrame % 2 === 0) {
        const w = canvas.width;
        const h = canvas.height;
        const imgData = ctx.createImageData(w, h);
        const buf = new Uint32Array(imgData.data.buffer);
        const len = buf.length;
        for (let i = 0; i < len; i++) {
          if (Math.random() < 0.22) {
            buf[i] = Math.random() > 0.45 ? 0x40ffffff : 0x40000000;
          }
        }
        ctx.putImageData(imgData, 0, 0);
      }
      requestAnimationFrame(animateGrain);
    }
    animateGrain();

    // 2. Track Data & App Logic
    const tracks = [[TRACKS_DATA]];

    function toggleDrawer() {
      const drawer = document.getElementById('drawer');
      const overlay = document.getElementById('drawerOverlay');
      drawer.classList.toggle('active');
      overlay.classList.toggle('active');
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

    // Precise Interactive Highlighting
    function handleLyricClick(trackIdx, cardIdx, el) {
      const trackSec = document.getElementById('track-' + tracks[trackIdx].num);
      trackSec.querySelectorAll('.lyric-line').forEach(l => l.classList.remove('active-line'));
      trackSec.querySelectorAll('.analysis-card').forEach(c => c.classList.remove('highlighted'));

      el.classList.add('active-line');

      if (cardIdx >= 0) {
        const targetCard = document.getElementById(`card-${trackIdx}-${cardIdx}`);
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
      track.stanzas.forEach((stanza) => {
        lyricsHtml += `<div class="stanza-block">`;
        if (stanza.title) {
          lyricsHtml += `<div class="stanza-title">${stanza.title}</div>`;
        }
        stanza.lines.forEach((lineObj) => {
          lyricsHtml += `<div class="lyric-line" onclick="handleLyricClick(${tIdx}, ${lineObj.target_card}, this)">${lineObj.text}</div>`;
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
          <!-- Left: Lyrics -->
          <div class="lyrics-col">
            <div class="col-header">Lyrics</div>
            <div class="lyrics-wrapper">${lyricsHtml}</div>
          </div>
          <!-- Right: Interpretation & Deconstruction -->
          <div class="analysis-col">
            <div class="col-header">Interpretation & Deconstruction</div>
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

html_final = html_template.replace('[[TRACKS_DATA]]', json.dumps(tracks))

# Write English HTML files
with open('c:/Users/Hakan/Documents/antigravity/modest-meitner/ALBUM_REVIEW_READER_EN.html', 'w', encoding='utf-8') as f:
    f.write(html_final)

with open('c:/Users/Hakan/Documents/antigravity/modest-meitner/album_review_und_interpretation/index_en.html', 'w', encoding='utf-8') as f:
    f.write(html_final)

print("English version generated successfully!")
