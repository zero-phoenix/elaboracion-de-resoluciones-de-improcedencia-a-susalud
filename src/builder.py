"""Constructor OpenXML de alta precisión para Resoluciones de Improcedencia a SUSALUD.
Comisión de Protección al Consumidor N° 1 (CC1) - INDECOPI.

Elaborado por: David Chávez
Supervisado por: Loussiana Salazar
Equipo: Seguros
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
    TAMANO_METADATA_PT,
    TAMANO_TEXTO_PT,
    TAMANO_TITULO_PT,
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
    font_name: str = FUENTE_PRINCIPAL,
) -> Any:
    """Añade un run garantizando la fuente en todos los slots OpenXML."""
    run = parrafo.add_run(texto)
    run.font.name = font_name
    rPr = run._element.get_or_add_rPr()
    rFonts = rPr.find(qn("w:rFonts"))
    if rFonts is None:
        rFonts = OxmlElement("w:rFonts")
        rPr.insert(0, rFonts)
    rFonts.set(qn("w:ascii"), font_name)
    rFonts.set(qn("w:hAnsi"), font_name)
    rFonts.set(qn("w:cs"), font_name)
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
    font_name: str = FUENTE_PRINCIPAL,
) -> None:
    """Detecta 'N°' o números ordinales como 1° y formatea la volada en superíndice."""
    partes = re.split(r"(N°|N\s*°|\b\d+°)", texto)
    for p in partes:
        if not p:
            continue
        if p.startswith("N") and "°" in p:
            add_run(parrafo, "N", bold=bold, size=size, font_name=font_name)
            add_run(parrafo, "°", bold=bold, size=size, superscript=True, font_name=font_name)
        elif re.match(r"^\d+°$", p):
            num = p[:-1]
            add_run(parrafo, num, bold=bold, size=size, font_name=font_name)
            add_run(parrafo, "°", bold=bold, size=size, superscript=True, font_name=font_name)
        else:
            add_run(parrafo, p, bold=bold, size=size, font_name=font_name)


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


def construir_resolucion_desde_dossier(
    dossier: Dict[str, Any],
    ruta_salida: Path,
    ruta_plantilla: Path | None = None,
) -> Path:
    """Clona la plantilla maestra institucional y vuelca el dossier con fidelidad tipográfica."""
    if ruta_plantilla is None:
        plantillas = list(PLANTILLAS_DIR.glob("*.docx"))
        if not plantillas:
            raise FileNotFoundError(f"No se encontró ninguna plantilla base en {PLANTILLAS_DIR}")
        ruta_plantilla = plantillas[0]

    ruta_salida.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(ruta_plantilla, ruta_salida)

    doc = Document(str(ruta_salida))

    # 1. Actualizar el Expediente en el encabezado oficial
    exp_num = dossier["metadatos"]["expediente"]
    for s in doc.sections:
        if len(s.header.paragraphs) > 2:
            p_hdr = s.header.paragraphs[2]
            p_hdr.text = f"\tEXPEDIENTE  {exp_num}"
            for r in p_hdr.runs:
                r.font.name = FUENTE_PRINCIPAL
                r.font.size = Pt(8.5)

    # 2. Limpiar el cuerpo del documento preservando sección/encabezados/pies
    for p in list(doc.paragraphs):
        p._element.getparent().remove(p._element)

    m = dossier["metadatos"]

    # --- PÁRRAFOS DE CONTROL INTERNO (8 pt) ---
    p_elab = nuevo_parrafo(doc, WD_ALIGN_PARAGRAPH.LEFT)
    add_run(p_elab, f"Elaborado por: {m['elaborado_por']}", size=Pt(TAMANO_METADATA_PT))

    p_sup = nuevo_parrafo(doc, WD_ALIGN_PARAGRAPH.LEFT)
    add_run(p_sup, f"Supervisado por: {m['supervisado_por']}", size=Pt(TAMANO_METADATA_PT))

    p_eq = nuevo_parrafo(doc, WD_ALIGN_PARAGRAPH.LEFT)
    add_run(p_eq, f"Equipo: {m['equipo']}", size=Pt(TAMANO_METADATA_PT))

    p_venc = nuevo_parrafo(doc, WD_ALIGN_PARAGRAPH.LEFT)
    add_run(p_venc, f"Vencimiento: {m['vencimiento']}", size=Pt(TAMANO_METADATA_PT))

    nuevo_parrafo(doc)

    # --- TÍTULO DE LA RESOLUCIÓN (16 pt Bold) ---
    p_tit = nuevo_parrafo(doc, WD_ALIGN_PARAGRAPH.CENTER)
    add_texto_con_superindices(p_tit, m["numero_resolucion"], bold=True, size=Pt(TAMANO_TITULO_PT))

    nuevo_parrafo(doc)

    # --- CUADRO DE IDENTIFICACIÓN ---
    p_den = nuevo_parrafo(doc, WD_ALIGN_PARAGRAPH.JUSTIFY)
    add_run(p_den, "DENUNCIANTE\t:\t", bold=True)
    add_run(p_den, m["denunciante_linea"])

    p_denun = nuevo_parrafo(doc, WD_ALIGN_PARAGRAPH.JUSTIFY)
    add_run(p_denun, "DENUNCIADO\t:\t", bold=True)
    add_run(p_denun, m["denunciado_linea"])

    p_mat = nuevo_parrafo(doc, WD_ALIGN_PARAGRAPH.JUSTIFY)
    add_run(p_mat, "MATERIA\t:\t", bold=True)
    add_run(p_mat, m["materia_lineas"][0])
    for l_extra in m["materia_lineas"][1:]:
        p_extra = nuevo_parrafo(doc, WD_ALIGN_PARAGRAPH.JUSTIFY)
        add_run(p_extra, f"\t\t{l_extra}")

    p_act = nuevo_parrafo(doc, WD_ALIGN_PARAGRAPH.JUSTIFY)
    add_run(p_act, "ACTIVIDAD\t:\t", bold=True)
    add_run(p_act, m["actividad"])

    nuevo_parrafo(doc)

    # --- FECHA ---
    p_fec = nuevo_parrafo(doc, WD_ALIGN_PARAGRAPH.LEFT)
    add_run(p_fec, f"Lima, {m['fecha_emision']}")

    nuevo_parrafo(doc)

    # --- ANTECEDENTES ---
    p_ant_tit = nuevo_parrafo(doc, WD_ALIGN_PARAGRAPH.LEFT)
    add_run(p_ant_tit, "ANTECEDENTES", bold=True)

    for texto in dossier["parrafos_antecedentes"]:
        p_ant = nuevo_parrafo(doc, WD_ALIGN_PARAGRAPH.JUSTIFY)
        add_texto_con_superindices(p_ant, texto)
        nuevo_parrafo(doc)

    # --- ANÁLISIS ---
    p_an_tit = nuevo_parrafo(doc, WD_ALIGN_PARAGRAPH.LEFT)
    add_run(p_an_tit, "ANÁLISIS", bold=True)

    p_an_sub = nuevo_parrafo(doc, WD_ALIGN_PARAGRAPH.LEFT)
    add_run(p_an_sub, dossier["subtitulo_analisis"], bold=True)

    for texto in dossier["parrafos_analisis"]:
        p_an = nuevo_parrafo(doc, WD_ALIGN_PARAGRAPH.JUSTIFY)
        add_texto_con_superindices(p_an, texto)
        nuevo_parrafo(doc)

    # Subsección (i)
    p_sub1_tit = nuevo_parrafo(doc, WD_ALIGN_PARAGRAPH.LEFT)
    add_run(p_sub1_tit, dossier["tit_sub1"], bold=True)

    for texto in dossier["parrafos_sub1"]:
        p_s1 = nuevo_parrafo(doc, WD_ALIGN_PARAGRAPH.JUSTIFY)
        add_texto_con_superindices(p_s1, texto)
        nuevo_parrafo(doc)

    # Subsección (ii)
    p_sub2_tit = nuevo_parrafo(doc, WD_ALIGN_PARAGRAPH.LEFT)
    add_run(p_sub2_tit, dossier["tit_sub2"], bold=True)

    for texto in dossier["parrafos_sub2"]:
        p_s2 = nuevo_parrafo(doc, WD_ALIGN_PARAGRAPH.JUSTIFY)
        add_texto_con_superindices(p_s2, texto)
        nuevo_parrafo(doc)

    # --- RESUELVE ---
    p_res_tit = nuevo_parrafo(doc, WD_ALIGN_PARAGRAPH.LEFT)
    add_run(p_res_tit, "RESUELVE", bold=True)

    for articulo in dossier["articulos_resuelve"]:
        p_art = nuevo_parrafo(doc, WD_ALIGN_PARAGRAPH.JUSTIFY)
        add_texto_con_superindices(p_art, articulo)
        nuevo_parrafo(doc)

    doc.save(str(ruta_salida))
    return ruta_salida
