import api from '../api';

export const getSensors = async () => {return await api.get('/sensors/getsensors');};
export const createSensor = async (sensor) => {return await api.post('/sensors/createsensor', sensor);};
export const deleteSensor = async (id) => {return await api.delete(`/sensors/deletesensor:${id}`);};
export const updateSensor = async (id, sensor) => {return await api.patch(`/sensors/updatesensor:${id}`, sensor);};