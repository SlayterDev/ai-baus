import React, { useState, useEffect, useCallback } from "react";
import api from "../../Api";

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
                                {new Date(msg.timestamp).toLocaleTimeString()}
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
    );
}

export default MeetingRoom; 