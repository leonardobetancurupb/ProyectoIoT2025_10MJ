import React, { useEffect, useState } from 'react';
import { useNavigate, Outlet } from 'react-router-dom';
import { validateToken } from './api/user/user';

const ProtectRoutes = () => {
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const checkToken = async () => {
      const token = localStorage.getItem('UserToken');
      if (!token) {
        navigate('/login');
        return;
      }

      try {
        const res = await validateToken(token);
        if (!res.data.success) {
          localStorage.removeItem('UserToken');
          navigate('/login');
        } else {
          setLoading(false); // Auth ok → renderiza el contenido
        }
      } catch (err) {
        localStorage.removeItem('UserToken');
        navigate('/login');
      }
    };

    checkToken();
  }, [navigate]);

  if (loading) return <div>Validando sesión...</div>;

  return <Outlet />;
};

export default ProtectRoutes;

