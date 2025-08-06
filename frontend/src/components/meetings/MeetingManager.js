import React, { useState } from "react";
import MeetingForm from "./MeetingForm";
import MeetingCard from "./MeetingCard";
import MeetingRoom from "./MeetingRoom";

function MeetingManager({ meetings, employees, onMeetingsChange }) {
    const [showForm, setShowForm] = useState(false);
    const [activeMeeting, setActiveMeeting] = useState(null);

    return (
        <div className="meeting-manager">
            {!activeMeeting ? (
                <>
                    <div className="section-header">
                        <h2>Meetings</h2>
                        <button 
                            onClick={() => setShowForm(true)}
                            disabled={employees.length < 2}
                            title={employees.length < 2 ? "At least 2 employees are required to create a meeting" : ""}
                        >
                            + New Meeting
                        </button>
                    </div>

                    {showForm && (
                        <MeetingForm
                            employees={employees}
                            onClose={() => setShowForm(false)}
                            onSuccess={() => {
                                setShowForm(false);
                                onMeetingsChange();
                            }}
                        />
                    )}

                    <div className="meeting-list">
                        {meetings.map(meeting => (
                            <MeetingCard
                                key={meeting.id}
                                meeting={meeting}
                                employees={employees}
                                onJoin={() => setActiveMeeting(meeting)}
                            />
                        ))}
                    </div>

                    {meetings.length === 0 && !showForm && (
                        <div className="no-meetings">
                            <p>No meetings yet. {employees.length >= 2 ? 'Create your first meeting!' : 'Create at least 2 employees first.'}</p>
                        </div>
                    )}
                </>
            ) : (
                <MeetingRoom
                    meeting={activeMeeting}
                    employees={employees}
                    onExit={() => setActiveMeeting(null)}
                />
            )}
        </div>
    );
}

export default MeetingManager; 