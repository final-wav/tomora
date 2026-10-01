---
name: interactive-album-reader
description: >-
  Standard-Architektur und Design-System zur Erstellung von interaktiven, zweisprachigen 
  Album-Review & Close-Reading Webanwendungen mit 2-Spalten-Layout (Genius + Pitchfork Standard), 
  vertikal ausgerichteten Tiefenanalyse-Karten und Neural TTS Audio-Essays.
---

# 🎵 Interaktiver Album-Interpretation-Reader: Architektur & UI-Design-System

Dieses Dokument definiert den exakten, reproduzierbaren Standard für Web-Applikationen zur multimodalen Albumdekonstruktion. Das Layout, die Interaktionsmuster und das Design-System werden **1:1 für alle zukünftigen Alben und Künstler übernommen**, wobei lediglich das Theme (Akzentfarben, Hero-Video/Cover, YouTube-Track-IDs) angepasst wird.

---

## 1. UI- & Design-System-Spezifikation (1:1 Übernahme)

### A. Farb- und Theme-Architektur (`:root` CSS-Variablen)
Um das System an einen neuen Künstler anzupassen, werden **nur diese CSS-Variablen** ausgetauscht:

```css
:root {
  /* Basis-Oberflächen (Darkmode Luxus / Pitchfork / Apple Music Ästhetik) */
  --bg: #0c0c0f;                          /* Tiefschwarzer Hintergrund */
  --bg-surface: #141418;                  /* Karten & Drawer Hintergrund */
  --bg-elevated: #1a1a20;                 /* Schwebende Elemente / Glass Dock */
  --text: #ffffff;                        /* Reines Weiß für Überschriften & Fokus */
  --text-muted: #8e8e93;                  /* Muted Gray für Fließtext & Metadaten */
  
  /* Künstler-spezifische Akzentfarben (Beispiel: TOMORA Neon-Magenta) */
  --accent: #ff007a;                      /* Primäre Akzentfarbe */
  --accent-dim: rgba(255, 0, 122, 0.12);  /* Subtile Hintergründe & Badges */
  --accent-glow: rgba(255, 0, 122, 0.35); /* Glow-Effekte für Player & Hover */
  
  /* Typografie */
  --font-main: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}
```

### B. Canvas Film-Grain (35mm Analog-Textur)
Ein animierter 35mm Analogfilm-Korn-Effekt liegt permanent als Overlay über der gesamten App:
```html
<canvas id="grainCanvas" style="position:fixed;top:0;left:0;width:100vw;height:100vh;pointer-events:none;z-index:9999;opacity:0.035;"></canvas>
```

### C. Hero-Section: Full-Bleed Video / Cover
* **Format:** 100% Breite, maximal `75vh` Höhe, `object-fit: cover`.
* **Verhalten:** Autoplay, loop, muted, playsinline.
* Bei reinem Bild-Artwork: Hochauflösendes WebP/JPG mit leichtem Parallax-Effekt.

---

## 2. Das 2-Spalten Layout (Track-Grid)

Das Kern-Layout besteht aus einem responsive CSS-Grid:
```css
.track-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;  /* Links: Songtext | Rechts: Review / Karte */
  gap: 60px;
  align-items: start;
  position: relative;
}

@media (max-width: 992px) {
  .track-grid {
    grid-template-columns: 1fr;
    gap: 40px;
  }
}
```

### Spalte 1 (Links): Interaktiver Songtext (`.lyrics-col`)
* **Schrift:** `1.08rem`, Zeilenabstand `1.65`, Farbe `rgba(255,255,255,0.75)`.
* **Strophen-Titel:** `0.75rem`, `800` Weight, Uppercase, `var(--accent)`.
* **Interaktive Zeilen (`.lyric-trigger`):**
  * Subtiler Akzent-Border oder Unterstreichung bei Hover.
  * Cursor: `pointer`.
  * Jede Zeile besitzt Attribute: `data-track-num="XX"` und `data-target-card="IDX"`.

### Spalte 2 (Rechts): Narrative Review & Dynamisches Karten-Deck (`.analysis-col`)
* **Standard-Ansicht (`.narrative-review`):**
  * Ausführlicher, ungekürzter Essay (Pitchfork/The Quietus Niveau).
  * Schriftgröße `1.05rem`, Zeilenhöhe `1.75`.
  * Zitate im Fließtext werden in `var(--accent)` hervorgehoben (`.lyric-quote-highlight`).
* **Karten-Ansicht (`.card-deck-view`):**
  * Standardmäßig ausgeblendet (`display: none;`).
  * Sobald links eine Zeile geklickt wird: Review blendet aus, Karten-Deck blendet ein.
  * **Vertikale Ausrichtung:** Die Karte wird per JavaScript exakt auf der Scroll-Höhe der angeklickten Zeile positioniert (`marginTop = relativeTop`).

### Das Karten-Design (`.analysis-card`):
* **Rahmen & Glas:** `background: #141418; border: 1px solid rgba(255,255,255,0.12); border-radius: 12px; padding: 24px;`.
* **Header-Bar:**
  * **Zurück-Pfeil:** Minimaler, randloser SVG-Pfeil (`←`), kein Rahmen, keine Box, pure Icon-Optik (`background: none; border: none;`).
  * **Badge-Counter:** `Tiefen-Analyse X / Y` in dezentem Grau.
* **Quote-Titel:** Fett, `var(--accent)`, Slash-separierte Triggerphrasen.
* **Body:** Psychoanalytische & somatische Dekonstruktion der Zeile.

---

## 3. JavaScript Interaktions-Standard

```javascript
// 1. Öffnen & Exakte Vertikale Positionierung
function openCardDeck(trackSection, targetCardIdx, triggerEl) {
  const currentLang = document.body.getAttribute('data-lang') || 'de';
  const trackNum = trackSection.id.replace('track-', '');
  const reviewEl = trackSection.querySelector(`#review-${trackNum}-${currentLang}`);
  const deckEl = trackSection.querySelector(`#card-deck-${trackNum}-${currentLang}`);
  if (!deckEl || !reviewEl) return;

  reviewEl.style.display = 'none';
  deckEl.style.display = 'block';

  const cards = deckEl.querySelectorAll('.analysis-card');
  cards.forEach(c => {
    c.classList.toggle('active', parseInt(c.getAttribute('data-card-idx')) === targetCardIdx);
  });

  // Desktop: Vertikales Alignment auf Höhe der Lyrics-Zeile
  if (window.innerWidth > 992 && triggerEl) {
    const grid = trackSection.querySelector('.track-grid');
    const gridRect = grid.getBoundingClientRect();
    const triggerRect = triggerEl.getBoundingClientRect();
    const relativeTop = Math.max(0, triggerRect.top - gridRect.top);
    deckEl.style.marginTop = `${relativeTop}px`;
  } else {
    deckEl.style.marginTop = '0px';
  }
}

// 2. Schließen
function closeCardDeck(trackSection) {
  const currentLang = document.body.getAttribute('data-lang') || 'de';
  const trackNum = trackSection.id.replace('track-', '');
  const reviewEl = trackSection.querySelector(`#review-${trackNum}-${currentLang}`);
  const deckEl = trackSection.querySelector(`#card-deck-${trackNum}-${currentLang}`);
  if (reviewEl) reviewEl.style.display = 'block';
  if (deckEl) deckEl.style.display = 'none';
}

// 3. Globales Klick-Verhalten (Outside-Click & Trigger-Switch)
document.addEventListener('click', (e) => {
  const trigger = e.target.closest('.lyric-trigger');
  const backBtn = e.target.closest('.card-back-btn');
  const insideCard = e.target.closest('.analysis-card');

  if (trigger) {
    const trackSection = trigger.closest('.track-section');
    const cardIdx = parseInt(trigger.getAttribute('data-target-card'));
    openCardDeck(trackSection, cardIdx, trigger);
  } else if (backBtn) {
    closeCardDeck(backBtn.closest('.track-section'));
  } else if (!insideCard) {
    // Klick ins Leere schließt alle geöffneten Decks
    document.querySelectorAll('.track-section').forEach(closeCardDeck);
  }
});
```

---

## 4. Floating Glass Audio Player (Globaler Dock Player)

Am unteren Bildschirmrand schwebt ein minimalistischer Player (`.audio-dock`):
* **Design:** `position: fixed; bottom: 24px; left: 50%; transform: translateX(-50%); border-radius: 40px; background: rgba(20, 20, 24, 0.85); backdrop-filter: blur(16px); border: 1px solid rgba(255,255,255,0.15);`.
* **Funktionen:**
  * Play / Pause / Prev / Next.
  * Timeline-Scrubber mit verbleibender & abgelaufener Zeit.
  * Track-Titel & Sprachanzeige (DE/EN synchron zum globalen Language-Toggle).
  * Auto-Advance zum nächsten Track nach Beendigung.

---

## 5. Neural TTS Audio-Pipeline (`generate_audio_tts.py`)

* **Stimmen:**
  * Deutsch: `de-DE-KillianNeural` (intellektuell, profund, ruhig).
  * Englisch: `en-US-ChristopherNeural` (sonor, essayistisch, literarisch).
* **Regel für Audios:**
  * **Nur die narrative Review vorlesen** (Karten sind vom Audio ausgeschlossen).
  * Absätze mit ` ... \n\n` verbinden, um natürliche Atempausen der KI-Stimme zu erzeugen.

---

## 6. Der 100% Zeilen-Matching-Algorithmus (`clean_txt` + Multi-Token)

Damit wirklich **jede Zeile** des Songtextes links als Trigger erkannt wird:

```python
def clean_txt(t):
    return re.sub(r'[^a-zA-Z0-9]', '', t).lower()

def find_matching_card(line_text, cards):
    line_lower = line_text.lower()
    line_clean = clean_txt(line_text)
    if not line_clean or len(line_clean) < 2:
        return None
    
    for idx, card in enumerate(cards):
        q_full = card.get("quote", "").lower()
        parts = [p.strip() for p in q_full.split('/')]
        
        # 1. Substring-Match
        for p in parts:
            p_clean = clean_txt(p)
            if p_clean and (p_clean in line_clean or line_clean in p_clean):
                return idx
                
        # 2. Token-Schnittmenge (ohne Füllwörter)
        for p in parts:
            tokens = [t.strip() for t in re.findall(r'[a-zA-Z]{3,}', p) 
                      if t.strip() not in ['the', 'and', 'for', 'von', 'der', 'die', 'das', 'mit', 'wie', 'ein', 'eine', 'you']]
            matched = [t for t in tokens if t in line_lower]
            if len(tokens) >= 2 and len(matched) >= min(len(tokens), 2):
                return idx
            elif len(tokens) == 1 and len(matched) == 1 and len(tokens[0]) >= 4:
                return idx
    return None
```

---

## 7. Schritt-für-Schritt Workflow für ein neues Album

1. **Dateien vorbereiten:**
   * Textkorpus anlegen: `album_analyse/Phase_1/XX_Songname.md`.
   * Module anlegen: `analysis_modules/tracks_01_04.py`, etc.
2. **Textanalyse durchführen:**
   * Nach den 4 Säulen des `song-poem-analysis`-Skills Zeile für Zeile dekonstruieren.
   * `review` (Essay) und `cards` (Zeilen-Analysen) befüllen.
3. **100% Abdeckung verifizieren:**
   * Prüfen, ob `unannotated == 0`.
4. **HTML / Web-App kompilieren:**
   * `python build_master_complete.py` ausführen.
5. **Audio-Essays generieren:**
   * `python generate_audio_tts.py` ausführen (Review-Only).
6. **Deployen:**
   * Git Commit & Push auf GitHub Pages (`index.html`).
