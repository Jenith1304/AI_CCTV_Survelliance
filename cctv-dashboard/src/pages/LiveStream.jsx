import React, { useState, useEffect } from 'react';
import api, { setAuthToken } from '../utils/api';
import '../styles/LiveStream.css';

const LiveStream = () => {
    const [cameraURL, setCameraURL] = useState('');
    const [connected, setConnected] = useState(false);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const [userId, setUserId] = useState('');

    // Fetch user ID from profile
    useEffect(() => {
        const token = localStorage.getItem("token");
        if (token) {
            setAuthToken(token);
            api.get("/auth/profile")
                .then(res => {
                    console.log(res.data);
                    setUserId(res.data._id); // Adjust if your profile sends differently
                })
                .catch(() => {
                    setError("Failed to fetch user profile");
                });
        }
    }, []);

    // Handle connecting to camera
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

    // Handle reset
    const handleReset = () => {
        setCameraURL('');
        setConnected(false);
        setError('');
        window.location.reload();
    };

    return (
        <div className="livestream-container">
            <h2 className="livestream-title">📡 Live Stream Viewer</h2>

            <div className="stream-input-card">
                <label htmlFor="cameraURL">Camera Stream URL:</label>
                <input
                    type="text"
                    id="cameraURL"
                    placeholder="e.g., 0 (webcam) or rtsp://ip or http://192.168.30.244:8080/video"
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
                        src={`http://localhost:5000/api/stream/video-feed?user=${userId}`}

                        alt="Live Feed"
                        className="video-frame"
                    />

                </div>
            )}
        </div>
    );
};

export default LiveStream;



