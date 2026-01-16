import { useState, useEffect, useRef } from 'react'
import { api } from '../services/api'
import QuestionInput from '../components/QuestionInput'
import FilterPanel from '../components/FilterPanel'
import AnswerDisplay from '../components/AnswerDisplay'
import SourcesList from '../components/SourcesList'

function ChatPage({ onNavigate }) {
    const [sessions, setSessions] = useState([])
    const [currentSessionId, setCurrentSessionId] = useState(null)
    const [messages, setMessages] = useState([])
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState(null)
    const [filters, setFilters] = useState({})

    const [materials, setMaterials] = useState([])

    // Auto-scroll ref
    const messagesEndRef = useRef(null)

    // Load data on mount
    useEffect(() => {
        loadSessions()
        loadMaterials()
    }, [])

    const loadMaterials = async () => {
        try {
            const data = await api.getMaterials()
            setMaterials(data)
        } catch (err) {
            console.error("Failed to load materials", err)
        }
    }

    // Load history when session changes
    useEffect(() => {
        if (currentSessionId) {
            loadHistory(currentSessionId)
        } else {
            setMessages([])
        }
    }, [currentSessionId])

    // Auto-scroll to bottom
    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
    }, [messages, loading])

    const loadSessions = async () => {
        try {
            const data = await api.getSessions()
            setSessions(data)
            if (data.length > 0 && !currentSessionId) {
                // Select most recent session? Or wait for user?
                // setCurrentSessionId(data[0].id) 
            }
        } catch (err) {
            setError("Failed to load sessions")
        }
    }

    const loadHistory = async (sessionId) => {
        try {
            setLoading(true)
            const history = await api.getHistory(sessionId)
            setMessages(history)
        } catch (err) {
            setError("Failed to load history")
        } finally {
            setLoading(false)
        }
    }

    const handleNewChat = async () => {
        try {
            const newSession = await api.createSession("New Chat")
            setSessions([newSession, ...sessions])
            setCurrentSessionId(newSession.id)
            setMessages([])
        } catch (err) {
            setError("Failed to create new chat")
        }
    }

    const handleSelectSession = (sessionId) => {
        setCurrentSessionId(sessionId)
    }

    const handleSendMessage = async (question) => {
        setError(null)
        setLoading(true)

        let sessionId = currentSessionId

        // If no session, create one
        if (!sessionId) {
            try {
                // Generate title from first few words of question
                const title = question.slice(0, 30) + (question.length > 30 ? '...' : '')
                const newSession = await api.createSession(title)
                setSessions([newSession, ...sessions])
                setCurrentSessionId(newSession.id)
                sessionId = newSession.id
            } catch (err) {
                setError("Failed to initialize chat")
                setLoading(false)
                return
            }
        }

        // Optimistic UI update for user message
        const userMsg = {
            id: 'temp-' + Date.now(),
            role: 'user',
            content: question,
            timestamp: new Date().toISOString()
        }
        setMessages(prev => [...prev, userMsg])

        // Send to API
        try {
            const response = await api.sendMessage(question, sessionId, filters)

            // The API response is QueryResponse (answer, sources, etc.)
            // We need to convert it to a message format or reload history?
            // Reloading history is safer to get the DB-assigned IDs and consistent format
            await loadHistory(sessionId)

            // Refresh sessions list to update timestamp/order
            loadSessions()

        } catch (err) {
            setError(err.message)
            // Remove temp message? Or show error state?
        } finally {
            setLoading(false)
        }
    }

    return (
        <div className="chat-page">
            {/* Sidebar */}
            <div className="chat-sidebar">
                <button onClick={handleNewChat} className="new-chat-btn">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"><line x1="12" y1="5" x2="12" y2="19"></line><line x1="5" y1="12" x2="19" y2="12"></line></svg>
                    New Chat
                </button>
                <div className="session-list">
                    {sessions.map(session => (
                        <div
                            key={session.id}
                            onClick={() => handleSelectSession(session.id)}
                            className={`session-item ${currentSessionId === session.id ? 'active' : ''}`}
                        >
                            <div className="session-title">{session.title || 'Untitled'}</div>
                            <div className="session-date">{new Date(session.updated_at).toLocaleDateString()}</div>
                        </div>
                    ))}
                </div>

                <div style={{ padding: '1.25rem 0.5rem 0.5rem', borderTop: '1px solid var(--border-light)', marginTop: 'auto' }}>
                    <button
                        onClick={() => onNavigate('materials')}
                        className="new-chat-btn"
                        style={{ background: 'transparent', border: '1px solid var(--border-light)', width: '100%', marginBottom: 0 }}
                    >
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"></path></svg>
                        Materials
                    </button>
                </div>
            </div>

            {/* Main Chat Area */}
            <div className="chat-main">
                <div className="messages-area">
                    {messages.length === 0 && !loading && (
                        <div style={{ textAlign: 'center', marginTop: '22vh', opacity: 0.9 }}>
                            <h2 style={{ fontFamily: 'var(--font-display)', fontSize: '2.5rem', fontWeight: 700, marginBottom: '0.5rem', background: 'linear-gradient(135deg, #fff 0%, #a0a0ab 100%)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>
                                Technical Assistant
                            </h2>
                            <p style={{ color: 'var(--text-secondary)', fontSize: '1.1rem' }}>How can I help with your interview prep today?</p>
                        </div>
                    )}

                    {messages.map((msg) => (
                        <div key={msg.id} className={`message ${msg.role}`}>
                            <div className="message-bubble">
                                <div className="message-avatar">
                                    {msg.role === 'user' ? 'U' : 'AI'}
                                </div>
                                <div className="message-content">
                                    {msg.role === 'user' ? (
                                        <p style={{ whiteSpace: 'pre-wrap' }}>{msg.content}</p>
                                    ) : (
                                        <div className="assistant-content">
                                            <AnswerDisplay
                                                answer={msg.content}
                                                faithfulnessScore={msg.verification_result?.faithfulness}
                                                verificationStatus={msg.verification_result?.status}
                                                confidence={0}
                                                sources={msg.sources}
                                                fullWidth={true}
                                            />
                                        </div>
                                    )}
                                </div>
                            </div>
                        </div>
                    ))}

                    {loading && (
                        <div className="message assistant">
                            <div className="message-bubble">
                                <div className="message-avatar">AI</div>
                                <div className="message-content">
                                    <div className="spinner"></div>
                                </div>
                            </div>
                        </div>
                    )}
                    <div ref={messagesEndRef} />
                </div>

                {/* Input Area */}
                <div className="input-area">
                    <div style={{ width: '100%', maxWidth: '800px', marginBottom: '14px' }}>
                        <FilterPanel
                            filters={filters}
                            onChange={setFilters}
                            collapsed={true}
                            materials={materials}
                        />
                    </div>
                    <QuestionInput onSubmit={handleSendMessage} loading={loading} />
                    <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginTop: '14px', letterSpacing: '0.02em' }}>
                        Local RAG Assistant • Verified against internal knowledge base.
                    </div>
                </div>
            </div>
        </div>
    )
}

export default ChatPage
