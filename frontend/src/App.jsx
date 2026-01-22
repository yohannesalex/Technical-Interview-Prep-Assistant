import { useEffect, useState } from 'react'
import ChatPage from './pages/ChatPage'
import MaterialsBrowser from './pages/MaterialsBrowser'
import PdfViewerPage from './pages/PdfViewerPage'

function App() {
    const [currentPage, setCurrentPage] = useState('chat')
    const [isPdfPreview, setIsPdfPreview] = useState(false)

    useEffect(() => {
        const checkHash = () => {
            const hash = window.location.hash || ''
            setIsPdfPreview(hash.startsWith('#/preview'))
        }

        checkHash()
        window.addEventListener('hashchange', checkHash)
        return () => window.removeEventListener('hashchange', checkHash)
    }, [])

    return (
        <div className="app">
            <main className="main-content">
                {isPdfPreview ? (
                    <PdfViewerPage />
                ) : currentPage === 'chat' && (
                    <ChatPage onNavigate={(page) => setCurrentPage(page)} />
                )}
                {currentPage === 'materials' && (
                    <MaterialsBrowser onNavigate={(page) => setCurrentPage(page)} />
                )}
            </main>
        </div>
    )
}

export default App
