# Sistema de Elaboración de Resoluciones de Improcedencia a SUSALUD
### Comisión de Protección al Consumidor N° 1 (CC1) — INDECOPI

* **Elaborado por:** David Chávez  
* **Supervisado por:** Loussiana Salazar  
* **Equipo:** Seguros  
* **Órgano Resolutivo:** Comisión de Protección al Consumidor N° 1 (Órgano Colegiado)  

---

## 🏛️ Marco Institucional y Regla de Oro Procesal

> [!IMPORTANT]
> **REGLA FUNDAMENTAL DE COMPETENCIA Y FIRMA (CERO SECRETARÍA TÉCNICA):**
> A diferencia de las resoluciones de admisibilidad o de requerimiento de subsanación (que son emitidas por la Secretaría Técnica), **las resoluciones que declaran la improcedencia (total o parcial) son emitidas y suscritas exclusivamente por el Órgano Colegiado de la Comisión de Protección al Consumidor N° 1 (CC1)**.
> El sistema sanciona como violación grave cualquier resolución o firma atribuida a la Secretaría Técnica.

---

## 📚 Delimitación Dogmática y Normativa (SUSALUD vs. INDECOPI)

El motor clasifica minuciosamente la condición jurídica de los denunciados y aplica el marco legal correspondiente:

### 1. IAFAS (Instituciones Administradoras de Fondos de Aseguramiento en Salud)
* **Entidades:** Compañías de seguros (ramo salud/asistencia médica), Entidades Prestadoras de Salud (EPS), Empresas de Medicina Prepagada, AFOCAT, Seguro Integral de Salud (SIS), EsSalud.
* **Normativa específica vinculante:**
  * **Artículo 3°, numeral 2 y artículo 6° del Decreto Legislativo N° 1158.**
  * **Ley N° 29344** (Ley Marco de Aseguramiento Universal en Salud) y **D.S. N° 008-2010-SA**.
  * **Anexo I-B del Decreto Supremo N° 031-2014-SA** (Reglamento de Infracciones y Sanciones de Susalud) respecto a la falta o demora injustificada en brindar cobertura conforme a lo pactado.
  * **Artículo 8° del Decreto Supremo N° 026-2015-SA** (Transferencia de Funciones a Susalud respecto a seguros y SOAT gastos médicos).

### 2. IPRESS (Instituciones Prestadoras de Servicios de Salud)
* **Entidades:** Clínicas privadas, hospitales públicos, policlínicos, centros médicos de apoyo y laboratorios.
* **Normativa específica vinculante:**
  * **Artículo 3°, numeral 3 y artículo 7° del Decreto Legislativo N° 1158.**
  * **Ley N° 26842** (Ley General de Salud): Título I y II (acto médico, deber de reserva, acceso a historia clínica, consentimiento informado).
  * **Decreto Supremo N° 031-2014-SA** (sanción de conductas de IPRESS en perjuicio de los usuarios de servicios de salud).
  * **Materias exclusivas:** Calidad, idoneidad, oportunidad y seguridad asistencial, presunta mala praxis médica, diagnóstico y facturación médica directa.

### 3. Supuestos Mixtos (Concurrencia IAFAS + IPRESS)
* **Fórmula resolutiva:** Cuando coexisten pretensiones contra la aseguradora/EPS (cobertura/carta de garantía) y contra el establecimiento de salud (cobro particular/atención médica), se invocan copulativamente los numerales 2 y 3 del artículo 3° del D. Leg. N° 1158, efectuando la subsunción individualizada en el considerando de aplicación al caso concreto.

---

## 📂 Estructura del Repositorio

```text
elaboracion-de-resoluciones-de-improcedencia-a-susalud/
├── AGENTS.md                                        # Protocolo operativo y reglas críticas
├── README.md                                        # Documentación integral del sistema
├── requirements.txt                                 # Dependencias Python
├── improcedencia-engine.spec                        # Especificación de empaquetado PyInstaller
├── .github/
│   └── workflows/
│       └── build_and_release.yml                    # Pipeline CI/CD automatizado
├── config/
│   └── config.py                                    # Constantes institucionales y rutas
├── docs/
│   ├── MODELO_UNIVERSAL_IMPROCEDENCIA_SUSALUD.md    # Plantilla universal documentada
│   └── MARCO_NORMATIVO_SUSALUD_IPRESS_IAFAS.md      # Dogmática jurídica
├── plantillas_maestras/
│   ├── plantilla_maestra_ipress.docx                # Precedente clínico (p.ej. 2920-2026)
│   ├── plantilla_maestra_iafas.docx                 # Precedente asegurador (p.ej. 2927-2026)
│   ├── plantilla_maestra_mixta_iafas_ipress.docx     # Precedente concurrente (p.ej. 3012-2026 LSQok)
│   └── plantilla_maestra_universal.docx             # Base limpia con notas al pie completas
├── scripts/
│   ├── improcedencia.py                             # CLI unificado
│   ├── verificar_improcedencia.py                   # Suite de verificación popperiana
│   └── guardia_improcedencia.py                     # Guardia DLP contra fuga de variables
├── src/
│   ├── __init__.py
│   ├── builder.py                                   # Ensamblador OpenXML de alta precisión
│   ├── improcedencia_engine.py                      # Motor de subsunción jurídica
│   └── rules_engine.py                              # Reglas institucionales CC1
└── dist/
    └── improcedencia-engine.exe                     # Ejecutable standalone compiled para Windows
```

---

## ⚡ Uso del Ejecutable Standalone y CLI

El ejecutable `improcedencia-engine.exe` se encuentra disponible en la carpeta `dist/` y en los [Releases de GitHub](https://github.com/zero-phoenix/elaboracion-de-resoluciones-de-improcedencia-a-susalud/releases):

```bash
# Consultar información del sistema y equipo
improcedencia info

# Desglose normativo de delimitación competencial
improcedencia normas

# Verificar un proyecto .docx con la batería popperiana
improcedencia verificar "generados/mi_resolucion.docx" --entidad IPRESS --modalidad TOTAL

# Ejecutar la Guardia DLP (cero variables o corchetes sin resolver)
improcedencia guardia "generados/mi_resolucion.docx"

# Certificación de Entrega Oficial (Triple Barrera)
improcedencia entregar "generados/mi_resolucion.docx" --entidad IPRESS --modalidad TOTAL
```
