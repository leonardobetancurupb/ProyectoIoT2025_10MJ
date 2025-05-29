import React, { useState, useEffect } from "react";
import "./SensorsView.css";
import Swal from "sweetalert2";
import { getSensors, createSensor, deleteSensor } from "../../api/sensor/sensor";
import {
  FaThermometerHalf,
  FaTint,
  FaUsers,
  FaList,
  FaChartBar,
  FaPlus,
  FaTrash,
  FaTimes
} from "react-icons/fa";
import NavBar from "../navBar/NavBar";

const SensorsView = () => {
  const [sensors, setSensors] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showModal, setShowModal] = useState(false);
  const [newSensor, setNewSensor] = useState({
    id: "",
    type: "",
    value: "",
    valueType: ""
  });

  const typeOptions = {
    temperatura: ["float", "int"],
    humedad: ["float", "int"],
    radiacion: ["float", "int"],
    presion: ["float", "int"]
  };

  let info = []

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

  const totalRecords = 4521;
  const totalSensors = sensors.length;
  const totalUsers = 5;
  const avgTemp = (
    sensors
      .filter(s => s.temperatura)
      .reduce((sum, s) => sum + s.temperatura.value, 0) /
    (sensors.filter(s => s.temperatura).length || 1)
  ).toFixed(1);

  const avgHum = (
    sensors
      .filter(s => s.humedad)
      .reduce((sum, s) => sum + s.humedad.value, 0) /
    (sensors.filter(s => s.humedad).length || 1)
  ).toFixed(1);

  const lastRecord = sensors[sensors.length - 1];

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setNewSensor(prev => ({
      ...prev,
      [name]: name === "value" ? parseFloat(value) : value
    }));
  };

  const handleSaveSensor = async () => {
    const { id, type, value, valueType } = newSensor;

    if (!id || !type || isNaN(value) || !valueType) {
      alert("Por favor completa todos los campos correctamente.");
      return;
    }

    const sensorObject = {
      "id": id,
      "type": type,
      [type]: {
        "value": value,
        "type": valueType
      }
    };

    try {
      const response = await createSensor(sensorObject);

      if (response.data && response.data.success) {

        Swal.fire({
          title: "¡Éxito!",
          text: "Sensor creado correctamente.",
          icon: "success",
          confirmButtonText: "OK"
        })
          .then(() => {
            window.location.reload();
          });

        setSensors([...sensors, sensorObject]);
        setNewSensor({ id: "", type: "", value: "", valueType: "" });
        setShowModal(false);
      } else {
        Swal.fire({
          title: "Error",
          text: "No se pudo crear el sensor.",
          icon: "error",
          confirmButtonText: "OK"
        });
        console.error("Failed to create sensor:", response.data);
      }
    } catch (error) {
      console.error("Error creating sensor:", error);
      alert("Error al crear el sensor. Por favor intente nuevamente.");
    }
  };

  const handleDeleteSensor = async (id) => {
    try {
      const response = await deleteSensor(id);
      console.log(id);

      if (response.data && response.data.success) {
        Swal.fire({
          title: "¡Éxito!",
          text: "Sensor eliminado correctamente.",
          icon: "success",
          confirmButtonText: "OK"
        })
          .then(() => {
            window.location.reload();
          });
        // Remove the deleted sensor from state
        const updated = sensors.filter(sensor => sensor.id !== id);
        setSensors(updated);
      } else {
        Swal.fire({
          title: "Error",
          text: "No se pudo eliminar el sensor.",
          icon: "error",
          confirmButtonText: "OK"
        });
        console.error("Failed to delete sensor:", response.data);
      }
    } catch (error) {
      console.error("Error deleting sensor:", error);
      alert("Error al eliminar el sensor. Por favor intente nuevamente.");
    }
  };

  return (
    <div className="sensor">
      <div className="nav">
        <NavBar active={"sensores"} />
      </div>

      <div className="sensor-view">
        <h2 className="sv-title">Panel de Sensores</h2>

        {loading ? (
          <div className="loading-container">
            <p>Cargando sensores...</p>
          </div>
        ) : error ? (
          <div className="error-container">
            <p>{error}</p>
            <button onClick={() => window.location.reload()}>Reintentar</button>
          </div>
        ) : (
          <>
            <div className="sv-metrics">
              <div className="sv-card"><FaChartBar /><p>{totalRecords}</p><span>Registros</span></div>
              <div className="sv-card"><FaList /><p>{totalSensors}</p><span>Sensores</span></div>
              <div className="sv-card"><FaUsers /><p>{totalUsers}</p><span>Usuarios</span></div>
              <div className="sv-card"><FaThermometerHalf /><p>{avgTemp}°C</p><span>Temp. Prom.</span></div>
              <div className="sv-card"><FaTint /><p>{avgHum}%</p><span>Hum. Prom.</span></div>
            </div>

            <div className="sv-last">
              <h3>Último Registro</h3>
              <p><strong>ID:</strong> {lastRecord?.id}</p>
              <p><strong>Tipo:</strong> {lastRecord?.type}</p>
            </div>

            <div className="sv-actions">
              <button className="btn-add" onClick={() => setShowModal(true)}>
                <FaPlus /> Crear Sensor
              </button>
            </div>

            <div className="sv-carousel">
              <h3>Lista de Sensores</h3>
              <div className="carousel-container">

                {sensors.map((sensor, index) => {  
                    return(         
                    <a className="carousel-item" href={`/sensor/${sensor.id}`}  key={index}>
                      <h4>{sensor.id}</h4>
                      <p><strong>Tipo:</strong> {sensor.type}</p>
                      <button className="btn-delete" onClick={() => handleDeleteSensor(sensor.id)}>
                        <FaTrash />
                      </button>
                    </a>)
                })}
              </div>
            </div>

            {showModal && (
              <div className="modal-overlay">
                <div className="modal">
                  <button className="close-btn" onClick={() => setShowModal(false)}><FaTimes /></button>
                  <h3>Nuevo Sensor</h3>
                  <input type="text" name="id" placeholder="ID del sensor" value={newSensor.id} onChange={handleInputChange} />
                  <select name="type" value={newSensor.type} onChange={handleInputChange}>
                    <option value="">Selecciona tipo</option>
                    <option value="temperatura">Temperatura</option>
                    <option value="humedad">Humedad</option>
                    <option value="radiacion">Radiación</option>
                    <option value="presion">Presión</option>
                  </select>
                  <input type="number" name="value" placeholder="Valor" value={newSensor.value} onChange={handleInputChange} />
                  <select name="valueType" value={newSensor.valueType} onChange={handleInputChange}>
                    <option value="">Selecciona unidad</option>
                    {(typeOptions[newSensor.type] || []).map((unit, i) => (
                      <option key={i} value={unit}>{unit}</option>
                    ))}
                  </select>
                  <button className="save-btn" onClick={handleSaveSensor}>Guardar</button>
                </div>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
};

export default SensorsView;
