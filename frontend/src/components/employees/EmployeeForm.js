import React, { useState } from "react";
import api from "../../Api";

function EmployeeForm({ onClose, onSuccess }) {
    const [formData, setFormData] = useState({
        name: '',
        role: '',
        personality: '',
        expertise: '',
        llm_provider: 'openai',
        llm_model: 'gpt-3.5-turbo',
    });
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        
        try {
            const submitData = {
                ...formData,
                expertise: typeof formData.expertise === 'string' 
                    ? formData.expertise.split(',').map(item => item.trim()).filter(s => s)
                    : formData.expertise
            };

            await api.post('/employees', submitData);
            onSuccess();
        } catch (error) {
            alert("Error creating employee: " + error.message);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="modal">
            <div className="modal-content">
                <div className="modal-header">
                    <h3>Create New AI Employee</h3>
                    <button onClick={onClose}>×</button>
                </div>
                
                <form onSubmit={handleSubmit}>
                    <div className="form-group">
                        <label>Name *</label>
                        <input
                            type="text"
                            value={formData.name}
                            onChange={(e) => setFormData({...formData, name: e.target.value})}
                            placeholder="e.g., Sarah Johnson"
                            required
                        />
                    </div>

                    <div className="form-group">
                        <label>Role *</label>
                        <input
                            type="text"
                            value={formData.role}
                            onChange={(e) => setFormData({...formData, role: e.target.value})}
                            placeholder="e.g., Project Manager, Researcher, Developer"
                            required
                        />
                    </div>

                    <div className="form-group">
                        <label>Personality *</label>
                        <textarea
                            value={formData.personality}
                            onChange={(e) => setFormData({...formData, personality: e.target.value})}
                            placeholder="Describe their communication style, approach to work, etc."
                            required
                        />
                    </div>

                    <div className="form-group">
                        <label>Areas of Expertise (comma-separated)</label>
                        <input
                            type="text"
                            value={formData.expertise}
                            onChange={(e) => setFormData({...formData, expertise: e.target.value})}
                            placeholder="e.g., Python, Machine Learning, Data Analysis"
                        />
                    </div>

                    <div className="form-row">
                        <div className="form-group">
                            <label>LLM Provider *</label>
                            <select
                                value={formData.llm_provider}
                                onChange={(e) => setFormData({...formData, llm_provider: e.target.value})}
                            >
                                <option value="openai">OpenAI</option>
                                <option value="anthropic">Anthropic</option>
                            </select>
                        </div>

                        <div className="form-group">
                            <label>Model *</label>
                            <select
                                value={formData.llm_model}
                                onChange={(e) => setFormData({...formData, llm_model: e.target.value})}
                            >
                                {formData.llm_provider === 'openai' ? (
                                    <>
                                        <option value="gpt-3.5-turbo">GPT-3.5 Turbo</option>
                                        <option value="gpt-4">GPT-4</option>
                                        <option value="gpt-4-turbo">GPT-4 Turbo</option>
                                    </>
                                ) : (
                                    <>
                                        <option value="claude-3-sonnet-20240229">Claude 3 Sonnet</option>
                                        <option value="claude-3-opus-20240229">Claude 3 Opus</option>
                                    </>
                                )}
                            </select>
                        </div>
                    </div>

                    <div className="form-actions">
                        <button type="button" onClick={onClose}>Cancel</button>
                        <button type="submit" disabled={loading}>
                            {loading ? 'Creating...' : 'Create Employee'}
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
}

export default EmployeeForm; 