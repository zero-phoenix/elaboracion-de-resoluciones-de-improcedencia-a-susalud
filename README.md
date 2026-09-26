# Sistema de Elaboración de Resoluciones de Improcedencia a SUSALUD
### Comisión de Protección al Consumidor N° 1 (CC1) — INDECOPI

Repositorio especializado en la formulación, redacción determinista y validación de resoluciones emitidas por la **Comisión de Protección al Consumidor N° 1** que declaran la **improcedencia total o parcial** de denuncias administrativas por incompetencia material frente a la **Superintendencia Nacional de Salud (SUSALUD)**.

---

## 🏛️ Marco Institucional y Regla de Competencia

A diferencia de las resoluciones de admisibilidad o requerimiento de subsanación (que son emitidas por la Secretaría Técnica), **las resoluciones de improcedencia son emitidas y suscritas por el Órgano Colegiado de la Comisión de Protección al Consumidor N° 1 (CC1)**.

### Delimitación Sustantiva:
- **IAFAS (Instituciones Administradoras de Fondos de Aseguramiento en Salud):** Coberturas, planes médicos, preexistencias, copagos, reembolsos, carencias (Art. 3.2 D. Leg. 1158, Ley 29344, D.S. 008-2010-SA).
- **IPRESS (Instituciones Prestadoras de Servicios de Salud):** Prestación del servicio de salud, actos médicos, oportunidad, idoneidad, historia clínica, consentimiento informado, presunta mala praxis (Art. 3.3 D. Leg. 1158, Ley 26842 Ley General de Salud).
- **Supuestos Mixtos:** Concurrencia simultánea de conflicto en la cobertura (IAFAS) y en la atención clínica hospitalaria (IPRESS).
- **Improcedencia Total vs. Parcial:** Total cuando todos los hechos van a SUSALUD; Parcial cuando coexisten pretensiones de SUSALUD y pretensiones bajo competencia del Indecopi (e.g., Libro de Reclamaciones).

---

## 📂 Estructura del Repositorio

```text
elaboracion-de-resoluciones-de-improcedencia-a-susalud/
├── AGENTS.md                                   # Protocolo operativo y reglas críticas del sistema
├── README.md                                   # Documentación general del repositorio
├── requirements.txt                            # Dependencias Python
├── config/
│   └── config.py                               # Rutas y constantes institucionales
├── docs/                                       # Guías metodológicas y catálogos de precedentes
├── normas/
│   └── MARCO_NORMATIVO_SUSALUD_IPRESS_IAFAS.md # Dogmática y delimitación de competencias
├── plantillas_maestras/                        # Plantillas oficiales en formato .docx
├── scripts/
│   ├── improcedencia.py                        # CLI unificado
│   ├── verificar_improcedencia.py              # Suite de verificación popperiana
│   └── guardia_improcedencia.py                # Guardia DLP contra fuga de placeholders
└── src/
    ├── __init__.py
    ├── builder.py                              # Ensamblador OpenXML de alta precisión
    ├── improcedencia_engine.py                 # Motor de razonamiento y subsunción jurídica
    └── rules_engine.py                         # Motor de reglas y validaciones
```

---

## 🚀 Uso Rápido (CLI)

```bash
# Verificar un documento generado con la batería popperiana
python scripts/improcedencia.py verificar "generados/mi_resolucion.docx" --entidad IPRESS --modalidad TOTAL

# Ejecutar la Guardia DLP (cero variables sin resolver)
python scripts/improcedencia.py guardia "generados/mi_resolucion.docx"

# Certificación integral de entrega (Triple Barrera)
python scripts/improcedencia.py entregar "generados/mi_resolucion.docx" --entidad IAFAS --modalidad TOTAL
```
