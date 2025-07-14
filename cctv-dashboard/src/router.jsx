import { Routes, Route } from 'react-router-dom';
import Login from './pages/Login';
import Dashboard from './pages/Dasboard';
import ZonesPage from './pages/ZonesPage';
import Media from './pages/Media';
import EmailConfig from './pages/EmailConfig';
import LiveStream from './pages/LiveStream';
import Register from './pages/Register';
import NotFound from './pages/NotFound';

export default function RoutesConfig() {
    return (
        <Routes>
            <Route path="/" element={<Register />} />
            <Route path="/register" element={<Register />} />
            <Route path="/login" element={<Login />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/zones" element={<ZonesPage />} />
            <Route path="/media" element={<Media />} />
            <Route path="/email-config" element={<EmailConfig />} />
            <Route path="/live-stream" element={<LiveStream />} />
            <Route path="*" element={<NotFound />} />
        </Routes>
    );
}
