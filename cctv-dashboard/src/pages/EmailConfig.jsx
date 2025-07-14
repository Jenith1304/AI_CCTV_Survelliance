// File: src/pages/EmailConfig.jsx

import React, { useEffect, useState } from 'react';
import api, { setAuthToken } from '../utils/api';
import '../styles/EmailConfig.css';
import { toast, ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

const EmailConfig = () => {
    const [form, setForm] = useState({ sender: '', app_password: '', receiver: '' });
    const [config, setConfig] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const token = localStorage.getItem('token');
        if (token) {
            setAuthToken(token);
            fetchConfig();
        }
    }, []);

    const fetchConfig = async () => {
        setLoading(true);
        try {
            const res = await api.get('/email-config');
            setConfig(Object.keys(res.data).length ? res.data : null);
        } catch {
            setConfig(null);
        } finally {
            setLoading(false);
        }
    };

    const handleChange = (e) => {
        setForm({ ...form, [e.target.name]: e.target.value });
    };

    const handleSubmit = async () => {
        if (!form.sender || !form.app_password || !form.receiver) {
            toast.error("All fields are required.");
            return;
        }
        try {
            const res = await api.post('/email-config', form);
            toast.success(res.data.message);
            setForm({ sender: '', app_password: '', receiver: '' });
            fetchConfig();
        } catch (err) {
            toast.error(err.response?.data?.error || "Error saving config.");
        }
    };

    const handleDelete = async () => {
        try {
            const res = await api.delete('/email-config');
            toast.success(res.data.message);
            setConfig(null);
        } catch (err) {
            toast.error("Failed to delete config.");
        }
    };

    return (
        <div className="email-config-container">
            <ToastContainer />
            <h2>Email Configuration</h2>

            <div className="instructions-box">
                <h4>📧 How to get Gmail App Password:</h4>
                <ul>
                    <li>Go to <a href="https://myaccount.google.com/security" target="_blank" rel="noreferrer">Google Account Security</a></li>
                    <li>Enable 2-Step Verification</li>
                    <li>Click on "App passwords"</li>
                    <li>Generate a 16-digit password and paste it below without spaces</li>
                </ul>
            </div>

            {loading ? (
                <p>Loading...</p>
            ) : !config ? (
                <>
                    <p className="no-config">No configuration found.</p>
                    <div className="form-section">
                        <input
                            name="sender"
                            placeholder="Sender Gmail"
                            value={form.sender}
                            onChange={handleChange}
                        />
                        <input
                            name="app_password"
                            placeholder="App Password"
                            type="password"
                            value={form.app_password}
                            onChange={handleChange}
                        />
                        <input
                            name="receiver"
                            placeholder="Receiver Email"
                            value={form.receiver}
                            onChange={handleChange}
                        />
                        <button onClick={handleSubmit}>Save Configuration</button>
                    </div>
                </>
            ) : (
                <div className="config-box">
                    <h4>Current Config:</h4>
                    <p><strong>Sender:</strong> {config.sender}</p>
                    <p><strong>Receiver:</strong> {config.receiver}</p>
                    <button className="delete-btn" onClick={handleDelete}>Delete Configuration</button>
                </div>
            )}
        </div>
    );
};

export default EmailConfig;
