import React, { useState, useEffect } from "react";
import './App.css';

import MeetingManager from "./Meetings";
import api from "./Api";

function App() {
    const [currentView, setCurrentView] = useState('employees');
    const [employees, setEmployees] = useState([]);
    const [meetings, setMeetings] = useState([]);

    useEffect(() => {
        loadEmployees();
        loadMeetings();
    }, []);

    const loadEmployees = async () => {
        try {
            const data = await api.get('/employees');
            setEmployees(data);
        } catch (error) {
            console.error("Error loading employees:", error);
        }
    };

    const loadMeetings = async () => {
        try {
            const data = await api.get('/meetings');
            setMeetings(data);
        } catch (error) {
            console.error("Error loading meetings:", error);
        }
    };

    return (
        <div className="App">
            <header className="App-header">
                <h1>AI Boss</h1>
                <nav>
                    <button className={currentView === 'employees' ? 'active' : ''} onClick={() => setCurrentView('employees')}>Employees</button>
                    <button className={currentView === 'meetings' ? 'active' : ''} onClick={() => setCurrentView('meetings')}>Meetings</button>
                </nav>
            </header>
            <main>
                {currentView === 'employees' && (
                    <EmployeeManager
                        employees={employees}
                        onEmployeeChange={loadEmployees}
                    />
                )}
                {currentView === 'meetings' && (
                    <MeetingManager
                        meetings={meetings}
                        employees={employees}
                        onMeetingsChange={loadMeetings}
                    />
                )}
            </main>
        </div>
    )
}

function EmployeeManager({ employees, onEmployeeChange }) {
    const [showForm, setShowForm] = useState(false);

    return (
        <div className="employee-manager">
            <div className="section-header">
                <h2>AI Employees</h2>
                <button onClick={() => setShowForm(true)}>
                    + Create New Employee
                </button>
            </div>
            {showForm && (
                <EmployeeForm
                    onClose={() => setShowForm(false)}
                    onSuccess={() => {
                        setShowForm(false);
                        onEmployeeChange();
                    }}
                />
            )}

            <div className="employee-grid">
                {employees.map(emp => (
                    <EmployeeCard
                        key={emp.id}
                        employee={emp}
                        onDelete={onEmployeeChange}
                    />
                ))}
            </div>

            {employees.length === 0 && !showForm && (
                <div className="empty-state">
                    <p>No AI employees found. Click the button above to create one.</p>
                </div>
            )}
        </div>
    );
}

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
    )
}

function EmployeeCard({ employee, onDelete }) {
    const handleDelete = async () => {
        if (window.confirm(`Are you sure you want to delete ${employee.name}?`)) {
            try {
                await api.delete(`/employees/${employee.id}`);
                onDelete(employee.id);
            } catch (error) {
                alert("Error deleting employee: " + error.message);
            }
        }
    };

    return (
        <div className="employee-card">
            <div className="employee-header">
                <h3>{employee.name}</h3>
                <button onClick={handleDelete}>×</button>
            </div>
            <div className="employee-role">{employee.role}</div>
            <div className="employee-personality">{employee.personality}</div>

            {employee.expertise && employee.expertise.length > 0 && (
                <div className="employee-expertise">
                    {employee.expertise.map((skill, index) => (
                        <span key={index} className="expertise-tag">
                            {skill}
                        </span>
                    ))}
                </div>
            )}

            <div className="employee-model">
                {employee.llmProvider} - {employee.llmModel}
            </div>
        </div>
    )
}

export default App;
