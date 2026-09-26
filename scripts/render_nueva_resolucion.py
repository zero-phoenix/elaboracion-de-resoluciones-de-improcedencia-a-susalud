import pymupdf
from pathlib import Path
import shutil

BASE_DIR = Path(__file__).resolve().parent.parent
PDF_PATH = BASE_DIR / "generados" / "RESOLUCION_0842-2026_CC1_RIMAC_ANGLO.pdf"
OUT_DIR = BASE_DIR / "generados" / "capturas_nueva_resolucion"
OUT_DIR.mkdir(parents=True, exist_ok=True)
ARTIFACT_DIR = Path(r"C:\Users\Admin\.gemini\antigravity\brain\18369d91-b2f7-445f-b6d3-baa02401afcd")

doc = pymupdf.open(PDF_PATH)
print(f"Total paginas de la nueva resolucion: {len(doc)}")

for i, page in enumerate(doc):
    pix = page.get_pixmap(dpi=150)
    png_name = f"nueva_res_0842_pag_{i+1}.png"
    out_file = OUT_DIR / png_name
    pix.save(str(out_file))
    shutil.copyfile(out_file, ARTIFACT_DIR / png_name)
    print(f"Página {i+1}/9 guardada en: {out_file} y copiada al artefacto.")

print("Renderizado completo de las 9 paginas.")
