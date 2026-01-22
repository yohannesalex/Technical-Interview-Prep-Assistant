import { useState, useEffect } from 'react'

function VerificationReport({ result, activeSourceIndex = null }) {
    const [currentIndex, setCurrentIndex] = useState(0)

    useEffect(() => {
        if (activeSourceIndex !== null && activeSourceIndex >= 0) {
            setCurrentIndex(activeSourceIndex)
        }
    }, [activeSourceIndex])

    const sources = result.sources || []
    const currentSource = sources[currentIndex]

    const getStatusColor = (status) => {
        switch (status) {
            case 'passed': return '#10a37f'
            case 'warning': return '#f59e0b'
            case 'failed': return '#ef4444'
            default: return 'var(--text-muted)'
        }
    }

    const getSourceLabel = (source) => {
        if (!source) return ''
        const parts = []
        if (source.material_title) parts.push(source.material_title)
        if (source.section) parts.push(source.section)
        if (source.page) parts.push(`Page ${source.page}`)
        return parts.join(' • ')
    }

    if (sources.length === 0) {
        return (
            <div style={{ padding: '3rem', textAlign: 'center', color: 'var(--text-muted)' }}>
                No source information available for this answer.
            </div>
        )
    }

    return (
        <div className="verification-report-full" style={{ height: '100%', display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
            {/* Ultra-Minimal Header */}
            <div style={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between',
                padding: '0 0.5rem 0.5rem',
                borderBottom: '1px solid var(--border-light)'
            }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                        <div className="status-badge" style={{
                            backgroundColor: `${getStatusColor(result.verification_status)}22`,
                            color: getStatusColor(result.verification_status),
                            fontSize: '0.65rem',
                            padding: '2px 6px'
                        }}>
                            {result.verification_status?.toUpperCase()}
                        </div>
                        <span style={{ fontSize: '0.9rem', fontWeight: 600, color: 'var(--text-primary)' }}>
                            {currentSource.material_title}
                        </span>
                        <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
                            {currentSource.page ? `• Page ${currentSource.page}` : ''}
                        </span>
                    </div>
                </div>

                <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                    <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginRight: '8px' }}>
                        Source {currentIndex + 1} of {sources.length}
                    </span>
                    <button
                        disabled={currentIndex === 0}
                        onClick={() => setCurrentIndex(i => i - 1)}
                        className="new-chat-btn"
                        style={{ padding: '4px 12px', width: 'auto', marginBottom: 0, opacity: currentIndex === 0 ? 0.3 : 1, fontSize: '0.8rem' }}
                    >
                        Prev
                    </button>
                    <button
                        disabled={currentIndex === sources.length - 1}
                        onClick={() => setCurrentIndex(i => i + 1)}
                        className="new-chat-btn"
                        style={{ padding: '4px 12px', width: 'auto', marginBottom: 0, opacity: currentIndex === sources.length - 1 ? 0.3 : 1, fontSize: '0.8rem' }}
                    >
                        Next
                    </button>
                </div>
            </div>

            <div style={{
                flex: 1,
                background: 'rgba(18, 18, 21, 0.9)',
                borderRadius: '8px',
                border: '1px solid var(--border-light)',
                padding: '1.5rem',
                display: 'flex',
                flexDirection: 'column',
                gap: '1rem'
            }}>
                <div style={{ fontSize: '0.9rem', color: 'var(--text-secondary)' }}>
                    {getSourceLabel(currentSource)}
                </div>
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, minmax(0, 1fr))', gap: '1rem' }}>
                    <div style={{ background: 'rgba(255,255,255,0.03)', border: '1px solid var(--border-light)', borderRadius: '8px', padding: '0.9rem' }}>
                        <div style={{ fontSize: '0.7rem', color: 'var(--text-muted)', marginBottom: '6px' }}>Faithfulness</div>
                        <div style={{ fontSize: '1.4rem', fontWeight: 700 }}>{Math.round((result.faithfulness_score || 0) * 100)}%</div>
                    </div>
                    <div style={{ background: 'rgba(255,255,255,0.03)', border: '1px solid var(--border-light)', borderRadius: '8px', padding: '0.9rem' }}>
                        <div style={{ fontSize: '0.7rem', color: 'var(--text-muted)', marginBottom: '6px' }}>Similarity</div>
                        <div style={{ fontSize: '1.4rem', fontWeight: 700 }}>{Math.round((currentSource.similarity_score || 0) * 100)}%</div>
                    </div>
                    <div style={{ background: 'rgba(255,255,255,0.03)', border: '1px solid var(--border-light)', borderRadius: '8px', padding: '0.9rem' }}>
                        <div style={{ fontSize: '0.7rem', color: 'var(--text-muted)', marginBottom: '6px' }}>Material Type</div>
                        <div style={{ fontSize: '1rem', fontWeight: 600 }}>{currentSource.material_type || 'unknown'}</div>
                    </div>
                    <div style={{ background: 'rgba(255,255,255,0.03)', border: '1px solid var(--border-light)', borderRadius: '8px', padding: '0.9rem' }}>
                        <div style={{ fontSize: '0.7rem', color: 'var(--text-muted)', marginBottom: '6px' }}>Chunk ID</div>
                        <div style={{ fontSize: '0.85rem', fontFamily: 'var(--font-sans)', wordBreak: 'break-all' }}>{currentSource.chunk_id}</div>
                    </div>
                </div>
            </div>

            {/* Compact Stats Footer */}
            <div style={{ display: 'flex', justifyContent: 'center', gap: '1.5rem', fontSize: '0.7rem', color: 'var(--text-muted)', padding: '0.25rem 0' }}>
                <span>Faithfulness: {(result.faithfulness_score * 100).toFixed(0)}%</span>
                <span>Match: {(currentSource.similarity_score * 100).toFixed(0)}%</span>
            </div>
        </div>
    )
}

export default VerificationReport
