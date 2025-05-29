import React, { useState, useEffect } from 'react';
import { useNavigate, Link, useLocation } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { useToast } from '@/components/ui/use-toast';
import { motion } from 'framer-motion';
import { Leaf, LogOut, BarChart3, SlidersHorizontal, Trash2, Plus } from 'lucide-react';

const FLASK_BASE_URL = 'http://127.0.0.1:5000';

const DashboardHeader = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { toast } = useToast();

  const handleLogout = () => {
    toast({
      title: "Cierre de Sesión Exitoso",
      description: "Has cerrado sesión.",
      variant: "default",
      className: "bg-primary text-primary-foreground"
    });
    navigate('/login');
  };

  const isActive = (path) => location.pathname === path;

  return (
    <header className="fixed top-0 left-0 right-0 z-50 bg-gradient-to-r from-background to-secondary/80 shadow-lg">
      <div className="container mx-auto px-6 py-4 flex justify-between items-center">
        <Link to="/dashboard/sensors" className="flex items-center">
          <Leaf className="h-8 w-8 text-primary mr-2" />
          <h1 className="text-2xl font-bold text-foreground">Sistema IoT UPB</h1>
        </Link>
        <nav className="flex items-center space-x-4">
          <Button 
            variant={isActive('/dashboard/sensors') ? "default" : "ghost"} 
            className={`font-medium ${isActive('/dashboard/sensors') ? 'bg-primary text-primary-foreground' : 'text-foreground hover:text-primary hover:bg-primary/10'}`}
            onClick={() => navigate('/dashboard/sensors')}
          >
            <SlidersHorizontal className="mr-2 h-5 w-5" />
            Sensores
          </Button>
          <Button 
            variant={isActive('/dashboard/main') ? "default" : "ghost"} 
            className={`font-medium ${isActive('/dashboard/main') ? 'bg-primary text-primary-foreground' : 'text-foreground hover:text-primary hover:bg-primary/10'}`}
            onClick={() => navigate('/dashboard/main')}
          >
            <BarChart3 className="mr-2 h-5 w-5" />
            Dashboard
          </Button>
        </nav>
        <Button variant="outline" onClick={handleLogout} className="text-destructive-foreground bg-destructive hover:bg-destructive/90 font-semibold py-2 px-4 rounded-lg shadow-md transition duration-300 ease-in-out transform hover:scale-105">
          <LogOut className="mr-2 h-5 w-5" />
          Cerrar Sesión
        </Button>
      </div>
    </header>
  );
};

const SensorsDisplayPage = () => {
  const [sensors, setSensors] = useState([]);
  const [newSensorId, setNewSensorId] = useState('');
  const [loading, setLoading] = useState(false);
  const { toast } = useToast();

  const fetchSensors = async () => {
    try {
      const res = await fetch(`${FLASK_BASE_URL}/api/listar_sensores`);
      const data = await res.json();
      setSensors(data);
    } catch (err) {
      console.error('Error al obtener sensores:', err);
      toast({
        title: "Error al cargar sensores",
        description: err.message,
        variant: "destructive"
      });
    }
  };

  const createSensor = async () => {
  if (!newSensorId) {
    toast({
      title: "ID requerido",
      description: "Debes ingresar un ID para el sensor.",
      variant: "destructive"
    });
    return;
  }

  if (!newSensorId.startsWith("sensor_W_MS_")) {
    toast({
      title: "Formato inválido",
      description: "El ID debe empezar con 'sensor_W_MS_'.",
      variant: "destructive"
    });
    return;
  }

  const sensorData = {
    id: newSensorId,
    type: 'sensor_W_MS',
    moisture: {
      value: Math.random() * 100, // dummy value
      type: 'float'
    }
  };

  try {
    const res = await fetch(`${FLASK_BASE_URL}/api/sensores`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(sensorData)
    });

    if (!res.ok) throw new Error('No se pudo crear el sensor');

    toast({
      title: "Sensor creado",
      description: `Sensor ${newSensorId} creado exitosamente.`,
    });

    setNewSensorId('');
    fetchSensors();
  } catch (err) {
    console.error('Error al crear sensor:', err);
    toast({
      title: "Error al crear sensor",
      description: err.message,
      variant: "destructive"
    });
  }
};

  const deleteSensor = async (id) => {
  try {
    const res = await fetch(`${FLASK_BASE_URL}/api/eliminar_entidad/${id}`, {
      method: 'DELETE'
    });

    if (!res.ok) throw new Error('No se pudo eliminar el sensor');

    toast({
      title: "Sensor eliminado",
      description: `Sensor ${id} eliminado exitosamente.`,
    });

    fetchSensors();
  } catch (err) {
    console.error('Error al eliminar sensor:', err);
    toast({
      title: "Error al eliminar sensor",
      description: err.message,
      variant: "destructive"
    });
  }
};

  useEffect(() => {
    fetchSensors();
  }, []);

  return (
    <div className="min-h-screen bg-gradient-to-br from-background via-secondary/10 to-background">
      <DashboardHeader />
      <main className="pt-28 pb-16 container mx-auto px-6">
        <motion.h2
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="text-4xl font-bold text-center text-foreground mb-12"
        >
          Gestor de Sensores
        </motion.h2>

        {/* Formulario para crear sensor */}
        <div className="flex flex-col items-center mb-8">
          <p className="text-sm text-muted-foreground text-center mb-2">
            El ID debe tener el formato: <span className="font-mono text-primary">sensor_W_MS_XXX</span>
          </p>
          <div className="flex flex-col md:flex-row gap-4 items-center justify-center">
            <Input
              placeholder="ID del nuevo sensor"
              value={newSensorId}
              onChange={(e) => setNewSensorId(e.target.value)}
              className="max-w-sm"
            />
            <Button onClick={createSensor} className="flex gap-2">
              <Plus className="w-4 h-4" /> Crear Sensor
            </Button>
          </div>
        </div>

        {/* Tabla de sensores */}
        <div className="overflow-x-auto border rounded-xl shadow-md bg-card">
          <table className="min-w-full divide-y divide-border text-sm">
            <thead className="bg-muted text-muted-foreground">
              <tr>
                <th className="px-6 py-3 text-left font-semibold">ID</th>
                <th className="px-6 py-3 text-left font-semibold">Tipo</th>
                <th className="px-6 py-3 text-left font-semibold">Datos</th>
                <th className="px-6 py-3 text-center font-semibold">Acciones</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-border text-foreground">
              {sensors.length === 0 ? (
                <tr>
                  <td colSpan="4" className="text-center py-6 text-muted-foreground">
                    No hay sensores registrados.
                  </td>
                </tr>
              ) : (
                sensors.map((sensor) => (
                  <tr key={sensor.id} className="hover:bg-muted/40 transition">
                    <td className="px-6 py-4">{sensor.id}</td>
                    <td className="px-6 py-4">{sensor.type}</td>
                    <td className="px-6 py-4">
                      {Object.entries(sensor)
                        .filter(([key]) => !['id', 'type'].includes(key))
                        .map(([key, val]) => (
                          <div key={key}>
                            {key}: <span className="text-primary">{val.value}</span>
                            {val.type && <span className="text-xs text-muted-foreground"> ({val.type})</span>}
                          </div>
                        ))}
                    </td>
                    <td className="px-6 py-4 text-center">
                      <Button
                        variant="destructive"
                        size="sm"
                        onClick={() => deleteSensor(sensor.id)}
                        className="flex gap-2 mx-auto"
                      >
                        <Trash2 className="w-4 h-4" /> Eliminar
                      </Button>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </main>
    </div>
  );
};

export default SensorsDisplayPage;