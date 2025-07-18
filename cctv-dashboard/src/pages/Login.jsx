// File: src/pages/Login.jsx

import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api, { setAuthToken } from '../utils/api';
import '../styles/Login.css';
import { toast, ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

const Login = () => {
    const navigate = useNavigate();
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();

        try {
            const res = await api.post('/auth/login', {
                username: email,
                password,
            });
            const token = res.data.token;
            localStorage.setItem('token', token);
            setAuthToken(token);
            toast.success('Login successful!');
            setTimeout(() => navigate('/dashboard'), 1500);
        } catch (err) {
            const message = err.response?.data?.error || 'Invalid credentials';
            toast.error(message);
        }
    };

    return (
        <div className="login-container">
            <ToastContainer />
            <form className="login-form" onSubmit={handleSubmit}>
                <h2>🔐 Login</h2>
                <input
                    type="email"
                    placeholder="Email Address"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                />
                <input
                    type="password"
                    placeholder="Password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                />
                <button type="submit">Login</button>
                <p className="login-footer">
                    Don't have an account? <a href="/register">Register</a>
                </p>
            </form>
        </div>
    );
};

export default Login;
