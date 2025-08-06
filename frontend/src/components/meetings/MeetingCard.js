import React from "react";

function MeetingCard({ meeting, employees, onJoin }) {
    const meetingEmployees = employees.filter(emp => meeting.employee_ids.includes(emp.id));

    return (
        <div className="meeting-card">
            <div className="meeting-header">
                <h3>{meeting.title}</h3>
                <button onClick={onJoin} className="join-btn">Join</button>
            </div>

            {meeting.description && (
                <div className="meeting-description">{meeting.description}</div>
            )}

            <div className="meeting-participants">
                <strong>Participants:</strong>
                {meetingEmployees.map(emp => (
                    <span key={emp.id} className="participant-tag">{emp.name}</span>
                ))}
            </div>
        </div>
    );
}

export default MeetingCard; 