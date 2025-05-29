import React, { useState, useEffect } from "react";
import { useParams } from 'react-router-dom';
import { getSensors } from "../../api/sensor/sensor";
import './Sensor.css'


export default function Sensor() {

    const { id } = useParams()
    console.log(id)

    const [sensors, setSensors] = useState([]);
     const [loading, setLoading] = useState(true);


    useEffect(() => {
        const fetchSensors = async () => {
            try {
                setLoading(true);
                const response = await getSensors();
                console.log(typeof response.data.data)
                console.log(response.data)
                if (response.data && response.data.success) {
                    console.log(sensors)
                    setSensors(response?.data?.data || []);
                    console.log(sensors)
                } else {
                    setError('Failed to fetch sensors data');
                }
            } catch (error) {
                console.error('Error fetching sensors:', error);
                setError('An error occurred while fetching sensors');
            } finally {
                setLoading(false);
            }
        };

        fetchSensors();
    }, []);





    return (
        <div className="sv-carousel">
            <h3>Lista de Sensores</h3>
            <div className="carousel-container-s">

                {
                    sensors.map((sensor, index) => {
                        if (sensor.id === id) {
                            const medida = Object.entries(sensor);
                            return medida.map(([nombre, data]) => (
                                
                                    <div className="sv-last" key={index}>
                                        <h4>{nombre? nombre : ''}</h4>
                                        <p><strong>Tipo:</strong> {data.type ? data.type : 'n/a'}</p>
                                        <p><strong>Valor:</strong> {data.value ? data.value : 'n/a'}</p>
                                    </div>
                            ))
                        }
                    })
                }
            </div>
        </div>
    )
}
