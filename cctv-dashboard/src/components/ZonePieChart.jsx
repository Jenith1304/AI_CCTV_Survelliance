import React from 'react';
import { Pie } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend,
  Title
} from 'chart.js';

ChartJS.register(ArcElement, Tooltip, Legend, Title);

const ZonePieChart = ({ data }) => {
  if (!data || Object.keys(data).length === 0) {
    return <p>No Zone Data Available</p>;
  }

  const chartData = {
    labels: Object.keys(data),
    datasets: [
      {
        label: 'Zone Activity',
        data: Object.values(data),
        backgroundColor: [
          '#42a5f5', '#66bb6a', '#ffa726', '#ab47bc', '#ff7043',
          '#26c6da', '#ef5350', '#8d6e63', '#d4e157', '#5c6bc0'
        ]
      }
    ]
  };

  const options = {
    responsive: true,
    plugins: {
      legend: { position: 'bottom' },
      title: {
        display: true,
        text: 'Detections by Zone'
      }
    }
  };

  return (
    <div className="chart-card">
      <Pie data={chartData} options={options} />
    </div>
  );
};

export default ZonePieChart;
