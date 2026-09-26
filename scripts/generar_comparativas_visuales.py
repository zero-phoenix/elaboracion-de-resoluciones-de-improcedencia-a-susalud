import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

src_dir = Path(r"C:\Users\Admin\.gemini\antigravity\brain\18369d91-b2f7-445f-b6d3-baa02401afcd")
out_dir = Path(r"C:\Users\Admin\Documents\antigravity\zealous-kepler\elaboracion-de-resoluciones-de-improcedencia-a-susalud\generados\comparativas")
out_dir.mkdir(parents=True, exist_ok=True)

for i in range(1, 10):
    img_iafas_path = src_dir / f"0146_iafa_pag_{i}.png"
    img_ipress_path = src_dir / f"0147_ipress_pag_{i}.png"
    
    if not (img_iafas_path.exists() and img_ipress_path.exists()):
        print(f"Saltando pagina {i}, no existen ambos archivos")
        continue
        
    img_iafas = Image.open(img_iafas_path)
    img_ipress = Image.open(img_ipress_path)
    
    # Redimensionar a la misma altura si difieren
    target_height = max(img_iafas.height, img_ipress.height)
    if img_iafas.height != target_height:
        ratio = target_height / img_iafas.height
        img_iafas = img_iafas.resize((int(img_iafas.width * ratio), target_height), Image.Resampling.LANCZOS)
    if img_ipress.height != target_height:
        ratio = target_height / img_ipress.height
        img_ipress = img_ipress.resize((int(img_ipress.width * ratio), target_height), Image.Resampling.LANCZOS)
        
    header_height = 80
    border_width = 8
    total_width = img_iafas.width + img_ipress.width + border_width
    total_height = target_height + header_height
    
    comp = Image.new("RGB", (total_width, total_height), color=(245, 245, 245))
    draw = ImageDraw.Draw(comp)
    
    # Dibujar cabeceras
    # Fondo encabezado
    draw.rectangle([(0, 0), (total_width, header_height)], fill=(26, 54, 93))
    
    # Texto cabecera
    # Intentar cargar fuente estándar
    try:
        font_title = ImageFont.truetype("arial.ttf", 26)
        font_sub = ImageFont.truetype("arialbd.ttf", 22)
    except:
        font_title = ImageFont.load_default()
        font_sub = ImageFont.load_default()
        
    title_left = f"RESOLUCIÓN N° 0146-2026/CC1 | IAFAS (SEGUROS SOAT)"
    title_right = f"RESOLUCIÓN N° 0147-2026/CC1 | IPRESS (CLÍNICA MÉDICA)"
    
    draw.text((40, 25), title_left, fill=(255, 255, 255), font=font_sub)
    draw.text((img_iafas.width + border_width + 40, 25), title_right, fill=(255, 255, 255), font=font_sub)
    
    # Pegar imágenes
    comp.paste(img_iafas, (0, header_height))
    # Linea divisoria
    draw.rectangle([(img_iafas.width, header_height), (img_iafas.width + border_width, total_height)], fill=(200, 200, 200))
    comp.paste(img_ipress, (img_iafas.width + border_width, header_height))
    
    out_file = out_dir / f"comparativo_pagina_{i}.png"
    comp.save(str(out_file), quality=95)
    
    # Copiar a artifact dir
    artifact_comp = src_dir / f"comparativo_pagina_{i}.png"
    comp.save(str(artifact_comp), quality=95)
    
    print(f"Generado comparativo pagina {i}: {out_file}")

print("Proceso de generacion de comparativas completado.")
