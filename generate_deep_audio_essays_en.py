# -*- coding: utf-8 -*-
"""
Generate Full-Length English Neural TTS Audio Essays for TOMORA
Source: album_analyse_fallstudie/Phase_1_Mikro_Dekonstruktion_EN/*.md
Voice: en-US-ChristopherNeural
"""

import asyncio
import os
import re
import time
import edge_tts

VOICE_EN = "en-US-ChristopherNeural"
P1_EN_DIR = "album_analyse_fallstudie/Phase_1_Mikro_Dekonstruktion_EN"
OUTPUT_DIRS = [
    "c:/Users/Hakan/Documents/antigravity/modest-meitner/audio",
    "H:/Meine Ablage/Album_Review_und_Interpretation/audio"
]

def prepare_markdown_for_speech_en(raw):
    # Remove raw lyric code blocks
    text = re.sub(r'```text.*?```', '', raw, flags=re.DOTALL)
    text = re.sub(r'### II\.\s*Complete,?\s*Verified Lyric Corpus.*?---', '', text, flags=re.DOTALL)
    text = re.sub(r'### II\.\s*Verified Lyric Corpus.*?---', '', text, flags=re.DOTALL)

    # Clean headings into spoken phrases
    text = re.sub(r'# Track (\d+):\s*"?([^"\n]+)"?', r'Track \1: \2. \n\n', text)
    text = re.sub(r'## ([^\n]+)', r'\1. \n\n', text)
    text = re.sub(r'### I\.\s*Album Dramaturgy:[^\n]*', r'Section One: Album Dramaturgy and Context. \n\n', text)
    text = re.sub(r'### III\.\s*The Exhaustive Reading:[^\n]*', r'Section Two: The Exhaustive Reading. \n\n', text)
    text = re.sub(r'### IV\.\s*Synthesis:[^\n]*', r'Section Three: Synthesis and Dramaturgical Fault Line. \n\n', text)

    # Format numbered points
    text = re.sub(r'#### (\d+)\.\s*([^\n]+)', r'Point \1: \2. \n\n', text)
    text = re.sub(r'#### ([^\n]+)', r'\1. \n\n', text)

    # Clean markdown syntax
    text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
    text = re.sub(r'\*(.+?)\*', r'\1', text)
    text = re.sub(r'`(.+?)`', r'\1', text)
    text = text.replace('—', ', ').replace('–', ', ')
    text = text.replace('->', ' leads to ').replace('→', ' leads to ')
    text = text.replace('>', '')
    text = re.sub(r'---', '', text)
    text = re.sub(r'\n{3,}', '\n\n', text)

    # Natural sentence breathing
    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
    spoken_text = " ... \n\n".join(paragraphs)
    return spoken_text

async def generate_track(num_str, semaphore):
    filepath = None
    for f in sorted(os.listdir(P1_EN_DIR)):
        if f.startswith(num_str) and f.endswith('.md'):
            filepath = os.path.join(P1_EN_DIR, f)
            break
            
    if not filepath:
        print(f"Error: File for Track {num_str} not found in {P1_EN_DIR}")
        return

    with open(filepath, 'r', encoding='utf-8') as f:
        raw = f.read()

    spoken_text = prepare_markdown_for_speech_en(raw)
    word_count = len(spoken_text.split())
    
    async with semaphore:
        t0 = time.time()
        print(f"[{num_str}] Starting generation ({word_count} words)...")
        communicate = edge_tts.Communicate(spoken_text, VOICE_EN, rate="+0%", pitch="+0Hz")
        
        primary_dir = OUTPUT_DIRS[0]
        os.makedirs(primary_dir, exist_ok=True)
        primary_file = os.path.join(primary_dir, f"track_{num_str}_en.mp3")
        
        await communicate.save(primary_file)
        elapsed = round(time.time() - t0, 1)
        size_mb = round(os.path.getsize(primary_file) / (1024 * 1024), 2)
        print(f"[{num_str}] Finished in {elapsed}s: {primary_file} ({size_mb} MB)")
        
        # Mirror to secondary dir
        try:
            with open(primary_file, 'rb') as f_in:
                audio_data = f_in.read()
            backup_dir = OUTPUT_DIRS[1]
            if os.path.exists(os.path.dirname(backup_dir)):
                os.makedirs(backup_dir, exist_ok=True)
                backup_file = os.path.join(backup_dir, f"track_{num_str}_en.mp3")
                with open(backup_file, 'wb') as f_out:
                    f_out.write(audio_data)
                print(f"[{num_str}] Mirrored to: {backup_file}")
        except Exception as e:
            print(f"[{num_str}] Backup mirroring skipped: {e}")

async def main():
    print("=" * 60)
    print("TOMORA - Full Deep Audio Essay Generator (English)")
    print(f"Voice: {VOICE_EN}")
    print("=" * 60)
    
    semaphore = asyncio.Semaphore(4) # 4 parallel synthesis streams
    tasks = []
    
    for num in range(1, 13):
        num_str = f"{num:02d}"
        tasks.append(generate_track(num_str, semaphore))
        
    await asyncio.gather(*tasks)
    print("=" * 60)
    print("SUCCESS: All 12 Full Deep English Audio Essays generated!")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(main())
