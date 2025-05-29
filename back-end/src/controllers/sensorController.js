//Controlador sensor
import { getSensors, createSensor, deleteSensor, updateSensor } from "../services/sensorService.js";

export const getSensorsController = async (req, res) => {
  try {
    const sensors = await getSensors();
    res.status(200).json(sensors);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
}


export const createSensorController = async (req, res) => { 
  try {
    const sensor = req.body;
    const response = await createSensor(sensor);
    res.status(201).json(response);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
}

export const deleteSensorController = async (req, res) => {
  try {
    const sensorId = req.params.id.split(":")[1]; // Extracting the sensor ID from the URL
    const response = await deleteSensor(sensorId);
    res.status(200).json(response);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
}

export const updateSensorController = async (req, res) => {
  try {
    const sensorId = req.params.id.split(":")[1]; // Extracting the sensor ID from the URL
    const sensorData = req.body;
    const response = await updateSensor(sensorId, sensorData);
    res.status(200).json(response);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
}