import { Routes, Route } from 'react-router-dom';


// import SetCamera from './pages/SetCamera';
// import LiveFeed from './pages/LiveFeed';
// import UploadMedia from './pages/UploadMedia';
// import DetectionLogs from './pages/DetectionLogs';
// import EmailSettings from './pages/EmailSettings';
// import Zones from './pages/Zones';
// import NotFound from './pages/NotFound';
import Login from './pages/Login';
import Dashboard from './pages/Dasboard';
import ZonesPage from './pages/ZonesPage';
import Media from './pages/Media';
import EmailConfig from './pages/EmailConfig';
import LiveStream from './pages/LiveStream';

export default function RoutesConfig() {
    return (
        <Routes>
            <Route path="/" element={<Login />} />
            <Route path="/login" element={<Login />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/zones" element={<ZonesPage />} />
            <Route path="/media" element={<Media />} />
            <Route path="/email-config" element={<EmailConfig />} />
            <Route path="/live-stream" element={<LiveStream />} />
            {/* <Route path="/set-camera" element={<SetCamera />} />
            <Route path="/live-feed" element={<LiveFeed />} />
            
            <Route path="/logs" element={<DetectionLogs />} />
            <Route path="/email-settings" element={<EmailSettings />} />
         
            <Route path="*" element={<NotFound />} /> */}
        </Routes>
    );
}
