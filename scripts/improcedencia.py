"""CLI Unificado para el Sistema de Resoluciones de Improcedencia a SUSALUD.
Comisión de Protección al Consumidor N° 1 - INDECOPI.

Elaborado por: David Chávez
Supervisado por: Loussiana Salazar
Equipo: Seguros

Uso:
  python scripts/improcedencia.py simular
  python scripts/improcedencia.py verificar <archivo.docx> [--entidad IAFAS|IPRESS|MIXTO]
  python scripts/improcedencia.py guardia <archivo.docx>
  python scripts/improcedencia.py entregar <archivo.docx> [--entidad IAFAS|IPRESS|MIXTO]
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

# Añadir raíz al sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.builder import construir_resolucion_desde_dossier
from src.config import GENERADOS_DIR, PLANTILLAS_DIR
from src.improcedencia_engine import (
    CasoImprocedencia,
    ImprocedenciaEngine,
    TipoEntidad,
    TipoImprocedencia,
)
from scripts.guardia_improcedencia import auditar_documento
from scripts.verificar_improcedencia import ejecutar_verificacion_popperiana


def docx_a_pdf(ruta_docx: Path, ruta_pdf: Path) -> Path:
    """Convierte un archivo docx a pdf usando Word COM."""
    ps_cmd = f"""
$w = New-Object -ComObject Word.Application
$w.Visible = $false
try {{
    $d = $w.Documents.Open('{ruta_docx.resolve()}')
    $d.SaveAs([ref]'{ruta_pdf.resolve()}', [ref]17)
    $d.Close()
}} finally {{
    $w.Quit()
}}
"""
    subprocess.run(["powershell", "-Command", ps_cmd], check=True)
    return ruta_pdf


def pdf_a_imagenes(ruta_pdf: Path, carpeta_salida: Path) -> list[Path]:
    """Convierte cada página del pdf en una imagen PNG de alta resolución."""
    import fitz  # PyMuPDF

    carpeta_salida.mkdir(parents=True, exist_ok=True)
    doc = fitz.open(str(ruta_pdf))
    imagenes = []

    for i, pagina in enumerate(doc):
        pix = pagina.get_pixmap(dpi=150)
        img_path = carpeta_salida / f"pagina_{i+1:02d}.png"
        pix.save(str(img_path))
        imagenes.append(img_path)

    return imagenes


def cmd_simular(args):
    """Genera una resolución de improcedencia inventada y completa, convirtiéndola a imágenes."""
    print("==================================================")
    print("🚀 GENERANDO SIMULACIÓN DE RESOLUCIÓN DE IMPROCEDENCIA")
    print("==================================================")

    caso = CasoImprocedencia(
        expediente="9999-2026/CC1",
        denunciante_nombre="CARLOS ALBERTO MENDOZA VÁSQUEZ",
        denunciante_alias="SEÑOR MENDOZA",
        denunciado_nombre="CLÍNICA INTERNACIONAL S.A.",
        denunciado_alias="CLÍNICA",
        tipo_entidad=TipoEntidad.IPRESS,
        tipo_improcedencia=TipoImprocedencia.TOTAL,
        vencimiento="30 de octubre de 2026",
        fecha_emision="25 de setiembre de 2026",
        numero_resolucion="RESOLUCIÓN FINAL N° 9999-2026/CC1",
        fecha_denuncia="14 de agosto de 2026",
        hechos_antecedentes=[
            "El 10 de mayo de 2026, el señor Mendoza acudió al área de emergencia de la Clínica manifestando un intenso dolor abdominal y sintomatología febril aguda.",
            "Fue atendido por el médico de guardia, quien le prescribió analgésicos comunes y dispuso su alta médica sin ordenar exámenes ecográficos ni de laboratorio complementarios para descartar un cuadro de apendicitis aguda.",
            "Al persistir e intensificarse el cuadro doloroso en las horas posteriores, tuvo que ser ingresado de urgencia en otra institución prestadora de salud, donde se le diagnosticó apendicitis aguda perforada con peritonitis, debiendo ser sometido a una laparotomía de emergencia.",
            "Posteriormente, solicitó formalmente a la Clínica la entrega íntegra y legible de su historia clínica y el reporte de atención médica de emergencia, sin haber obtenido respuesta oportuna dentro del plazo legal.",
        ],
        hechos_cuestionados_resumen=(
            "no le habría brindado una atención médica diligente y adecuada durante su ingreso por emergencia el 10 de mayo de 2026, "
            "al prescribirle únicamente analgésicos sin practicarle exámenes de descarte para apendicitis aguda, y no le habría cumplido "
            "con entregar la copia completa de su historia clínica y hoja de atención médica"
        ),
        denuncio_previamente_susalud=True,
        solicito_medida_cautelar=True,
        medidas_correctivas_solicitadas=(
            "(i) el reembolso total de los gastos médicos y de hospitalización asumidos para la intervención de emergencia; "
            "(ii) una indemnización económica por el daño físico y emocional generado; y, "
            "(iii) la entrega inmediata de la copia fedateada de la historia clínica"
        ),
    )

    dossier = ImprocedenciaEngine.generar_dossier_desde_caso(caso)
    ruta_docx = GENERADOS_DIR / "RESOLUCION_SIMULADA_9999-2026_CC1_IMPRO_SUSALUD.docx"
    ruta_pdf = GENERADOS_DIR / "RESOLUCION_SIMULADA_9999-2026_CC1_IMPRO_SUSALUD.pdf"
    carpeta_imgs = GENERADOS_DIR / "capturas_simulacion"

    print(f"📄 1. Ensamblando documento Word en: {ruta_docx}")
    construir_resolucion_desde_dossier(dossier, ruta_docx)

    print("🛡️ 2. Verificando Guardia DLP...")
    fugas = auditar_documento(ruta_docx)
    if fugas:
        print(f"❌ Fallo DLP: {fugas}")
        sys.exit(1)
    print("✅ Guardia DLP aprobada.")

    print("🔬 3. Verificando con batería Popperiana...")
    ok = ejecutar_verificacion_popperiana(ruta_docx, caso.tipo_entidad.value, caso.tipo_improcedencia.value)
    if not ok:
        print("❌ Fallo de verificación popperiana.")
        sys.exit(1)

    print(f"🖨️ 4. Convirtiendo a PDF vía Word COM: {ruta_pdf}")
    docx_a_pdf(ruta_docx, ruta_pdf)

    print(f"📸 5. Renders de cada página en: {carpeta_imgs}")
    imgs = pdf_a_imagenes(ruta_pdf, carpeta_imgs)
    print(f"✅ Se generaron {len(imgs)} páginas capturadas exitosamente:")
    for img in imgs:
        print(f"   - {img.name} ({img.resolve()})")


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
        print("✅ GUARDIA DLP APROBADA: Cero placeholders o variables sin resolver.")


def cmd_entregar(args):
    ruta = Path(args.archivo)
    print(f"🚀 CERTIFICACIÓN DE ENTREGA: {ruta.name}")

    fugas = auditar_documento(ruta)
    if fugas:
        print("❌ Fallo en Guardia DLP.")
        sys.exit(1)

    ok = ejecutar_verificacion_popperiana(ruta, args.entidad, args.modalidad)
    if not ok:
        print("❌ Fallo en verificación popperiana.")
        sys.exit(1)

    print("🏆 DOCUMENTO CERTIFICADO Y LISTO PARA ELEVACIÓN AL COLEGIADO CC1.")


def main():
    parser = argparse.ArgumentParser(description="CLI de Resoluciones de Improcedencia a SUSALUD")
    subparsers = parser.add_subparsers(dest="comando", required=True)

    # simular
    subparsers.add_parser("simular", help="Genera una resolución de improcedencia inventada y sus capturas")

    # verificar
    p_ver = subparsers.add_parser("verificar", help="Verifica un .docx")
    p_ver.add_argument("archivo", help="Ruta al archivo .docx")
    p_ver.add_argument("--entidad", default="IPRESS", choices=["IAFAS", "IPRESS", "MIXTO"])
    p_ver.add_argument("--modalidad", default="TOTAL", choices=["TOTAL", "PARCIAL"])

    # guardia
    p_gua = subparsers.add_parser("guardia", help="Audita fuga DLP")
    p_gua.add_argument("archivo", help="Ruta al archivo .docx")

    # entregar
    p_ent = subparsers.add_parser("entregar", help="Certifica el documento")
    p_ent.add_argument("archivo", help="Ruta al archivo .docx")
    p_ent.add_argument("--entidad", default="IPRESS", choices=["IAFAS", "IPRESS", "MIXTO"])
    p_ent.add_argument("--modalidad", default="TOTAL", choices=["TOTAL", "PARCIAL"])

    args = parser.parse_args()

    if args.comando == "simular":
        cmd_simular(args)
    elif args.comando == "verificar":
        cmd_verificar(args)
    elif args.comando == "guardia":
        cmd_guardia(args)
    elif args.comando == "entregar":
        cmd_entregar(args)


if __name__ == "__main__":
    main()
