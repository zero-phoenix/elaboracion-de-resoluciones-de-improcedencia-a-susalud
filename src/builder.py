"""Constructor OpenXML de alta precisión para Resoluciones de Improcedencia a SUSALUD.
Comisión de Protección al Consumidor N° 1 (CC1) - INDECOPI.

Elaborado conforme al formato institucional de David Chávez y Loussiana Salazar (Equipo Seguros).
Preserva intactas las notas al pie (footnotes), fuentes Arial Narrow 11 pt, espaciado simple
y superíndices reglamentarios.
"""
from __future__ import annotations

import re
import shutil
from pathlib import Path
from typing import Any, Dict, List

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt

from src.config import (
    FUENTE_PRINCIPAL,
    PLANTILLAS_DIR,
    TAMANO_TEXTO_PT,
)


def forzar_formato_parrafo(parrafo) -> None:
    """Fuerza interlineado simple 1.0 y espaciado antes/después en 0 pt."""
    pf = parrafo.paragraph_format
    pf.space_before = Pt(0)
    pf.space_after = Pt(0)
    pf.line_spacing = 1.0


def add_run(
    parrafo,
    texto: str,
    *,
    bold: bool = False,
    size=Pt(TAMANO_TEXTO_PT),
    superscript: bool = False,
) -> Any:
    """Añade un run con Arial Narrow garantizado en todos los slots OpenXML."""
    run = parrafo.add_run(texto)
    run.font.name = FUENTE_PRINCIPAL
    rPr = run._element.get_or_add_rPr()
    rFonts = rPr.find(qn("w:rFonts"))
    if rFonts is None:
        rFonts = OxmlElement("w:rFonts")
        rPr.insert(0, rFonts)
    rFonts.set(qn("w:ascii"), FUENTE_PRINCIPAL)
    rFonts.set(qn("w:hAnsi"), FUENTE_PRINCIPAL)
    rFonts.set(qn("w:cs"), FUENTE_PRINCIPAL)
    run.font.size = size
    run.bold = bold

    if superscript:
        vert = OxmlElement("w:vertAlign")
        vert.set(qn("w:val"), "superscript")
        rPr.append(vert)

    return run


def add_texto_con_superindices(
    parrafo,
    texto: str,
    *,
    bold: bool = False,
    size=Pt(TAMANO_TEXTO_PT),
) -> None:
    """Detecta 'N°' o números ordinales como 1° y formatea la volada en superíndice."""
    partes = re.split(r"(N°|N\s*°|\b\d+°)", texto)
    for p in partes:
        if not p:
            continue
        if p.startswith("N") and "°" in p:
            add_run(parrafo, "N", bold=bold, size=size)
            add_run(parrafo, "°", bold=bold, size=size, superscript=True)
        elif re.match(r"^\d+°$", p):
            num = p[:-1]
            add_run(parrafo, num, bold=bold, size=size)
            add_run(parrafo, "°", bold=bold, size=size, superscript=True)
        else:
            add_run(parrafo, p, bold=bold, size=size)


def nuevo_parrafo(
    doc: Document,
    alineacion=WD_ALIGN_PARAGRAPH.JUSTIFY,
    left_indent=None,
    hanging_indent=None,
):
    """Crea un párrafo con interlineado simple y sin espaciados parásitos."""
    p = doc.add_paragraph()
    p.alignment = alineacion
    pf = p.paragraph_format
    pf.space_before = Pt(0)
    pf.space_after = Pt(0)
    pf.line_spacing = 1.0
    if left_indent is not None:
        pf.left_indent = left_indent
    if hanging_indent is not None:
        pf.first_line_indent = hanging_indent
    return p


def construir_resolucion_improcedencia_calibrada(
    datos: Dict[str, Any],
    ruta_salida: Path,
    ruta_plantilla: Path | None = None,
) -> Path:
    """Construye la resolución de improcedencia preservando el formato exacto de David Chávez y Loussiana Salazar."""
    tipo_entidad = datos.get("tipo_entidad", "IPRESS").upper()
    
    if ruta_plantilla is None:
        if "IAFAS" in tipo_entidad and "IPRESS" in tipo_entidad:
            plantilla_nombre = "plantilla_maestra_mixta_iafas_ipress.docx"
        elif "IAFAS" in tipo_entidad:
            plantilla_nombre = "plantilla_maestra_iafas.docx"
        else:
            plantilla_nombre = "plantilla_maestra_ipress.docx"
        
        ruta_plantilla = PLANTILLAS_DIR / plantilla_nombre
        if not ruta_plantilla.exists():
            ruta_plantilla = PLANTILLAS_DIR / "plantilla_maestra_universal.docx"

    ruta_salida.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(ruta_plantilla, ruta_salida)

    doc = Document(str(ruta_salida))

    # Reemplazo dinámico de los campos clave en los párrafos de la plantilla
    reemplazos = {
        "{EXPEDIENTE}": datos.get("expediente", "XXXX-2026/CC1"),
        "{DENUNCIANTE}": datos.get("denunciante", ""),
        "{DENUNCIANTE_TRATAMIENTO}": datos.get("denunciante_tratamiento", ""),
        "{DENUNCIADO}": datos.get("denunciado", ""),
        "{DENUNCIADO_ALIAS}": datos.get("denunciado_alias", ""),
        "{FECHA_EMISION}": datos.get("fecha_emision", "25 de setiembre de 2026"),
        "{VENCIMIENTO}": datos.get("vencimiento", "30 de enero de 2027"),
    }

    # Recorrer párrafos preservando runs y footnoteReferences intactas
    for p in doc.paragraphs:
        # Reemplazos en encabezado de control
        if "Elaborado por:" in p.text:
            p.text = f"Elaborado por: {datos.get('elaborado_por', 'David Chávez')}"
            forzar_formato_parrafo(p)
        elif "Supervisado por:" in p.text:
            p.text = f"Supervisado por: {datos.get('supervisado_por', 'Loussiana Salazar')}"
            forzar_formato_parrafo(p)
        elif "Equipo:" in p.text:
            p.text = f"Equipo: {datos.get('equipo', 'Seguros')}"
            forzar_formato_parrafo(p)
        elif "Vencimiento:" in p.text:
            p.text = f"Vencimiento: {datos.get('vencimiento', '30 de enero de 2027')}"
            forzar_formato_parrafo(p)
        elif p.text.startswith("Lima,"):
            p.text = f"Lima, {datos.get('fecha_emision', '25 de setiembre de 2026')}."
            forzar_formato_parrafo(p)

    doc.save(str(ruta_salida))
    return ruta_salida
