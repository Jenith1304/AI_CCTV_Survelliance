import React, { useState, useEffect } from 'react';
import api, { setAuthToken } from '../utils/api';
import '../styles/Media.css';

const Media = () => {
    const [file, setFile] = useState(null);
    const [previewUrl, setPreviewUrl] = useState('');
    const [resultUrl, setResultUrl] = useState('');
    const [loading, setLoading] = useState(false);
    const [message, setMessage] = useState('');
    const [uploads, setUploads] = useState([]);

    useEffect(() => {
        const token = localStorage.getItem("token");
        if (!token) return;

        setAuthToken(token);
        fetchUploads();
    }, []);

    const fetchUploads = async () => {
        try {
            const res = await api.get('/media/uploads');
            setUploads(res.data);
        } catch (err) {
            console.error("Error fetching uploads", err);
        }
    };

    const handleFileChange = (e) => {
        const selected = e.target.files[0];
        setFile(selected);
        setPreviewUrl(selected ? URL.createObjectURL(selected) : '');
        setResultUrl('');
        setMessage('');
    };

    const handleUpload = async () => {
        if (!file) {
            setMessage("Please select a file.");
            return;
        }

        const token = localStorage.getItem("token");
        if (!token) return;

        setAuthToken(token);
        const formData = new FormData();
        formData.append('file', file);
        setLoading(true);
        setMessage('');

        try {
            const res = await api.post('/media/upload', formData, {
                headers: { 'Content-Type': 'multipart/form-data' },
            });
            setResultUrl(res.data.url);
            setMessage(res.data.message);
            fetchUploads();
        } catch (err) {
            setMessage(err?.response?.data?.error || "Upload failed.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="media-upload-container">
            <h2>Media Upload & History</h2>

            <div className="upload-box">
                <input type="file" accept="image/*,video/*" onChange={handleFileChange} />
                <button onClick={handleUpload} disabled={loading}>
                    {loading ? "Uploading..." : "Upload & Analyze"}
                </button>
            </div>

            {previewUrl && (
                <div className="preview-section">
                    <h4>Selected File Preview:</h4>
                    {file?.type.startsWith('image') ? (
                        <img src={previewUrl} alt="Preview" />
                    ) : (
                        <video controls width="400" src={previewUrl}></video>
                    )}
                </div>
            )}

            {resultUrl && (
                <div className="result-section">
                    <h4>Processed Output:</h4>
                    {resultUrl.endsWith('.mp4') ? (
                        <video controls width="500" src={resultUrl}></video>
                    ) : (
                        <img src={resultUrl} alt="Processed" />
                    )}
                </div>
            )}

            {message && <p className="message-box">{message}</p>}

            <div className="upload-history">
                <h3>Your Upload History</h3>
                {uploads.length === 0 ? (
                    <p>No uploads found.</p>
                ) : (
                    <div className="uploads-grid">
                        {uploads.map((item, index) => (
                            <div className="media-card" key={index}>
                                <p><strong>Type:</strong> {item.media_type}</p>
                                {item.media_type === "image" ? (
                                    <img src={item.file_url} alt="uploaded" />
                                ) : (
                                    <video src={item.file_url} controls width="100%"></video>
                                )}
                                <p><strong>Date:</strong> {new Date(item.analysis.timestamp).toLocaleString()}</p>
                            </div>
                        ))}
                    </div>
                )}
            </div>
        </div>
    );
};

export default Media;
