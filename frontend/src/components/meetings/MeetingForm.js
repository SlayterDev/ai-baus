import React, { useState } from "react";
import api from "../../Api";

function MeetingForm({ employees, onClose, onSuccess }) {
    const [formData, setFormData] = useState({
        title: '',
        description: '',
        employee_ids: []
    });

    const handleEmployeeToggle = (empId) => {
        const newIds = formData.employee_ids.includes(empId)
            ? formData.employee_ids.filter(id => id !== empId)
            : [...formData.employee_ids, empId];

        setFormData({ ...formData, employee_ids: newIds });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        
        if (formData.employee_ids.length < 2) {
            alert("At least 2 employees are required for a meeting.");
            return;
        }

        try {
            await api.post('/meetings', formData);
            onSuccess();
        } catch (error) {
            alert("Error creating meeting: " + error.message);
        }
    };

    return (
        <div className="modal">
            <div className="modal-content">
                <div className="modal-header">
                    <h3>Create New Meeting</h3>
                    <button onClick={onClose}>×</button>
                </div>

                <form onSubmit={handleSubmit}>
                    <div className="form-group">
                        <label>Meeting Title *</label>
                        <input
                            type="text"
                            value={formData.title}
                            onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                            placeholder="e.g., Weekly Planning Meeting"
                            required
                        />
                    </div>

                    <div className="form-group">
                        <label>Description</label>
                        <textarea
                            value={formData.description}
                            onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                            placeholder="What will you discuss in this meeting?"
                        />
                    </div>

                    <div className="form-group">
                        <label>Select Employees ({formData.employee_ids.length} selected)</label>
                        <div className="employee-selector">
                            {employees.map(emp => (
                                <label key={emp.id} className="checkbox-label">
                                    <input
                                        type="checkbox"
                                        checked={formData.employee_ids.includes(emp.id)}
                                        onChange={() => handleEmployeeToggle(emp.id)}
                                    />
                                    <span>{emp.name} - {emp.role}</span>
                                </label>
                            ))}
                        </div>
                    </div>

                    <div className="form-actions">
                        <button type="button" onClick={onClose}>Cancel</button>
                        <button type="submit">Create Meeting</button>
                    </div>
                </form>
            </div>
        </div>
    );
}

export default MeetingForm; 