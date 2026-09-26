"""Motor de Razonamiento y Ensamblaje Jurídico para Resoluciones de Improcedencia a SUSALUD.
Comisión de Protección al Consumidor N° 1 (CC1) - INDECOPI.

Elaborado por: David Chávez
Supervisado por: Loussiana Salazar
Equipo: Seguros
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional

from src.config import ELABORADO_POR, EQUIPO, SUPERVISADO_POR


class TipoEntidad(str, Enum):
    IAFAS = "IAFAS"
    IPRESS = "IPRESS"
    MIXTO = "MIXTO"


class TipoImprocedencia(str, Enum):
    TOTAL = "TOTAL"
    PARCIAL = "PARCIAL"


@dataclass
class CasoImprocedencia:
    expediente: str
    denunciante_nombre: str
    denunciante_alias: str
    denunciado_nombre: str
    denunciado_alias: str
    tipo_entidad: TipoEntidad
    tipo_improcedencia: TipoImprocedencia
    vencimiento: str
    fecha_emision: str
    numero_resolucion: str
    fecha_denuncia: str
    hechos_antecedentes: List[str]
    hechos_cuestionados_resumen: str
    denuncio_previamente_susalud: bool = False
    solicito_medida_cautelar: bool = False
    medidas_correctivas_solicitadas: Optional[str] = None
    subtipo_seguro: Optional[str] = None  # ej. "SOAT", "Enfermedades Graves", "Asistencia Médica"
    nombre_iafas_mixto: Optional[str] = None
    nombre_ipress_mixto: Optional[str] = None


class ImprocedenciaEngine:
    """Ensambla el dossier determinista estructurado para la inyección OpenXML."""

    @classmethod
    def generar_dossier_desde_caso(cls, caso: CasoImprocedencia) -> Dict[str, Any]:
        # 1. Metadatos del encabezado
        metadatos = {
            "elaborado_por": ELABORADO_POR,
            "supervisado_por": SUPERVISADO_POR,
            "equipo": EQUIPO,
            "vencimiento": caso.vencimiento,
            "numero_resolucion": caso.numero_resolucion,
            "expediente": caso.expediente,
            "denunciante_linea": f"{caso.denunciante_nombre.upper()} ({caso.denunciante_alias})",
            "denunciado_linea": f"{caso.denunciado_nombre.upper()} ({caso.denunciado_alias})",
            "materia_lineas": ["IMPROCEDENCIA DE LA DENUNCIA", "DECLINACIÓN DE COMPETENCIA"],
            "actividad": "ACTIVIDADES RELACIONADAS CON LA SALUD HUMANA",
            "fecha_emision": caso.fecha_emision,
        }

        # 2. ANTECEDENTES
        parrafos_antecedentes = [
            f"Mediante escrito del {caso.fecha_denuncia}, {caso.denunciante_alias} denunció a {caso.denunciado_alias} "
            f"por presuntas infracciones a la Ley N° 29571, Código de Protección y Defensa del Consumidor "
            f"(en adelante, el Código), señalando lo siguiente:"
        ]
        parrafos_antecedentes.extend(caso.hechos_antecedentes)

        if caso.denuncio_previamente_susalud:
            parrafos_antecedentes.append(
                f"Interpuso una denuncia ante la Superintendencia Nacional de Salud (en adelante, Susalud) "
                f"debido a la gravedad del caso; sin embargo, ello no genera una duplicidad, en tanto ante "
                f"Indecopi denuncia infracciones al Código, vinculadas a la idoneidad de un trato justo e informado."
            )

        if caso.medidas_correctivas_solicitadas:
            parrafos_antecedentes.append(
                f"{caso.denunciante_alias} solicitó, en calidad de medida correctiva, que {caso.denunciado_alias} "
                f"cumpla con: {caso.medidas_correctivas_solicitadas}. Asimismo, requirió el reembolso de costos "
                f"y costas del presente procedimiento."
            )

        # 3. ANÁLISIS
        subtitulo_analisis = f"Sobre la improcedencia de la denuncia interpuesta por {caso.denunciante_alias}"

        parrafos_analisis = [
            "El artículo 105° del Código establece que el Indecopi es la autoridad con competencia primaria y de alcance nacional para conocer las presuntas infracciones a las disposiciones contenidas en el Código, así como para imponer las sanciones y medidas correctivas establecidas, conforme a la Ley de Organización y Funciones del Indecopi, aprobada por el Decreto Legislativo 1033. Asimismo, en la referida norma se señala que dicha competencia solo puede ser negada cuando ella haya sido asignada o se asigne a favor de otro organismo por norma expresa con rango de ley.",
            "Dicho criterio fue recogido previamente en el precedente de observancia obligatoria aprobado por el Tribunal de Defensa de la Competencia mediante Resolución 0277-1999/TDC-INDECOPI, que señaló lo siguiente:",
            "“Por excepción establecida en norma expresa de rango legal, únicamente pueden entenderse aquellas disposiciones contenidas en las leyes, u otras normas de igual jerarquía, que señalen que una entidad administrativa, distinta a la Comisión de Protección al Consumidor del Indecopi, será competente para sancionar presuntas infracciones (a la Ley de Protección al Consumidor) que puedan cometerse en las relaciones de consumo que se presenten en un sector específico”.",
            f"Al respecto, la Comisión de Protección al Consumidor N° 1 (en adelante, la Comisión) debe verificar si el Indecopi es el órgano competente para pronunciarse sobre el hecho cuestionado por {caso.denunciante_alias} en su denuncia.",
        ]

        # Subsección (i)
        tit_sub1 = "(i) 	De la competencia de la Superintendencia Nacional de Salud (Susalud)"
        parrafos_sub1 = [
            "El Decreto Legislativo 1158, cuerpo normativo orientado al fortalecimiento de Susalud, tiene como objetivo promover, proteger y defender los derechos de quienes accedan a los servicios de salud, garantizando que estos sean de calidad, estableciendo bajo su ámbito de competencia a las Instituciones Administradoras de Fondos de Aseguramiento en Salud (IAFAS) y las Instituciones Prestadoras de Servicios de Salud (IPRESS).",
            "Los artículos 6 y 7 del referido cuerpo normativo precisan que las IAFAS comprenden, entre otras entidades, a las compañías aseguradoras, las Entidades Prestadoras de Servicios de Salud (EPS) y Asociaciones de Fondos Regionales y Provinciales contra Accidentes de Tránsito (AFOCAT), mientras que las IPRESS se encuentran comprendidas por establecimientos de salud, servicios de apoyo médico y servicios complementarios o auxiliares de atención médica.",
            "De la lectura conjunta de los referidos dispositivos legales, se desprende que Susalud es una entidad que tiene como finalidad la protección de los intereses de las personas que accedan a servicios de salud, lográndose dicho objetivo a través de la supervisión de las IAFAS e IPRESS.",
            "A fin de garantizar el cumplimiento de sus funciones y objetivos, Susalud cuenta con potestad sancionadora para reprimir aquellas conductas que afecten: (i) el derecho a la vida, salud e información de los usuarios de servicios de salud y la cobertura para su aseguramiento; y, (ii) los estándares de acceso, calidad, oportunidad y disponibilidad con los que dichas prestaciones serán otorgadas.",
            "Dichas conductas, conforme al artículo 11 del citado dispositivo legal, acarrean la imposición de sanciones que abarcan desde una amonestación escrita hasta la revocación de la autorización de funcionamiento para las IAFAS e IPRESS.",
        ]

        # Infracción específica según IAFAS / IPRESS / MIXTO
        if caso.tipo_entidad == TipoEntidad.IAFAS:
            subtipo = caso.subtipo_seguro if caso.subtipo_seguro else "Salud / SOAT"
            parrafos_sub1.append(
                f"Asimismo, conforme al Anexo I-C del Reglamento de Infracciones y Sanciones de Susalud, "
                f"aprobado por el Decreto Supremo N° 031-2014-SA, dicha entidad se encuentra facultada para "
                f"sancionar, entre otras conductas, el hecho consistente en no brindar cobertura oportuna a los "
                f"afiliados o sus beneficiarios de acuerdo a las condiciones pactadas y la normatividad vigente, "
                f"siendo ello relacionado al Seguro de {subtipo} materia de denuncia."
            )
        elif caso.tipo_entidad == TipoEntidad.IPRESS:
            parrafos_sub1.append(
                "Asimismo, conforme al Anexo I-B del Reglamento de Infracciones y Sanciones de Susalud, "
                "aprobado por el Decreto Supremo N° 031-2014-SA, dicha entidad se encuentra facultada para "
                "sancionar las conductas incurridas por parte de las IPRESS en perjuicio de los usuarios de los servicios de salud."
            )
        else:  # MIXTO
            parrafos_sub1.append(
                "Asimismo, conforme a los Anexos I-C e I-B del Reglamento de Infracciones y Sanciones de Susalud, "
                "aprobado por el Decreto Supremo N° 031-2014-SA, dicha entidad se encuentra facultada para sancionar "
                "concurrentemente las conductas incurridas tanto por parte de las IAFAS (en materia de aseguramiento "
                "y coberturas pactadas) como de las IPRESS (en la prestación del servicio médico asistencial) en perjuicio "
                "de los usuarios de los servicios de salud."
            )

        parrafos_sub1.extend([
            "Adicionalmente a su potestad sancionadora, Susalud se encuentra facultada a ordenar medidas correctivas, a fin de corregir o revertir los efectos que la conducta infractora hubiera ocasionado o evitar que esta se produzca nuevamente.",
            "En efecto, dichas medidas correctivas consistirán, por ejemplo, en la devolución de los cobros indebidos realizados por quienes incurrieron en la conducta infractora, la atención a la solicitud de información requerida por el asegurado, la declaración de inexigibilidad de las cláusulas de sus contratos que resulten abusivas y/o la publicación de avisos rectificatorios o informativos, así como las medidas correctivas que dispone el Código y que resultan aplicables a su ámbito de competencia.",
            "Además, Susalud tiene la potestad de aplicar multas coercitivas en el supuesto que los infractores sancionados sean renuentes al cumplimiento de la sanción impuesta, las medidas correctivas ordenadas y/o en caso incurran nuevamente en la conducta infractora.",
            "Por otro lado, el 13 de agosto de 2015, se publicó el Reglamento del Procedimiento de Transferencia de Funciones del Indecopi a Susalud, aprobado por Decreto Supremo N° 026-2015-SA (en adelante, Reglamento de Transferencia de Funciones), el cual establece que esta última entidad es la autoridad competente para promover, proteger y defender los derechos de las personas al acceso a los servicios de salud, así como para conocer, con competencia primaria y alcance nacional, las presuntas infracciones a las disposiciones relativas a la protección de los derechos de los usuarios en su relación de consumo con la IPRESS y/o IAFAS.",
            "Ahora bien, respecto de la competencia de Susalud y del Indecopi, el artículo 9 del citado Reglamento dispone lo siguiente:",
            "(i) 	Susalud asume competencia sobre todos aquellos actos u omisiones ocurridos a partir de la vigencia de la norma (14 de agosto de 2015), que constituyan presuntas infracciones a las disposiciones relativas a la protección de los derechos de los usuarios en su relación de consumo con las instituciones bajo su ámbito de competencia, así como aquellas previas o derivadas de esta.",
            "(ii) 	Indecopi mantiene competencia sobre todos aquellos actos u omisiones ocurridos antes de la vigencia de la norma (hasta el 13 de agosto de 2015), en las materias señaladas en el párrafo precedente, hasta su conclusión en la vía administrativa, arbitral y/o sede judicial.",
            "Por su parte, el Reglamento para la Atención de Reclamos y Quejas de los Usuarios de las IAFAS, IPRESS y UGIPRESS, aprobado por Decreto Supremo N° 030-2016-SA y publicado el 27 de julio de 2016, establece que Susalud es la autoridad competente para conocer y resolver los procedimientos para la atención de reclamos y quejas de usuarios establecidos por dicha entidad.",
            f"A continuación, se determinará la autoridad competente para conocer la denuncia interpuesta por {caso.denunciante_alias} contra {caso.denunciado_alias}, de ser el caso, imponer las sanciones correspondientes.",
        ])

        # Subsección (ii)
        tit_sub2 = "(ii) 	Aplicación al caso concreto"
        parrafos_sub2 = [
            "El numeral 5.3 del artículo 5 del Reglamento del Procedimiento de Transferencia de Funciones establece que Susalud es la entidad encargada de velar por el cumplimiento del Código, así como sus normas complementarias y conexas en materia de protección de los derechos de los usuarios de los servicios de salud.",
            "De lo expuesto se desprende que Susalud es la entidad competente para supervisar el cumplimiento de las normas que protegen a los consumidores de la falta de idoneidad respecto de las prestaciones de salud, así como el derecho de los consumidores a acceder a información vinculada a dichas prestaciones.",
        ]

        if caso.tipo_entidad in (TipoEntidad.IAFAS, TipoEntidad.MIXTO):
            parrafos_sub2.append(
                "Asimismo, el artículo 8 del Reglamento de Procedimiento de Transferencia de Funciones del Indecopi a SUSALUD, "
                "aprobado por Decreto Supremo N° 026-2015-SA, establece que SUSALUD es competente para supervisar el cumplimiento "
                "de las normas que protegen a los consumidores en las IAFAS - Empresas de Seguros, incluidas las que oferten la "
                "cobertura del SOAT (gastos médicos), ejerciendo su potestad sancionadora de acuerdo a lo establecido en el Decreto Legislativo N° 1158."
            )

        parrafos_sub2.append(
            f"En el presente caso, {caso.denunciante_alias} cuestionó que {caso.denunciado_alias} {caso.hechos_cuestionados_resumen}."
        )

        if caso.tipo_entidad == TipoEntidad.IPRESS:
            parrafos_sub2.append(
                f"Por lo cual, dichas conductas infractoras, al estar vinculadas a servicios de salud, deben ser analizadas por "
                f"Susalud al ser materia de su competencia, toda vez que el artículo 7 del Decreto Legislativo 1158 precisa que "
                f"las IPRESS se encuentran comprendidas por establecimientos de salud, servicios de apoyo médico y servicios "
                f"complementarios o auxiliares de atención médica; con lo cual se desprende que Susalud es la entidad que tiene "
                f"como finalidad la protección de los intereses de las personas que accedan a servicios de salud, lográndose "
                f"dicho objetivo a través de la supervisión de las IPRESS, entre las cuales se encuentra {caso.denunciado_alias}."
            )
        elif caso.tipo_entidad == TipoEntidad.IAFAS:
            parrafos_sub2.append(
                f"Por lo cual, dicha conducta infractora, al estar referida a la cobertura de gastos médicos y prestaciones de salud "
                f"del seguro, debe ser analizada por Susalud al ser materia de su competencia, de conformidad con lo establecido en el "
                f"Decreto Legislativo N° 1158 y el Decreto Supremo N° 026-2015-SA."
            )
        else:  # MIXTO
            parrafos_sub2.append(
                f"Por lo cual, dichas conductas infractoras, al estar vinculadas concurrentemente tanto a la cobertura de aseguramiento "
                f"en salud brindada por {caso.nombre_iafas_mixto or 'la aseguradora'} como a las prestaciones asistenciales médicas "
                f"brindadas por {caso.nombre_ipress_mixto or 'el establecimiento de salud'}, deben ser analizadas por Susalud al ser "
                f"materia de su exclusiva competencia..."
            )

        if caso.denuncio_previamente_susalud:
            parrafos_sub2.append(
                "Ahora bien, la parte denunciante señaló que interpuso una denuncia a Susalud debido a la gravedad del caso; "
                "sin embargo, ello no genera una duplicidad, en tanto ante Indecopi denuncia infracciones al Código."
            )

        parrafos_sub2.append(
            f"En consecuencia, la Comisión considera que corresponde declarar improcedente la denuncia interpuesta por "
            f"{caso.denunciante_alias} contra {caso.denunciado_alias}, en la medida que las conductas cuestionadas por el "
            f"denunciante resultan ser materia de competencia de Susalud."
        )
        parrafos_sub2.append(
            "Adicionalmente, este órgano colegiado estima pertinente remitir a Susalud el original de todo lo actuado en "
            "el presente procedimiento, a efectos de que adopte las medidas correspondientes en el ámbito de su competencia."
        )

        if caso.solicito_medida_cautelar:
            parrafos_sub2.append(
                f"Finalmente, este órgano colegiado considera que no corresponde pronunciarse sobre la solicitud de la medida "
                f"cautelar presentada por {caso.denunciante_alias} en la medida que la presente denuncia fue declarada improcedente."
            )

        # 4. RESUELVE (Fórmula canónica oficial de la CC1)
        art_primero = (
            f"PRIMERO: declarar improcedente la denuncia interpuesta por {caso.denunciante_nombre} contra "
            f"{caso.denunciado_nombre}, por presunta infracción a la Ley N° 29571, Código de Protección y Defensa del Consumidor, "
            f"en la medida que ha quedado acreditado que la conducta cuestionada resulta ser materia de exclusiva competencia de la "
            f"Superintendencia Nacional de Salud. En consecuencia, disponer la devolución al denunciante de la tasa por derecho de "
            f"trámite pagada, previa solicitud a la Unidad de Finanzas y Contabilidad del Indecopi."
        )
        art_segundo = (
            "SEGUNDO: ordenar a la Secretaría Técnica de la Comisión de Protección al Consumidor N° 1 que remita el original de "
            "todo lo actuado en el presente procedimiento a la Superintendencia Nacional de Salud, a efectos de que adopte las "
            "medidas correspondientes en el ámbito de su competencia."
        )
        art_tercero = (
            f"TERCERO: informar al {caso.denunciante_nombre} que la presente resolución tiene vigencia desde el día de su notificación "
            f"y no agota la vía administrativa. En tal sentido, de conformidad con lo dispuesto por el artículo 38° del Decreto Legislativo "
            f"Nº 807, el único recurso impugnativo que puede interponerse contra lo dispuesto por la Comisión de Protección al "
            f"Consumidor N° 1 es el de apelación, el cual debe ser presentado ante dicho órgano colegiado en un plazo no mayor de "
            f"quince (15) días hábiles, contado a partir del día siguiente de su notificación, ello de acuerdo con lo establecido en "
            f"el artículo 212° del Texto Único Ordenado de la Ley N° 27444, Ley del Procedimiento Administrativo General, aprobado por "
            f"Decreto Supremo N° 006-2026-JUS; caso contrario, la resolución quedará consentida."
        )

        articulos_resuelve = [art_primero, art_segundo, art_tercero]

        return {
            "metadatos": metadatos,
            "parrafos_antecedentes": parrafos_antecedentes,
            "subtitulo_analisis": subtitulo_analisis,
            "parrafos_analisis": parrafos_analisis,
            "tit_sub1": tit_sub1,
            "parrafos_sub1": parrafos_sub1,
            "tit_sub2": tit_sub2,
            "parrafos_sub2": parrafos_sub2,
            "articulos_resuelve": articulos_resuelve,
            "comisionados_texto": "Con la intervención de los señores comisionados: miembros integrantes de la Comisión de Protección al Consumidor N° 1.",
        }
