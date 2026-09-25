"""CLI Unificado para el Sistema de Resoluciones de Improcedencia a SUSALUD.
Comisión de Protección al Consumidor N° 1 - INDECOPI.

Elaborado por: David Chávez
Supervisado por: Loussiana Salazar
Equipo: Seguros

Uso:
  improcedencia info
  improcedencia normas
  improcedencia verificar <archivo.docx> [--entidad IPRESS|IAFAS|MIXTO]
  improcedencia guardia <archivo.docx>
  improcedencia entregar <archivo.docx>
"""
from __future__ import annotations

import argparse
import sys
import io
from pathlib import Path

# Configurar encoding seguro para consola Windows (cp1252 / UTF-8)
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# Añadir raíz al sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.builder import construir_resolucion_improcedencia_calibrada
from src.config import GENERADOS_DIR, PLANTILLAS_DIR
from scripts.guardia_improcedencia import auditar_documento
from scripts.verificar_improcedencia import ejecutar_verificacion_popperiana


def cmd_info(args):
    print("================================================================================")
    print("🏛️  SISTEMA DE RESOLUCIONES DE IMPROCEDENCIA A SUSALUD (CC1 - INDECOPI)")
    print("================================================================================")
    print("Autor: David Chávez")
    print("Supervisora: Loussiana Salazar")
    print("Equipo: Seguros")
    print("Órgano Resolutivo: Comisión de Protección al Consumidor N° 1 (Órgano Colegiado)")
    print("Regla Fundamental: Cero firma o resolución atribuida a la Secretaría Técnica.")
    print("Normativa Central: Decreto Legislativo N° 1158 | D.S. N° 030-2016-SA | D.S. N° 006-2026-JUS")
    print("================================================================================")


def cmd_normas(args):
    print("\n📚 CATÁLOGO NORMATIVO COMPARATIVO: IAFAS vs. IPRESS vs. MIXTO\n")
    print("1. IAFAS (Aseguradoras, EPS, Prepagadas, AFOCAT, SIS, EsSalud):")
    print("   - Definición legal: Art. 3° num 2 y Art. 6° del Decreto Legislativo N° 1158.")
    print("   - Ley sectorial: Ley N° 29344 (Aseguramiento Universal en Salud) y D.S. N° 008-2010-SA.")
    print("   - Infracciones SUSALUD: Anexo I-B del D.S. N° 031-2014-SA (cobertura inoportuna, pólizas).")
    print("   - Transferencia Indecopi-Susalud: Art. 8° D.S. N° 026-2015-SA (seguros, SOAT gastos médicos).\n")
    print("2. IPRESS (Clínicas, Hospitales, Policlínicos, Laboratorios):")
    print("   - Definición legal: Art. 3° num 3 y Art. 7° del Decreto Legislativo N° 1158.")
    print("   - Ley sectorial: Ley N° 26842 (Ley General de Salud - acto médico, historia clínica).")
    print("   - Infracciones SUSALUD: D.S. N° 031-2014-SA (conductas de IPRESS en perjuicio de usuarios).")
    print("   - Materia: Calidad, oportunidad, seguridad asistencial, idoneidad del acto médico.\n")
    print("3. CASOS MIXTOS (IAFAS + IPRESS):")
    print("   - Concurrencia de cobertura y servicio médico (ej. Clínica + EPS / Aseguradora).")
    print("   - Cita concurrente de Art. 3° num 2 y 3 del D. Leg. N° 1158 y análisis individualizado.\n")


def cmd_verificar(args):
    ruta = Path(args.archivo)
    if not ruta.exists():
        print(f"Error: No existe el archivo {ruta}")
        sys.exit(1)
    ejecutar_verificacion_popperiana(ruta, args.entidad, args.modalidad)


def cmd_guardia(args):
    ruta = Path(args.archivo)
    if not ruta.exists():
        print(f"Error: No existe el archivo {ruta}")
        sys.exit(1)
    fugas = auditar_documento(ruta)
    if fugas:
        print(f"❌ FALLO DLP: Se encontraron {len(fugas)} fugas.")
        sys.exit(1)
    else:
        print("✅ GUARDIA DLP APROBADA: Documento completamente limpio.")


def cmd_entregar(args):
    ruta = Path(args.archivo)
    if not ruta.exists():
        print(f"Error: No existe el archivo {ruta}")
        sys.exit(1)
    print(f"🚀 INICIANDO CERTIFICACIÓN DE ENTREGA: {ruta.name}")

    fugas = auditar_documento(ruta)
    if fugas:
        print("❌ Certificación abortada: Fallo en guardia DLP.")
        sys.exit(1)

    ok = ejecutar_verificacion_popperiana(ruta, args.entidad, args.modalidad)
    if not ok:
        print("❌ Certificación abortada: No superó la batería popperiana.")
        sys.exit(1)

    print("\n🏆 CERTIFICACIÓN TRIPLE BARRERA SUPERADA: Documento listo para la firma del Colegiado de la CC1.")


def main():
    parser = argparse.ArgumentParser(
        prog="improcedencia",
        description="Sistema de Resoluciones de Improcedencia a SUSALUD (CC1 - Indecopi)",
    )
    subparsers = parser.add_subparsers(dest="comando", required=True)

    # Subcomando info
    subparsers.add_parser("info", help="Muestra información institucional y del equipo")

    # Subcomando normas
    subparsers.add_parser("normas", help="Muestra el desglose normativo IAFAS vs IPRESS vs Mixto")

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

    if args.comando == "info":
        cmd_info(args)
    elif args.comando == "normas":
        cmd_normas(args)
    elif args.comando == "verificar":
        cmd_verificar(args)
    elif args.comando == "guardia":
        cmd_guardia(args)
    elif args.comando == "entregar":
        cmd_entregar(args)


if __name__ == "__main__":
    main()
