from pathlib import Path
from zipfile import ZipFile
import re

for name in ['2685', '2755']:
    p = Path(r'C:\Users\Admin\Desktop\impros susalud\MODELOS IMPROS SUSALUD CON FUNDAMENTO MEJORADO') / f'{name}-2025 RXX IMPRO SUSALUD okOK .docx'
    with ZipFile(p) as z:
        doc = z.read('word/document.xml').decode('utf-8')
        fn = z.read('word/footnotes.xml').decode('utf-8')
        print(f'{name}: doc length={len(doc)}, fn count={fn.count("<w:footnote ")}, has comments={"word/comments.xml" in z.namelist()}')
        anom = re.findall(r'(\[.*?\]|OJO[A-Z]*|Comentad[a-z0-9 \[\]:]+|\/\/\/.*?\/|\bXXXX\b|\b\*{3,}\b)', doc)
        print(f'  anomalias en doc: {len(anom)} -> {anom[:5]}')
