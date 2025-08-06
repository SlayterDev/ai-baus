import React, { useState, useEffect, useCallback } from "react";
import './App.css';

import api from "./Api";

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
    )
}

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

function MeetingRoom({ meeting, employees, onExit }) {
    const [messages, setMessages] = useState([]);
    const [newMessage, setNewMessage] = useState('');
    const [loading, setLoading] = useState(false);

    const meetingEmployees = employees.filter(emp => meeting.employee_ids.includes(emp.id));

    const loadMessages = useCallback(async () => {
        try {
            const response = await api.get(`/meetings/${meeting.id}/messages`);
            // Handle different response structures
            const messagesData = response.data || response || [];
            setMessages(Array.isArray(messagesData) ? messagesData : []);
        } catch (error) {
            console.error("Error loading messages:", error);
            setMessages([]); // Set empty array on error
        }
    }, [meeting.id]);

    useEffect(() => {
        loadMessages();
    }, [loadMessages]);

    const sendMessage = async (e) => {
        e.preventDefault();
        if (!newMessage.trim() || loading) return;

        try {
            setLoading(true);
            await api.post(`/meetings/${meeting.id}/messages`, {
                meeting_id: meeting.id,
                content: newMessage,
                sender_type: 'user'
            });

            setNewMessage('');
            await loadMessages();
        } catch (error) {
            alert("Error sending message: " + error.message);
        } finally {
            setLoading(false);
        }
    }

    const requestResponse = async (employeeId) => {
        try {
            setLoading(true);
            await api.post(`/meetings/${meeting.id}/messages/${employeeId}/respond`);
            await loadMessages();
        } catch (error) {
            alert("Error responding to message: " + error.message);
        } finally {
            setLoading(false);
        }
    };

    // Render meeting room content from markdown if meeting.description is markdown
    const renderMarkdown = (markdown) => {
        // Simple markdown rendering using marked (if available)
        // You can install 'marked' with: npm install marked
        try {
            // Dynamically import marked if available
            const marked = window.marked || require('marked');
            return <div dangerouslySetInnerHTML={{ __html: marked.parse(markdown) }} />;
        } catch {
            // Fallback: render as plain text
            return <div>{markdown}</div>;
        }
    };

    return (
        <div className="meeting-room">
            <div className="meeting-room-header">
                <div>
                    <h2>{meeting.title}</h2>
                    <div className="meeting-participants">
                        {meetingEmployees.map(emp => (
                            <span key={emp.id} className="participant-tag">{emp.name}</span>
                        ))}
                    </div>
                </div>
                <button onClick={onExit} className="exit-btn">Exit Meeting</button>
            </div>

            {meeting.description && (
                <div className="meeting-description">
                    {meeting.description}
                </div>
            )}

            <div className="messages-container">
                {messages && messages.length > 0 ? (
                    messages.map(msg => (
                        <div key={msg.id} className={`message ${msg.sender_type}`}>
                            <div className="message-header">
                                <strong>{msg.sender_name}</strong>
                                {msg.sender_type === 'employee' && (
                                    <span className="employee-role">
                                        {meetingEmployees.find(emp => emp.id === msg.sender_id)?.role || 'Unknown'}
                                    </span>
                                )}
                            </div>
                            <span className="timestamp">
                                {new Date(msg.created_at).toLocaleTimeString()}
                            </span>
                            <div className="message-content">
                                {renderMarkdown(msg.content)}
                            </div>
                        </div>
                    ))
                ) : (
                    <div className="empty-messages">
                        <p>No messages yet. Start the conversation!</p>
                    </div>
                )}
            </div>

            <div className="meeting-controls">
                <div className="employee-responses">
                    <div className="response-buttons">
                        {meetingEmployees.map(emp => (
                            <button
                                key={emp.id}
                                onClick={() => requestResponse(emp.id)}
                                className="response-btn"
                                disabled={loading}
                            >
                                {loading ? 'Requesting...' : `Ask ${emp.name}`}
                            </button>
                        ))}
                    </div>
                </div>
            </div>

            <form className="message-form" onSubmit={sendMessage}>
                <input
                    type="text"
                    value={newMessage}
                    onChange={(e) => setNewMessage(e.target.value)}
                    placeholder="Type your message..."
                    disabled={loading}
                />
                <button type="submit" disabled={!newMessage.trim() || loading}>
                    {loading ? 'Sending...' : 'Send'}
                </button>
            </form>
        </div>
    )
}

export default MeetingManager;
