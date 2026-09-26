from docx import Document

d = Document(r'C:\Users\Admin\Desktop\impros susalud\MODELOS IMPROS SUSALUD CON FUNDAMENTO MEJORADO\2685-2025 RXX IMPRO SUSALUD okOK .docx')
with open('2685_paragraphs.txt', 'w', encoding='utf-8') as f:
    for i, p in enumerate(d.paragraphs):
        f.write(f"P{i} [style={p.style.name}]: {p.text}\n")
print("Guardado en 2685_paragraphs.txt")
