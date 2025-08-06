import React, { useState, useEffect } from "react";
import './App.css';

import { Header, EmployeeManager, MeetingManager } from "./components";
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
            <Header 
                currentView={currentView} 
                setCurrentView={setCurrentView} 
            />
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
    );
}

export default App;
