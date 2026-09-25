"""Motor de Reglas y Verificación Determinista para Resoluciones de Improcedencia a SUSALUD.
Comisión de Protección al Consumidor N° 1 - INDECOPI.
"""
from __future__ import annotations

import re
from typing import Any, Dict, List, Tuple


class ReglasImprocedencia:
    """Conjunto de reglas sustantivas y formales obligatorias."""

    @staticmethod
    def validar_emisor_y_firmas(texto_documento: str) -> List[Tuple[bool, str]]:
        """Verifica que el documento sea emitido por la Comisión y NO por la Secretaría Técnica."""
        resultados = []

        # 1. Regla de Oro: Cero Secretaría Técnica como firmante o decisor
        patron_st_firma = re.compile(
            r"(SECRETARI[AO]\s+T[EÉ]CNIC[AO]|SECRETARIA\s+TECNICA\s+AD\s+HOC)",
            re.IGNORECASE,
        )
        if patron_st_firma.search(texto_documento):
            resultados.append((
                False,
                "VIOLACIÓN PROCESAL GRAVE: Se detectó mención resolutiva o de firma de la Secretaría Técnica. "
                "Las resoluciones de improcedencia deben ser emitidas y suscritas por los Miembros de la Comisión.",
            ))
        else:
            resultados.append((True, "OK: Cero firma o atribución indebida a Secretaría Técnica."))

        # 2. Presencia de la Comisión de Protección al Consumidor N° 1
        if "COMISIÓN DE PROTECCIÓN AL CONSUMIDOR N° 1" in texto_documento.upper() or "COMISION DE PROTECCION AL CONSUMIDOR N" in texto_documento.upper():
            resultados.append((True, "OK: Órgano resolutivo identificado como Comisión de Protección al Consumidor N° 1."))
        else:
            resultados.append((False, "ERROR: No se identifica a la Comisión de Protección al Consumidor N° 1 como órgano emisor."))

        # 3. Mención a la intervención de los comisionados
        if "COMISIONADOS" in texto_documento.upper():
            resultados.append((True, "OK: Consta la fórmula colegiada de intervención de comisionados."))
        else:
            resultados.append((False, "ERROR: Falta la indicación de intervención de los señores comisionados."))

        return resultados

    @staticmethod
    def validar_marco_susalud(texto_documento: str, tipo_entidad: str) -> List[Tuple[bool, str]]:
        """Valida que se cite la normativa correcta de SUSALUD, IAFAS e IPRESS."""
        resultados = []
        texto_upper = texto_documento.upper()

        # SUSALUD y D. Leg. 1158
        if "SUSALUD" in texto_upper or "SUPERINTENDENCIA NACIONAL DE SALUD" in texto_upper:
            resultados.append((True, "OK: SUSALUD citada adecuadamente."))
        else:
            resultados.append((False, "ERROR: No se menciona a SUSALUD."))

        if "1158" in texto_documento:
            resultados.append((True, "OK: Decreto Legislativo N° 1158 citado."))
        else:
            resultados.append((False, "ERROR: Falta citar el Decreto Legislativo N° 1158."))

        # IAFAS
        if tipo_entidad in ("IAFAS", "MIXTO"):
            if "IAFAS" in texto_upper or "ADMINISTRADORAS DE FONDOS DE ASEGURAMIENTO" in texto_upper:
                resultados.append((True, "OK: Término y marco de IAFAS citado."))
            else:
                resultados.append((False, "ERROR: Se omitió citar la condición y normativa de IAFAS."))

        # IPRESS
        if tipo_entidad in ("IPRESS", "MIXTO"):
            if "IPRESS" in texto_upper or "PRESTADORAS DE SERVICIOS DE SALUD" in texto_upper:
                resultados.append((True, "OK: Término y marco de IPRESS citado."))
            else:
                resultados.append((False, "ERROR: Se omitió citar la condición y normativa de IPRESS."))

        return resultados

    @staticmethod
    def validar_resuelve(texto_documento: str, tipo_improcedencia: str) -> List[Tuple[bool, str]]:
        """Valida coherencia en los artículos del resuelve."""
        resultados = []
        texto_upper = texto_documento.upper()

        if "IMPROCEDENTE" in texto_upper:
            resultados.append((True, "OK: Declaración expresa de IMPROCEDENTE encontrada."))
        else:
            resultados.append((False, "ERROR: Falta declarar IMPROCEDENTE en el fallo."))

        if "INCOMPETENCIA" in texto_upper:
            resultados.append((True, "OK: Incompetencia por razón de la materia expresada."))
        else:
            resultados.append((False, "ERROR: Falta motivar la improcedencia en la incompetencia por razón de la materia."))

        if tipo_improcedencia == "PARCIAL":
            if "CONTINÚE" in texto_upper or "CONTINUE" in texto_upper:
                resultados.append((True, "OK: Disposición de trámite para extremos procedentes en improcedencia parcial."))
            else:
                resultados.append((False, "ERROR: En improcedencia parcial debe disponerse el trámite de los extremos procedentes."))

        return resultados
