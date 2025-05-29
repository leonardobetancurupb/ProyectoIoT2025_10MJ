import React from 'react';
    import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
    import LandingPage from '@/pages/LandingPage';
    import LoginPage from '@/pages/LoginPage';
    import DashboardPage from '@/pages/DashboardPage';
    import AboutPage from '@/pages/AboutPage';
    import SensorsDisplayPage from '@/pages/SensorsDisplayPage';
    import { Toaster } from '@/components/ui/toaster';

    function App() {
      return (
        <Router>
          <Routes>
            <Route path="/" element={<LandingPage />} />
            <Route path="/login" element={<LoginPage />} />
            <Route path="/dashboard" element={<Navigate to="/dashboard/sensors" replace />} />
            <Route path="/dashboard/main" element={<DashboardPage />} />
            <Route path="/dashboard/sensors" element={<SensorsDisplayPage />} />
            <Route path="/about" element={<AboutPage />} />
          </Routes>
          <Toaster />
        </Router>
      );
    }

    export default App;