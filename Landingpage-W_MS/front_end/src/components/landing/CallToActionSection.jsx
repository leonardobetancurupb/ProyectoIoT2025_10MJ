import React from 'react';
    import { Link } from 'react-router-dom';
    import { Button } from '@/components/ui/button';
    import { motion } from 'framer-motion';

    const CallToActionSection = () => (
      <section className="py-24 bg-gradient-to-r from-primary to-accent text-primary-foreground">
        <div className="container mx-auto px-6 text-center">
          <motion.h2 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            className="text-4xl font-bold mb-6"
          >
            ¿Listo para Tomar el Control de tu Entorno?
          </motion.h2>
          <motion.p 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.2 }}
            className="text-xl mb-10 max-w-2xl mx-auto"
          >
            Nuestra plataforma te brinda las herramientas para un futuro más informado y sostenible.
          </motion.p>
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.5, delay: 0.4 }}
          >
            <Link to="/login">
              <Button size="lg" className="bg-card text-primary hover:bg-secondary/50 font-bold py-4 px-10 rounded-lg shadow-xl transition duration-300 ease-in-out transform hover:scale-105 text-lg">
                Acceder a la Plataforma
              </Button>
            </Link>
          </motion.div>
        </div>
      </section>
    );

    export default CallToActionSection;