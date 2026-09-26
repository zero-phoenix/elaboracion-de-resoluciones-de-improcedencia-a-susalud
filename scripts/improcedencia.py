"""CLI Unificado para el Sistema de Resoluciones de Improcedencia a SUSALUD.
Comisión de Protección al Consumidor N° 1 - INDECOPI.

Uso:
  python scripts/improcedencia.py construir-muestra
  python scripts/improcedencia.py verificar <archivo.docx>
  python scripts/improcedencia.py guardia <archivo.docx>
  python scripts/improcedencia.py entregar <archivo.docx>
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Añadir raíz al sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.builder import construir_resolucion_improcedencia
from src.config import GENERADOS_DIR, PLANTILLAS_DIR
from src.improcedencia_engine import (
    CasoImprocedencia,
    ImprocedenciaEngine,
    TipoEntidad,
    TipoImprocedencia,
)
from scripts.guardia_improcedencia import auditar_documento
from scripts.verificar_improcedencia import ejecutar_verificacion_popperiana


def cmd_construir_muestra(args):
    """Genera una muestra demostrativa de improcedencia a SUSALUD."""
    caso = CasoImprocedencia(
        expediente="0150-2026/CC1",
        denunciante="JUAN PÉREZ GARCÍA",
        denunciado="CLÍNICA SAN PABLO S.A.C.",
        tipo_entidad=TipoEntidad.IPRESS,
        tipo_improcedencia=TipoImprocedencia.TOTAL,
        hechos_salud=[
            "Presunta negligencia médica en la intervención quirúrgica de apendicectomía realizada el 12 de enero de 2026.",
            "Demora injustificada en la atención en el área de emergencia.",
            "Falta de entrega oportuna de la copia de la historia clínica solicitada por el paciente.",
        ],
        numero_resolucion="RESOLUCIÓN N° 0150-2026/CC1",
    )

    dossier = ImprocedenciaEngine.construir_dossier_resolucion(caso)
    ruta_salida = GENERADOS_DIR / "RESOLUCION_0150-2026_CC1_IMPROCEDENCIA_SUSALUD.docx"

    print(f"Generando resolución de muestra en: {ruta_salida}")
    # Priorizar la plantilla maestra limpia de 9 páginas verificada popperianamente
    plantilla = None
    plantilla_limpia = PLANTILLAS_DIR / "plantilla_maestra_clean_9paginas.docx"
    if plantilla_limpia.exists():
        plantilla = plantilla_limpia
    else:
        plantillas_locales = list(PLANTILLAS_DIR.glob("*.docx"))
        if plantillas_locales:
            plantilla = plantillas_locales[0]
        else:
            # Buscar en repo anterior
            otras = list(Path("c:/Users/Admin/Documents/antigravity/zealous-kepler").glob("**/*.docx"))
            if otras:
                plantilla = otras[0]

    construir_resolucion_improcedencia(dossier, ruta_salida, plantilla)
    print(f"✅ Documento generado exitosamente.")


def cmd_verificar(args):
    ruta = Path(args.archivo)
    ejecutar_verificacion_popperiana(ruta, args.entidad, args.modalidad)


def cmd_guardia(args):
    ruta = Path(args.archivo)
    fugas = auditar_documento(ruta)
    if fugas:
        print(f"❌ FALLO DLP: Se encontraron {len(fugas)} fugas.")
        sys.exit(1)
    else:
        print("✅ GUARDIA DLP APROBADA: Documento limpio.")


def cmd_entregar(args):
    ruta = Path(args.archivo)
    print(f"🚀 INICIANDO CERTIFICACIÓN DE ENTREGA: {ruta.name}")

    # 1. Guardia DLP
    fugas = auditar_documento(ruta)
    if fugas:
        print("❌ Certificación abortada: Fallo en guardia DLP.")
        sys.exit(1)

    # 2. Verificación Popperiana
    ok = ejecutar_verificacion_popperiana(ruta, args.entidad, args.modalidad)
    if not ok:
        print("❌ Certificación abortada: No superó la batería popperiana.")
        sys.exit(1)

    print("\n🏆 CERTIFICACIÓN TRIPLE BARRERA SUPERADA: Documento listo para el Colegiado de la CC1.")


def main():
    parser = argparse.ArgumentParser(description="CLI de Resoluciones de Improcedencia a SUSALUD")
    subparsers = parser.add_subparsers(dest="comando", required=True)

    # Subcomando muestra
    subparsers.add_parser("construir-muestra", help="Genera una resolución de muestra")

    # Subcomando verificar
    parser_ver = subparsers.add_parser("verificar", help="Verifica un archivo .docx con la batería popperiana")
    parser_ver.add_argument("archivo", help="Ruta al archivo .docx")
    parser_ver.add_argument("--entidad", default="IPRESS", choices=["IAFAS", "IPRESS", "MIXTO"])
    parser_ver.add_argument("--modalidad", default="TOTAL", choices=["TOTAL", "PARCIAL"])

    # Subcomando guardia
    parser_gua = subparsers.add_parser("guardia", help="Verifica fuga de placeholders con Guardia DLP")
    parser_gua.add_argument("archivo", help="Ruta al archivo .docx")

    # Subcomando entregar
    parser_ent = subparsers.add_parser("entregar", help="Certifica el documento con la triple barrera")
    parser_ent.add_argument("archivo", help="Ruta al archivo .docx")
    parser_ent.add_argument("--entidad", default="IPRESS", choices=["IAFAS", "IPRESS", "MIXTO"])
    parser_ent.add_argument("--modalidad", default="TOTAL", choices=["TOTAL", "PARCIAL"])

    args = parser.parse_args()

    if args.comando == "construir-muestra":
        cmd_construir_muestra(args)
    elif args.comando == "verificar":
        cmd_verificar(args)
    elif args.comando == "guardia":
        cmd_guardia(args)
    elif args.comando == "entregar":
        cmd_entregar(args)


if __name__ == "__main__":
    main()
