import { api } from '../services/api'

function VerificationReport({ result }) {
    const getStatusColor = (status) => {
        switch (status) {
            case 'passed': return '#10a37f'
            case 'warning': return '#f59e0b'
            case 'failed': return '#ef4444'
            default: return 'var(--text-muted)'
        }
    }

    const handleSourceClick = (materialId) => {
        if (!materialId) return
        const url = api.getFileUrl(materialId)
        window.open(url, '_blank')
    }

    return (
        <div className="verification-report" style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>
            <div className="report-section">
                <h3 style={{ fontSize: '0.9rem', textTransform: 'uppercase', letterSpacing: '0.05em', color: 'var(--text-secondary)', marginBottom: '1.25rem' }}>
                    Metrics Assessment
                </h3>
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))', gap: '1.5rem' }}>
                    <div className="assessment-item">
                        <label style={{ fontSize: '0.75rem', color: 'var(--text-muted)', display: 'block', marginBottom: '8px' }}>Status</label>
                        <div
                            className="status-badge"
                            style={{
                                backgroundColor: `${getStatusColor(result.verification_status)}22`,
                                color: getStatusColor(result.verification_status),
                                display: 'inline-block'
                            }}
                        >
                            {result.verification_status?.toUpperCase()}
                        </div>
                    </div>
                    <div className="assessment-item">
                        <label style={{ fontSize: '0.75rem', color: 'var(--text-muted)', display: 'block', marginBottom: '8px' }}>Faithfulness</label>
                        <div style={{ fontSize: '1.5rem', fontWeight: 700, fontFamily: 'var(--font-display)' }}>
                            {result.faithfulness_score !== null && result.faithfulness_score !== undefined
                                ? `${(result.faithfulness_score * 100).toFixed(0)}%`
                                : '--'}
                        </div>
                    </div>
                    <div className="assessment-item">
                        <label style={{ fontSize: '0.75rem', color: 'var(--text-muted)', display: 'block', marginBottom: '8px' }}>Confidence</label>
                        <div style={{ fontSize: '1.5rem', fontWeight: 700, fontFamily: 'var(--font-display)' }}>
                            {result.confidence ? `${(result.confidence * 100).toFixed(0)}%` : '--'}
                        </div>
                    </div>
                </div>
            </div>

            <div className="report-section">
                <h3 style={{ fontSize: '0.9rem', textTransform: 'uppercase', letterSpacing: '0.05em', color: 'var(--text-secondary)', marginBottom: '1rem' }}>
                    Interpretation
                </h3>
                <div style={{ padding: '1.25rem', background: 'rgba(255,255,255,0.03)', borderRadius: '10px', borderLeft: `4px solid ${getStatusColor(result.verification_status)}` }}>
                    {result.verification_status === 'passed' && (
                        <p>✓ High Reliability: The answer is strictly grounded in your materials. All key claims match verified source documents.</p>
                    )}
                    {result.verification_status === 'warning' && (
                        <p>⚠ Partial Support: Some details could not be explicitly verified in the materials. Use with discretion.</p>
                    )}
                    {result.verification_status === 'failed' && (
                        <p>✗ Low Faithfulness: The response deviates significantly from provided sources. Review the documents below.</p>
                    )}
                    {result.verification_status === 'llm_refused' || result.verification_status === 'no_materials' ? (
                        <p>ℹ Insufficient Data: Your materials do not contain enough information to answer this reliably.</p>
                    ) : null}
                </div>
            </div>

            <div className="report-section">
                <h3 style={{ fontSize: '0.9rem', textTransform: 'uppercase', letterSpacing: '0.05em', color: 'var(--text-secondary)', marginBottom: '1rem' }}>
                    Reference Sources ({result.sources?.length || 0})
                </h3>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                    {result.sources && result.sources.map((source, index) => (
                        <div
                            key={source.chunk_id || index}
                            className="source-card clickable"
                            onClick={() => handleSourceClick(source.material_id)}
                            style={{
                                display: 'flex',
                                alignItems: 'center',
                                gap: '1rem',
                                padding: '1rem',
                                background: 'rgba(255,255,255,0.03)',
                                borderRadius: '8px',
                                border: '1px solid var(--border-light)',
                                cursor: source.material_id ? 'pointer' : 'default',
                                transition: 'var(--transition)'
                            }}
                        >
                            <div style={{ color: 'var(--text-muted)', fontWeight: 600 }}>#{index + 1}</div>
                            <div style={{ flex: 1 }}>
                                <div style={{ fontWeight: 600, fontSize: '0.95rem' }}>{source.material_title}</div>
                                <div style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>
                                    {source.page && `Page ${source.page}`}
                                    {source.section && ` • ${source.section}`}
                                    {` • ${source.material_type}`}
                                </div>
                            </div>
                            <div style={{ fontSize: '0.8rem', color: 'var(--accent-secondary)', fontWeight: 600 }}>
                                {(source.similarity_score * 100).toFixed(0)}% Match
                            </div>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    )
}

export default VerificationReport
