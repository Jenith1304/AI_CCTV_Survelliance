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

const EventPieChart = ({ data }) => {
    if (!data) return <p>No Event Data</p>;

    const chartData = {
        labels: ['Entered', 'Exited', 'Unattended'],
        datasets: [
            {
                label: 'Event Summary',
                data: [
                    data['Entered'] || 0,
                    data['Exited'] || 0,
                    data['Unattended'] || 0
                ],
                backgroundColor: ['#42a5f5', '#ef5350', '#ffca28']
            }
        ]
    };

    const options = {
        responsive: true,
        plugins: {
            legend: { position: 'bottom' },
            title: {
                display: true,
                text: 'Events Summary'
            }
        }
    };

    return (
        <div className="chart-card">
            <Pie data={chartData} options={options} />
        </div>
    );
};

export default EventPieChart;
