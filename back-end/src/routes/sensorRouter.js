//Rutas para el sensor
import { getSensorsController, createSensorController, deleteSensorController, updateSensorController } from '../controllers/sensorController.js';    
import express from 'express';

const sensorRouter = express.Router();

sensorRouter.get('/getsensors', getSensorsController);
sensorRouter.post('/createsensor', createSensorController);
sensorRouter.delete('/deletesensor:id', deleteSensorController);
sensorRouter.patch('/updatesensor:id', updateSensorController);

export default sensorRouter;
