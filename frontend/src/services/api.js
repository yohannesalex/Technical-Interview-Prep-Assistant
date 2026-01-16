const API_BASE = '/api'

export const api = {
    // Chat Sessions
    createSession: async (title = null) => {
        const res = await fetch(`${API_BASE}/chat/sessions`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ title })
        })
        if (!res.ok) throw new Error('Failed to create session')
        return res.json()
    },

    getSessions: async () => {
        const res = await fetch(`${API_BASE}/chat/sessions`)
        if (!res.ok) throw new Error('Failed to fetch sessions')
        return res.json()
    },

    getSession: async (sessionId) => {
        const res = await fetch(`${API_BASE}/chat/sessions/${sessionId}`)
        if (!res.ok) throw new Error('Failed to fetch session')
        return res.json()
    },

    updateSessionTitle: async (sessionId, title) => {
        const res = await fetch(`${API_BASE}/chat/sessions/${sessionId}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ title })
        })
        if (!res.ok) throw new Error('Failed to update session')
        return res.json()
    },

    // Chat History
    getHistory: async (sessionId) => {
        const res = await fetch(`${API_BASE}/chat/sessions/${sessionId}/history`)
        if (!res.ok) throw new Error('Failed to fetch history')
        return res.json()
    },

    // Messaging
    sendMessage: async (question, sessionId, filters = null) => {
        const res = await fetch(`${API_BASE}/ask`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                question,
                filters,
                top_k: 12,
                session_id: sessionId
            })
        })
        if (!res.ok) {
            const err = await res.json()
            throw new Error(err.detail || 'Failed to send message')
        }
        return res.json()
    },

    // Files
    getFileUrl: (materialId) => `${API_BASE}/files/${materialId}`,

    getMaterials: async () => {
        const res = await fetch(`${API_BASE}/materials`)
        if (!res.ok) throw new Error('Failed to fetch materials')
        return res.json()
    }
}
