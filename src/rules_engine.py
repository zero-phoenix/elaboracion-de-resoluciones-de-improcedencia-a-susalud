"""Motor de Reglas y Verificación Determinista para Resoluciones de Improcedencia a SUSALUD.
Comisión de Protección al Consumidor N° 1 - INDECOPI.

Elaborado por: David Chávez
Supervisado por: Loussiana Salazar
Equipo: Seguros
"""
from __future__ import annotations

import re
from typing import Any, Dict, List, Tuple


class ReglasImprocedencia:
    """Batería de reglas sustantivas y de consistencia formal."""

    @staticmethod
    def validar_emisor_y_firmas(texto_documento: str) -> List[Tuple[bool, str]]:
        resultados = []
        texto_upper = texto_documento.upper()

        # 1. Órgano competente: Comisión de Protección al Consumidor N° 1
        if "COMISIÓN DE PROTECCIÓN AL CONSUMIDOR" in texto_upper or "COMISION DE PROTECCION AL CONSUMIDOR" in texto_upper:
            resultados.append((True, "OK: Órgano resolutivo identificado como Comisión de Protección al Consumidor N° 1."))
        else:
            resultados.append((False, "ERROR: No se identifica a la Comisión de Protección al Consumidor N° 1."))

        # 2. Control del equipo interno
        if "DAVID CHÁVEZ" in texto_upper or "DAVID CHAVEZ" in texto_upper:
            resultados.append((True, "OK: Autoría consignada correctamente (David Chávez)."))
        else:
            resultados.append((False, "ADVERTENCIA: No se encontró 'David Chávez' en el bloque de elaboración."))

        if "LOUSSIANA SALAZAR" in texto_upper:
            resultados.append((True, "OK: Supervisión consignada correctamente (Loussiana Salazar)."))
        else:
            resultados.append((False, "ADVERTENCIA: No se encontró 'Loussiana Salazar' en el bloque de supervisión."))

        # 3. La Secretaría Técnica solo recibe la orden en el SEGUNDO del resuelve, no decide ni firma
        lineas_finales = "\n".join(texto_documento.splitlines()[-15:])
        if "SECRETARIA TECNICA\n" in lineas_finales.upper() or "SECRETARIO TECNICO\n" in lineas_finales.upper():
            resultados.append((False, "ERROR GRAVE: Firma decisoria erróneamente atribuida a la Secretaría Técnica."))
        else:
            resultados.append((True, "OK: Cero firma resolutiva indebida de la Secretaría Técnica."))

        return resultados

    @staticmethod
    def validar_marco_susalud(texto_documento: str, tipo_entidad: str) -> List[Tuple[bool, str]]:
        resultados = []
        texto_upper = texto_documento.upper()

        # SUSALUD y D. Leg. 1158
        if "SUSALUD" in texto_upper:
            resultados.append((True, "OK: SUSALUD citada en el cuerpo del documento."))
        else:
            resultados.append((False, "ERROR: Falta citar a SUSALUD."))

        if "1158" in texto_documento:
            resultados.append((True, "OK: Decreto Legislativo N° 1158 citado."))
        else:
            resultados.append((False, "ERROR: Falta citar el Decreto Legislativo N° 1158."))

        # D.S. 026-2015-SA (Transferencia)
        if "026-2015-SA" in texto_documento or "REGLAMENTO DE TRANSFERENCIA DE FUNCIONES" in texto_upper:
            resultados.append((True, "OK: Reglamento de Transferencia de Funciones (D.S. N° 026-2015-SA) citado."))
        else:
            resultados.append((False, "ERROR: Falta citar el D.S. N° 026-2015-SA."))

        # Entidad específica
        if tipo_entidad in ("IAFAS", "MIXTO"):
            if "IAFAS" in texto_upper or "ASEGURAMIENTO" in texto_upper:
                resultados.append((True, "OK: Régimen de IAFAS debidamente fundamentado."))
            else:
                resultados.append((False, "ERROR: Falta fundamentar la condición de IAFAS."))

        if tipo_entidad in ("IPRESS", "MIXTO"):
            if "IPRESS" in texto_upper or "PRESTADORAS DE SERVICIOS DE SALUD" in texto_upper:
                resultados.append((True, "OK: Régimen de IPRESS debidamente fundamentado."))
            else:
                resultados.append((False, "ERROR: Falta fundamentar la condición de IPRESS."))

        return resultados

    @staticmethod
    def validar_resuelve(texto_documento: str, tipo_improcedencia: str = "TOTAL") -> List[Tuple[bool, str]]:
        resultados = []
        texto_upper = texto_documento.upper()

        # Artículo PRIMERO
        if "DECLARAR IMPROCEDENTE LA DENUNCIA" in texto_upper and "DEVOLUCIÓN" in texto_upper and "TASA" in texto_upper:
            resultados.append((True, "OK: PRIMERO declara improcedencia y dispone devolución de tasa."))
        else:
            resultados.append((False, "ERROR: El artículo PRIMERO debe declarar improcedente y disponer devolución de tasa."))

        # Artículo SEGUNDO
        if "ORDENAR A LA SECRETARÍA TÉCNICA" in texto_upper and "REMITA EL ORIGINAL" in texto_upper:
            resultados.append((True, "OK: SEGUNDO ordena a la Secretaría Técnica la remisión del original a SUSALUD."))
        else:
            resultados.append((False, "ERROR: El artículo SEGUNDO debe ordenar a la Secretaría Técnica remitir el original a SUSALUD."))

        # Artículo TERCERO
        if "APELACIÓN" in texto_upper and "QUINCE (15) DÍAS HÁBILES" in texto_upper and ("006-2026-JUS" in texto_documento or "27444" in texto_documento):
            resultados.append((True, "OK: TERCERO informa plazo de apelación (15 días hábiles, D.S. 006-2026-JUS)."))
        else:
            resultados.append((False, "ERROR: El artículo TERCERO debe informar sobre la apelación en 15 días hábiles y citar el D.S. N° 006-2026-JUS."))

        return resultados
