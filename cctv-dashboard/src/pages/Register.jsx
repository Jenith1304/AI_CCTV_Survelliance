// File: src/pages/Register.jsx

import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../utils/api';
import '../styles/Register.css';
import { toast, ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

const Register = () => {
    const navigate = useNavigate();
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [confirm, setConfirm] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();

        if (password !== confirm) {
            return toast.error("Passwords don't match");
        }

        try {
            await api.post('/auth/register', {
                username: email,
                password,
            });
            toast.success('Registration successful!');
            setTimeout(() => navigate('/login'), 1500);
        } catch (err) {
            const message = err.response?.data?.error || 'User already exists';
            toast.error(message);
        }
    };

    return (
        <div className="register-container">
            <ToastContainer />
            <form className="register-form" onSubmit={handleSubmit}>
                <h2>📝 Register</h2>
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
                <input
                    type="password"
                    placeholder="Confirm Password"
                    value={confirm}
                    onChange={(e) => setConfirm(e.target.value)}
                    required
                />
                <button type="submit">Register</button>
                <p className="register-footer">
                    Already have an account? <a href="/login">Login</a>
                </p>
            </form>
        </div>
    );
};

export default Register;
