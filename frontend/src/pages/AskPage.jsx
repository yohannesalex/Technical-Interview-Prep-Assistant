import { useEffect, useState } from 'react'
import QuestionInput from '../components/QuestionInput'
import FilterPanel from '../components/FilterPanel'
import AnswerDisplay from '../components/AnswerDisplay'
import SourcesList from '../components/SourcesList'

function AskPage({ onQueryResult }) {
    const [loading, setLoading] = useState(false)
    const [result, setResult] = useState(null)
    const [error, setError] = useState(null)
    const [filters, setFilters] = useState({})
    const [materials, setMaterials] = useState([])

    useEffect(() => {
        const loadMaterials = async () => {
            try {
                const response = await fetch('/api/materials')
                if (!response.ok) return
                const data = await response.json()
                setMaterials(data)
            } catch (err) {
                console.error('Failed to load materials', err)
            }
        }

        loadMaterials()
    }, [])

    const handleAsk = async (question) => {
        setLoading(true)
        setError(null)

        try {
            const response = await fetch('/api/ask', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    question,
                    filters: Object.keys(filters).length > 0 ? filters : undefined,
                    top_k: 12
                }),
            })

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`)
            }

            const data = await response.json()
            setResult(data)
            onQueryResult(data)
        } catch (err) {
            setError(err.message)
        } finally {
            setLoading(false)
        }
    }

    return (
        <div className="ask-page">
            <div className="ask-container">
                <QuestionInput onSubmit={handleAsk} loading={loading} />
                <FilterPanel filters={filters} onChange={setFilters} materials={materials} />
            </div>

            {error && (
                <div className="error-message">
                    <strong>Error:</strong> {error}
                </div>
            )}

            {loading && (
                <div className="loading">
                    <div className="spinner"></div>
                    <p>Processing your question...</p>
                </div>
            )}

            {result && !loading && (
                <div className="results">
                    <AnswerDisplay
                        answer={result.answer}
                        faithfulnessScore={result.faithfulness_score}
                        verificationStatus={result.verification_status}
                        confidence={result.confidence}
                    />
                    <SourcesList sources={result.sources} />
                </div>
            )}
        </div>
    )
}

export default AskPage
