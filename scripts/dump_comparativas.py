import pypdf
import docx
from pathlib import Path

folder = Path(r"C:\Users\Admin\Desktop\impros susalud")

def dump_pdf_key_sections(pdf_path, out_txt):
    reader = pypdf.PdfReader(pdf_path)
    text = ""
    for i, p in enumerate(reader.pages):
        text += f"\n--- PAGINA {i+1} ---\n" + (p.extract_text() or "")
    open(out_txt, "w", encoding="utf-8").write(text)
    print(f"Dumped {pdf_path.name} to {out_txt}")

dump_pdf_key_sections(folder / "0146-2026-CC1 MODELO gastos médicos SOAT (IAFA) ACTUALIZADO 19-01-26 SIN FIRMA.pdf", "iafas_soat_dump.txt")
dump_pdf_key_sections(folder / "0147-2026-CC1 MODELO servicios medicos (IPRESS) ACTUALIZADO 19-01-26 SIN FIRMA.pdf", "ipress_servicios_dump.txt")

def dump_docx_summary(docx_path, out_txt):
    doc = docx.Document(docx_path)
    paras = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
    open(out_txt, "w", encoding="utf-8").write("\n".join(paras))
    print(f"Dumped {docx_path.name} to {out_txt}")

dump_docx_summary(folder / "00 MODELO IMPRO SUSALUD + falta relación de consumo por parte de denunciado (RELACION LABORAL).docx", "laboral_dump.txt")
dump_docx_summary(folder / "000 MODELO IMPRO SUSALUD + DECLINACION CUANTIA 1577-2023-CC1.docx", "cuantia_dump.txt")
