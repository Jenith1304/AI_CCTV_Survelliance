import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api, { setAuthToken } from '../utils/api';
import '../styles/Dashboard.css';
import HelmetChart from '../components/HelmetChart';
import ZonePieChart from '../components/ZonePieChart';
import EventPieChart from '../components/EventPieChart';
import RecentLogTable from '../components/RecentLogTable';

const Dashboard = () => {
    const [username, setUsername] = useState('');
    const [dashboardData, setDashboardData] = useState(null);
    const navigate = useNavigate();

    useEffect(() => {
        const token = localStorage.getItem('token');
        if (!token) {
            navigate('/login');
            return;
        }

        setAuthToken(token);

        api.get('/auth/profile')
            .then((res) => setUsername(res.data.username))
            .catch(() => {
                localStorage.removeItem('token');
                navigate('/login');
            });

        api.get('/dashboard/summary')
            .then((res) => setDashboardData(res.data))
            .catch(console.error);
    }, []);

    const handleLogout = () => {
        localStorage.removeItem('token');
        navigate('/login');
    };

    return (
        <div className="dashboard-container">
            <div className="dashboard-header">
                <h2>Welcome, {username}</h2>
                <button onClick={handleLogout}>Logout</button>
            </div>

            <div className="dashboard-grid">
                <div className="dashboard-card" onClick={() => navigate('/zones')}>📍 Zones</div>
                <div className="dashboard-card" onClick={() => navigate('/media')}>🎥 Media</div>
                {/* <div className="dashboard-card" onClick={() => navigate('/logs')}>📄 Logs</div> */}
                <div className="dashboard-card" onClick={() => navigate('/live-stream')}>📡 Live Stream</div>
                <div className="dashboard-card" onClick={() => navigate('/email-config')}>📧 Email Config</div>
            </div>

            {dashboardData ? (
                <div className="charts-section">
                    <div className="charts-row">
                        <HelmetChart data={dashboardData.helmetChart} />
                        <ZonePieChart data={dashboardData.zoneDistribution} />
                        <EventPieChart data={dashboardData.eventChart} />
                    </div>
                    <div className="logs-table-section">
                        <RecentLogTable logs={dashboardData.recentLogs} />
                    </div>
                </div>
            ) : (
                <p className="loading-msg">Loading dashboard data...</p>
            )}
        </div>
    );
};

export default Dashboard;
