import React from 'react';
    import { motion } from 'framer-motion';
    import { Sun, Thermometer, Droplets, Zap } from 'lucide-react';

    const SensorCard = ({ icon, name, description }) => (
      <motion.div 
        className="bg-gradient-to-br from-card to-secondary/30 p-8 rounded-xl shadow-lg hover:shadow-2xl transition-shadow duration-300 border border-border"
        whileHover={{ y: -5 }}
      >
        <div className="flex items-center text-accent mb-4">
          {icon}
          <h3 className="text-2xl font-semibold ml-3 text-card-foreground">{name}</h3>
        </div>
        <p className="text-muted-foreground">{description}</p>
      </motion.div>
    );

    const SensorsSection = () => {
      const sensors = [
        { 
          icon: <Sun className="w-10 h-10" />, 
          name: 'Sensor de Radiación Solar', 
          description: 'Mide la intensidad de la radiación solar, esencial para estudios de energía renovable y agricultura de precisión.' 
        },
        { 
          icon: <Droplets className="w-10 h-10" />, 
          name: 'Sensor de Humedad', 
          description: 'Registra los niveles de humedad en el aire y el suelo, vital para el confort, la agricultura y la conservación de materiales.' 
        },
        { 
          icon: <Thermometer className="w-10 h-10" />, 
          name: 'Sensor de Temperatura', 
          description: 'Proporciona mediciones exactas de la temperatura ambiente, crucial para análisis climáticos y control de procesos.' 
        },
        { 
          icon: <Zap className="w-10 h-10" />, 
          name: 'Sensor de Humedad del Suelo', 
          description: 'Detecta el contenido de agua en el suelo, fundamental para optimizar el riego y mejorar el rendimiento de los cultivos.' 
        },
      ];

      return (
        <section className="py-20 bg-gradient-to-b from-background to-secondary/20">
          <div className="container mx-auto px-6">
            <h2 className="text-4xl font-bold text-center text-primary mb-16">Nuestros Sensores</h2>
            <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
              {sensors.map((sensor, index) => (
                <motion.div
                  key={sensor.name}
                  initial={{ opacity: 0, y: 50 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.5, delay: index * 0.1 }}
                >
                  <SensorCard {...sensor} />
                </motion.div>
              ))}
            </div>
          </div>
        </section>
      );
    };

    export default SensorsSection;