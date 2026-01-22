import { useEffect, useRef, useState } from 'react'
import { Document, Page, pdfjs } from 'react-pdf'
import 'react-pdf/dist/Page/AnnotationLayer.css'
import 'react-pdf/dist/Page/TextLayer.css'
import workerSrc from 'pdfjs-dist/build/pdf.worker.min?url'

pdfjs.GlobalWorkerOptions.workerSrc = workerSrc

function PdfPreview({ fileUrl, initialPage = 1, title = 'Source Preview' }) {
    const containerRef = useRef(null)
    const [pdfInstance, setPdfInstance] = useState(null)
    const [numPages, setNumPages] = useState(null)
    const [pageNumber, setPageNumber] = useState(initialPage || 1)
    const [pageWidth, setPageWidth] = useState(900)
    const [loadError, setLoadError] = useState(null)

    useEffect(() => {
        const parsedPage = Number.parseInt(initialPage, 10)
        setPageNumber(Number.isFinite(parsedPage) && parsedPage > 0 ? parsedPage : 1)
    }, [initialPage])

    useEffect(() => {
        if (!containerRef.current) return

        const updateWidth = () => {
            const width = containerRef.current?.clientWidth || 900
            setPageWidth(Math.max(320, Math.min(width - 24, 1200)))
        }

        updateWidth()

        const observer = new ResizeObserver(updateWidth)
        observer.observe(containerRef.current)

        return () => observer.disconnect()
    }, [])

    const onDocumentLoadSuccess = (pdf) => {
        const total = pdf?.numPages || pdf?.numPages === 0 ? pdf.numPages : null
        if (total) {
            setNumPages(total)
            if (pageNumber > total) setPageNumber(total)
        }
        setPdfInstance(pdf?.getPage ? pdf : null)
        setLoadError(null)
    }



    const goToPrev = () => setPageNumber((p) => Math.max(1, p - 1))
    const goToNext = () => setPageNumber((p) => Math.min(numPages || p + 1, p + 1))

    const handlePageInput = (event) => {
        const value = parseInt(event.target.value, 10)
        if (!Number.isNaN(value)) {
            setPageNumber(Math.min(Math.max(value, 1), numPages || value))
        }
    }

    if (!fileUrl) {
        return (
            <div className="pdf-preview-empty">
                No file available for preview.
            </div>
        )
    }

    return (
        <div className="pdf-preview" ref={containerRef}>
            <div className="pdf-preview-toolbar">
                <span className="pdf-preview-title">{title}</span>
                <div className="pdf-preview-controls">
                    <button onClick={goToPrev} disabled={pageNumber <= 1}>
                        Prev
                    </button>
                    <div className="pdf-preview-page-input">
                        <input
                            type="number"
                            min="1"
                            value={pageNumber}
                            onChange={handlePageInput}
                        />
                        <span> / {numPages || '-'}</span>
                    </div>
                    <button onClick={goToNext} disabled={numPages ? pageNumber >= numPages : false}>
                        Next
                    </button>
                </div>
            </div>

            <div className="pdf-preview-body">
                <Document
                    file={fileUrl}
                    onLoadSuccess={onDocumentLoadSuccess}
                    onLoadError={(error) => setLoadError(error?.message || 'Failed to load PDF')}
                    loading={<div className="pdf-preview-loading">Loading PDF…</div>}
                    error={<div className="pdf-preview-error">{loadError || 'Failed to load PDF.'}</div>}
                >
                    <Page
                        pageNumber={pageNumber}
                        width={pageWidth}
                        renderAnnotationLayer
                        renderTextLayer
                    />
                </Document>
            </div>
        </div>
    )
}

export default PdfPreview
