function MaterialCard({ material, onDelete }) {
    const formatDate = (dateString) => {
        return new Date(dateString).toLocaleDateString()
    }

    return (
        <div className="material-card">
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '1.25rem' }}>
                <span className="status-badge orange" style={{ fontSize: '0.65rem' }}>{material.material_type}</span>
                <button
                    onClick={onDelete}
                    style={{ background: 'transparent', border: 'none', color: 'var(--text-muted)', cursor: 'pointer', display: 'flex' }}
                    title="Delete material"
                >
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                        <polyline points="3 6 5 6 21 6"></polyline>
                        <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                    </svg>
                </button>
            </div>

            <div style={{ display: 'flex', gap: '14px', alignItems: 'flex-start' }}>
                <div style={{ fontSize: '2.5rem', lineHeight: 1 }}>
                    {material.filename.toLowerCase().endsWith('.pdf') ? '📄' : '📝'}
                </div>
                <div style={{ flex: 1, overflow: 'hidden' }}>
                    <div style={{
                        fontWeight: 600,
                        fontSize: '1rem',
                        marginBottom: '4px',
                        whiteSpace: 'nowrap',
                        overflow: 'hidden',
                        textOverflow: 'ellipsis',
                        fontFamily: 'var(--font-display)',
                        color: 'var(--text-primary)'
                    }}>
                        {material.filename}
                    </div>
                    {material.course && (
                        <div style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>
                            {material.course}
                        </div>
                    )}
                </div>
            </div>

            <div style={{
                marginTop: '1.5rem',
                paddingTop: '1rem',
                borderTop: '1px solid var(--border-light)',
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                fontSize: '0.72rem',
                color: 'var(--text-muted)',
                fontWeight: 500
            }}>
                <span>{material.chunk_count} segments</span>
                <span>{formatDate(material.upload_date)}</span>
            </div >
        </div >
    )
}

export default MaterialCard
