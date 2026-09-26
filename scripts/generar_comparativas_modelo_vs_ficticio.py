from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import shutil

src_dir = Path(r"C:\Users\Admin\.gemini\antigravity\brain\18369d91-b2f7-445f-b6d3-baa02401afcd")
out_dir = Path(r"c:\Users\Admin\Documents\antigravity\zealous-kepler\elaboracion-de-resoluciones-de-improcedencia-a-susalud\generados\comparativas_popperianas")
out_dir.mkdir(parents=True, exist_ok=True)

for i in range(1, 10):
    img_modelo_path = src_dir / f"0146_iafa_pag_{i}.png"
    img_ficticio_path = src_dir / f"mixta_pag_{i}.png"
    
    if not (img_modelo_path.exists() and img_ficticio_path.exists()):
        print(f"Saltando pagina {i}, no existen ambos archivos")
        continue
        
    img_modelo = Image.open(img_modelo_path)
    img_ficticio = Image.open(img_ficticio_path)
    
    # Redimensionar a la misma altura si difieren
    target_height = max(img_modelo.height, img_ficticio.height)
    if img_modelo.height != target_height:
        ratio = target_height / img_modelo.height
        img_modelo = img_modelo.resize((int(img_modelo.width * ratio), target_height), Image.Resampling.LANCZOS)
    if img_ficticio.height != target_height:
        ratio = target_height / img_ficticio.height
        img_ficticio = img_ficticio.resize((int(img_ficticio.width * ratio), target_height), Image.Resampling.LANCZOS)
        
    header_height = 80
    border_width = 10
    total_width = img_modelo.width + img_ficticio.width + border_width
    total_height = target_height + header_height
    
    comp = Image.new("RGB", (total_width, total_height), color=(245, 245, 245))
    draw = ImageDraw.Draw(comp)
    
    # Dibujar cabeceras
    draw.rectangle([(0, 0), (total_width, header_height)], fill=(20, 35, 60))
    
    try:
        font_sub = ImageFont.truetype("arialbd.ttf", 22)
    except:
        font_sub = ImageFont.load_default()
        
    title_left = f"[IZQUIERDA: MODELO REAL CC1] RES. N° 0146-2026/CC1 (PÁG. {i}/9)"
    title_right = f"[DERECHA: CASO COMPLEJO ELABORADO] RES. N° 0512-2026/CC1 (PÁG. {i}/9)"
    
    draw.text((40, 26), title_left, fill=(255, 255, 255), font=font_sub)
    draw.text((img_modelo.width + border_width + 40, 26), title_right, fill=(130, 220, 255), font=font_sub)
    
    # Pegar imágenes
    comp.paste(img_modelo, (0, header_height))
    # Linea divisoria vertical
    draw.rectangle([(img_modelo.width, header_height), (img_modelo.width + border_width, total_height)], fill=(0, 120, 215))
    comp.paste(img_ficticio, (img_modelo.width + border_width, header_height))
    
    out_file = out_dir / f"comparativo_popperiano_pag_{i}.png"
    comp.save(str(out_file), quality=95)
    
    artifact_comp = src_dir / f"comparativo_popperiano_pag_{i}.png"
    comp.save(str(artifact_comp), quality=95)
    
    print(f"Generado comparativo Popperiano pagina {i}: {out_file}")

print("Proceso completado exitosamente.")
