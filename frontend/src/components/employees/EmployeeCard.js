import React from "react";
import api from "../../Api";

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
                {employee.llm_provider} - {employee.llm_model}
            </div>
        </div>
    );
}

export default EmployeeCard; 