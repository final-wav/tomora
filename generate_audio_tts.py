# -*- coding: utf-8 -*-
"""
Generate high-fidelity Neural TTS Audio Files for TOMORA using Edge-TTS
With natural pauses between paragraphs, quotes and cards.
"""

import asyncio
import os
import re
import edge_tts

from analysis_modules.tracks_01_04 import de_tracks_01_04, en_tracks_01_04
from analysis_modules.tracks_05_08 import de_tracks_05_08, en_tracks_05_08
from analysis_modules.tracks_09_12 import de_tracks_09_12, en_tracks_09_12

de_tracks = {}
de_tracks.update(de_tracks_01_04)
de_tracks.update(de_tracks_05_08)
de_tracks.update(de_tracks_09_12)

en_tracks = {}
en_tracks.update(en_tracks_01_04)
en_tracks.update(en_tracks_05_08)
en_tracks.update(en_tracks_09_12)

VOICE_DE = "de-DE-KillianNeural"
VOICE_EN = "en-US-ChristopherNeural"

def clean_markdown_for_speech(text):
    text = re.sub(r'###\s*.*', '', text)
    text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
    text = re.sub(r'\*(.+?)\*', r'\1', text)
    text = re.sub(r'`(.+?)`', r'\1', text)
    text = text.replace('—', ', ').replace('–', ', ')
    return text.strip()

def build_ssml_text(review_raw, lang):
    review_clean = clean_markdown_for_speech(review_raw)
    paragraphs = [p.strip() for p in review_clean.split('\n\n') if p.strip()]
    
    text_blocks = []
    # Add review paragraphs with pauses (excluding cards)
    for p in paragraphs:
        text_blocks.append(p)
    
    # Join with distinct paragraph pauses (ellipses and line breaks give Edge TTS natural breathing)
    full_text = " ... \n\n".join(text_blocks)
    return full_text

async def generate_track_audio(num_str, de_info, en_info, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. German Audio (Review only)
    de_text = build_ssml_text(de_info["review"], "de")
    de_file = os.path.join(output_dir, f"track_{num_str}_de.mp3")
    print(f"Generating German audio for Track {num_str} ({VOICE_DE})...")
    communicate_de = edge_tts.Communicate(de_text, VOICE_DE, rate="-4%", pitch="+0Hz")
    await communicate_de.save(de_file)
    
    # 2. English Audio (Review only)
    en_text = build_ssml_text(en_info["review"], "en")
    en_file = os.path.join(output_dir, f"track_{num_str}_en.mp3")
    print(f"Generating English audio for Track {num_str} ({VOICE_EN})...")
    communicate_en = edge_tts.Communicate(en_text, VOICE_EN, rate="-2%", pitch="+0Hz")
    await communicate_en.save(en_file)

async def main():
    output_dirs = [
        "c:/Users/Hakan/Documents/antigravity/modest-meitner/audio",
        "H:/Meine Ablage/Album_Review_und_Interpretation/audio"
    ]
    
    for out_dir in output_dirs:
        os.makedirs(out_dir, exist_ok=True)
        
    for num_str in ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]:
        de_info = de_tracks.get(num_str)
        en_info = en_tracks.get(num_str)
        for out_dir in output_dirs:
            await generate_track_audio(num_str, de_info, en_info, out_dir)
            
    print("All 24 Neural TTS Audio Tracks generated successfully!")

if __name__ == "__main__":
    asyncio.run(main())
