"""Generador Popperiano de Resolución Compleja Mixta (IAFAS + IPRESS).
Clona la plantilla maestra 'plantilla_base_susalud.docx' preservando 100% de los
enlaces OpenXML de notas al pie, encabezados limpios sin highlight, tipografía
Arial uniforme y maquetación idéntica a las resoluciones auténticas de la CC1.
"""
from __future__ import annotations

import re
import shutil
from pathlib import Path
from zipfile import ZipFile
import xml.etree.ElementTree as ET

BASE_DIR = Path(__file__).resolve().parent.parent
PLANTILLA = BASE_DIR / "plantillas_maestras" / "plantilla_base_susalud.docx"
OUT_DOCX = BASE_DIR / "generados" / "RESOLUCION_0512-2026_CC1_MIXTA_COMPLEJA.docx"
OUT_PDF = BASE_DIR / "generados" / "RESOLUCION_0512-2026_CC1_MIXTA_COMPLEJA.pdf"
CAPTURA_DIR = BASE_DIR / "generados" / "capturas_mixta"
CAPTURA_DIR.mkdir(parents=True, exist_ok=True)
ARTIFACT_DIR = Path(r"C:\Users\Admin\.gemini\antigravity\brain\18369d91-b2f7-445f-b6d3-baa02401afcd")

def generar_documento_mixto():
    # 1. Copiar plantilla maestra
    shutil.copyfile(PLANTILLA, OUT_DOCX)
    
    # Vamos a operar directamente sobre word/document.xml y word/header1.xml
    # para garantizar preservación perfecta de notas al pie y estilos OpenXML
    with ZipFile(OUT_DOCX, "r") as zin:
        xml_doc = zin.read("word/document.xml").decode("utf-8")
        xml_hdr = zin.read("word/header1.xml").decode("utf-8")
        
    # --- A. Limpieza de Header: Quitar highlight verde y actualizar expediente ---
    # En header1.xml: cambiar '1879-2025/CC1' por '0512-2026/CC1' y remover <w:highlight .../>
    xml_hdr_clean = re.sub(r'<w:highlight\s+w:val="[^"]*"\s*/>', '', xml_hdr)
    xml_hdr_clean = xml_hdr_clean.replace("1879-2025/CC1", "0512-2026/CC1")
    xml_hdr_clean = xml_hdr_clean.replace("3125-2025/CC1", "0512-2026/CC1")
    xml_hdr_clean = xml_hdr_clean.replace("3278-2025/CC1", "0512-2026/CC1")

    # --- B. Modificación precisa de document.xml preservando footnoteReference ---
    # Metadatos
    xml_doc = xml_doc.replace("Luis Gamonal", "Loussiana Salazar")
    xml_doc = xml_doc.replace("30 de enero de 2026", "28 de setiembre de 2026")
    xml_doc = xml_doc.replace("RESOLUCIÓN FINAL N° XXXX-2026/CC1", "RESOLUCIÓN FINAL N° 0512-2026/CC1")
    xml_doc = xml_doc.replace("RESOLUCIÓN FINAL N° ****", "RESOLUCIÓN FINAL N° 0512-2026/CC1")
    
    # Partes en carátula
    xml_doc = xml_doc.replace(
        "NELSON RADAMÉS DURAN CASTILLO (SEÑOR DURAN)",
        "MARCO ANTONIO REYES SALVATIERRA (SEÑOR REYES)"
    )
    xml_doc = xml_doc.replace(
        "CLÍNICAS MAISON DE SANTÉ SOCIEDAD ANONIMA (CLÍNICA)",
        "PACÍFICO COMPAÑÍA DE SEGUROS Y REASEGUROS S.A. (PACÍFICO SEGUROS)\n\t\t\tCLÍNICA SAN FELIPE S.A. (CLÍNICA)"
    )
    xml_doc = xml_doc.replace("xx de junio de 2026", "25 de setiembre de 2026")
    xml_doc = xml_doc.replace("xx de setiembre de 2026", "25 de setiembre de 2026")

    # Reemplazo de antecedentes fácticos
    # 1. Párrafo inicial
    xml_doc = xml_doc.replace(
        "18 de julio de 2025, el señor Duran denunció a la Clínica",
        "14 de mayo de 2025, el señor Reyes denunció a Pacífico Seguros y a la Clínica"
    )
    xml_doc = xml_doc.replace(
        "18 de marzo de 2024, adquirió el Seguro Obligatorio de Accidentes de Tránsito – Certificado N° 2872275100000000000 (en adelante, “SOAT”), emitido por la Positiva Seguros y Reaseguros S.A.A. vinculado al vehículo con Placa de Rodaje N° 8628-AC.",
        "10 de enero de 2025, el vehículo de placa de rodaje N° B8K-412 en el que se transportaba contaba con el Seguro Obligatorio de Accidentes de Tránsito – Póliza N° 0588291044 emitido por Pacífico Seguros (en adelante, SOAT)."
    )
    xml_doc = xml_doc.replace(
        "El 18 de marzo de 2024, sufrió un accidente de tránsito y acudió a la Clínica, operada bajo el",
        "El 15 de marzo de 2025, sufrió un accidente de tránsito y fue ingresado en estado de emergencia a la Clínica, donde fue intervenido quirúrgicamente mediante osteosíntesis traumatológica compleja y permaneció cinco (5) días internado. La Clínica facturó un importe total de S/ 38 450,00, incluyendo un cobro no presupuestado de S/ 6 800,00 por material médico no catalogado, negándose a entregarle copia de su historia clínica y condicionando el alta al pago en garantía."
    )
    xml_doc = xml_doc.replace(
        "El señor Alejos solicitó, en calidad de medida correctiva, que la Clínica cumpla con: (i) restituir el servicio médico bajo una cobertura de un seguro adecuado para la rehabilitación de las secuelas ocasionadas a consecuencia de los actos irregulares que lesionaron la lex artis médica, a los fines de que sea reparado el daño causado y rehabilitación necesaria; (ii) otorgar una compensación económica, por el daño físico y emocional causado; (iii) realizar el cese inmediato de la operatividad de Maison de Santé bajo cualquier denominación. Asimismo, requirió el reembolso de costos y costas del presente procedimiento.",
        "El señor Reyes solicitó, en calidad de medida correctiva, que: (i) Pacífico Seguros cumpla con otorgar la cobertura integral de gastos médicos del SOAT; (ii) la Clínica cumpla con devolver el cobro indebido de S/ 6 800,00 y entregar copia íntegra fedateada de su historia clínica; y, (iii) se declare la nulidad del pagaré suscrito en garantía. Asimismo, requirió el reembolso de costas y costos del presente procedimiento."
    )
    
    # Análisis - Cuestión previa
    xml_doc = xml_doc.replace(
        "denuncia interpuesta por el señor Duran",
        "denuncia interpuesta por el señor Reyes"
    )
    xml_doc = xml_doc.replace(
        "cuestionado por el señor Duran en su denuncia.",
        "cuestionados por el señor Reyes en su denuncia contra Pacífico Seguros y la Clínica."
    )

    # Subsunción armónica de IAFAS + IPRESS en potestad sancionadora
    # Reemplazamos la bifurcación '/// O ///' por la conjunción armónica oficial:
    patron_bifurcacion = r"Asimismo, conforme al Anexo I-C del Reglamento de Infracciones.*?concurridas por parte de las IAFAS en perjuicio de los usuarios de los servicios de salud\."
    texto_armonico = (
        "Asimismo, conforme al Anexo I-C del Reglamento de Infracciones y Sanciones de Susalud, aprobado por el Decreto Supremo N° 031-2014-SA, "
        "dicha entidad se encuentra facultada para sancionar, entre otras conductas, el hecho consistente en no brindar cobertura oportuna a los afiliados "
        "o sus beneficiarios de acuerdo a las condiciones pactadas y la normatividad vigente emitida por la SBS, respecto a las IAFAS; y, conforme al Anexo I-B "
        "del citado cuerpo normativo, sancionar a las IPRESS por realizar cobros no pactados, deficiencias asistenciales o negativa de entrega de documentación médica obligatoria."
    )
    xml_doc = re.sub(patron_bifurcacion, texto_armonico, xml_doc, flags=re.DOTALL)

    # Subsunción al caso concreto
    xml_doc = xml_doc.replace(
        "denuncia interpuesta por el señor Duran contra la Clínica,",
        "denuncia interpuesta por el señor Reyes contra Pacífico Seguros y la Clínica,"
    )
    
    # Detalle de hechos en el caso concreto
    hechos_reemplazo = (
        "En el presente caso, el señor Reyes cuestionó que: (i) Pacífico Seguros se habría negado injustificadamente a otorgar la cobertura de gastos médicos "
        "derivada del accidente de tránsito cubierto por el SOAT; (ii) la Clínica habría realizado un cobro en exceso no presupuestado ascendente a S/ 6 800,00 "
        "por concepto de material médico durante la intervención quirúrgica; y, (iii) la Clínica se habría negado a hacer entrega de la copia de su historia clínica, "
        "condicionando el alta médica a la suscripción de un título valor en garantía."
    )
    xml_doc = re.sub(r"En el presente caso, el señor Duran cuestionó que la Clínica.*?la atención de su madre\.", hechos_reemplazo, xml_doc, flags=re.DOTALL)
    
    # Conclusión caso concreto
    xml_doc = re.sub(
        r"Por lo cual, dicha\(SSSS\) conducta infractora.*?entre las cuales se encuentra la Clínica\.",
        "Por lo cual, dichas conductas infractoras, al estar directamente vinculadas a la cobertura del aseguramiento en salud (IAFAS) y a la prestación de servicios médicos asistenciales (IPRESS), deben ser analizadas por Susalud al ser materia de su competencia exclusiva, toda vez que los artículos 6 y 7 del Decreto Legislativo 1158 precisan que tanto las compañías de seguros como los establecimientos de salud se encuentran bajo su ámbito de supervisión.",
        xml_doc,
        flags=re.DOTALL
    )
    
    # Resuelve
    xml_doc = xml_doc.replace(
        "señor Nelson Radamés Duran Castillo contra Clínicas Maison de Santé Sociedad Anónima",
        "señor Marco Antonio Reyes Salvatierra contra Pacífico Compañía de Seguros y Reaseguros S.A. y Clínica San Felipe S.A."
    )
    xml_doc = xml_doc.replace(
        "informar al señor Nelson Radamés Duran Castillo",
        "informar al señor Marco Antonio Reyes Salvatierra"
    )

    # Grabar de vuelta en el ZIP
    import tempfile
    temp_zip = Path(tempfile.mktemp(suffix=".docx"))
    
    with ZipFile(OUT_DOCX, "r") as zin:
        with ZipFile(temp_zip, "w") as zout:
            for item in zin.infolist():
                if item.filename == "word/document.xml":
                    zout.writestr(item, xml_doc.encode("utf-8"))
                elif item.filename == "word/header1.xml":
                    zout.writestr(item, xml_hdr_clean.encode("utf-8"))
                else:
                    zout.writestr(item, zin.read(item.filename))
                    
    shutil.move(temp_zip, OUT_DOCX)
    print(f"Documento DOCX generado con éxito en: {OUT_DOCX}")

if __name__ == "__main__":
    generar_documento_mixto()
