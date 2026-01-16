function FilterPanel({ filters, onChange, collapsed = false, materials = [] }) {
    const handleFilterChange = (key, value) => {
        const newFilters = { ...filters }
        if (value === '' || value === null) {
            delete newFilters[key]
        } else {
            newFilters[key] = value
        }
        onChange(newFilters)
    }

    const handleMaterialChange = (materialId) => {
        const newFilters = { ...filters }
        if (materialId === '') {
            delete newFilters.material_ids
        } else {
            newFilters.material_ids = [parseInt(materialId)]
        }
        onChange(newFilters)
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
    };

    const labelStyle = {
        fontSize: '0.65rem',
        color: 'var(--text-muted)',
        fontWeight: 700,
        textTransform: 'uppercase',
        letterSpacing: '0.08em',
        marginBottom: '6px',
        display: 'block'
    };

    return (
        <div style={{
            padding: collapsed ? '0' : '1.5rem',
            background: collapsed ? 'transparent' : 'rgba(255,255,255,0.02)',
            borderRadius: '12px',
            border: collapsed ? 'none' : '1px solid var(--border-light)'
        }}>
            <div style={{ display: 'grid', gridTemplateColumns: '1.5fr 1fr', gap: '1rem' }}>
                <div className="filter-item">
                    <label style={labelStyle}>Search Target</label>
                    <select
                        value={filters.material_ids ? filters.material_ids[0] : ''}
                        onChange={(e) => handleMaterialChange(e.target.value)}
                        style={inputStyle}
                    >
                        <option value="">All Materials</option>
                        {materials.map(m => (
                            <option key={m.id} value={m.id}>{m.filename}</option>
                        ))}
                    </select>
                </div>

                <div className="filter-item">
                    <label style={labelStyle}>Specific Topic</label>
                    <input
                        type="text"
                        value={filters.topic || ''}
                        onChange={(e) => handleFilterChange('topic', e.target.value)}
                        placeholder="Search topic..."
                        style={inputStyle}
                    />
                </div>
            </div>
        </div>
    )
}

export default FilterPanel
