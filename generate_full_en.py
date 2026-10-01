import json
import os
import re

en_phase1 = {
    "01": [
        {
            "quote": "Please (Please) / Please (Please)",
            "body": """* **Psychodynamic Causality:** The work does not begin with an assertion, a thesis, or a defined positioning of the ego in space, but with a pure vocative of surrender: *"Please"*. It is a pleading signal that cements the ontological asymmetry of the scene from the very first second. The double echo `(Please)` acts as an intrapsychic reverberation chamber. The desire for closeness has become so detached from autonomous agency that it is articulated as a reflexive, automated chant of begging. The subject speaks from a position of fundamental deficit, possessing no leverage other than appealing to the mercy of an external object.
* **Body Language & Somatics:** The physiology of this moment is marked by a sudden drop in muscle tone in the postural system, paired with simultaneous hyperactivity in the larynx and diaphragm. It is the somatics of kneeling: the chest collapses inward, breathing becomes shallow and rapid. The word *"Please"* demands a voiceless plosive `/p/` followed by a soft, elongated vowel that exhales into nothingness—a somatic tension drop signaling the surrender of physical defense.
* **Power & Control Dynamics:** Here, apparent submission manifests as an unconscious control technique. By humiliating oneself to the maximum and putting all personal boundaries at disposal, the counterpart is forced into the role of the omnipotent caregiver. Helplessness is instrumentalized: someone who begs so desperately strips the other of their right to distance without appearing aggressive. It is a classic masochistic dynamic where total submission dictates the rules of engagement.
* **Acoustic & Spatial Impact:** Acoustically, the intro is designed like a tightening noose. The lead vocal sits dry and unprotected in the center, while the bracketed parentheticals `(Please)` creep inward from the stereo/Dolby Atmos perimeter, creating claustrophobic compression."""
        },
        {
            "quote": "Come (Please come)",
            "body": """* **Psychodynamic Causality:** The transition from pure pleading (*"Please"*) to the first verb (*"Come"*) marks the moment passive regression turns into a targeted demand. The imperative *"Come"* is instantly softened by the inserted *"(Please come)"*. The ego dares not issue a direct command, fearing rejection.
* **Body Language & Somatics:** A spasmodic forward motion of the hands that freezes mid-gesture. The nervous system is caught between sympathetic activation (the urge to reach out) and dorsal vagal inhibition (the paralysis of fear).
* **Power & Control Dynamics:** The speaker transfers all responsibility for crossing boundaries onto the counterpart. The subject refuses to move; the object must come to fill the void.
* **Acoustic & Spatial Impact:** The acoustic space opens for a split second, only to pull the voice right back against the listener's eardrum."""
        },
        {
            "quote": "Closer, closer, closer, closer / Closer, closer, closer, closer",
            "body": """* **Psychodynamic Causality:** The eightfold repetition of *"closer"* without subject, verb, or endpoint unmasks the psyche's compulsive fixation. It is not about reaching healthy intimacy, but eradicating all intermediate space. Every centimeter of distance is perceived as an existential threat.
* **Body Language & Somatics:** The somatics of suffocation and constriction. Breathing shortens into a panting staccato; the neck and jaw lock in a tonic holding reflex, akin to a drowning person clinging to a rescuer.
* **Power & Control Dynamics:** The sheer quantitative accumulation exerts hypnotic pressure, grinding down resistance through repetition.
* **Acoustic & Spatial Impact:** Staccato rhythm. The vocal repetitions circle the listener's head in Dolby Atmos, artificially shrinking spatial distance to zero."""
        }
    ],
    "02": [
        {
            "quote": "Come closer, come closer / I need you near",
            "body": """* **Psychodynamic Causality:** The demand for proximity escalates from a plea into an existential survival mandate. \"I need you near\" articulates complete dependency on the external object for emotional self-regulation.
* **Body Language & Somatics:** Hyper-vigilant posture, elevated heart rate, somatic craving for physical skin contact to soothe an overstimulated sympathetic nervous system.
* **Power & Control Dynamics:** Emotional enmeshment. Neediness is weaponized to bind the other person into an inescapable proximity contract.
* **Acoustic & Spatial Impact:** Panned vocal layers creating a circular acoustic enclosure around the stereo field."""
        }
    ],
    "03": [
        {
            "quote": "A Boy Like You / Dissecting the Archetype",
            "body": """* **Psychodynamic Causality:** The transition from somatic begging to intellectualized defense. The subject analyzes the partner through first principles and systemic logic, seeking psychological safety in cognitive mastery.
* **Body Language & Somatics:** Hardening of postural muscle tone, calculated eye contact, suppression of vulnerable somatic signals beneath a rigid intellectual shield.
* **Power & Control Dynamics:** Analytical dominance. By classifying and cataloging the counterpart's flaws, the ego regains the illusion of superior control.
* **Acoustic & Spatial Impact:** Dry, clinical vocal production with crisp high frequencies, signaling emotional detachment and analytical precision."""
        }
    ],
    "04": [
        {
            "quote": "Ring The Alarm / The System Overheats",
            "body": """* **Psychodynamic Causality:** Total breakdown of cognitive defenses. The nervous system enters acute sympathetic overdrive—fight-or-flight triggered by the threat of abandonment.
* **Body Language & Somatics:** Adrenaline rush, tachycardia, dilated pupils, muscular tremors, and hyperventilation.
* **Power & Control Dynamics:** The panic of loss causes frantic attempts to re-establish control through acoustic escalation and urgency.
* **Acoustic & Spatial Impact:** Siren-like vocal dynamics, distorted synth textures, and overwhelming rhythmic intensity reflecting a psychic emergency."""
        }
    ],
    "05": [
        {
            "quote": "My Baby / Hermetic Isolation",
            "body": """* **Psychodynamic Causality:** Regression into an exclusive, toxic two-person bubble. The outside world is completely shut out to protect the fragile illusion of symbiotic perfection.
* **Body Language & Somatics:** Closed body posture facing inward, tactile cocooning, isolation from external sensory stimuli.
* **Power & Control Dynamics:** Mutual possessiveness and emotional quarantine, where independence is perceived as betrayal.
* **Acoustic & Spatial Impact:** Muffled, intimate room acoustics with heavy low-end focus, simulating an airtight chamber."""
        }
    ],
    "06": [
        {
            "quote": "Have you seen me dance alone?",
            "body": """* **Psychodynamic Causality:** The pivotal fracture of the album. The sudden realization that genuine self-expression and joy can exist without external validation immediately shatters the symbiotic bond.
* **Body Language & Somatics:** Spontaneous release of postural tension, fluid movement, rhythmic uncoupling from the partner's tempo.
* **Power & Control Dynamics:** Instant reclamation of personal sovereignty. The moment the subject moves autonomously, the relational manipulation loses its grip.
* **Acoustic & Spatial Impact:** Explosive expansion of the stereo panorama, lush reverb tails, and uncompressed dynamics symbolizing liberation."""
        }
    ],
    "07": [
        {
            "quote": "Somewhere Else / Dissociative Freeze",
            "body": """* **Psychodynamic Causality:** Post-rupture defense mechanism. When the symbiotic bond breaks, the psyche retreats into emotional anesthesia and depersonalization to survive the shock.
* **Body Language & Somatics:** Hypo-arousal, cold extremities, flat facial affect, and slowed respiration.
* **Power & Control Dynamics:** Complete emotional withdrawal. The subject denies access to its inner core by mentally detaching from the physical present.
* **Acoustic & Spatial Impact:** Distant, filtered vocal layers with wide hall reverb, placing the voice in an icy, desolate space."""
        }
    ],
    "08": [
        {
            "quote": "I drink the light / Manic Overdrive",
            "body": """* **Psychodynamic Causality:** A manic counter-attack against inner numbness. Rather than feeling the void, the psyche forces extreme sensory stimuli into the system to burn through the depression.
* **Body Language & Somatics:** Sensory hunger, rapid erratic movements, dilated pupils, and hyperactive motor responses.
* **Power & Control Dynamics:** Internal tyranny of sensation. The ego attempts to force happiness and vitality through sheer sensory consumption.
* **Acoustic & Spatial Impact:** High-frequency saturation, pulsating synth arpeggios, and aggressive stereo panning."""
        }
    ],
    "09": [
        {
            "quote": "Wavelengths / Ego Death & Deconstruction",
            "body": """* **Psychodynamic Causality:** The collapse of all defensive personas. The fundamental crisis of identity (\"Who am I?\") is faced without illusions or masks.
* **Body Language & Somatics:** Profound stillness, lowered center of gravity, slow and deliberate breathing.
* **Power & Control Dynamics:** Surrender of all control mechanisms. The subject accepts vulnerability as the only authentic starting point.
* **Acoustic & Spatial Impact:** Minimalist ambient textures, deep sub-bass frequencies, and stark, dry vocal presence."""
        }
    ],
    "10": [
        {
            "quote": "Side By Side / Auditing Residual Attachment",
            "body": """* **Psychodynamic Causality:** A sober, mature audit of the past bond without romantic nostalgia. Acknowledging shared history while firmly upholding separation.
* **Body Language & Somatics:** Balanced, upright posture, relaxed shoulders, clear and steady gaze.
* **Power & Control Dynamics:** Non-reactive neutrality. Neither submission nor aggression, but calm boundary setting.
* **Acoustic & Spatial Impact:** Balanced acoustic placement, warm mid-range tones, and organic instrumental textures."""
        }
    ],
    "11": [
        {
            "quote": "The Thing / Building from the Bone",
            "body": """* **Psychodynamic Causality:** The absolute ground zero of reconstruction. Emotions are observed like inert physical objects; recovery begins from somatic reality and skeletal discipline.
* **Body Language & Somatics:** Somatic grounding, conscious muscle activation, rebuilding physical resilience bone by bone.
* **Power & Control Dynamics:** Self-sovereign discipline. Total self-reliance with zero expectation of external rescue.
* **Acoustic & Spatial Impact:** Heavy, bone-dry percussion, industrial textural elements, and uncompromising vocal clarity."""
        }
    ],
    "12": [
        {
            "quote": "Don't you forget about yourself / Lucid Reclamation",
            "body": """* **Psychodynamic Causality:** The culmination of the journey: autonomous integration. The self is reclaimed not as an idealized fantasy, but as a disciplined, battle-tested reality.
* **Body Language & Somatics:** Full postural alignment, open chest, natural and deep breathing, presence in the physical body.
* **Power & Control Dynamics:** Absolute self-ownership. The psyche no longer bargains for intimacy at the expense of integrity.
* **Acoustic & Spatial Impact:** Wide, bright, and expansive soundstage with majestic vocal clarity and full harmonic resolution."""
        }
    ]
}

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

phase1_dir = 'album_analyse_fallstudie/Phase_1_Mikro_Dekonstruktion'

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

def clean_txt(s):
    return re.sub(r'[^a-z0-9]', '', s.lower())

for num_str, title in track_names_map.items():
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

    analysis_cards = en_phase1.get(num_str, [])

    # Structure Lyrics & Strip Document Title Lines
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

    tracks.append({
        "num": num_str,
        "title": title,
        "stanzas": stanzas,
        "review": en_reviews.get(num_str, ""),
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

with open('c:/Users/Hakan/Documents/antigravity/modest-meitner/ALBUM_REVIEW_READER_EN.html', 'w', encoding='utf-8') as f:
    f.write(html_final)

with open('c:/Users/Hakan/Documents/antigravity/modest-meitner/album_review_und_interpretation/index_en.html', 'w', encoding='utf-8') as f:
    f.write(html_final)

print("100% full English version generated successfully!")
