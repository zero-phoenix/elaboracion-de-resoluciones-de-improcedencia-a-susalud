"""Constructor OpenXML de alta precisión para Resoluciones de Improcedencia a SUSALUD.
Comisión de Protección al Consumidor N° 1 (CC1) - INDECOPI.

Filosofía Popperiana:
NUNCA reconstruir párrafos desde cero cuando la plantilla maestra contiene enlaces
OpenXML críticos (<w:footnoteReference> a word/footnotes.xml) y membretes institucionales.
Se opera a nivel atómico de runs (<w:r>) preservando íntegramente las notas al pie,
las fuentes Arial 10 regular / Arial negrita para ordinales, encabezados sin resaltados,
y la estructura de 9 páginas oficial de la CC1.
"""
from __future__ import annotations

import re
import shutil
from pathlib import Path
from typing import Any, Dict, List
from zipfile import ZipFile

from docx import Document

from src.config import PLANTILLAS_DIR, GENERADOS_DIR

def set_paragraph_text_preserving_footnotes(p, new_text_before_fn=None, new_text_after_fn=None, full_text=None):
    """
    Modifica el texto de un párrafo preservando intactos los runs que contienen <w:footnoteReference>.
    """
    fn_indices = [idx for idx, r in enumerate(p.runs) if 'footnoteReference' in r._r.xml]
    
    if not fn_indices:
        if full_text is not None:
            if p.runs:
                p.runs[0].text = full_text
                for r in p.runs[1:]:
                    r.text = ""
            else:
                p.text = full_text
        return
        
    fn_idx = fn_indices[0]
    
    if new_text_before_fn is not None:
        for i in range(fn_idx):
            if i == 0:
                p.runs[i].text = new_text_before_fn
            else:
                p.runs[i].text = ""
                
    if new_text_after_fn is not None:
        after_runs = list(range(fn_idx + 1, len(p.runs)))
        if after_runs:
            p.runs[after_runs[0]].text = new_text_after_fn
            for i in after_runs[1:]:
                p.runs[i].text = ""
        else:
            p.add_run(new_text_after_fn)

def construir_resolucion_improcedencia_popperiana(
    datos: Dict[str, Any],
    ruta_salida: Path,
    ruta_plantilla: Path | None = None,
) -> Path:
    """
    Construye una resolución de improcedencia a SUSALUD preservando 100% el estándar CC1.
    """
    if ruta_plantilla is None:
        plantillas = list(PLANTILLAS_DIR.glob("*.docx"))
        if not plantillas:
            raise FileNotFoundError(f"No se encontró plantilla en {PLANTILLAS_DIR}")
        ruta_plantilla = plantillas[0]
        
    ruta_salida.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(ruta_plantilla, ruta_salida)
    
    doc = Document(ruta_salida)
    
    # 1. Metadatos de control
    expediente = datos.get("expediente", "0000-2026/CC1")
    numero_resolucion = datos.get("numero_resolucion", "RESOLUCIÓN FINAL N° 0000-2026/CC1")
    denunciante = datos.get("denunciante", "")
    denunciado = datos.get("denunciado", "")
    fecha_emision = datos.get("fecha_emision", "25 de setiembre de 2026")
    
    set_paragraph_text_preserving_footnotes(doc.paragraphs[0], full_text="Elaborado por:\tDavid Chávez")
    set_paragraph_text_preserving_footnotes(doc.paragraphs[1], full_text="Supervisado por:\tLoussiana Salazar")
    set_paragraph_text_preserving_footnotes(doc.paragraphs[2], full_text="Equipo:\tSeguros y Salud")
    set_paragraph_text_preserving_footnotes(doc.paragraphs[3], full_text="Vencimiento:\t28/10/2026")
    set_paragraph_text_preserving_footnotes(doc.paragraphs[5], full_text=numero_resolucion)
    
    set_paragraph_text_preserving_footnotes(doc.paragraphs[7], full_text=f"DENUNCIANTE\t:\t{denunciante}")
    set_paragraph_text_preserving_footnotes(doc.paragraphs[8], full_text=f"DENUNCIADO(S)\t:\t{denunciado}")
    set_paragraph_text_preserving_footnotes(doc.paragraphs[9], full_text="MATERIA\t:\tIMPROCEDENCIA DE LA DENUNCIA")
    set_paragraph_text_preserving_footnotes(doc.paragraphs[10], full_text="\t\tDECLINACIÓN DE COMPETENCIA")
    set_paragraph_text_preserving_footnotes(doc.paragraphs[11], full_text="ACTIVIDAD\t:\tACTIVIDADES RELACIONADAS CON LA SALUD HUMANA")
    set_paragraph_text_preserving_footnotes(doc.paragraphs[13], full_text=f"Lima, {fecha_emision}")
    
    # 2. Antecedentes
    set_paragraph_text_preserving_footnotes(doc.paragraphs[15], full_text="ANTECEDENTES")
    escrito_fecha = datos.get("escrito_fecha", "14 de mayo de 2026")
    subsanado_fecha = datos.get("subsanado_fecha", "10 de junio de 2026")
    set_paragraph_text_preserving_footnotes(
        doc.paragraphs[17],
        new_text_before_fn=f"Mediante escrito del {escrito_fecha}, subsanado mediante escrito del {subsanado_fecha}, la parte denunciante denunció a los denunciados por presuntas infracciones a la Ley N° 29571, Código de Protección y Defensa del Consumidor",
        new_text_after_fn=" (en adelante, el Código), señalando lo siguiente:"
    )
    
    # Hechos
    hechos = datos.get("hechos", [])
    indices_hechos = [19, 21, 23, 25, 27, 29, 31]
    for idx_h, texto_h in zip(indices_hechos, hechos):
        set_paragraph_text_preserving_footnotes(doc.paragraphs[idx_h], full_text=texto_h)
        
    # Medida correctiva
    medida_correctiva = datos.get("medida_correctiva", "")
    set_paragraph_text_preserving_footnotes(doc.paragraphs[33], full_text=medida_correctiva)
    
    # Análisis y Cuestión Previa
    set_paragraph_text_preserving_footnotes(doc.paragraphs[37], full_text=f"Sobre la improcedencia de la denuncia interpuesta")
    set_paragraph_text_preserving_footnotes(doc.paragraphs[45], full_text="Al respecto, la Comisión de Protección al Consumidor N° 1 (en adelante, la Comisión) debe verificar si el Indecopi es el órgano competente para pronunciarse sobre los hechos cuestionados en la denuncia.")
    
    # Subsunción normativa
    subsun_normativa = datos.get("subsun_normativa", "")
    if subsun_normativa:
        set_paragraph_text_preserving_footnotes(
            doc.paragraphs[59],
            new_text_before_fn="Asimismo, conforme al Anexo I-C del Reglamento de Infracciones y Sanciones de Susalud, aprobado por el Decreto Supremo N° 031-2014-SA",
            new_text_after_fn=f", {subsun_normativa}"
        )
        
    set_paragraph_text_preserving_footnotes(doc.paragraphs[77], full_text="A continuación, se determinará la autoridad competente para conocer la denuncia y, de ser el caso, imponer las sanciones correspondientes.")
    
    # Subsunción caso concreto
    subsun_concreto = datos.get("subsun_concreto", "")
    if subsun_concreto:
        set_paragraph_text_preserving_footnotes(doc.paragraphs[85], full_text=subsun_concreto)
        
    set_paragraph_text_preserving_footnotes(doc.paragraphs[87], full_text="En consecuencia, la Comisión considera que corresponde declarar improcedente la denuncia interpuesta, en la medida que las conductas cuestionadas resultan ser materia de competencia exclusiva de Susalud.")
    
    # 3. Parte Resolutiva con tipografía calibrada (ordinal en negrita, cuerpo regular)
    primero_cuerpo = datos.get("primero_cuerpo", "")
    p93 = doc.paragraphs[93]
    if len(p93.runs) >= 2:
        p93.runs[0].text = "PRIMERO: "
        p93.runs[0].bold = True
        set_paragraph_text_preserving_footnotes(
            p93,
            new_text_before_fn=f"PRIMERO: {primero_cuerpo}",
            new_text_after_fn=", previa solicitud a la Unidad de Finanzas y Contabilidad del Indecopi."
        )
        # Asegurar que después del ordinal el texto no sea negrita
        for r in p93.runs[1:]:
            if 'footnoteReference' not in r._r.xml:
                r.bold = False
                
    segundo_p = doc.paragraphs[95]
    if len(segundo_p.runs) >= 2:
        segundo_p.runs[0].text = "SEGUNDO:"
        segundo_p.runs[0].bold = True
        segundo_p.runs[1].text = " ordenar a la Secretaría Técnica de la Comisión de Protección al Consumidor N° 1 que remita el original de todo lo actuado en el presente procedimiento a la Superintendencia Nacional de Salud, a efectos de que adopte las medidas correspondientes en el ámbito de su competencia."
        segundo_p.runs[1].bold = False
        for r in segundo_p.runs[2:]:
            r.text = ""
            
    tercero_p = doc.paragraphs[97]
    if len(tercero_p.runs) >= 8:
        tercero_p.runs[0].text = "TERCERO: "
        tercero_p.runs[0].bold = True
        tercero_p.runs[1].text = "informar "
        tercero_p.runs[1].bold = False
        tercero_p.runs[2].text = datos.get("tercero_destinatario_prefijo", "al señor ")
        tercero_p.runs[2].bold = False
        tercero_p.runs[3].text = ""
        tercero_p.runs[4].text = datos.get("tercero_destinatario_nombre", denunciante)
        tercero_p.runs[4].bold = False
        tercero_p.runs[5].text = ""
        tercero_p.runs[6].text = ""
        tercero_p.runs[7].text = " que la presente resolución tiene vigencia desde el día de su notificación y no agota la vía administrativa. En tal sentido, de conformidad con lo dispuesto por el artículo 38° del Decreto Legislativo N° 807, el único recurso impugnativo que puede interponerse contra lo dispuesto por la Comisión de Protección al Consumidor N° 1 es el de apelación"
        tercero_p.runs[7].bold = False
        
    # Firmas del Colegiado
    set_paragraph_text_preserving_footnotes(
        doc.paragraphs[98],
        full_text="Con la intervención de los señores Comisionados: Mónica Tatiana Siverio Puycan, María de Fátima Ponce Regalado, Ernesto Alonso Calderón Burneo y Aldrin Capcha Coronado."
    )
    set_paragraph_text_preserving_footnotes(
        doc.paragraphs[99],
        full_text="MÓNICA TATIANA SIVERIO PUYCAN\nPresidenta"
    )
    
    doc.save(ruta_salida)
    
    # 4. Actualizar Expediente en header1.xml
    temp_zip = Path(ruta_salida.with_suffix(".tmp.zip"))
    with ZipFile(ruta_salida, "r") as zin:
        with ZipFile(temp_zip, "w") as zout:
            for item in zin.infolist():
                if item.filename == "word/header1.xml":
                    hdr = zin.read(item.filename).decode("utf-8")
                    hdr = hdr.replace("2685-2025/CC1", expediente)
                    zout.writestr(item, hdr.encode("utf-8"))
                else:
                    zout.writestr(item, zin.read(item.filename))
    shutil.move(temp_zip, ruta_salida)
    return ruta_salida


def construir_resolucion_improcedencia(
    datos: Dict[str, Any],
    ruta_salida: Path,
    ruta_plantilla: Path | None = None,
) -> Path:
    """
    Función de compatibilidad y adaptador universal para la construcción popperiana.
    Asegura que cualquier diccionario de datos o dossier de caso se adapte con los
    campos requeridos para el ensamblaje en la plantilla maestra de 9 páginas.
    """
    denunciante = datos.get("denunciante", "PARTE DENUNCIANTE")
    denunciado = datos.get("denunciado", "PARTE DENUNCIADA")
    
    if "primero_cuerpo" not in datos:
        datos["primero_cuerpo"] = (
            f"declarar improcedente la denuncia interpuesta por {denunciante} en contra de {denunciado}, "
            f"y ordenar la devolución de la tasa cancelada por derecho de tramitación, ascendente a S/ 36,00 "
            f"(treinta y seis con 00/100 Soles)"
        )
        
    if "hechos" not in datos:
        hechos_extraidos = []
        if "hechos_salud" in datos:
            hechos_extraidos.extend(datos["hechos_salud"])
        if not hechos_extraidos:
            hechos_extraidos = [
                f"- {denunciado} no habría brindado una atención oportuna e idónea en sus instalaciones asistenciales de salud.",
                f"- {denunciado} se habría negado injustificadamente a hacer entrega de la historia clínica solicitada.",
                f"- {denunciado} habría aplicado cobros indebidos por conceptos no presupuestados al paciente."
            ]
        datos["hechos"] = hechos_extraidos
        
    if "subsun_normativa" not in datos:
        datos["subsun_normativa"] = (
            "constituye infracción grave o muy grave vulnerar los derechos de los usuarios de los servicios de salud, "
            "así como omitir la entrega de la historia clínica o incumplir las obligaciones normadas por SUSALUD."
        )
        
    if "subsun_concreto" not in datos:
        datos["subsun_concreto"] = (
            f"En el presente caso, de la revisión de los actuados se advierte que los cuestionamientos formulados por la parte "
            f"denunciante inciden de manera directa en la prestación del servicio de salud o cobertura de aseguramiento brindada "
            f"por {denunciado}, materias atribuidas por mandato legal expreso a la competencia exclusiva de Susalud."
        )
        
    return construir_resolucion_improcedencia_popperiana(datos, ruta_salida, ruta_plantilla)

