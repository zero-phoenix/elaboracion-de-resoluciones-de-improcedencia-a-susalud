import pymupdf
from pathlib import Path
import shutil

pdf_path = Path(r"C:\Users\Admin\Documents\antigravity\zealous-kepler\elaboracion-de-resoluciones-de-improcedencia-a-susalud\generados\RESOLUCION_COMPLEJA_CC1_IMPROCEDENCIA_SUSALUD.pdf")
out_dir = Path(r"C:\Users\Admin\Documents\antigravity\zealous-kepler\elaboracion-de-resoluciones-de-improcedencia-a-susalud\generados\capturas")
out_dir.mkdir(parents=True, exist_ok=True)

artifact_dir = Path(r"C:\Users\Admin\.gemini\antigravity\brain\18369d91-b2f7-445f-b6d3-baa02401afcd")

doc = pymupdf.open(str(pdf_path))
print(f"Total de paginas en la resolucion: {len(doc)}")

image_paths = []
for i, page in enumerate(doc):
    # Render at 150 DPI for high quality
    pix = page.get_pixmap(dpi=150)
    img_name = f"resolucion_pagina_{i+1}.png"
    img_file = out_dir / img_name
    pix.save(str(img_file))
    
    # Copy to artifact directory
    artifact_img = artifact_dir / img_name
    shutil.copyfile(img_file, artifact_img)
    
    image_paths.append(str(artifact_img))
    print(f"Pagina {i+1} guardada en: {img_file} y {artifact_img}")

print("Renderizado completado.")
