import React from 'react';
    import { motion } from 'framer-motion';

    const HeroSection = () => (
      <section className="pt-32 pb-20 bg-gradient-to-br from-background via-secondary/30 to-background">
        <div className="container mx-auto px-6 text-center">
          <motion.h2 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            className="text-5xl font-extrabold text-foreground mb-6"
          >
            Monitoreo Ambiental Inteligente
          </motion.h2>
          <motion.p 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.2 }}
            className="text-xl text-muted-foreground mb-12 max-w-3xl mx-auto"
          >
            Descubre cómo nuestros sensores avanzados te ayudan a comprender y proteger tu entorno, proporcionando datos precisos y en tiempo real.
          </motion.p>
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.5, delay: 0.4 }}
          >
            <img    
              className="rounded-xl shadow-2xl mx-auto w-full max-w-4xl h-auto object-cover" 
              alt="Paisaje natural con superposición de datos de sensores ambientales"
             src="https://images.unsplash.com/photo-1700301928232-4d35afd6f82f" />
          </motion.div>
        </div>
      </section>
    );

    export default HeroSection;