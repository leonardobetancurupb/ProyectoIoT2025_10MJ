import React from 'react';
    import { motion } from 'framer-motion';

    const WhyMonitorSection = () => (
      <section className="py-20 bg-card">
        <div className="container mx-auto px-6">
          <h2 className="text-4xl font-bold text-center text-primary mb-16">¿Por qué Monitorear el Ambiente?</h2>
          <div className="grid md:grid-cols-2 gap-12 items-center">
            <motion.div
              initial={{ opacity: 0, x: -50 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.7 }}
            >
              <img    
                className="rounded-lg shadow-xl w-full h-auto object-cover" 
                alt="Infografía mostrando los beneficios del monitoreo ambiental"
               src="https://images.unsplash.com/photo-1688413399498-e35ed74b554f" />
            </motion.div>
            <motion.div
              initial={{ opacity: 0, x: 50 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.7 }}
              className="space-y-6 text-lg text-card-foreground"
            >
              <p>El monitoreo de variables ambientales es crucial para entender nuestro entorno. Nos permite tomar decisiones informadas para:</p>
              <ul className="list-disc list-inside space-y-3 pl-4 text-primary">
                <li><span className="text-card-foreground">Proteger la salud pública al identificar riesgos contaminantes.</span></li>
                <li><span className="text-card-foreground">Optimizar la agricultura y el uso de recursos naturales.</span></li>
                <li><span className="text-card-foreground">Conservar la biodiversidad y los ecosistemas.</span></li>
                <li><span className="text-card-foreground">Combatir el cambio climático mediante la recopilación de datos precisos.</span></li>
                <li><span className="text-card-foreground">Mejorar la planificación urbana y la calidad de vida.</span></li>
              </ul>
              <p>Con datos fiables, podemos actuar proactivamente para un futuro más sostenible.</p>
            </motion.div>
          </div>
        </div>
      </section>
    );

    export default WhyMonitorSection;