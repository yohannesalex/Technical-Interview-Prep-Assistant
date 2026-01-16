import { api } from '../services/api'

function SourcesList({ sources }) {
    if (!sources || sources.length === 0) {
        return null
    }

    const handleSourceClick = (materialId) => {
        if (materialId) {
            window.open(api.getFileUrl(materialId), '_blank')
        }
    }

    return (
        <div className="sources-list">
            <h3>Sources ({sources.length})</h3>
            <div className="sources-grid">
                {sources.map((source, index) => (
                    <div
                        key={source.chunk_id}
                        className="source-card clickable"
                        onClick={() => handleSourceClick(source.material_id)}
                        style={{ cursor: source.material_id ? 'pointer' : 'default' }}
                        title="Click to view source file"
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
                    </div>
                ))}
            </div>
        </div>
    )
}

export default SourcesList
