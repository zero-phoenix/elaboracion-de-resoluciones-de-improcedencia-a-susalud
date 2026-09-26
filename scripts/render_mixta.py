import fitz
from pathlib import Path
import shutil

pdf_path = Path("generados/RESOLUCION_0512-2026_CC1_MIXTA_COMPLEJA.pdf")
out_dir = Path("generados/capturas_mixta")
out_dir.mkdir(parents=True, exist_ok=True)
artifact_dir = Path(r"C:\Users\Admin\.gemini\antigravity\brain\18369d91-b2f7-445f-b6d3-baa02401afcd")

doc = fitz.open(pdf_path)
print(f"Total paginas: {len(doc)}")

for i, page in enumerate(doc):
    pix = page.get_pixmap(dpi=150)
    png_name = f"mixta_pag_{i+1}.png"
    out_file = out_dir / png_name
    pix.save(str(out_file))
    shutil.copyfile(out_file, artifact_dir / png_name)
    print(f"Guardada pagina {i+1} en {out_file}")
