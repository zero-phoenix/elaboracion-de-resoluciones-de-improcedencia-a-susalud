"""Guardia DLP (Data Loss Prevention / Fuga de Placeholders) para Resoluciones de Improcedencia.
Detecta cadenas parásitas, variables sin resolver o corchetes residuales.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import List, Tuple

from docx import Document

PATRONES_FUGA = [
    r"\[NOMBRE\]",
    r"\[EXPEDIENTE\]",
    r"\[DENUNCIANTE\]",
    r"\[DENUNCIADO\]",
    r"\[FECHA\]",
    r"\[XXX+\]",
    r"\{[A-Za-z0-9_]+\}",
    r"TODO",
    r"FIXME",
    r"COMPLETAR",
    r"INSERTAR",
]


def auditar_documento(ruta_docx: Path) -> List[Tuple[str, str, int]]:
    """Inspecciona párrafos y tablas buscando placeholders sin resolver."""
    doc = Document(str(ruta_docx))
    hallazgos = []

    for idx, p in enumerate(doc.paragraphs, 1):
        texto = p.text
        for pat in PATRONES_FUGA:
            if re.search(pat, texto, re.IGNORECASE):
                hallazgos.append((pat, texto[:100], idx))

    for t_idx, tabla in enumerate(doc.tables, 1):
        for f_idx, fila in enumerate(tabla.rows, 1):
            for c_idx, celda in enumerate(fila.cells, 1):
                texto = celda.text
                for pat in PATRONES_FUGA:
                    if re.search(pat, texto, re.IGNORECASE):
                        hallazgos.append((pat, f"Tabla {t_idx} Fila {f_idx} Celda {c_idx}: {texto[:60]}", 0))

    return hallazgos


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python guardia_improcedencia.py <archivo.docx>")
        sys.exit(1)

    archivo = Path(sys.argv[1])
    if not archivo.exists():
        print(f"Error: No existe el archivo {archivo}")
        sys.exit(1)

    fugas = auditar_documento(archivo)
    if fugas:
        print(f"❌ FALLO DE GUARDIA DLP: Se encontraron {len(fugas)} elementos sin resolver:")
        for pat, texto, parrafo in fugas:
            print(f"  - Patrón '{pat}' en párrafo/bloque {parrafo}: {texto}")
        sys.exit(1)
    else:
        print("✅ GUARDIA DLP APROBADA: Cero placeholders o variables sin resolver.")
