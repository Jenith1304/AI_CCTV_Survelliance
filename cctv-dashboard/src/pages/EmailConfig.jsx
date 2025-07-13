import React, { useEffect, useState } from 'react';
import api, { setAuthToken } from '../utils/api';
import '../styles/EmailConfig.css';

const EmailConfig = () => {
    const [form, setForm] = useState({ sender: '', app_password: '', receiver: '' });
    const [config, setConfig] = useState(null);
    const [message, setMessage] = useState('');

    useEffect(() => {
        const token = localStorage.getItem('token');
        if (token) {
            setAuthToken(token);
            fetchConfig();
        }
    }, []);

    const fetchConfig = async () => {
        try {
            const res = await api.get('/email-config');
            setConfig(res.data);
        } catch {
            setConfig(null);
        }
    };

    const handleChange = (e) => {
        setForm({ ...form, [e.target.name]: e.target.value });
    };

    const handleSubmit = async () => {
        if (!form.sender || !form.app_password || !form.receiver) {
            setMessage("All fields are required.");
            return;
        }
        try {
            const res = await api.post('/email-config', form);
            setMessage(res.data.message);
            fetchConfig();
        } catch (err) {
            setMessage(err.response?.data?.error || "Error saving config.");
        }
    };

    const handleDelete = async () => {
        try {
            const res = await api.delete('/email-config');
            setMessage(res.data.message);
            setConfig(null);
        } catch (err) {
            setMessage("Failed to delete config.");
        }
    };

    return (
        <div className="email-config-container">
            <h2>Email Configuration</h2>

            <div className="instructions-box">
                <h4>📧 How to get Gmail App Password:</h4>
                <ul>
                    <li>Go to <a href="https://myaccount.google.com/security" target="_blank" rel="noreferrer">Google Account Security</a></li>
                    <li>Enable 2-Step Verification</li>
                    <li>Click on "App passwords"</li>
                    <li>Generate a 16-digit password and paste it below without space</li>
                </ul>
            </div>

            {!config ? (
                <div className="form-section">
                    <input name="sender" placeholder="Sender Gmail" value={form.sender} onChange={handleChange} />
                    <input name="app_password" placeholder="App Password" value={form.app_password} onChange={handleChange} />
                    <input name="receiver" placeholder="Receiver Email" value={form.receiver} onChange={handleChange} />
                    <button onClick={handleSubmit}>Save Configuration</button>
                </div>
            ) : (
                <div className="config-box">
                    <h4>Current Config:</h4>
                    <p><strong>Sender:</strong> {config.sender}</p>
                    <p><strong>Receiver:</strong> {config.receiver}</p>
                    <button className="delete-btn" onClick={handleDelete}>Delete Configuration</button>
                </div>
            )}

            {message && <p className="message">{message}</p>}
        </div>
    );
};

export default EmailConfig;
