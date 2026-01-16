import { useState } from 'react'
import VerificationReport from './VerificationReport'
import { api } from '../services/api'

function AnswerDisplay({ answer, faithfulnessScore, verificationStatus, confidence, sources }) {
    const [showVerification, setShowVerification] = useState(false)

    const getStatusColor = (status) => {
        switch (status) {
            case 'passed': return 'green'
            case 'warning': return 'orange'
            case 'failed': return 'red'
            case 'llm_refused': return 'gray'
            default: return 'blue'
        }
    }

    const getStatusText = (status) => {
        switch (status) {
            case 'passed': return '✓ Verified'
            case 'warning': return '⚠ Partially Verified'
            case 'failed': return '✗ Low Confidence'
            case 'llm_refused': return 'ℹ No Answer Available'
            case 'no_materials': return 'ℹ No Materials'
            case 'no_matches': return 'ℹ No Matches'
            default: return status
        }
    }

    // Construct the result object expected by VerificationReport
    const verificationResult = {
        verification_status: verificationStatus,
        faithfulness_score: faithfulnessScore,
        confidence: confidence,
        answer: answer,
        sources: sources
    }

    return (
        <div className="answer-display">
            <div className="answer-header">
                <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
                    <div className="status-badge green" style={{ display: 'none' }}>Answer</div>
                    <div className="answer-meta">
                        <span className={`status-badge ${getStatusColor(verificationStatus)}`}>
                            {getStatusText(verificationStatus)}
                        </span>
                    </div>
                </div>

                <button
                    onClick={() => setShowVerification(true)}
                    className="new-chat-btn"
                    style={{
                        padding: '4px 12px',
                        fontSize: '0.75rem',
                        background: 'rgba(255,255,255,0.05)',
                        border: '1px solid var(--border-light)',
                        borderRadius: '6px',
                        margin: 0,
                        height: 'auto'
                    }}
                >
                    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" style={{ marginRight: '6px' }}><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path></svg>
                    Verification
                </button>
            </div>

            <div className="answer-content">
                {answer.split('\n').map((line, i) => (
                    <p key={i} style={{ marginBottom: line.trim() === '' ? '1rem' : '0.5rem' }}>{line}</p>
                ))}
            </div>

            {/* Verification Modal */}
            {showVerification && (
                <div className="verification-modal">
                    <div className="modal-content">
                        <button
                            onClick={() => setShowVerification(false)}
                            style={{
                                position: 'absolute',
                                top: '1.25rem',
                                right: '1.25rem',
                                background: 'transparent',
                                border: 'none',
                                color: 'var(--text-secondary)',
                                fontSize: '1.5rem',
                                cursor: 'pointer'
                            }}
                        >
                            &times;
                        </button>

                        <h2 style={{ fontFamily: 'var(--font-display)', marginBottom: '1.5rem' }}>Verification Report</h2>
                        <VerificationReport result={verificationResult} />

                        <div style={{ marginTop: '2.5rem', textAlign: 'right' }}>
                            <button onClick={() => setShowVerification(false)} className="new-chat-btn" style={{ display: 'inline-flex', width: 'auto', marginBottom: 0 }}>
                                Done
                            </button>
                        </div>
                    </div>
                </div>
            )}
        </div>
    )
}

export default AnswerDisplay
