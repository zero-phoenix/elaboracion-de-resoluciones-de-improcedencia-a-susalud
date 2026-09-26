$docxPath = "C:\Users\Admin\Documents\antigravity\zealous-kepler\elaboracion-de-resoluciones-de-improcedencia-a-susalud\generados\RESOLUCION_COMPLEJA_CC1_IMPROCEDENCIA_SUSALUD.docx"
$pdfPath = "C:\Users\Admin\Documents\antigravity\zealous-kepler\elaboracion-de-resoluciones-de-improcedencia-a-susalud\generados\RESOLUCION_COMPLEJA_CC1_IMPROCEDENCIA_SUSALUD.pdf"

$word = New-Object -ComObject Word.Application
$word.Visible = $false
try {
    $doc = $word.Documents.Open($docxPath)
    # wdFormatPDF = 17
    $doc.SaveAs([ref]$pdfPath, [ref]17)
    $doc.Close([ref]$false)
    Write-Output "PDF generado exitosamente en: $pdfPath"
} catch {
    Write-Error "Error al convertir a PDF: $_"
} finally {
    $word.Quit()
}
