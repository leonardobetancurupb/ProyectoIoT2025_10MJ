import React from 'react';
    import { Link } from 'react-router-dom';
    import { Button } from '@/components/ui/button';
    import { motion } from 'framer-motion';
    import { Leaf, Info } from 'lucide-react';
    import HeroSection from '@/components/landing/HeroSection';
    import WhyMonitorSection from '@/components/landing/WhyMonitorSection';
    import SensorsSection from '@/components/landing/SensorsSection';
    import CallToActionSection from '@/components/landing/CallToActionSection';

    const Header = () => {
      return (
        <header className="fixed top-0 left-0 right-0 z-50 bg-gradient-to-r from-background to-secondary/80 shadow-lg">
          <div className="container mx-auto px-6 py-4 flex justify-between items-center">
            <Link to="/" className="flex items-center">
              <Leaf className="h-8 w-8 text-primary mr-2" />
              <h1 className="text-2xl font-bold text-foreground">Sistema IoT UPB</h1>
            </Link>
            <nav className="flex items-center space-x-4">
              <Link to="/about">
                <Button 
                  variant="ghost" 
                  className="text-foreground hover:text-primary font-semibold py-2 px-4 rounded-lg transition duration-300 ease-in-out"
                >
                  <Info className="h-5 w-5 mr-2" />
                  Acerca de
                </Button>
              </Link>
              <Link to="/login">
                <Button variant="default" className="bg-primary hover:bg-primary/90 text-primary-foreground font-semibold py-2 px-4 rounded-lg shadow-md transition duration-300 ease-in-out transform hover:scale-105">
                  Iniciar Sesión
                </Button>
              </Link>
            </nav>
          </div>
        </header>
      );
    };

    const LandingPage = () => {
      return (
        <div className="min-h-screen bg-background">
          <Header />
          <main>
            <HeroSection />
            <WhyMonitorSection />
            <SensorsSection />
            <CallToActionSection />
          </main>
        </div>
      );
    };

    export default LandingPage;