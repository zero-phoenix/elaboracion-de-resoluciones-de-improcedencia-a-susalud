from pathlib import Path
from zipfile import ZipFile
import shutil
import re

SRC_DOCX = Path(r"C:\Users\Admin\Desktop\impros susalud\MODELOS IMPROS SUSALUD CON FUNDAMENTO MEJORADO\2685-2025 RXX IMPRO SUSALUD okOK .docx")
BASE_DIR = Path(r"c:\Users\Admin\Documents\antigravity\zealous-kepler\elaboracion-de-resoluciones-de-improcedencia-a-susalud")
OUT_DOCX = BASE_DIR / "generados" / "RESOLUCION_0512-2026_CC1_MIXTA_COMPLEJA.docx"
OUT_PDF = BASE_DIR / "generados" / "RESOLUCION_0512-2026_CC1_MIXTA_COMPLEJA.pdf"
CAPTURA_DIR = BASE_DIR / "generados" / "capturas_mixta"
CAPTURA_DIR.mkdir(parents=True, exist_ok=True)
ARTIFACT_DIR = Path(r"C:\Users\Admin\.gemini\antigravity\brain\18369d91-b2f7-445f-b6d3-baa02401afcd")

def build_resolution():
    shutil.copyfile(SRC_DOCX, OUT_DOCX)
    
    with ZipFile(OUT_DOCX, "r") as zin:
        xml_doc = zin.read("word/document.xml").decode("utf-8")
        xml_hdr = zin.read("word/header1.xml").decode("utf-8")
        xml_fn = zin.read("word/footnotes.xml").decode("utf-8")
        namelist = zin.namelist()

    # 1. Header: Actualizar expediente a 0512-2026/CC1
    xml_hdr_clean = xml_hdr.replace("2685-2025/CC1", "0512-2026/CC1")
    
    # 2. Document.xml: Reemplazo coherente y limpio
    # Datos de control
    xml_doc = xml_doc.replace("Elaborado por: David Chávez", "Elaborado por: David Chávez\nSupervisado por: Loussiana Salazar\nEquipo: Seguros y Salud")
    xml_doc = xml_doc.replace("Supervisado por: Luis Gamonal", "")
    xml_doc = xml_doc.replace("17/04/2026", "28/10/2026")
    
    # Quitar cualquier highlight residual
    xml_doc = re.sub(r'<w:highlight\s+w:val="[^"]*"\s*/>', '', xml_doc)
    
    # Reemplazo exacto del título de la resolución
    xml_doc = re.sub(
        r'<w:p[^>]*>.*?RESOLUCI.*?XXXX-202.*?<\/w:p>',
        '<w:p w14:paraId="075AEEBF" w14:textId="675B3629" w:rsidR="0067638B" w:rsidRPr="006B087A" w:rsidRDefault="0067638B" w:rsidP="007C6C37"><w:pPr><w:tabs><w:tab w:val="left" w:pos="2127"/><w:tab w:val="left" w:pos="2694"/></w:tabs><w:spacing w:after="0" w:line="240" w:lineRule="auto"/><w:ind w:right="49"/><w:jc w:val="center"/><w:outlineLvl w:val="0"/><w:rPr><w:rFonts w:ascii="Arial" w:eastAsia="Calibri" w:hAnsi="Arial" w:cs="Arial"/><w:b/><w:color w:val="000000"/><w:kern w:val="0"/><w:sz w:val="32"/><w:szCs w:val="32"/><w:lang w:eastAsia="es-PE"/></w:rPr></w:pPr><w:r><w:rPr><w:rFonts w:ascii="Arial" w:eastAsia="Calibri" w:hAnsi="Arial" w:cs="Arial"/><w:b/><w:color w:val="000000"/><w:kern w:val="0"/><w:sz w:val="32"/><w:szCs w:val="32"/><w:lang w:eastAsia="es-PE"/></w:rPr><w:t>RESOLUCIÓN FINAL N° 0512-2026/CC1</w:t></w:r></w:p>',
        xml_doc,
        flags=re.DOTALL
    )
    xml_doc = xml_doc.replace("T EODORA GUADALUPE CHALLCO ZUÑIGA   (SEÑOR A   CHALLCO )", "MARCO ANTONIO REYES SALVATIERRA (SEÑOR REYES)")
    xml_doc = xml_doc.replace(
        "MAPFRE PERÚ COMPAÑIA DE SEGUROS Y REASEGUROS S.A. (MAPFRE)",
        "PACÍFICO COMPAÑÍA DE SEGUROS Y REASEGUROS S.A. (PACÍFICO SEGUROS)\n\t\t\tCLÍNICA SAN FELIPE S.A. (CLÍNICA)"
    )
    xml_doc = xml_doc.replace("MAPFRE PERÚ COMPAÑIA DE SEGUROS Y REASEGUROS S.A.  ( MAPFRE )",
        "PACÍFICO COMPAÑÍA DE SEGUROS Y REASEGUROS S.A. (PACÍFICO SEGUROS)\n\t\t\tCLÍNICA SAN FELIPE S.A. (CLÍNICA)"
    )
    xml_doc = xml_doc.replace("xx de diciembre de 2025", "25 de setiembre de 2026")

    # Antecedentes fácticos
    xml_doc = xml_doc.replace(
        "Mediante escrito del 21 de octubre de 2025, subsanado mediante escrito del 27 de noviembre de 2025, la señora Challco denunció a Mapfre por presuntas infracciones a la Ley N° 29571, Código de Protección y Defensa del Consumidor",
        "Mediante escrito del 14 de mayo de 2026, subsanado mediante escrito del 10 de junio de 2026, el señor Reyes denunció a Pacífico Seguros y a la Clínica por presuntas infracciones a la Ley N° 29571, Código de Protección y Defensa del Consumidor"
    )
    
    # Sustitución de los hechos numerados del accidente y la clínica
    xml_doc = xml_doc.replace(
        "El 29 de septiembre de 2023, se trasladaba como pasajera en el vehículo ómnibus con Placa de Rodaje N° BS0291, el cual contaba con un Seguro Obligatorio de Accidentes de Tránsito (en adelante, SOAT) emitido por Mapfre, cuando, a raíz de una maniobra del conductor, se produjo un accidente de tránsito que le ocasionó una lesión en la columna dorsal, siendo atendida de emergencia en el hospital de Sicuani, provincia de Canchis, departamento de Cusco.",
        "El 15 de marzo de 2026, el vehículo de placa de rodaje N° B8K-412 en el que se transportaba sufrió un accidente de tránsito de magnitud, contando dicha unidad con el Seguro Obligatorio de Accidentes de Tránsito – Póliza N° 0588291044 emitido por Pacífico Seguros (en adelante, SOAT)."
    )
    
    xml_doc = xml_doc.replace(
        "Posteriormente, continuó presentando dolor en la columna dorsal, razón por la cual acudió al Hospital Daniel Alcides Carrión, donde se le practicaron exámenes, determinándose la existencia de una lesión dorsal que requería una intervención quirúrgica con colocación de una prótesis y posterior rehabilitación.",
        "A consecuencia del despiste, fue ingresado en estado de emergencia a la Clínica, donde requirió intervención quirúrgica de urgencia mediante osteosíntesis traumatológica de tibia y peroné, permaneciendo hospitalizado durante cinco (5) días calendarios."
    )
    
    xml_doc = xml_doc.replace(
        "Como consecuencia de dicha lesión, presentó limitaciones para su movilidad y requirió apoyo de terceros para la realización de sus actividades cotidianas.",
        "Pacífico Seguros se negó injustificadamente a otorgar la cobertura integral de gastos médicos del SOAT, alegando mediante comunicación denegatoria que la Clínica no formaba parte de su red preferente de atención médica para accidentes vehiculares."
    )
    
    xml_doc = xml_doc.replace(
        "Posteriormente, solicitó a Mapfre la cobertura del SOAT por el concepto de atención médica y hospitalaria, así como la entrega de la póliza, carta de garantía o documento equivalente que permitiera la programación de la intervención quirúrgica recomendada.",
        "Asimismo, la Clínica emitió una preliquidación y liquidación asistencial exigiendo el cobro no pactado de S/ 6 800,00 por concepto de material médico quirúrgico de osteosíntesis no catalogado en el presupuesto inicial informado."
    )
    
    xml_doc = xml_doc.replace(
        "En respuesta, mediante correo electrónico, Mapfre le indicó que debía presentar un informe médico relativo al siniestro ocurrido en 2023, en el que se consignara el tiempo de lesión, antecedentes del siniestro, estado actual de la paciente, tratamiento recibido, plan y pronóstico, lo cual cumplió remitiendo el informe correspondiente.",
        "Adicionalmente, al solicitar el alta y la documentación de su internamiento, la Clínica se negó a entregarle copia íntegra y fedateada de su historia clínica, condicionando su egreso hospitalario a la suscripción forzosa de un pagaré bancario en garantía por el saldo pendiente."
    )
    
    xml_doc = xml_doc.replace(
        "Posteriormente, la compañía aseguradora le solicitó que presentara los documentos originales en las oficinas de Mapfre ubicadas en la Av. Armendáris N° 335-345, distrito de Miraflores, Lima. El 3 de octubre de 2025, presentó en las oficinas de Mapfre, los documentos médicos originales requeridos para la evaluación de la cobertura del SOAT fecha.",
        "Pese a los reiterados requerimientos formales efectuados por el señor Reyes, Pacífico Seguros ratificó su negativa de cobertura y la Clínica mantuvo la retención de su expediente clínico."
    )
    
    xml_doc = xml_doc.replace(
        "Hasta la fecha, no había recibido respuesta sobre la aprobación o denegatoria de la cobertura de atención médica y hospitalaria solicitada, ni se le había otorgado carta de garantía, póliza u otra constancia que permitiera la realización de la intervención quirúrgica y su posterior rehabilitación, ni se le había efectuado desembolso alguno por dicho concepto.",
        "Por tales motivos, interpuso denuncia administrativa ante el Indecopi solicitando medidas correctivas y sanciones para ambos proveedores en el ámbito de la relación de consumo."
    )
    
    # Medida correctiva
    xml_doc = xml_doc.replace(
        "La señora Challco solicitó, en calidad de medida correctiva, que Mapfre cumpla con otorgar la cobertura del Seguro Obligatorio de Accidentes de Tránsito por reembolso de gastos médicos. Asimismo, requirió el reembolso de costos y costas del presente procedimiento.",
        "El señor Reyes solicitó, en calidad de medida correctiva, que: (i) Pacífico Seguros cumpla con otorgar la cobertura integral de gastos médicos del SOAT; (ii) la Clínica cumpla con reintegrar el cobro indebido de S/ 6 800,00 y hacer entrega formal de la copia completa fedateada de la historia clínica; y, (iii) se declare la inexigibilidad del pagaré suscrito bajo coacción. Asimismo, solicitó la imposición de costas y costos."
    )
    
    # Análisis
    xml_doc = xml_doc.replace(
        "Sobre la improcedencia de la denuncia interpuesta por la señora Challco",
        "Sobre la improcedencia de la denuncia interpuesta por el señor Reyes"
    )
    xml_doc = xml_doc.replace(
        "hecho cuestionado por la señora Challco en su denuncia.",
        "hechos cuestionados por el señor Reyes en su denuncia contra Pacífico Seguros y la Clínica."
    )
    xml_doc = xml_doc.replace(
        "denuncia interpuesta por la señora Challco contra Mapfre",
        "denuncia interpuesta por el señor Reyes contra Pacífico Seguros y la Clínica"
    )

    # Subsunción armónica de la potestad sancionadora (IAFAS + IPRESS)
    subsun_iafas_orig = "Asimismo, conforme al Anexo I-C del Reglamento de Infracciones y Sanciones de Susalud, aprobado por el Decreto Supremo N° 031-2014-SA, dicha entidad se encuentra facultada para sancionar, entre otras conductas, el hecho consistente en modificar o contravenir el clausulado mínimo de los contratos o convenios suscritos con una IAFAS."
    subsun_iafas_ipress = (
        "Asimismo, conforme al Anexo I-C del Reglamento de Infracciones y Sanciones de Susalud, aprobado por el Decreto Supremo N° 031-2014-SA, "
        "dicha entidad se encuentra facultada para sancionar el hecho de no brindar cobertura oportuna a los afiliados o beneficiarios según las condiciones "
        "pactadas y la normativa de la SBS, respecto de las IAFAS; y, conforme al Anexo I-B del referido reglamento, sancionar a las IPRESS por realizar cobros no pactados, "
        "negar la entrega de la historia clínica o condicionar la atención médica."
    )
    xml_doc = xml_doc.replace(subsun_iafas_orig, subsun_iafas_ipress)

    # Aplicación al caso concreto
    caso_orig = (
        "En el presente caso, la señora Challco cuestionó que Mapfre no habría atendido su solicitud de cobertura de gastos médicos del Seguro Obligatorio de Accidentes de Tránsito ni le habría otorgado la póliza, carta de garantía o documento equivalente necesario para la programación de la intervención quirúrgica recomendada en la atención de las lesiones sufridas como consecuencia del accidente de tránsito ocurrido el 29 de septiembre de 2023; en ese sentido cuestionó que Mapfre habría brindado un deficiente servicio de prestación de salud en relación a la cobertura de gastos médicos en su calidad de beneficiaria del Seguro Obligatorio de Accidentes de Tránsito."
    )
    caso_mixto = (
        "En el presente caso, el señor Reyes cuestionó que: (i) Pacífico Seguros (IAFAS) no habría otorgado la cobertura de gastos médicos derivada del Seguro Obligatorio de Accidentes de Tránsito (SOAT), desconociendo la cobertura obligatoria de urgencia; (ii) la Clínica (IPRESS) habría exigido un cobro excesivo no presupuestado de S/ 6 800,00 por concepto de material médico durante la intervención traumatológica; y, (iii) la Clínica se habría negado a entregar copia completa fedateada de la historia clínica, condicionando el alta médica a la suscripción de un pagaré. En ese sentido, los cuestionamientos planteados inciden de manera directa tanto en la cobertura del aseguramiento en salud por parte de la aseguradora, como en las prestaciones asistenciales y entrega de documentación médica a cargo del establecimiento de salud."
    )
    xml_doc = xml_doc.replace(caso_orig, caso_mixto)

    xml_doc = xml_doc.replace(
        "denuncia interpuesta por la señora Challco contra Mapfre, en la medida que las conductas cuestionadas por el denunciante resulta ser materia de competencia de Susalud.",
        "denuncia interpuesta por el señor Reyes contra Pacífico Seguros y la Clínica, en la medida que las conductas cuestionadas resultan ser materia de competencia exclusiva de Susalud."
    )

    # RESUELVE
    resuelve_primero_orig = (
        "PRIMERO: declarar improcedente la denuncia interpuesta por la señora Teodora Guadalupe Challco Zuñiga contra Mapfre Perú Compañía de Seguros y Reaseguros S.A., por presunta infracción a la Ley N° 29571, Código de Protección y Defensa del Consumidor, en la medida que ha quedado acreditado que la conducta cuestionada resulta ser materia de exclusiva competencia de la Superintendencia Nacional de Salud. En consecuencia, disponer la devolución a la denunciante de la tasa por derecho de trámite pagada, previa solicitud a la Unidad de Finanzas y Contabilidad del Indecopi."
    )
    resuelve_primero_mixto = (
        "PRIMERO: declarar improcedente la denuncia interpuesta por el señor Marco Antonio Reyes Salvatierra contra Pacífico Compañía de Seguros y Reaseguros S.A. y Clínica San Felipe S.A., por presunta infracción a la Ley N° 29571, Código de Protección y Defensa del Consumidor, en la medida que ha quedado acreditado que las conductas cuestionadas resultan ser materia de exclusiva competencia de la Superintendencia Nacional de Salud. En consecuencia, disponer la devolución a la parte denunciante de la tasa por derecho de trámite pagada, previa solicitud a la Unidad de Finanzas y Contabilidad del Indecopi."
    )
    xml_doc = xml_doc.replace(resuelve_primero_orig, resuelve_primero_mixto)

    xml_doc = xml_doc.replace(
        "informar a la señora Teodora Guadalupe Challco Zuñiga",
        "informar al señor Marco Antonio Reyes Salvatierra"
    )

    # Firmas del Colegiado
    firmas_bloque = (
        "\n\nCon la intervención de los señores Comisionados: Mónica Tatiana Siverio Puycan, "
        "María de Fátima Ponce Regalado, Ernesto Alonso Calderón Burneo y Aldrin Capcha Coronado.\n\n\n\n"
        "MÓNICA TATIANA SIVERIO PUYCAN\nPresidenta\n"
    )
    # Si después del TERCERO no están los comisionados, agregarlos antes del cierre del documento
    if "MÓNICA TATIANA SIVERIO PUYCAN" not in xml_doc:
        xml_doc = xml_doc.replace(
            "caso contrario, la resolución quedará consentida.",
            "caso contrario, la resolución quedará consentida.</w:t></w:r></w:p><w:p><w:pPr><w:jc w:val=\"both\"/><w:rPr><w:rFonts w:ascii=\"Arial\" w:hAnsi=\"Arial\"/><w:sz w:val=\"20\"/></w:rPr></w:pPr><w:r><w:rPr><w:rFonts w:ascii=\"Arial\" w:hAnsi=\"Arial\"/><w:b/><w:sz w:val=\"20\"/></w:rPr><w:t xml:space=\"preserve\">Con la intervención de los señores Comisionados: Mónica Tatiana Siverio Puycan, María de Fátima Ponce Regalado, Ernesto Alonso Calderón Burneo y Aldrin Capcha Coronado.</w:t></w:r></w:p><w:p><w:pPr><w:spacing w:before=\"720\"/><w:jc w:val=\"center\"/><w:rPr><w:rFonts w:ascii=\"Arial\" w:hAnsi=\"Arial\"/><w:b/><w:sz w:val=\"20\"/></w:rPr></w:pPr><w:r><w:rPr><w:rFonts w:ascii=\"Arial\" w:hAnsi=\"Arial\"/><w:b/><w:sz w:val=\"20\"/></w:rPr><w:t>MÓNICA TATIANA SIVERIO PUYCAN</w:t></w:r></w:p><w:p><w:pPr><w:jc w:val=\"center\"/><w:rPr><w:rFonts w:ascii=\"Arial\" w:hAnsi=\"Arial\"/><w:b/><w:sz w:val=\"20\"/></w:rPr></w:pPr><w:r><w:rPr><w:rFonts w:ascii=\"Arial\" w:hAnsi=\"Arial\"/><w:b/><w:sz w:val=\"20\"/></w:rPr><w:t>Presidenta</w:t></w:r>"
        )

    # Guardar en archivo temporal y mover
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
    print(f"Resolución DOCX generada en: {OUT_DOCX}")

if __name__ == "__main__":
    build_resolution()
