"""Generador de Resolución de Improcedencia Compleja (CC1 - Indecopi).
Integra en un solo caso todos los supuestos analizados:
1. IAFAS: Negativa de cobertura de gastos médicos SOAT y póliza de asistencia médica.
2. IPRESS: Cobros indebidos por técnica robótica no presupuestada, no entrega de comprobantes ni historia clínica, y condicionamiento de alta médica a pagaré.
3. EMPLEADOR: Descuentos por planilla de saldo hospitalario -> Improcedencia por falta de relación de consumo laboral (NO devolución de tasa).
4. CUANTÍA: Declinación a favor del OPS 1 respecto a la indemnización por incapacidad temporal (descanso médico SOAT < 3 UIT).
5. DENUNCIA PREVIA A SUSALUD: Desestimación de duplicidad/competencia.
6. MEDIDA CAUTELAR: Improcedencia por accesoriedad.
7. FIRMA COLEGIADA: Comisión de Protección al Consumidor N° 1.
"""
from __future__ import annotations

import re
import shutil
from pathlib import Path
import docx
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt, Inches
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

BASE_DIR = Path(__file__).resolve().parent.parent
PLANTILLA = BASE_DIR / "plantillas_maestras" / "plantilla_base_susalud.docx"
SALIDA_DOCX = BASE_DIR / "generados" / "RESOLUCION_COMPLEJA_CC1_IMPROCEDENCIA_SUSALUD.docx"
SALIDA_DOCX.parent.mkdir(parents=True, exist_ok=True)

FUENTE = "Arial"
TAM_TEXTO = Pt(10)
TAM_TITULO = Pt(10.5)

def add_run(p, text, bold=False, italic=False, size=TAM_TEXTO, superscript=False):
    run = p.add_run(text)
    run.font.name = FUENTE
    run.font.size = size
    run.bold = bold
    run.italic = italic
    rPr = run._element.get_or_add_rPr()
    rFonts = rPr.find(qn("w:rFonts"))
    if rFonts is None:
        rFonts = OxmlElement("w:rFonts")
        rPr.insert(0, rFonts)
    rFonts.set(qn("w:ascii"), FUENTE)
    rFonts.set(qn("w:hAnsi"), FUENTE)
    rFonts.set(qn("w:cs"), FUENTE)
    if superscript:
        vert = OxmlElement("w:vertAlign")
        vert.set(qn("w:val"), "superscript")
        rPr.append(vert)
    return run

def add_text_with_superscripts(p, text, bold=False, italic=False, size=TAM_TEXTO):
    parts = re.split(r"(N°|N\s*°|\b\d+°)", text)
    for part in parts:
        if not part:
            continue
        if part.startswith("N") and "°" in part:
            add_run(p, "N", bold=bold, italic=italic, size=size)
            add_run(p, "°", bold=bold, italic=italic, size=size, superscript=True)
        elif re.match(r"^\d+°$", part):
            num = part[:-1]
            add_run(p, num, bold=bold, italic=italic, size=size)
            add_run(p, "°", bold=bold, italic=italic, size=size, superscript=True)
        else:
            add_run(p, part, bold=bold, italic=italic, size=size)

def nuevo_parrafo(doc, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=0, left_indent=None, hanging_indent=None):
    p = doc.add_paragraph()
    p.alignment = align
    pf = p.paragraph_format
    pf.space_before = Pt(0)
    pf.space_after = Pt(space_after)
    pf.line_spacing = 1.0
    if left_indent:
        pf.left_indent = left_indent
    if hanging_indent:
        pf.first_line_indent = hanging_indent
    return p

def generar_resolucion():
    print(f"Copiando plantilla base desde: {PLANTILLA}")
    shutil.copyfile(PLANTILLA, SALIDA_DOCX)
    
    doc = docx.Document(str(SALIDA_DOCX))
    
    # Vaciar cuerpo manteniendo encabezado institucional
    for p in list(doc.paragraphs):
        p._element.getparent().remove(p._element)
        
    # --- METADATOS INTERNOS ---
    p = nuevo_parrafo(doc)
    add_run(p, "Elaborado por: David Chávez", bold=True)
    p = nuevo_parrafo(doc)
    add_run(p, "Supervisado por: Loussiana Salazar", bold=True)
    p = nuevo_parrafo(doc)
    add_run(p, "Equipo: Seguros", bold=True)
    p = nuevo_parrafo(doc, space_after=6)
    add_run(p, "Vencimiento: 30 de noviembre de 2026", bold=True)
    
    # --- NÚMERO DE RESOLUCIÓN ---
    p = nuevo_parrafo(doc, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=6)
    add_text_with_superscripts(p, "RESOLUCIÓN FINAL N° 0450-2026/CC1", bold=True, size=Pt(11))
    
    # --- IDENTIFICACIÓN DEL EXPEDIENTE ---
    lineas_id = [
        ("DENUNCIANTE\t:\t", "GUILLERMO ALEJANDRO VALDIVIA ROJAS (SEÑOR VALDIVIA)"),
        ("DENUNCIADOS\t:\t", "RÍMAC SEGUROS Y REASEGUROS S.A. (RÍMAC SEGUROS)\n\t\t\tCLÍNICA INTERNACIONAL S.A. (CLÍNICA)\n\t\t\tCOMPAÑÍA MINERA DEL CENTRO S.A.A. (MINERA)"),
        ("MATERIA\t:\t", "IMPROCEDENCIA DE LA DENUNCIA\n\t\t\tDECLINACIÓN DE COMPETENCIA\n\t\t\tRELACIÓN DE CONSUMO"),
        ("ACTIVIDAD\t:\t", "ACTIVIDADES RELACIONADAS CON LA SALUD HUMANA"),
    ]
    for eti, val in lineas_id:
        p = nuevo_parrafo(doc)
        add_run(p, eti, bold=True)
        add_text_with_superscripts(p, val, bold=True)
        
    p = nuevo_parrafo(doc, space_after=6)
    add_run(p, "Lima, 25 de septiembre de 2026", bold=False)
    
    # --- ANTECEDENTES ---
    p = nuevo_parrafo(doc, space_after=3)
    add_run(p, "ANTECEDENTES", bold=True)
    
    p = nuevo_parrafo(doc)
    add_text_with_superscripts(p, "1. Mediante escrito del 14 de mayo de 2025, complementado el 23 de junio de 2025, el señor Valdivia denunció a Rímac Seguros, a la Clínica y a la Minera, por presuntas infracciones a la Ley N° 29571, Código de Protección y Defensa del Consumidor (en adelante, el Código), señalando lo siguiente:")
    
    hechos = [
        "(i) El 14 de marzo de 2025, en circunstancias en que se desempeñaba como supervisor de operaciones de la Minera, sufrió un grave accidente de tránsito en el vehículo asegurado bajo la Póliza de Seguro Obligatorio de Accidentes de Tránsito N° 0594829104 (en adelante, SOAT) emitida por Rímac Seguros, contando adicionalmente con el Plan Colectivo de Asistencia Médica suscrito entre su empleador y la referida aseguradora.",
        "(ii) A consecuencia del siniestro, fue trasladado en estado de emergencia a la Clínica, donde fue intervenido quirúrgicamente mediante técnica laparoscópica robótica de emergencia y permaneció diez (10) días internado en la Unidad de Cuidados Intensivos.",
        "(iii) El 25 de marzo de 2025, la Clínica le remitió una liquidación hospitalaria por la suma total de S/ 48 950,00, la cual contemplaba un cargo no presupuestado ni informado de S/ 9 450,00 por el uso de equipamiento robótico, omitiendo entregarle el comprobante de pago desagregado y copia de su historia clínica, pese a haber sido solicitados reiteradamente.",
        "(iv) Asimismo, el personal administrativo de la Clínica condicionó el otorgamiento de su alta médica a la suscripción forzosa de un pagaré y letra de cambio en blanco por el saldo supuestamente descubierto.",
        "(v) El 2 de abril de 2025, presentó formalmente ante Rímac Seguros la solicitud de activación y cobertura de gastos médicos derivados del accidente al amparo del SOAT; sin embargo, mediante carta del 18 de abril de 2025, la compañía aseguradora denegó la cobertura aduciendo que la Clínica no contaba con acreditación de categoría para intervenciones robóticas de alta complejidad.",
        "(vi) Adicionalmente, el 25 de abril de 2025, solicitó a Rímac Seguros la liquidación y pago de la indemnización por incapacidad temporal por cuarenta (40) días de descanso médico prescritos por el médico tratante (equivalente a S/ 3 850,00); no obstante, la aseguradora no emitió pronunciamiento ni cumplió con efectuar el desembolso.",
        "(vii) Frente a la falta de cobertura de Rímac Seguros, la Clínica trasladó el requerimiento de pago a la Minera, ante lo cual esta última procedió a descontar compulsivamente de sus boletas de remuneración de mayo y junio de 2025 la suma total de S/ 15 200,00 bajo el concepto de 'recupero de atenciones médicas corporativas'.",
        "(viii) Precisó que interpuso una denuncia ante la Superintendencia Nacional de Salud (en adelante, Susalud) debido a la gravedad de los hechos; sin embargo, indicó que ello no genera duplicidad procesal, en tanto ante el Indecopi denuncia infracciones autónomas al Código, referidas a la falta de idoneidad, transgresión al deber de información, tratos comerciales vejatorios y cobros indebidos.",
    ]
    for h in hechos:
        p = nuevo_parrafo(doc, left_indent=Inches(0.2))
        add_text_with_superscripts(p, h)
        
    p = nuevo_parrafo(doc)
    add_text_with_superscripts(p, "2. El señor Valdivia solicitó, en calidad de medida correctiva, que: (i) Rímac Seguros otorgue la cobertura integral de gastos médicos del SOAT; (ii) la Clínica cumpla con devolver el importe no presupuestado de S/ 9 450,00, emita los comprobantes de pago respectivos y entregue copia fedateada de la historia clínica; (iii) se declare la nulidad e inexigibilidad del pagaré suscrito en blanco; (iv) la Minera cese de inmediato los descuentos por planilla y reintegre los S/ 15 200,00 retenidos; y, (v) Rímac Seguros abone la indemnización por incapacidad temporal de S/ 3 850,00. Asimismo, requirió el dictado de una medida cautelar y el reembolso de costas y costos del procedimiento.")
    
    # --- ANÁLISIS ---
    p = nuevo_parrafo(doc, space_after=3)
    add_run(p, "ANÁLISIS", bold=True)
    
    p = nuevo_parrafo(doc, space_after=3)
    add_text_with_superscripts(p, "Sobre la improcedencia de la denuncia respecto de los extremos vinculados a Rímac Seguros y a la Clínica", bold=True)
    
    p = nuevo_parrafo(doc)
    add_text_with_superscripts(p, "3. El artículo 105° del Código establece que el Indecopi es la autoridad con competencia primaria y de alcance nacional para conocer las presuntas infracciones a las disposiciones contenidas en el Código, así como para imponer las sanciones y medidas correctivas establecidas, conforme a la Ley de Organización y Funciones del Indecopi, aprobada por el Decreto Legislativo 1033. Asimismo, en la referida norma se señala que dicha competencia solo puede ser negada cuando ella haya sido asignada o se asigne a favor de otro organismo por norma expresa con rango de ley.")
    
    p = nuevo_parrafo(doc)
    add_text_with_superscripts(p, "4. Dicho criterio fue recogido previamente en el precedente de observancia obligatoria aprobado por el Tribunal de Defensa de la Competencia mediante Resolución 0277-1999/TDC-INDECOPI, que señaló lo siguiente:")
    
    p = nuevo_parrafo(doc, left_indent=Inches(0.4))
    add_run(p, "“Por excepción establecida en norma expresa de rango legal, únicamente pueden entenderse aquellas disposiciones contenidas en las leyes, u otras normas de igual jerarquía, que señalen que una entidad administrativa, distinta a la Comisión de Protección al Consumidor del Indecopi, será competente para sancionar presuntas infracciones (a la Ley de Protección al Consumidor) que puedan cometerse en las relaciones de consumo que se presenten en un sector específico”.", italic=True)
    
    p = nuevo_parrafo(doc)
    add_text_with_superscripts(p, "5. Al respecto, la Comisión de Protección al Consumidor N° 1 (en adelante, la Comisión) debe verificar si el Indecopi es el órgano competente para pronunciarse sobre los hechos cuestionados por el señor Valdivia en su denuncia.")
    
    # Subtítulo (i)
    p = nuevo_parrafo(doc, space_after=2)
    add_run(p, "(i)\tDe la competencia de la Superintendencia Nacional de Salud (Susalud)", bold=True)
    
    p = nuevo_parrafo(doc)
    add_text_with_superscripts(p, "6. El Decreto Legislativo 1158, cuerpo normativo orientado al fortalecimiento de Susalud, tiene como objetivo promover, proteger y defender los derechos de quienes accedan a los servicios de salud, garantizando que estos sean de calidad, estableciendo bajo su ámbito de competencia a las Instituciones Administradoras de Fondos de Aseguramiento en Salud (IAFAS) y las Instituciones Prestadoras de Servicios de Salud (IPRESS).")
    
    p = nuevo_parrafo(doc)
    add_text_with_superscripts(p, "7. Los artículos 6 y 7 del referido cuerpo normativo precisan que las IAFAS comprenden, entre otras entidades, a las compañías aseguradoras, las Entidades Prestadoras de Servicios de Salud (EPS) y Asociaciones de Fondos Regionales y Provinciales contra Accidentes de Tránsito (AFOCAT), mientras que las IPRESS se encuentran comprendidas por establecimientos de salud, servicios de apoyo médico y servicios complementarios o auxiliares de atención médica.")
    
    p = nuevo_parrafo(doc)
    add_text_with_superscripts(p, "8. De la lectura conjunta de los referidos dispositivos legales, se desprende que Susalud es una entidad que tiene como finalidad la protección de los intereses de las personas que accedan a servicios de salud, lográndose dicho objetivo a través de la supervisión de las IAFAS e IPRESS.")
    
    p = nuevo_parrafo(doc)
    add_text_with_superscripts(p, "9. A fin de garantizar el cumplimiento de sus funciones y objetivos, Susalud cuenta con potestad sancionadora para reprimir aquellas conductas que afecten: (i) el derecho a la vida, salud e información de los usuarios de servicios de salud y la cobertura para su aseguramiento; y, (ii) los estándares de acceso, calidad, oportunidad y disponibilidad con los que dichas prestaciones serán otorgadas.")
    
    p = nuevo_parrafo(doc)
    add_text_with_superscripts(p, "10. Dichas conductas, conforme al artículo 11 del citado dispositivo legal, acarrean la imposición de sanciones que abarcan desde una amonestación escrita hasta la revocación de la autorización de funcionamiento para las IAFAS e IPRESS.")
    
    p = nuevo_parrafo(doc)
    add_text_with_superscripts(p, "11. Asimismo, conforme al Anexo I-C del Reglamento de Infracciones y Sanciones de Susalud, aprobado por el Decreto Supremo N° 031-2014-SA, dicha entidad se encuentra facultada para sancionar, entre otras conductas, el hecho consistente en no brindar cobertura oportuna a los afiliados o sus beneficiarios de acuerdo a las condiciones pactadas y la normatividad vigente emitida por la SBS, siendo ello relacionado a la cobertura del SOAT y pólizas de salud materia de denuncia; y, conforme al Anexo I-B del citado reglamento, sancionar las conductas incurridas por parte de las IPRESS en perjuicio de los usuarios de los servicios de salud, tales como la realización de cobros no pactados, deficiencias asistenciales o negativa de entrega de documentación médica.")
    
    p = nuevo_parrafo(doc)
    add_text_with_superscripts(p, "12. Adicionalmente a su potestad sancionadora, Susalud se encuentra facultada a ordenar medidas correctivas, a fin de corregir o revertir los efectos que la conducta infractora hubiera ocasionado o evitar que esta se produzca nuevamente.")
    
    p = nuevo_parrafo(doc)
    add_text_with_superscripts(p, "13. En efecto, dichas medidas correctivas consistirán, por ejemplo, en la devolución de los cobros indebidos realizados por quienes incurrieron en la conducta infractora, la atención a la solicitud de información requerida por el asegurado, la declaración de inexigibilidad de las cláusulas de sus contratos que resulten abusivas y/o la publicación de avisos rectificatorios o informativos, así como las medidas correctivas que dispone el Código y que resultan aplicables a su ámbito de competencia.")
    
    p = nuevo_parrafo(doc)
    add_text_with_superscripts(p, "14. Además, Susalud tiene la potestad de aplicar multas coercitivas en el supuesto que los infractores sancionados sean renuentes al cumplimiento de la sanción impuesta, las medidas correctivas ordenadas y/o en caso incurran nuevamente en la conducta infractora.")
    
    p = nuevo_parrafo(doc)
    add_text_with_superscripts(p, "15. Por otro lado, el 13 de agosto de 2015, se publicó el Reglamento del Procedimiento de Transferencia de Funciones del Indecopi a Susalud, aprobado por Decreto Supremo N° 026-2015-SA (en adelante, Reglamento de Transferencia de Funciones), el cual establece que esta última entidad es la autoridad competente para promover, proteger y defender los derechos de las personas al acceso a los servicios de salud, así como para conocer, con competencia primaria y alcance nacional, las presuntas infracciones a las disposiciones relativas a la protección de los derechos de los usuarios en su relación de consumo con la IPRESS y/o IAFAS.")
    
    p = nuevo_parrafo(doc)
    add_text_with_superscripts(p, "16. Ahora bien, respecto de la competencia de Susalud y del Indecopi, el artículo 9 del citado Reglamento dispone lo siguiente:")
    
    p = nuevo_parrafo(doc, left_indent=Inches(0.2))
    add_text_with_superscripts(p, "(i) Susalud asume competencia sobre todos aquellos actos u omisiones ocurridos a partir de la vigencia de la norma (14 de agosto de 2015), que constituyan presuntas infracciones a las disposiciones relativas a la protección de los derechos de los usuarios en su relación de consumo con las instituciones bajo su ámbito de competencia, así como aquellas previas o derivadas de esta.")
    
    p = nuevo_parrafo(doc, left_indent=Inches(0.2))
    add_text_with_superscripts(p, "(ii) Indecopi mantiene competencia sobre todos aquellos actos u omisiones ocurridos antes de la vigencia de la norma (hasta el 13 de agosto de 2015), en las materias señaladas en el párrafo precedente, hasta su conclusión en la vía administrativa, arbitral y/o sede judicial.")
    
    p = nuevo_parrafo(doc)
    add_text_with_superscripts(p, "17. Por su parte, el Reglamento para la Atención de Reclamos y Quejas de los Usuarios de las IAFAS, IPRESS y UGIPRESS, aprobado por Decreto Supremo N° 030-2016-SA y publicado el 27 de julio de 2016, establece que Susalud es la autoridad competente para conocer y resolver los procedimientos para la atención de reclamos y quejas de usuarios establecidos por dicha entidad.")
    
    p = nuevo_parrafo(doc)
    add_text_with_superscripts(p, "18. A continuación, se determinará la autoridad competente para conocer los hechos denunciados por el señor Valdivia contra Rímac Seguros y la Clínica, de ser el caso, imponer las sanciones correspondientes.")
    
    # Subtítulo (ii)
    p = nuevo_parrafo(doc, space_after=2)
    add_run(p, "(ii)\tAplicación al caso concreto", bold=True)
    
    p = nuevo_parrafo(doc)
    add_text_with_superscripts(p, "19. El numeral 5.3 del artículo 5 del Reglamento del Procedimiento de Transferencia de Funciones establece que Susalud es la entidad encargada de velar por el cumplimiento del Código, así como sus normas complementarias y conexas en materia de protección de los derechos de los usuarios de los servicios de salud.")
    
    p = nuevo_parrafo(doc)
    add_text_with_superscripts(p, "20. De lo expuesto se desprende que Susalud es la entidad competente para supervisar el cumplimiento de las normas que protegen a los consumidores de la falta de idoneidad respecto de las prestaciones de salud, así como el derecho de los consumidores a acceder a información vinculada a dichas prestaciones.")
    
    p = nuevo_parrafo(doc)
    add_text_with_superscripts(p, "21. Asimismo, el artículo 8 del Reglamento de Procedimiento de Transferencia de Funciones del Indecopi a SUSALUD, aprobado por Decreto Supremo N° 026-2015-SA, establece que SUSALUD es competente para supervisar el cumplimiento de las normas que protegen a los consumidores en las IAFAS - Empresas de Seguros, incluidas las que oferten la cobertura del SOAT (gastos médicos), ejerciendo su potestad sancionadora de acuerdo a lo establecido en el Decreto Legislativo N° 1158.")
    
    p = nuevo_parrafo(doc)
    add_text_with_superscripts(p, "22. En el presente caso, el señor Valdivia cuestionó que: (i) Rímac Seguros se habría negado injustificadamente a otorgarle la cobertura del SOAT y póliza médica por los gastos médicos derivados del accidente de tránsito sufrido; (ii) la Clínica habría cobrado indebidamente la suma de S/ 9 450,00 por el uso no informado de técnica robótica en la intervención quirúrgica laparoscópica; (iii) la Clínica se habría negado a entregar comprobantes de pago desagregados y copia de la historia clínica; y, (iv) la Clínica habría condicionado el otorgamiento del alta médica a la suscripción forzosa de un pagaré en blanco.")
    
    p = nuevo_parrafo(doc)
    add_text_with_superscripts(p, "23. Por lo cual, dichas conductas infractoras, al estar directamente vinculadas a la cobertura de aseguramiento en salud (IAFAS) y a la prestación de servicios médicos asistenciales y hospitalarios (IPRESS), deben ser analizadas por Susalud al ser materia de su exclusiva competencia, toda vez que los artículos 6 y 7 del Decreto Legislativo 1158 precisan que tanto las empresas de seguros (IAFAS) como los establecimientos de salud (IPRESS) se encuentran bajo la tutela especializada de Susalud.")
    
    p = nuevo_parrafo(doc)
    add_text_with_superscripts(p, "24. Ahora bien, la parte denunciante señaló que interpuso una denuncia a Susalud debido a la gravedad del caso; sin embargo, ello no genera una duplicidad, en tanto ante Indecopi denuncia infracciones al Código. Al respecto, cabe precisar que el Reglamento de Transferencia de Funciones transfirió expresamente a Susalud la facultad de velar por el cumplimiento de las disposiciones del Código en el ámbito de los servicios de salud y fondos de aseguramiento, por lo que la invocación formal de normas de protección al consumidor no desplaza la competencia material exclusiva conferida por ley a Susalud.")
    
    p = nuevo_parrafo(doc)
    add_text_with_superscripts(p, "25. En consecuencia, la Comisión considera que corresponde declarar improcedente la denuncia interpuesta por el señor Valdivia contra Rímac Seguros y la Clínica en los citados extremos, en la medida que las conductas cuestionadas resultan ser materia de competencia de Susalud.")
    
    p = nuevo_parrafo(doc)
    add_text_with_superscripts(p, "26. Adicionalmente, este órgano colegiado estima pertinente remitir a Susalud una copia certificada de todo lo actuado en el presente procedimiento, a efectos de que adopte las medidas correspondientes en el ámbito de su competencia.")
    
    # Subtítulo Laboral / Empleador
    p = nuevo_parrafo(doc, space_after=3)
    add_text_with_superscripts(p, "Sobre la improcedencia de la denuncia interpuesta por el señor Valdivia contra la Minera por falta de relación de consumo", bold=True)
    
    p = nuevo_parrafo(doc)
    add_text_with_superscripts(p, "27. Respecto a la protección al consumidor, es preciso advertir que el artículo 65° de la Constitución Política del Perú consagra la defensa por el Estado de los intereses de los consumidores. En el caso de una denuncia, se debe evaluar si esta cumple con los presupuestos de procedibilidad establecidos en el Código, verificando si el denunciante califica como consumidor y si existió una relación de consumo.")
    
    p = nuevo_parrafo(doc)
    add_text_with_superscripts(p, "28. Al respecto, el artículo III del Título Preliminar del Código establece que se protege al consumidor que se encuentre directa o indirectamente expuesto o comprendido por una relación de consumo. Asimismo, el numeral 1 del artículo IV del Título Preliminar define la relación de consumo como aquella configurada por la concurrencia de tres componentes: un consumidor o usuario, un proveedor y un producto o servicio materia de una transacción comercial.")
    
    p = nuevo_parrafo(doc)
    add_text_with_superscripts(p, "29. De la revisión de lo actuado, se advierte que la Minera no actuó como proveedora de un producto o servicio contratado por el señor Valdivia, sino que actuó en su calidad de empleadora dentro de una relación de subordinación laboral. Así, el cuestionamiento referido a los descuentos efectuados por planilla de remuneraciones respecto a los gastos médicos derivados del convenio corporativo constituye una controversia de naturaleza estrictamente laboral, mas no una relación de consumo.")
    
    p = nuevo_parrafo(doc)
    add_text_with_superscripts(p, "30. Por tanto, esta Comisión considera que corresponde declarar improcedente, por falta de relación de consumo, la denuncia interpuesta por el señor Valdivia contra la Compañía Minera del Centro S.A.A., por la presunta infracción al Código.")
    
    p = nuevo_parrafo(doc)
    add_text_with_superscripts(p, "31. Finalmente, corresponde señalar a la parte denunciante que en la medida que se realizó la evaluación sustantiva de procedencia de la denuncia contra su empleador, no corresponde la devolución de la tasa por derecho de trámite pagada, en la medida que dicho supuesto no se encuentra contemplado en la Directiva N° 001-2021-COD-INDECOPI.")
    
    # Subtítulo Cuantía OPS
    p = nuevo_parrafo(doc, space_after=3)
    add_text_with_superscripts(p, "Sobre la declinación de la competencia respecto al extremo de incapacidad temporal del SOAT", bold=True)
    
    p = nuevo_parrafo(doc)
    add_text_with_superscripts(p, "32. El artículo 93° del Texto Único Ordenado de la Ley N° 27444, Ley del Procedimiento Administrativo General, establece que cuando el órgano administrativo advierta su incompetencia para la tramitación de un procedimiento, deberá remitir todo lo actuado al órgano competente.")
    
    p = nuevo_parrafo(doc)
    add_text_with_superscripts(p, "33. Conforme a la Resolución N° 027-2013-INDECOPI-COD y al artículo 125° del Código, la Comisión tiene competencia para conocer denuncias en materia de seguros cuya cuantía supere las tres (3) Unidades Impositivas Tributarias (UIT), siendo los Órganos Resolutivos de Procedimientos Sumarísimos (OPS) competentes para tramitar aquellas controversias cuya cuantía no supere las 3 UIT.")
    
    p = nuevo_parrafo(doc)
    add_text_with_superscripts(p, "34. En el presente caso, la pretensión referida al pago de la indemnización por incapacidad temporal del SOAT asciende a S/ 3 850,00, monto que resulta notoriamente inferior a las tres (3) UIT vigentes. En tal virtud, corresponde declinar competencia a favor del Órgano Resolutivo de Procedimientos Sumarísimos N° 1 (OPS 1), a efectos de que asuma conocimiento de dicho extremo conforme a sus atribuciones.")
    
    p = nuevo_parrafo(doc)
    add_text_with_superscripts(p, "35. Finalmente, este órgano colegiado considera que no corresponde pronunciarse sobre la solicitud de medida cautelar formulada por el denunciante, en virtud del principio de accesoriedad, habida cuenta del sentido del pronunciamiento emitido en la presente resolución.")
    
    # --- RESUELVE ---
    p = nuevo_parrafo(doc, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=6)
    add_run(p, "RESUELVE", bold=True, size=Pt(11))
    
    p = nuevo_parrafo(doc)
    add_text_with_superscripts(p, "PRIMERO: declarar improcedente la denuncia interpuesta por el señor Guillermo Alejandro Valdivia Rojas contra Rímac Seguros y Reaseguros S.A. y Clínica Internacional S.A., por presunta infracción a la Ley N° 29571, Código de Protección y Defensa del Consumidor, respecto a los extremos vinculados a la negativa de cobertura de gastos médicos del SOAT y póliza médica, cobros no informados por técnica robótica, falta de entrega de comprobantes desagregados e historia clínica, y condicionamiento del alta hospitalaria, en la medida que ha quedado acreditado que dichas conductas resultan ser materia de exclusiva competencia de la Superintendencia Nacional de Salud.")
    
    p = nuevo_parrafo(doc)
    add_text_with_superscripts(p, "SEGUNDO: declarar improcedente, por falta de relación de consumo, la denuncia interpuesta por el señor Guillermo Alejandro Valdivia Rojas contra la Compañía Minera del Centro S.A.A., respecto a los descuentos por planilla de remuneraciones derivados del programa corporativo de salud, dejando a salvo su derecho para que lo haga valer en la vía laboral correspondiente. En consecuencia, precisar que no corresponde la devolución de la tasa por derecho de trámite pagada.")
    
    p = nuevo_parrafo(doc)
    add_text_with_superscripts(p, "TERCERO: declinar la competencia de la Comisión de Protección al Consumidor N° 1 a favor del Órgano Resolutivo de Procedimientos Sumarísimos N° 1, para conocer la denuncia interpuesta por el señor Guillermo Alejandro Valdivia Rojas contra Rímac Seguros y Reaseguros S.A., respecto del extremo referido al pago de indemnización del SOAT por incapacidad temporal de cuarenta (40) días prescritos por el médico tratante; y, por tanto, remitir copias pertinentes a dicho órgano colegiado para los fines de ley.")
    
    p = nuevo_parrafo(doc)
    add_text_with_superscripts(p, "CUARTO: ordenar a la Secretaría Técnica de la Comisión de Protección al Consumidor N° 1 que remita copia certificada de todo lo actuado a la Superintendencia Nacional de Salud, a efectos de que adopte las medidas correspondientes en el ámbito de su competencia.")
    
    p = nuevo_parrafo(doc)
    add_text_with_superscripts(p, "QUINTO: informar al señor Guillermo Alejandro Valdivia Rojas que la presente resolución tiene vigencia desde el día de su notificación y no agota la vía administrativa. En tal sentido, de conformidad con lo dispuesto por el artículo 38° del Decreto Legislativo N° 807, el único recurso impugnativo que puede interponerse contra lo dispuesto por la Comisión de Protección al Consumidor N° 1 es el de apelación, el cual debe ser presentado ante dicho órgano colegiado en un plazo no mayor de quince (15) días hábiles, contado a partir del día siguiente de su notificación, de conformidad con el artículo 212° del Texto Único Ordenado de la Ley N° 27444, aprobado por Decreto Supremo N° 006-2026-JUS; caso contrario, la resolución quedará consentida.")
    
    # --- INTERVENCIÓN COLEGIADA Y FIRMA ---
    nuevo_parrafo(doc)
    p = nuevo_parrafo(doc)
    add_text_with_superscripts(p, "Con la intervención de los señores Comisionados: Mónica Tatiana Siverio Puycan, María de Fátima Ponce Regalado, Ernesto Alonso Calderón Burneo y Aldrin Capcha Coronado.", bold=True)
    
    nuevo_parrafo(doc)
    nuevo_parrafo(doc)
    p = nuevo_parrafo(doc, align=WD_ALIGN_PARAGRAPH.CENTER)
    add_run(p, "MÓNICA TATIANA SIVERIO PUYCAN\nPresidenta", bold=True)
    
    doc.save(str(SALIDA_DOCX))
    print(f"[OK] Resolucion compleja generada exitosamente en: {SALIDA_DOCX}")

if __name__ == "__main__":
    generar_resolucion()
