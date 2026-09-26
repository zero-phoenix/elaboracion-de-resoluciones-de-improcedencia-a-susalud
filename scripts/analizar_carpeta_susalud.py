import os
import glob
from pathlib import Path
import docx
import pypdf

folder = Path(r"C:\Users\Admin\Desktop\impros susalud")

print(f"=== ANALIZANDO PRECEDENTES EN {folder} ===")

docx_files = list(folder.glob("*.docx"))
pdf_files = list(folder.glob("*.pdf"))

print(f"Total DOCX: {len(docx_files)}")
print(f"Total PDF: {len(pdf_files)}")

def analizar_docx(path):
    doc = docx.Document(path)
    paragraphs = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
    full_text = "\n".join(paragraphs)
    
    # extraer datos clave
    res_num = ""
    partes = []
    resuelve_items = []
    in_resuelve = False
    
    for p in paragraphs:
        if "RESOLUCIÓN" in p.upper() and ("CC1" in p.upper() or "INDECOPI" in p.upper() or "N°" in p.upper()):
            res_num = p
        if "DENUNCIANTE" in p.upper() or "DENUNCIADO" in p.upper() or "MATERIA" in p.upper():
            partes.append(p)
        if "RESUELVE" in p.upper():
            in_resuelve = True
            continue
        if in_resuelve:
            if p.startswith(("PRIMERO", "SEGUNDO", "TERCERO", "CUARTO", "QUINTO", "SEXTO")):
                resuelve_items.append(p[:150] + "...")
                
    has_iafas = "IAFAS" in full_text.upper()
    has_ipress = "IPRESS" in full_text.upper()
    has_devolucion_tasa = "DEVOLUCIÓN" in full_text.upper() and "TASA" in full_text.upper()
    has_laboral = "LABORAL" in full_text.upper() or "EMPLEADOR" in full_text.upper()
    has_soat = "SOAT" in full_text.upper()
    has_cuantia = "CUANTÍA" in full_text.upper() or "CUANTIA" in full_text.upper()
    
    print("\n" + "="*70)
    print(f"ARCHIVO: {path.name}")
    print(f"Encabezado/Resolución: {res_num}")
    print(f"Partes/Materia: {partes[:4]}")
    print(f"Flags: IAFAS={has_iafas}, IPRESS={has_ipress}, DevTasa={has_devolucion_tasa}, Laboral={has_laboral}, SOAT={has_soat}, Cuantia={has_cuantia}")
    print(f"Items Resuelve ({len(resuelve_items)}):")
    for r in resuelve_items:
        print(f"  - {r}")

for f in docx_files:
    analizar_docx(f)

def analizar_pdf(path):
    reader = pypdf.PdfReader(path)
    full_text = ""
    for page in reader.pages:
        full_text += page.extract_text() or ""
        
    print("\n" + "="*70)
    print(f"ARCHIVO PDF: {path.name} (Páginas: {len(reader.pages)})")
    has_iafas = "IAFAS" in full_text.upper()
    has_ipress = "IPRESS" in full_text.upper()
    has_soat = "SOAT" in full_text.upper()
    has_devolucion_tasa = "DEVOLUCIÓN" in full_text.upper() and "TASA" in full_text.upper()
    print(f"Flags: IAFAS={has_iafas}, IPRESS={has_ipress}, SOAT={has_soat}, DevTasa={has_devolucion_tasa}")
    # Primeros 400 caracteres
    print("Inicio:", full_text[:300].replace("\n", " "))

for f in pdf_files:
    analizar_pdf(f)
