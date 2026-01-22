import { useEffect, useRef, useState } from 'react'
import { Document, Page, pdfjs } from 'react-pdf'
import 'react-pdf/dist/Page/AnnotationLayer.css'
import 'react-pdf/dist/Page/TextLayer.css'
import workerSrc from 'pdfjs-dist/build/pdf.worker.min?url'

pdfjs.GlobalWorkerOptions.workerSrc = workerSrc

function PdfPreview({ fileUrl, initialPage = 1, title = 'Source Preview', searchText = '' }) {
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

    const normalizeText = (text) => text
        .replace(/[^a-zA-Z0-9\s]/g, ' ')
        .replace(/\s+/g, ' ')
        .trim()
        .toLowerCase()

    const buildSnippetTokens = (text) => {
        const clean = normalizeText(text)
        if (!clean) return []
        const words = clean.split(' ').filter(Boolean)
        return words.slice(0, 12)
    }

    const findPageForSnippet = async (tokens, preferredPage) => {
        if (!pdfInstance || tokens.length === 0) return null

        const total = pdfInstance.numPages || 0
        const requiredMatches = Math.min(4, tokens.length)

        const scorePage = async (pageIndex) => {
            const page = await pdfInstance.getPage(pageIndex)
            const content = await page.getTextContent()
            const pageText = normalizeText(content.items.map((item) => item.str).join(' '))

            let matches = 0
            for (const token of tokens) {
                if (pageText.includes(token)) {
                    matches += 1
                }
            }

            return { pageIndex, matches }
        }

        const candidates = []

        if (preferredPage && preferredPage >= 1 && preferredPage <= total) {
            candidates.push(await scorePage(preferredPage))
        }

        for (let i = 1; i <= total; i += 1) {
            if (i === preferredPage) continue
            candidates.push(await scorePage(i))
        }

        const best = candidates.reduce((acc, curr) => (curr.matches > acc.matches ? curr : acc), { pageIndex: null, matches: 0 })

        if (best.pageIndex && best.matches >= requiredMatches) {
            return best.pageIndex
        }

        return null
    }

    useEffect(() => {
        let isActive = true

        const runSearch = async () => {
            if (!pdfInstance || !searchText) return

            const tokens = buildSnippetTokens(searchText)
            if (tokens.length === 0) return

            const currentPage = Number.parseInt(initialPage, 10)
            const foundPage = await findPageForSnippet(tokens, Number.isFinite(currentPage) ? currentPage : null)

            if (isActive && foundPage && foundPage !== pageNumber) {
                setPageNumber(foundPage)
            }
        }

        runSearch()

        return () => {
            isActive = false
        }
    }, [pdfInstance, searchText, initialPage])

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
