import { useState, useEffect } from 'react'
import MaterialCard from '../components/MaterialCard'

function MaterialsBrowser({ onNavigate }) {
    const [materials, setMaterials] = useState([])
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState(null)
    const [uploading, setUploading] = useState(false)

    useEffect(() => {
        fetchMaterials()
    }, [])

    const fetchMaterials = async () => {
        try {
            const response = await fetch('/api/materials')
            if (!response.ok) throw new Error('Failed to fetch materials')
            const data = await response.json()
            setMaterials(data)
        } catch (err) {
            setError(err.message)
        } finally {
            setLoading(false)
        }
    }

    const handleUpload = async (event) => {
        const file = event.target.files[0]
        if (!file) return

        setUploading(true)
        const formData = new FormData()
        formData.append('file', file)
        formData.append('material_type', 'document')
        formData.append('course', '')

        try {
            const response = await fetch('/api/ingest', {
                method: 'POST',
                body: formData,
            })

            if (!response.ok) throw new Error('Upload failed')

            const result = await response.json()
            alert(result.message)
            fetchMaterials() // Refresh list
        } catch (err) {
            alert('Error uploading file: ' + err.message)
        } finally {
            setUploading(false)
            event.target.value = '' // Reset input
        }
    }

    const handleDelete = async (materialId) => {
        if (!confirm('Are you sure you want to delete this material?')) return

        try {
            const response = await fetch(`/api/materials/${materialId}`, {
                method: 'DELETE',
            })

            if (!response.ok) throw new Error('Delete failed')

            fetchMaterials() // Refresh list
        } catch (err) {
            alert('Error deleting material: ' + err.message)
        }
    }

    if (loading) return <div className="loading" style={{ display: 'flex', height: '100vh', justifyContent: 'center', alignItems: 'center' }}>Loading materials...</div>
    if (error) return <div className="error-message" style={{ display: 'flex', height: '100vh', justifyContent: 'center', alignItems: 'center', color: '#ff4b4b' }}>Error: {error}</div>

    return (
        <div className="materials-browser">
            <div className="materials-header">
                <div style={{ display: 'flex', alignItems: 'center', gap: '1.5rem' }}>
                    <button
                        onClick={() => onNavigate('chat')}
                        style={{ background: 'rgba(255,255,255,0.05)', border: '1px solid var(--border-light)', borderRadius: '8px', cursor: 'pointer', display: 'flex', alignItems: 'center', justifyContent: 'center', width: '36px', height: '36px', color: 'var(--text-primary)' }}
                        title="Back to Chat"
                    >
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"><line x1="19" y1="12" x2="5" y2="12"></line><polyline points="12 19 5 12 12 5"></polyline></svg>
                    </button>
                    <h2>Knowledge Base</h2>
                </div>
                <div style={{ display: 'flex', gap: '1.5rem' }}>
                    <label className="new-chat-btn" style={{ margin: 0, cursor: 'pointer' }}>
                        <input
                            type="file"
                            accept=".pdf,.docx,.txt,.md"
                            onChange={handleUpload}
                            disabled={uploading}
                            style={{ display: 'none' }}
                        />
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="17 8 12 3 7 8"></polyline><line x1="12" y1="3" x2="12" y2="15"></line></svg>
                        {uploading ? 'Processing...' : 'Upload Materials'}
                    </label>
                </div>
            </div>

            {materials.length === 0 ? (
                <div className="empty-state" style={{ textAlign: 'center', marginTop: '15vh', opacity: 0.8 }}>
                    <div style={{ fontSize: '4rem', marginBottom: '1rem' }}>📂</div>
                    <h3 style={{ fontSize: '1.5rem', marginBottom: '0.5rem' }}>Your library is empty</h3>
                    <p style={{ color: 'var(--text-secondary)' }}>Upload PDFs or documents to build your technical knowledge base.</p>
                </div>
            ) : (
                <div className="materials-grid">
                    {materials.map((material) => (
                        <MaterialCard
                            key={material.id}
                            material={material}
                            onDelete={() => handleDelete(material.id)}
                        />
                    ))}
                </div>
            )}
        </div>
    )
}

export default MaterialsBrowser
