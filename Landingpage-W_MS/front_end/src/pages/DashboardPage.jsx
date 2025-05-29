import React, { useEffect, useState } from 'react';
import { useNavigate, Link, useLocation } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { useToast } from '@/components/ui/use-toast';
import { motion } from 'framer-motion';
import { Leaf, LogOut, BarChart3, SlidersHorizontal } from 'lucide-react';
import axios from 'axios';
import { Bar } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend } from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

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

const getColor = (value) => {
  if (value < 20) return 'bg-red-500';
  if (value < 40) return 'bg-orange-500';
  if (value < 60) return 'bg-yellow-400';
  if (value < 80) return 'bg-green-400';
  return 'bg-blue-400';
};

const DashboardPage = () => {
  const [sensores, setSensores] = useState([]);
  const [promedio, setPromedio] = useState(null);

  useEffect(() => {
    const fetchSensores = async () => {
      try {
        const res = await axios.get(`${FLASK_BASE_URL}/api/listar_sensores`);
        const sensoresValidos = res.data.filter(s => s.moisture && typeof s.moisture.value === 'number');
        setSensores(sensoresValidos);
        const valores = sensoresValidos.map(s => s.moisture.value);
        const prom = valores.reduce((a, b) => a + b, 0) / valores.length;
        setPromedio(prom.toFixed(2));
      } catch (error) {
        console.error('Error obteniendo sensores:', error);
      }
    };

    fetchSensores();
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
          Panel Principal del Sistema IoT UPB
        </motion.h2>

        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.2 }}
          className="text-center bg-card p-10 rounded-xl shadow-lg border border-border mb-10"
        >
          <p className="text-2xl text-card-foreground mb-4">Promedio de Humedad</p>
          {promedio && (
            <div className="flex justify-center items-center gap-6">
              <div className="text-4xl font-bold text-primary">{promedio}</div>
              <div className={`w-12 h-12 rounded ${getColor(promedio)}`} title="Nivel de humedad" />
            </div>
          )}
        </motion.div>

        <div className="bg-card p-6 rounded-xl shadow-md border border-border mt-10">
  <h3 className="text-xl font-semibold mb-4 text-card-foreground">Humedad por Sensor</h3>
  {sensores.length > 0 ? (
    <Bar
      data={{
        labels: sensores.map(s => s.id),
        datasets: [
          {
            label: 'Humedad',
            data: sensores.map(s => s.moisture.value),
            backgroundColor: 'rgba(34, 197, 94, 0.6)', // verde-500 con opacidad
            borderColor: 'rgba(34, 197, 94, 1)',
            borderWidth: 1,
          },
        ],
      }}
      options={{
        responsive: true,
        plugins: {
          legend: { display: false },
          title: {
            display: false,
          },
        },
        scales: {
          y: {
            beginAtZero: true,
            ticks: {
              callback: function(value) {
                return value;
              }
            }
          }
        }
      }}
    />
  ) : (
    <p className="text-muted-foreground text-sm">No hay sensores con datos válidos.</p>
  )}
</div>

      </main>
    </div>
  );
};

export default DashboardPage;