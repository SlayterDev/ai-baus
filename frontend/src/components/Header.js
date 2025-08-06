import React from "react";

function Header({ currentView, setCurrentView }) {
    return (
        <header className="App-header">
            <h1>AI Boss</h1>
            <nav>
                <button 
                    className={currentView === 'employees' ? 'active' : ''} 
                    onClick={() => setCurrentView('employees')}
                >
                    Employees
                </button>
                <button 
                    className={currentView === 'meetings' ? 'active' : ''} 
                    onClick={() => setCurrentView('meetings')}
                >
                    Meetings
                </button>
            </nav>
        </header>
    );
}

export default Header; 