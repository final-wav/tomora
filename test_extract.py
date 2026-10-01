import os
import re
import json

phase1_dir = 'album_analyse_fallstudie/Phase_1_Mikro_Dekonstruktion'
review_dir = 'album_review_und_interpretation'

files = sorted(os.listdir(phase1_dir))
print(f"Found {len(files)} track analysis files in Phase 1:")
for f in files:
    path = os.path.join(phase1_dir, f)
    with open(path, 'r', encoding='utf-8', errors='ignore') as fp:
        content = fp.read()
    
    # Extract lyrics block
    lyrics_match = re.search(r'### 1\.\s*Transkribierter Textkorpus\s*```text(.*?)```', content, re.DOTALL)
    lyrics = lyrics_match.group(1).strip() if lyrics_match else "No lyrics found"
    
    # Extract analysis part
    analysis_part = re.split(r'### 2\.\s*Zeile-f', content)
    analysis = "### Zeile-für-Zeile-Dekonstruktion" + analysis_part[1] if len(analysis_part) > 1 else content
    
    print(f"-> {f}: Lyrics length={len(lyrics)}, Analysis length={len(analysis)}")
