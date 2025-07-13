import React from 'react';
import '../styles/RecentLogTable.css'; // Make sure this CSS file exists

const RecentLogTable = ({ logs }) => {

  if (!logs || logs.length === 0) {
    return (
      <div className="table-card">
        <h4>Recent Logs</h4>
        <p>No recent logs available.</p>
      </div>
    );
  }

  const getHelmetBadge = (status) => {
    const color = status === 'No Helmet' ? 'danger' : status === 'Helmet' ? 'success' : 'neutral';
    return <span className={`badge badge-${color}`}>{status}</span>;
  };

  const getEventBadge = (event) => {
    const color = event === 'Entered' ? 'info' : event === 'Exited' ? 'warning' : 'dark';
    return <span className={`badge badge-${color}`}>{event}</span>;
  };

  return (
    <div className="table-card">
      <h4>📄 Recent Activity Logs</h4>
      <div className="table-container">
        <table className="recent-log-table">
          <thead>
            <tr>
              <th>Timestamp</th>
              <th>Zone</th>
              <th>Face ID</th>
              <th>Helmet</th>
              <th>Event</th>
            </tr>
          </thead>
          <tbody>
            {logs.map((log, index) => (
              <tr key={index}>
                <td>{log.timestamp}</td>
                <td>{log.zone}</td>
                <td>{log.face_id}</td>
                <td>{getHelmetBadge(log.helmet)}</td>
                <td>{getEventBadge(log.event)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default RecentLogTable;
