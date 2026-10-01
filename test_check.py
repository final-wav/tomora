import os
import re

p = 'album_analyse_fallstudie/Phase_1_Mikro_Dekonstruktion'
for f in sorted(os.listdir(p)):
    with open(os.path.join(p, f), 'r', encoding='utf-8', errors='ignore') as fp:
        c = fp.read()
    m = re.search(r'### 1\.\s*Transkribierter Textkorpus\s*```text(.*?)```', c, re.DOTALL)
    if m:
        lines = [l.strip() for l in m.group(1).strip().split('\n') if l.strip()]
        print(f[:2], lines[:2])
