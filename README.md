# Sistema de Elaboración de Resoluciones de Improcedencia a SUSALUD
### Comisión de Protección al Consumidor N° 1 (CC1) — INDECOPI

**Equipo:** Seguros  
**Elaborado por:** David Chávez  
**Supervisado por:** Loussiana Salazar  
**Versión:** 1.0.0 (Release con ejecutable `.exe` standalone)

Repositorio especializado en la formulación, redacción determinista, verificación popperiana y auditoría de resoluciones emitidas por la **Comisión de Protección al Consumidor N° 1 (CC1)** que declaran la **improcedencia total o parcial** de denuncias administrativas por incompetencia material frente a la **Superintendencia Nacional de Salud (SUSALUD)**.

---

## 🏛️ Marco Institucional y Regla de Competencia Resolutiva

> [!IMPORTANT]
> **A diferencia de las resoluciones de trámite o admisibilidad:**
> Las resoluciones de improcedencia **NUNCA son suscritas ni emitidas por la Secretaría Técnica**. Son actos resolutivos de fondo/calificación que deciden sobre la competencia material y son emitidas por el **Órgano Colegiado de la Comisión de Protección al Consumidor N° 1 (CC1)**.
> La Secretaría Técnica interviene en la parte resolutiva únicamente como ejecutora a la que se le **ordena remitir el original de todo lo actuado a SUSALUD** (Artículo Segundo del RESUELVE).

---

## ⚖️ Catálogo Taxonómico de Supuestos: IAFAS vs. IPRESS vs. MIXTO

El motor adapta con precisión milimétrica la fundamentación jurídica según la naturaleza de la entidad denunciada:

### 1. IAFAS (Empresas de Seguros / EPS / Fondos de Salud / AFOCAT)
* **Precedentes de referencia:** `0146-2026/CC1`, `2685-2025/CC1` (Mapfre - SOAT).
* **Materia:** Cobertura de gastos médicos derivados del SOAT o seguros de salud, cartas de garantía, reembolsos, deducibles, copagos, exclusiones o vigencia de pólizas.
* **Infracción Susalud:** Anexo I-C del Reglamento de Infracciones y Sanciones de Susalud (D.S. N° 031-2014-SA), numeral 1: *"No brindar cobertura oportuna a los afiliados o sus beneficiarios de acuerdo a las condiciones pactadas y la normatividad vigente"*.
* **Norma sectorial de transferencia:** Artículo 8° del D.S. N° 026-2015-SA (competencia exclusiva de Susalud sobre IAFAS - Empresas de Seguros y SOAT gastos médicos).

### 2. IPRESS (Clínicas / Hospitales / Policlínicos / Centros Médicos / Laboratorios)
* **Precedentes de referencia:** `0147-2026/CC1`, `2755-2025/CC1` (Detecta Centro Oncológico), `3280-2026/CC1` (Clínica Ricardo Palma), `3259-2026/CC1` (Clínica San Juan de Dios).
* **Materia:** Prestación de servicios de salud médica asistencial, diagnósticos, procedimientos quirúrgicos, historia clínica, deber de información, consentimiento informado y presunta mala praxis médica.
* **Infracción Susalud:** Anexo I-B (y Anexo III) del D.S. N° 031-2014-SA: conductas incurridas por parte de las IPRESS en perjuicio de los usuarios de servicios de salud.
* **Norma sectorial de delimitación:** Artículo 7° del Decreto Legislativo N° 1158 (establecimientos de salud y servicios médicos).

### 3. Concurrencia Mixta (IAFAS + IPRESS)
* **Materia:** Casos donde concurre una aseguradora (que rechazó la cobertura o carta de garantía) y una clínica (que exigió pagarés o retuvo la atención médica). Ambas conductas se subsumen bajo la supervisión integral de Susalud.

---

## 📜 Fórmula Canónica del RESUELVE

En estricta observancia del modelo institucional de la CC1, la parte resolutiva se estructura de forma unívoca:

1. **PRIMERO:** Declarar improcedente la denuncia por incompetencia por razón de la materia en favor de SUSALUD, y **disponer la devolución al denunciante de la tasa por derecho de trámite pagada**, previa solicitud a la Unidad de Finanzas y Contabilidad del Indecopi.
2. **SEGUNDO:** Ordenar a la **Secretaría Técnica de la Comisión de Protección al Consumidor N° 1 que remita el original de todo lo actuado** a SUSALUD para los fines de su competencia.
3. **TERCERO:** Informar al denunciante que la resolución no agota la vía administrativa, procediendo el recurso de apelación dentro del plazo de **quince (15) días hábiles** ante la Comisión, de conformidad con el artículo 38° del D. Leg. N° 807 y el artículo 212° del TUO de la Ley N° 27444 aprobado por **Decreto Supremo N° 006-2026-JUS**; caso contrario quedará consentida.

---

## 📦 Estructura del Repositorio

```text
elaboracion-de-resoluciones-de-improcedencia-a-susalud/
├── AGENTS.md                                        # Protocolo operativo y reglas críticas
├── README.md                                        # Documentación integral del sistema
├── requirements.txt                                 # Dependencias Python
├── dist/
│   └── improcedencia-susalud-engine.exe             # Ejecutable compilado para Windows
├── config/
│   └── config.py                                    # Constantes institucionales y del equipo
├── docs/
│   └── PATRONES_IAFAS_IPRESS_MIXTOS.md              # Guía comparativa y taxonómica
├── normas/
│   └── MARCO_NORMATIVO_SUSALUD_IPRESS_IAFAS.md      # Dogmática jurídica CC1 vs. SUSALUD
├── plantillas_maestras/
│   └── plantilla_maestra_impro_susalud.docx         # Plantilla oficial CC1 con membrete M-CPC-05/02
├── scripts/
│   ├── improcedencia.py                             # CLI unificado (simular, verificar, guardia, entregar)
│   ├── verificar_improcedencia.py                   # Suite de verificación popperiana
│   └── guardia_improcedencia.py                     # Guardia DLP contra fuga de placeholders
└── src/
    ├── __init__.py
    ├── builder.py                                   # Ensamblador OpenXML de alta precisión
    ├── improcedencia_engine.py                      # Motor de subsunción jurídica determinista
    └── rules_engine.py                              # Motor de reglas y validaciones formales
```

---

## 🚀 Uso del Ejecutable (`.exe`) y CLI Python

El sistema puede ejecutarse directamente desde el ejecutable compilado sin necesidad de tener Python instalado:

```bash
# 1. Generar simulación completa y capturas de páginas:
dist\improcedencia-susalud-engine.exe simular

# 2. Auditar documento contra fuga de datos y variables residuales:
dist\improcedencia-susalud-engine.exe guardia "generados/mi_resolucion.docx"

# 3. Verificar documento con la batería de comprobaciones popperianas:
dist\improcedencia-susalud-engine.exe verificar "generados/mi_resolucion.docx" --entidad IPRESS --modalidad TOTAL

# 4. Certificación de entrega (Triple Barrera):
dist\improcedencia-susalud-engine.exe entregar "generados/mi_resolucion.docx" --entidad IAFAS --modalidad TOTAL
```
