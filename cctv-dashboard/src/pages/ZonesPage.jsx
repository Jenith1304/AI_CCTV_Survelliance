import React, { useEffect, useState } from 'react';
import api, { setAuthToken } from '../utils/api';
import '../styles/Zones.css';
import { useNavigate } from 'react-router-dom';

const ZonesPage = () => {
    const [zones, setZones] = useState([]);
    const [form, setForm] = useState({ zone_name: '', x1: '', y1: '', x2: '', y2: '' });
    const [error, setError] = useState('');
    const navigate = useNavigate();

    useEffect(() => {
        const token = localStorage.getItem('token');
        if (!token) return navigate('/login');
        setAuthToken(token);
        fetchZones();
    }, []);

    const fetchZones = async () => {
        try {
            const res = await api.get('/zones');
            setZones(res.data);
        } catch (err) {
            console.error('Failed to fetch zones:', err);
        }
    };

    const handleChange = (e) => {
        setForm({ ...form, [e.target.name]: e.target.value });
    };

    const handleAddZone = async (e) => {
        e.preventDefault();
        const { zone_name, x1, y1, x2, y2 } = form;
        if (!zone_name || !x1 || !y1 || !x2 || !y2) {
            return setError('All fields are required');
        }
        try {
            await api.post('/zones', {
                zone_name,
                x1: parseInt(x1),
                y1: parseInt(y1),
                x2: parseInt(x2),
                y2: parseInt(y2)
            });
            setForm({ zone_name: '', x1: '', y1: '', x2: '', y2: '' });
            setError('');
            fetchZones();
        } catch (err) {
            console.error('Error adding zone:', err);
            setError('Failed to add zone');
        }
    };

    const handleDelete = async (zone_id) => {
        try {
            await api.delete(`/zones/${zone_id}`);
            fetchZones();
        } catch (err) {
            console.error('Error deleting zone:', err);
        }
    };

    return (
        <div className="zones-container">
            <h2>Zone Management</h2>

            <form onSubmit={handleAddZone} className="zone-form">
                <input type="text" name="zone_name" placeholder="Zone Name" value={form.zone_name} onChange={handleChange} />
                <input type="number" name="x1" placeholder="X1" value={form.x1} onChange={handleChange} />
                <input type="number" name="y1" placeholder="Y1" value={form.y1} onChange={handleChange} />
                <input type="number" name="x2" placeholder="X2" value={form.x2} onChange={handleChange} />
                <input type="number" name="y2" placeholder="Y2" value={form.y2} onChange={handleChange} />
                <button type="submit">Add Zone</button>
            </form>

            {error && <p className="error-msg">{error}</p>}

            <div className="zone-list">
                {zones.length === 0 ? (
                    <p>No zones found.</p>
                ) : (
                    zones.map((zone, index) => (
                        <div className="zone-card" key={index}>
                            <h4>{zone.zone_name}</h4>
                            <p><b>X1:</b> {zone.x1} | <b>Y1:</b> {zone.y1}</p>
                            <p><b>X2:</b> {zone.x2} | <b>Y2:</b> {zone.y2}</p>
                            <button onClick={() => handleDelete(zone._id)}>❌ Delete</button>
                        </div>
                    ))
                )}
            </div>
        </div>
    );
};

export default ZonesPage;
