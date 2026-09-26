from pathlib import Path

# Raíz del repositorio
BASE_DIR = Path(__file__).resolve().parent.parent

# Carpetas del sistema
CONFIG_DIR = BASE_DIR / "config"
DOCS_DIR = BASE_DIR / "docs"
GENERADOS_DIR = BASE_DIR / "generados"
NORMAS_DIR = BASE_DIR / "normas"
PLANTILLAS_DIR = BASE_DIR / "plantillas_maestras"
SCRIPTS_DIR = BASE_DIR / "scripts"
SRC_DIR = BASE_DIR / "src"

# Crear carpetas si no existen
for d in [CONFIG_DIR, DOCS_DIR, GENERADOS_DIR, NORMAS_DIR, PLANTILLAS_DIR, SCRIPTS_DIR, SRC_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# Parámetros Institucionales y del Equipo
AUTORIDAD_RESOLUTIVA = "COMISIÓN DE PROTECCIÓN AL CONSUMIDOR N° 1"
ORGANO_TIPO = "COLEGIADO"
EQUIPO = "Seguros"
ELABORADO_POR = "David Chávez"
SUPERVISADO_POR = "Loussiana Salazar"

# REGLA DE ORO PROCESAL:
# La Secretaría Técnica NO emite ni suscribe las resoluciones de improcedencia.
# Son emitidas exclusivamente por el Órgano Colegiado de la Comisión (CC1).
FIRMA_SECRETARIA_TECNICA_PERMITIDA = False

# Tipografía reglamentaria
FUENTE_PRINCIPAL = "Arial"
TAMANO_TEXTO_PT = 11
TAMANO_TITULO_PT = 16
TAMANO_METADATA_PT = 8

# Códigos de error y validación Popperiana
VALIDACIONES_TOTALES = 20
