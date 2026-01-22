import { useState, useRef, useEffect } from 'react'

function FilterPanel({ filters, onChange, collapsed = false, materials = [] }) {
    const [isDropdownOpen, setIsDropdownOpen] = useState(false)
    const [dropUp, setDropUp] = useState(false)
    const [dropdownMaxHeight, setDropdownMaxHeight] = useState(250)
    const dropdownRef = useRef(null)

    // Close dropdown when clicking outside
    useEffect(() => {
        const handleClickOutside = (event) => {
            if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
                setIsDropdownOpen(false)
            }
        }
        document.addEventListener('mousedown', handleClickOutside)
        return () => document.removeEventListener('mousedown', handleClickOutside)
    }, [])

    const toggleMaterial = (materialId) => {
        const currentIds = filters.material_ids || []
        let newIds

        if (currentIds.includes(materialId)) {
            newIds = currentIds.filter(id => id !== materialId)
        } else {
            newIds = [...currentIds, materialId]
        }

        const newFilters = { ...filters }
        if (newIds.length === 0) {
            delete newFilters.material_ids
        } else {
            newFilters.material_ids = newIds
        }
        onChange(newFilters)
    }

    const getSelectedLabel = () => {
        const selectedIds = filters.material_ids || []
        if (selectedIds.length === 0) return 'All Materials'
        if (selectedIds.length === 1) {
            const mat = materials.find(m => m.id === selectedIds[0])
            return mat ? mat.filename : '1 Selected'
        }
        return `${selectedIds.length} Materials Selected`
    }

    const labelStyle = {
        fontSize: '0.65rem',
        color: 'var(--text-muted)',
        fontWeight: 700,
        textTransform: 'uppercase',
        letterSpacing: '0.08em',
        marginBottom: '6px',
        display: 'block'
    }

    const inputStyle = {
        background: 'rgba(25, 25, 30, 0.6)',
        border: '1px solid var(--border-light)',
        borderRadius: '10px',
        color: 'var(--text-primary)',
        padding: '10px 14px',
        fontSize: '0.88rem',
        outline: 'none',
        width: '100%',
        transition: 'var(--transition)',
        backdropFilter: 'blur(10px)'
    }

    return (
        <div style={{
            padding: collapsed ? '0' : '1.5rem',
            background: collapsed ? 'transparent' : 'rgba(255,255,255,0.02)',
            borderRadius: '12px',
            border: collapsed ? 'none' : '1px solid var(--border-light)',
            position: 'relative'
        }}>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr', gap: '1rem' }}>
                <div className="filter-item">
                    <label style={labelStyle}>Search Target</label>

                    <div className="multi-select-container" ref={dropdownRef}>
                        <div
                            className="multi-select-header"
                            onClick={() => {
                                const nextOpen = !isDropdownOpen
                                setIsDropdownOpen(nextOpen)

                                if (nextOpen && dropdownRef.current) {
                                    const rect = dropdownRef.current.getBoundingClientRect()
                                    const spaceBelow = window.innerHeight - rect.bottom
                                    const spaceAbove = rect.top
                                    const shouldDropUp = spaceBelow < 260 && spaceAbove > spaceBelow
                                    setDropUp(shouldDropUp)
                                    const available = shouldDropUp ? spaceAbove - 16 : spaceBelow - 16
                                    setDropdownMaxHeight(Math.max(180, Math.min(320, available)))
                                }
                            }}
                        >
                            <span>{getSelectedLabel()}</span>
                            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" style={{ transform: isDropdownOpen ? 'rotate(180deg)' : 'none', transition: 'transform 0.2s' }}>
                                <polyline points="6 9 12 15 18 9"></polyline>
                            </svg>
                        </div>

                        {isDropdownOpen && (
                            <div
                                className={`multi-select-dropdown ${dropUp ? 'drop-up' : ''}`}
                                style={{ maxHeight: `${dropdownMaxHeight}px` }}
                            >
                                <div
                                    className={`multi-select-option ${(!filters.material_ids || filters.material_ids.length === 0) ? 'selected' : ''}`}
                                    onClick={() => {
                                        const newFilters = { ...filters }
                                        delete newFilters.material_ids
                                        onChange(newFilters)
                                        setIsDropdownOpen(false)
                                    }}
                                >
                                    <div className="multi-select-checkbox">
                                        {(!filters.material_ids || filters.material_ids.length === 0) && (
                                            <svg className="check-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="4" strokeLinecap="round" strokeLinejoin="round">
                                                <polyline points="20 6 9 17 4 12"></polyline>
                                            </svg>
                                        )}
                                    </div>
                                    <span>All Materials ({materials.length})</span>
                                </div>

                                {materials.map(m => {
                                    const isSelected = filters.material_ids?.includes(m.id)
                                    return (
                                        <div
                                            key={m.id}
                                            className={`multi-select-option ${isSelected ? 'selected' : ''}`}
                                            onClick={() => toggleMaterial(m.id)}
                                        >
                                            <div className="multi-select-checkbox">
                                                {isSelected && (
                                                    <svg className="check-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="4" strokeLinecap="round" strokeLinejoin="round">
                                                        <polyline points="20 6 9 17 4 12"></polyline>
                                                    </svg>
                                                )}
                                            </div>
                                            <span>{m.filename}</span>
                                        </div>
                                    )
                                })}
                            </div>
                        )}
                    </div>
                    <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)', marginTop: '6px' }}>
                        {materials.length} materials available. Leave unselected to search all.
                    </div>
                </div>
            </div>
        </div>
    )
}

export default FilterPanel
