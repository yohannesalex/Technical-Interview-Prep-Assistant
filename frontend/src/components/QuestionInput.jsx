import { useState } from 'react'

function QuestionInput({ onSubmit, loading }) {
    const [question, setQuestion] = useState('')

    const handleSubmit = (e) => {
        e.preventDefault()
        if (question.trim() && !loading) {
            onSubmit(question.trim())
            setQuestion('')
        }
    }

    const handleKeyDown = (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault()
            handleSubmit(e)
        }
    }

    return (
        <form onSubmit={handleSubmit} className="question-input">
            <textarea
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                onKeyDown={handleKeyDown}
                placeholder="Ask a technical interview question..."
                rows={1}
                disabled={loading}
                style={{
                    maxHeight: '200px',
                    minHeight: '24px',
                    height: 'auto',
                    overflowY: question.split('\n').length > 1 ? 'auto' : 'hidden'
                }}
            />
            <button
                type="submit"
                disabled={loading || !question.trim()}
                title="Send message"
            >
                {loading ? (
                    <span className="spinner small"></span>
                ) : (
                    <svg stroke="currentColor" fill="none" strokeWidth="2" viewBox="0 0 24 24" strokeLinecap="round" strokeLinejoin="round" height="1em" width="1em" xmlns="http://www.w3.org/2000/svg">
                        <line x1="22" y1="2" x2="11" y2="13"></line>
                        <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
                    </svg>
                )}
            </button>
        </form>
    )
}

export default QuestionInput
