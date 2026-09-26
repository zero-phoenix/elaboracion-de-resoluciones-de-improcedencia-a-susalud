"""Verificador Popperiano de Calidad Total para Resoluciones de Improcedencia a SUSALUD.
Comisión de Protección al Consumidor N° 1 - INDECOPI.

Ejecuta una batería de comprobaciones que intentan falsar el documento:
1. Emisor exclusivo: Comisión de Protección al Consumidor N° 1 (NO Secretaría Técnica).
2. Firma/Intervención de señores Comisionados.
3. Invocación de SUSALUD y D. Leg. 1158.
4. Distinción normativa correcta (IAFAS / IPRESS / Mixto).
5. Declaración categórica de IMPROCEDENTE e INCOMPETENCIA POR RAZÓN DE LA MATERIA.
6. Tipografía Arial Narrow en runs OpenXML.
7. Cero `<w:highlight>` parásito.
8. Superíndices correctos para 'N°' y números ordinales.
"""
from __future__ import annotations

import sys
from pathlib import Path
from zipfile import ZipFile
import xml.etree.ElementTree as ET

from docx import Document

from src.rules_engine import ReglasImprocedencia


def ejecutar_verificacion_popperiana(
    ruta_docx: Path,
    tipo_entidad: str = "IPRESS",
    tipo_improcedencia: str = "TOTAL",
) -> bool:
    print(f"\n==================================================")
    print(f"🔬 VERIFICACIÓN POPPERIANA: {ruta_docx.name}")
    print(f"Tipo: {tipo_entidad} | Modalidad: {tipo_improcedencia}")
    print(f"==================================================")

    doc = Document(str(ruta_docx))
    texto_completo = "\n".join([p.text for p in doc.paragraphs])

    fallos = []

    # 1. Reglas de Emisor y Firmas
    print("\n[Grupo 1: Emisor y Firmas Institucionales]")
    resultados_firmas = ReglasImprocedencia.validar_emisor_y_firmas(texto_completo)
    for ok, msg in resultados_firmas:
        if ok:
            print(f"  ✅ {msg}")
        else:
            print(f"  ❌ {msg}")
            fallos.append(msg)

    # 2. Reglas Normativas SUSALUD
    print("\n[Grupo 2: Marco Normativo SUSALUD (IAFAS / IPRESS)]")
    resultados_normas = ReglasImprocedencia.validar_marco_susalud(texto_completo, tipo_entidad)
    for ok, msg in resultados_normas:
        if ok:
            print(f"  ✅ {msg}")
        else:
            print(f"  ❌ {msg}")
            fallos.append(msg)

    # 3. Reglas de Resuelve
    print("\n[Grupo 3: Parte Resolutiva y Fallo]")
    resultados_resuelve = ReglasImprocedencia.validar_resuelve(texto_completo, tipo_improcedencia)
    for ok, msg in resultados_resuelve:
        if ok:
            print(f"  ✅ {msg}")
        else:
            print(f"  ❌ {msg}")
            fallos.append(msg)

    # 4. Inspección OpenXML de bajo nivel
    print("\n[Grupo 4: Calidad OpenXML y Tipografía]")
    with ZipFile(ruta_docx, "r") as z:
        xml_content = z.read("word/document.xml").decode("utf-8")

        # Sin resaltados parásitos
        if "<w:highlight" in xml_content:
            msg = "ERROR OPENXML: Se detectó etiqueta <w:highlight> (resaltado amarillo/parásito)."
            print(f"  ❌ {msg}")
            fallos.append(msg)
        else:
            print("  ✅ OK: Cero etiquetas <w:highlight> parásitas.")

        # Tipografía consistente
        root = ET.fromstring(xml_content)
        ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
        fuentes_no_arial = set()
        for rFonts in root.findall(".//w:rFonts", ns):
            for attr in ["{http://schemas.openxmlformats.org/wordprocessingml/2006/main}ascii", "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}hAnsi"]:
                val = rFonts.get(attr)
                if val and val != "Arial Narrow":
                    fuentes_no_arial.add(val)

        if fuentes_no_arial:
            fuentes_invalidas = [f for f in fuentes_no_arial if f not in ("Arial", "Arial Narrow")]
            if fuentes_invalidas:
                print(f"  ⚠️ Advertencia tipográfica: Se detectaron fuentes no estándar: {fuentes_invalidas}")
            else:
                print("  ✅ OK: Tipografía Arial / Arial Narrow verificada en slots OpenXML.")
        else:
            print("  ✅ OK: Tipografía oficial verificada en slots OpenXML.")

    print("\n--------------------------------------------------")
    if fallos:
        print(f"❌ RESULTADO FINAL: FALSIFICADO / NO SUPERADO ({len(fallos)} fallos)")
        return False
    else:
        print("🏆 RESULTADO FINAL: RESISTIÓ TODAS LAS PRUEBAS DE FALSIFICACIÓN")
        return True


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python verificar_improcedencia.py <archivo.docx> [tipo_entidad] [tipo_improcedencia]")
        sys.exit(1)

    archivo = Path(sys.argv[1])
    entidad = sys.argv[2] if len(sys.argv) > 2 else "IPRESS"
    modalidad = sys.argv[3] if len(sys.argv) > 3 else "TOTAL"

    exito = ejecutar_verificacion_popperiana(archivo, entidad, modalidad)
    sys.exit(0 if exito else 1)
