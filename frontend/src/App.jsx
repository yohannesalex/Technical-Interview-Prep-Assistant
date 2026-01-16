import { useState } from 'react'
import ChatPage from './pages/ChatPage'
import MaterialsBrowser from './pages/MaterialsBrowser'

function App() {
    const [currentPage, setCurrentPage] = useState('chat')

    return (
        <div className="app">
            <main className="main-content">
                {currentPage === 'chat' && (
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
