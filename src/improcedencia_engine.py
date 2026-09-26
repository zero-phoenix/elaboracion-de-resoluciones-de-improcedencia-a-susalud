"""Motor analítico y de razonamiento jurídico para Resoluciones de Improcedencia a SUSALUD.
Comisión de Protección al Consumidor N° 1 - INDECOPI.

Distingue minuciosamente entre:
- IAFAS (Instituciones Administradoras de Fondos de Aseguramiento en Salud)
- IPRESS (Instituciones Prestadoras de Servicios de Salud)
- Supuestos Mixtos (IAFAS + IPRESS)
- Improcedencia Total vs. Improcedencia Parcial
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List


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
    denunciante: str
    denunciado: str
    tipo_entidad: TipoEntidad
    tipo_improcedencia: TipoImprocedencia
    hechos_salud: List[str]
    hechos_indecopi: List[str] = field(default_factory=list)
    fecha_emision: str = "25 de septiembre de 2026"
    numero_resolucion: str = "RESOLUCIÓN N° 0001-2026/CC1"
    remitir_a_susalud: bool = True


class ImprocedenciaEngine:
    """Generador lógico y sustantivo de argumentos y artículos resolutivos."""

    @staticmethod
    def obtener_citas_normativas(tipo_entidad: TipoEntidad) -> Dict[str, str]:
        """Devuelve el marco legal y reglamentario específico según la condición del denunciado."""
        citas = {
            "lpag": "Texto Único Ordenado de la Ley N° 27444, Ley del Procedimiento Administrativo General (D.S. N° 004-2019-JUS / D.S. N° 006-2026-JUS)",
            "codigo_consumidor": "Ley N° 29571, Código de Protección y Defensa del Consumidor",
            "dleg_1158": "Decreto Legislativo N° 1158, que dispone medidas destinadas al fortalecimiento y cambio de denominación de la Superintendencia Nacional de Aseguramiento en Salud a SUSALUD",
            "ds_030_2016": "Decreto Supremo N° 030-2016-SA, Reglamento para la atención de reclamos y denuncias de usuarios de IAFAS, IPRESS y UGIPRESS",
        }

        if tipo_entidad == TipoEntidad.IAFAS:
            citas["especifica_definicion"] = (
                "numeral 2 del artículo 3° del Decreto Legislativo N° 1158, que define a las IAFAS como aquellas "
                "entidades o empresas públicas, privadas o mixtas, que administran fondos destinados al financiamiento "
                "de prestaciones de salud o que ofrecen cobertura de riesgos de salud a sus afiliados o asegurados"
            )
            citas["especifica_materia"] = (
                "Ley N° 29344 (Ley Marco de Aseguramiento Universal en Salud) y su Reglamento aprobado por Decreto Supremo N° 008-2010-SA, "
                "concerniente a las coberturas de planes de salud, preexistencias, periodos de carencia, copagos, reembolsos "
                "y vigencia de contratos de aseguramiento en salud"
            )
        elif tipo_entidad == TipoEntidad.IPRESS:
            citas["especifica_definicion"] = (
                "numeral 3 del artículo 3° del Decreto Legislativo N° 1158, que define a las IPRESS como aquellos "
                "establecimientos de salud y servicios médicos de apoyo, públicos, privados o mixtos, creados o por crearse, "
                "que realizan atención de salud con fines de prevención, promoción, diagnóstico, tratamiento y/o rehabilitación"
            )
            citas["especifica_materia"] = (
                "Ley N° 26842, Ley General de Salud, respecto a la calidad, idoneidad, oportunidad y seguridad de las "
                "prestaciones asistenciales y actos médicos, acceso a la historia clínica, consentimiento informado "
                "y deberes del personal de salud"
            )
        else:  # MIXTO
            citas["especifica_definicion"] = (
                "numerales 2 y 3 del artículo 3° del Decreto Legislativo N° 1158, comprendiendo en forma concurrente tanto a "
                "las entidades administradoras de planes y coberturas (IAFAS) como a los establecimientos prestadores de servicios "
                "de salud médica y hospitalaria (IPRESS)"
            )
            citas["especifica_materia"] = (
                "Ley N° 29344, Ley N° 26842 y Decreto Supremo N° 030-2016-SA, aplicables concurrentemente a la delimitación de "
                "cobertura aseguradora y a la idoneidad y oportunidad del servicio asistencial médico brindado"
            )

        return citas

    @classmethod
    def construir_dossier_resolucion(cls, caso: CasoImprocedencia) -> Dict[str, Any]:
        """Construye la estructura completa de datos lista para el builder OpenXML."""
        citas = cls.obtener_citas_normativas(caso.tipo_entidad)

        vistos = [
            f"El escrito de denuncia presentado por {caso.denunciante} contra {caso.denunciado}, en el que formula diversos reclamos vinculados a la prestación y/o aseguramiento en salud.",
            f"El informe preliminar de calificación y la documentación que obra en el Expediente N° {caso.expediente}.",
        ]

        # Considerandos organizados por secciones sustantivas
        secciones_considerando = []

        # Sección 1: Cuestión previa sobre la competencia
        sec_competencia = {
            "titulo": "I. COMPETENCIA DE LA COMISIÓN DE PROTECCIÓN AL CONSUMIDOR N° 1 Y DELIMITACIÓN FRENTE A SUSALUD",
            "parrafos": [
                f"1. De conformidad con lo establecido en el {citas['lpag']}, la competencia de los órganos administrativos es de orden público, debiendo ejercerse en el marco estricto de las facultades atribuidas por ley.",
                f"2. Conforme al {citas['dleg_1158']}, la Superintendencia Nacional de Salud (SUSALUD) es el organismo público técnico especializado encargado de promover, proteger y defender los derechos de las personas al acceso a los servicios de salud, así como supervisar y fiscalizar a las Instituciones Administradoras de Fondos de Aseguramiento en Salud (IAFAS) y a las Instituciones Prestadoras de Servicios de Salud (IPRESS).",
                f"3. En tal sentido, en virtud del {citas['especifica_definicion']}, corresponde a SUSALUD conocer, tramitar y sancionar las infracciones vinculadas a {citas['especifica_materia']}.",
            ],
        }
        secciones_considerando.append(sec_competencia)

        # Sección 2: Análisis del caso concreto
        parrafos_analisis = [
            f"4. En el presente caso, de la revisión del escrito de denuncia, se verifica que el denunciante imputa a {caso.denunciado} los siguientes hechos:",
        ]
        for h in caso.hechos_salud:
            parrafos_analisis.append(f"   - {h}")

        parrafos_analisis.append(
            f"5. Al respecto, se aprecia con claridad que los citados extremos versan sobre aspectos inherentes a la competencia exclusiva de SUSALUD, por cuanto atañen directamente a la relación de prestación médica y/o cobertura aseguradora de salud que regula el {citas['ds_030_2016']}."
        )

        if caso.tipo_improcedencia == TipoImprocedencia.PARCIAL:
            parrafos_analisis.append(
                f"6. Sin perjuicio de lo expuesto, se advierte que el denunciante también ha formulado cuestionamientos respecto a hechos tales como: {', '.join(caso.hechos_indecopi)}, los cuales sí resultan materia de competencia de esta Comisión en virtud del {citas['codigo_consumidor']}, por lo que corresponde disponer su tramitación en el extremo procedente."
            )
        else:
            parrafos_analisis.append(
                "6. Toda vez que la totalidad de las pretensiones denunciadas inciden de manera directa e inescindible en materias atribuidas por mandato legal expreso a SUSALUD, corresponde declarar la improcedencia de la denuncia por incompetencia por razón de la materia de esta Comisión."
            )

        sec_analisis = {
            "titulo": "II. ANÁLISIS DEL CASO CONCRETO",
            "parrafos": parrafos_analisis,
        }
        secciones_considerando.append(sec_analisis)

        # Artículos del RESUELVE
        articulos_resuelve = []

        if caso.tipo_improcedencia == TipoImprocedencia.TOTAL:
            articulos_resuelve.append(
                f"PRIMERO.- Declarar IMPROCEDENTE la denuncia administrativa interpuesta por {caso.denunciante} contra {caso.denunciado}, "
                f"por incompetencia por razón de la materia de la Comisión de Protección al Consumidor N° 1, en aplicación de lo dispuesto en el "
                f"Decreto Legislativo N° 1158 y el Texto Único Ordenado de la Ley N° 27444."
            )
            if caso.remitir_a_susalud:
                articulos_resuelve.append(
                    "SEGUNDO.- DISPONER la remisión de los actuados a la Superintendencia Nacional de Salud (SUSALUD) para los fines de su competencia, "
                    "haciendo de conocimiento del administrado para que ejerza los derechos que la ley le confiere ante dicha entidad."
                )
            else:
                articulos_resuelve.append(
                    "SEGUNDO.- DEJAR A SALVO el derecho del denunciante para que, de considerarlo pertinente, acuda ante la Superintendencia Nacional "
                    "de Salud (SUSALUD) a formular su denuncia o reclamo de acuerdo a ley."
                )
            articulos_resuelve.append(
                "TERCERO.- DISPONER el ARCHIVO DEFINITIVO del presente procedimiento administrativo sancionador ante esta Comisión una vez quede firme la presente resolución."
            )
        else:
            articulos_resuelve.append(
                f"PRIMERO.- Declarar IMPROCEDENTE la denuncia administrativa interpuesta por {caso.denunciante} contra {caso.denunciado} "
                f"respecto del extremo referido a: {', '.join(caso.hechos_salud)}, por incompetencia por razón de la materia de esta Comisión, "
                f"al ser competencia exclusiva de la Superintendencia Nacional de Salud (SUSALUD)."
            )
            articulos_resuelve.append(
                f"SEGUNDO.- DISPONER que continúe el trámite de la denuncia administrativa respecto del extremo referido a: "
                f"{', '.join(caso.hechos_indecopi)}, de conformidad con lo establecido en el Código de Protección y Defensa del Consumidor."
            )
            if caso.remitir_a_susalud:
                articulos_resuelve.append(
                    "TERCERO.- REMITIR a la Superintendencia Nacional de Salud (SUSALUD) copia certificada de los actuados correspondientes "
                    "al extremo declarado improcedente, para los fines de ley."
                )

        return {
            "expediente": caso.expediente,
            "denunciante": caso.denunciante,
            "denunciado": caso.denunciado,
            "numero_resolucion": caso.numero_resolucion,
            "fecha_emision": caso.fecha_emision,
            "vistos": vistos,
            "secciones_considerando": secciones_considerando,
            "articulos_resuelve": articulos_resuelve,
            "comisionados_texto": "miembros integrantes de la Comisión de Protección al Consumidor N° 1.",
        }
