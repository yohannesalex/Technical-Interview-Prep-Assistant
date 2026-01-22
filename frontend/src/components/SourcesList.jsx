function SourcesList({ sources }) {
    if (!sources || sources.length === 0) {
        return null
    }

    const buildPreviewUrl = (source) => {
        if (!source?.material_id) return
        const snippet = (source.text || '').slice(0, 160)
        const params = new URLSearchParams({
            material_id: String(source.material_id),
            page: String(source.page || 1),
            title: source.material_title || 'PDF Preview',
            snippet
        })
        const base = `${window.location.origin}${window.location.pathname}`
        return `${base}#/preview?${params.toString()}`
    }

    return (
        <div className="sources-list">
            <h3>Sources ({sources.length})</h3>
            <div className="sources-grid">
                {sources.map((source, index) => (
                    <a
                        key={source.chunk_id}
                        className="source-card clickable"
                        href={buildPreviewUrl(source)}
                        target="_blank"
                        rel="noopener noreferrer"
                        style={{ cursor: source.material_id ? 'pointer' : 'default' }}
                        title="Click to preview source"
                    >
                        <div className="source-header">
                            <span className="source-number">#{index + 1}</span>
                            <span className="source-type">{source.material_type}</span>
                            <span className="source-score">
                                {(source.similarity_score * 100).toFixed(0)}%
                            </span>
                        </div>
                        <div className="source-title">{source.material_title}</div>
                        <div className="source-location">
                            {source.page && <span>Page {source.page}</span>}
                            {source.section && <span>{source.section}</span>}
                        </div>
                    </a>
                ))}
            </div>
        </div>
    )
}

export default SourcesList
