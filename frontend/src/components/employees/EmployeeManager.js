import React, { useState } from "react";
import EmployeeForm from "./EmployeeForm";
import EmployeeCard from "./EmployeeCard";

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

export default EmployeeManager; 