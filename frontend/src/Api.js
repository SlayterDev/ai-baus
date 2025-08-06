const API_BASE = process.env.REACT_APP_API_BASE || "http://localhost:8000";

const api = {
    get: (endpoint) => fetch(`${API_BASE}${endpoint}`).then(res => res.json()),
    post: (endpoint, data) => 
        fetch(`${API_BASE}${endpoint}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        }).then(res => res.json()),
    delete: (endpoint) => 
        fetch(`${API_BASE}${endpoint}`, {
            method: 'DELETE',
        }).then(res => res.json())
};

export default api;
