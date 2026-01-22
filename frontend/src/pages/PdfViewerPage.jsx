import { useEffect, useMemo, useState } from 'react'
import { api } from '../services/api'
import PdfPreview from '../components/PdfPreview'

function PdfViewerPage() {
    const [params, setParams] = useState({ materialId: null, page: 1, title: 'PDF Preview', snippet: '' })

    useEffect(() => {
        const hash = window.location.hash || ''
        const queryString = hash.includes('?') ? hash.split('?')[1] : ''
        const searchParams = new URLSearchParams(queryString)

        const materialId = searchParams.get('material_id')
        const page = parseInt(searchParams.get('page') || '1', 10)
        const title = searchParams.get('title') || 'PDF Preview'
        const snippet = searchParams.get('snippet') || ''

        setParams({
            materialId: materialId ? parseInt(materialId, 10) : null,
            page: Number.isFinite(page) && page > 0 ? page : 1,
            title,
            snippet
        })
    }, [])

    const fileUrl = useMemo(() => {
        if (!params.materialId) return null
        // Add timestamp to prevent caching issues when IDs are reused
        return `${api.getFileUrl(params.materialId)}?t=${new Date().getTime()}`
    }, [params.materialId])

    return (
        <div className="pdf-viewer-page">
            <div className="pdf-viewer-toolbar">
                <span>{params.title}</span>
                <button onClick={() => window.close()}>Close</button>
            </div>
            <div className="pdf-viewer-body">
                <PdfPreview
                    fileUrl={fileUrl}
                    initialPage={params.page}
                    title=""
                />
            </div>
        </div>
    )
}

export default PdfViewerPage
