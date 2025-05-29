import React from 'react';
import { Doughnut } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend,
} from 'chart.js';

ChartJS.register(ArcElement, Tooltip, Legend);

const GraphReg = ({ value, label, color }) => {

  var lef = "30%";
  var und = "%";
  var top = '-5rem';
  if(label == 'Temperatura'){
    top = '-5rem';
    und = "°C";
    lef = "27%";
  }

  const data = {
    labels: [label, 'Restante'],
    datasets: [
      {
        data: [value, 100 - value],
        backgroundColor: [color, '#e5e7eb'],
        borderWidth: 0,
        cutout: '80%',
      },
    ],
  };

  const options = {
    rotation: -90,
    circumference: 180,
    plugins: {
      legend: {
        display: true,
        position: 'right',
        labels: {
          color: '#111',
          font: {
            size: 12,
          }
        }
      },
      tooltip: {
        enabled: false,
      },
    },
  };

  return (
    <div>
      <div style={{
         position: 'relative',
         marginTop: top,
         width: '20vw',
         overflow: 'hidden'
        }}>
        <Doughnut data={data} options={options} />
        <p style={{
          position: 'absolute',
          top: '55%',
          left: lef,
          transform: 'translate(-50%, -35%)',
          fontSize: '1.5rem',
          fontWeight: 'bold',
          color: '#1f2937',
          overflow: 'hidden'
        }}>
          {value}{und}
        </p>
      </div>
    </div>
  );
};

export default GraphReg;