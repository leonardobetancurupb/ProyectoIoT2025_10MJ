//Lógica para el sensor
const url = 'http://10.38.32.137:1026/v2/entities';

export const getSensors = async () => {
  try {
    const response = await fetch(url);
    
    if (!response.ok) {
      throw new Error(`Error al obtener sensores: ${response.status}`);
    }
    
    const data = await response.json();
    
    return {
      success: true,
      message: "Sensores obtenidos correctamente",
      data: data
    };
  }
  catch (error) {
    return {
      success: false,
      message: error.message
    };
  }
}

export const createSensor = async (sensor) => {
  try {
    const response = await fetch(url , {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(sensor)
    });
    
    if (!response.ok) {
      throw new Error(`Error al crear sensor: ${response.status}`);
    }
    
    return {
      success: true,
      message: "Sensor creado correctamente",
      sensor: sensor
    };
  } catch (error) {
    return {
      success: false,
      message: error.message
    };
  }
}

export const deleteSensor = async (sensorId) => {
  try {
    const response = await fetch(`${url}/${sensorId}`, {
      method: 'DELETE'
    });
    
    if (!response.ok) {
      throw new Error(`Error al eliminar sensor: ${response.status}`);
    }
    
    return {
      success: true,
      message: "Sensor eliminado correctamente",
      sensorId: sensorId
    };
  } catch (error) {
    return {
      success: false,
      message: error.message
    };
  }
}


export const updateSensor = async (sensorId, partialData) => {
  try {
    const response = await fetch(`${url}/${sensorId}/atrrs`, {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(partialData)
    });
    
    if (!response.ok) {
      throw new Error(`Error al actualizar parcialmente sensor: ${response.status}`);
    }
    
    return {
      success: true,
      message: "Sensor actualizado parcialmente",
      sensorId: sensorId,
      updatedFields: partialData
    };
  } catch (error) {
    return {
      success: false,
      message: error.message
    };
  }
}
