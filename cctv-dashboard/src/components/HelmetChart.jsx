import React from 'react';
import { Doughnut } from 'react-chartjs-2';
import {
    Chart as ChartJS,
    ArcElement,
    Tooltip,
    Legend,
    Title
} from 'chart.js';

ChartJS.register(ArcElement, Tooltip, Legend, Title);

const HelmetChart = ({ data }) => {
    if (!data) return <p>No Helmet data</p>;

    const chartData = {
        labels: ['Helmet', 'No Helmet', 'None'],
        datasets: [
            {
                label: 'Helmet Detections',
                data: [
                    data['Helmet'] || 0,
                    data['No Helmet'] || 0,
                    data['None'] || 0
                ],
                backgroundColor: ['#4caf50', '#f44336', '#9e9e9e'],
                borderWidth: 1
            }
        ]
    };

    const options = {
        responsive: true,
        plugins: {
            legend: { position: 'bottom' },
            title: {
                display: true,
                text: 'Helmet Detection Summary'
            }
        }
    };

    return (
        <div className="chart-card">
            <Doughnut data={chartData} options={options} />
        </div>
    );
};

export default HelmetChart;
