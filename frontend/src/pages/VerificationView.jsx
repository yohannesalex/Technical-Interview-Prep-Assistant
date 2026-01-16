import VerificationReport from '../components/VerificationReport'

function VerificationView({ result }) {
    if (!result) {
        return <div className="empty-state">No query result to verify</div>
    }

    const exportResults = () => {
        const exportData = {
            question: result.question || 'N/A',
            answer: result.answer,
            sources: result.sources,
            faithfulness_score: result.faithfulness_score,
            verification_status: result.verification_status,
            confidence: result.confidence,
            timestamp: new Date().toISOString()
        }

        const blob = new Blob([JSON.stringify(exportData, null, 2)], { type: 'application/json' })
        const url = URL.createObjectURL(blob)
        const a = document.createElement('a')
        a.href = url
        a.download = `verification_${Date.now()}.json`
        a.click()
        URL.revokeObjectURL(url)
    }

    return (
        <div className="verification-view">
            <div className="verification-header">
                <h2>Verification Report</h2>
                <button onClick={exportResults} className="export-button">
                    Export Results
                </button>
            </div>

            <VerificationReport result={result} />
        </div>
    )
}

export default VerificationView
