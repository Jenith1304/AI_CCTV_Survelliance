import React, { useState, useEffect } from 'react';
import api, { setAuthToken } from '../utils/api';
import '../styles/LiveStream.css';

const LiveStream = () => {
    const [cameraURL, setCameraURL] = useState('');
    const [connected, setConnected] = useState(false);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const [userId, setUserId] = useState('');

    const API_BASE = import.meta.env.VITE_API_BASE_URL;

    useEffect(() => {
        const token = localStorage.getItem("token");
        if (token) {
            setAuthToken(token);
            api.get("/auth/profile")
                .then(res => {
                    setUserId(res.data._id);
                })
                .catch(() => {
                    setError("Failed to fetch user profile");
                });
        }
    }, []);

    const handleConnect = async () => {
        if (!cameraURL.trim()) {
            setError("Please enter a camera URL.");
            return;
        }

        setLoading(true);
        setError('');

        try {
            const token = localStorage.getItem("token");
            setAuthToken(token);

            const res = await api.post('/stream/set-camera', { camera_url: cameraURL });
            if (res.data?.message) {
                setConnected(true);
            } else {
                setError("Unexpected response from server.");
            }
        } catch (err) {
            console.error(err);
            setError(err.response?.data?.error || "Failed to connect.");
        } finally {
            setLoading(false);
        }
    };

    const handleReset = () => {
        setCameraURL('');
        setConnected(false);
        setError('');
        window.location.reload();
    };

    return (
        <div className="livestream-container">
            <h2 className="livestream-title">📡 Live Stream Viewer</h2>

            <div className="ngrok-guide">
                <h4>🌐 Convert Local Camera URL to Public using ngrok:</h4>
                <ol>
                    <li>Install <a href="https://ngrok.com/download" target="_blank" rel="noreferrer">ngrok</a></li>
                    <li>Run: <code>ngrok http://192.168.30.7:8080</code></li>
                    <li>Copy the public URL shown (e.g., <code>https://abcd1234.ngrok.io</code>)</li>
                    <li>Append <code>/video</code> if needed (e.g., <code>https://abcd1234.ngrok.io/video</code>)</li>
                    <li>Paste the full URL above and click "Start Stream"</li>
                </ol>
            </div>

            <div className="stream-input-card">
                <label htmlFor="cameraURL">Camera Stream URL:</label>
                <input
                    type="text"
                    id="cameraURL"
                    placeholder="e.g., http://192.168.30.244:8080/video or ngrok URL"
                    value={cameraURL}
                    onChange={(e) => setCameraURL(e.target.value)}
                    disabled={connected}
                />
                <div className="button-group">
                    <button onClick={handleConnect} disabled={loading || connected}>
                        {loading ? 'Connecting...' : 'Start Stream'}
                    </button>
                    {connected && <button onClick={handleReset} className="reset-button">Reset</button>}
                </div>
                {error && <p className="error-msg">{error}</p>}
            </div>

            {connected && userId && (
                <div className="stream-frame">
                    <h4>Live Feed:</h4>
                    <img
                        src={`${API_BASE}/stream/video-feed?user=${userId}`}
                        alt="Live Feed"
                        className="video-frame"
                    />
                </div>
            )}
        </div>
    );
};

export default LiveStream;
