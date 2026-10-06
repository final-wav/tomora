# -*- coding: utf-8 -*-
"""
Generate German Neural TTS Audio Files for all 12 TOMORA Tracks using Edge-TTS
Voice: de-DE-KillianNeural
"""

import asyncio
import os
import re
import edge_tts

from analysis_modules.tracks_01_04 import de_tracks_01_04
from analysis_modules.tracks_05_08 import de_tracks_05_08
from analysis_modules.tracks_09_12 import de_tracks_09_12

de_tracks = {}
de_tracks.update(de_tracks_01_04)
de_tracks.update(de_tracks_05_08)
de_tracks.update(de_tracks_09_12)

VOICE_DE = "de-DE-KillianNeural"

def clean_markdown_for_speech(text):
    text = re.sub(r'###\s*.*', '', text)
    text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
    text = re.sub(r'\*(.+?)\*', r'\1', text)
    text = re.sub(r'`(.+?)`', r'\1', text)
    text = text.replace('—', ', ').replace('–', ', ')
    return text.strip()

def build_ssml_text(review_raw):
    review_clean = clean_markdown_for_speech(review_raw)
    paragraphs = [p.strip() for p in review_clean.split('\n\n') if p.strip()]
    full_text = " ... \n\n".join(paragraphs)
    return full_text

async def generate_single_track(num_str, output_dirs):
    de_info = de_tracks.get(num_str)
    if not de_info:
        print(f"Skipping Track {num_str}: not found")
        return

    text = build_ssml_text(de_info["review"])
    print(f"Generating DE Audio for Track {num_str} ({VOICE_DE})...")
    
    communicate = edge_tts.Communicate(text, VOICE_DE, rate="-4%", pitch="+0Hz")
    
    # Save first to local audio directory
    primary_dir = output_dirs[0]
    os.makedirs(primary_dir, exist_ok=True)
    primary_file = os.path.join(primary_dir, f"track_{num_str}_de.mp3")
    await communicate.save(primary_file)
    print(f"  -> Saved: {primary_file} ({os.path.getsize(primary_file)} bytes)")
    
    # Copy or save to backup dirs if they exist
    with open(primary_file, 'rb') as f_in:
        audio_bytes = f_in.read()
        
    for backup_dir in output_dirs[1:]:
        try:
            if os.path.exists(os.path.dirname(backup_dir)):
                os.makedirs(backup_dir, exist_ok=True)
                backup_file = os.path.join(backup_dir, f"track_{num_str}_de.mp3")
                with open(backup_file, 'wb') as f_out:
                    f_out.write(audio_bytes)
                print(f"  -> Mirrored to: {backup_file}")
        except Exception as e:
            print(f"  (Note: could not mirror to {backup_dir}: {e})")

async def main():
    output_dirs = [
        "c:/Users/Hakan/Documents/antigravity/modest-meitner/audio",
        "H:/Meine Ablage/Album_Review_und_Interpretation/audio"
    ]
    
    print("Starting generation of 12 German Neural TTS Audio Essays...")
    for num in range(1, 13):
        num_str = f"{num:02d}"
        await generate_single_track(num_str, output_dirs)
        
    print("All 12 German Audio Tracks generated successfully!")

if __name__ == "__main__":
    asyncio.run(main())
