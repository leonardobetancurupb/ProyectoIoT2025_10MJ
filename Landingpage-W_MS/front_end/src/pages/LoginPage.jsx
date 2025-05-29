import React, { useState } from 'react';
    import { Link, useNavigate } from 'react-router-dom';
    import { Button } from '@/components/ui/button';
    import { Input } from '@/components/ui/input';
    import { Label } from '@/components/ui/label';
    import { useToast } from '@/components/ui/use-toast';
    import { motion } from 'framer-motion';
    import { Leaf, LogIn } from 'lucide-react';

    const LoginPage = () => {
      const [username, setUsername] = useState('');
      const [password, setPassword] = useState('');
      const [isLoading, setIsLoading] = useState(false);
      const navigate = useNavigate();
      const { toast } = useToast();

      const handleSubmit = async (e) => {
        console.log("handleSubmit INVOCADO"); 
        e.preventDefault();
        setIsLoading(true);
        console.log("Intentando iniciar sesión con:", { username, password });

        const FLASK_LOGIN_URL = 'http://127.0.0.1:5000/api/login'; 

        if (!username || !password) {
          toast({
            title: "Campos Incompletos",
            description: "Por favor, ingrese su usuario y contraseña.",
            variant: "destructive",
            className: "bg-destructive text-destructive-foreground"
          });
          setIsLoading(false);
          return;
        }
        
        if (FLASK_LOGIN_URL === 'TU_URL_DE_FLASK_LOGIN_ENDPOINT') {
             console.warn("Advertencia: La URL del backend de Flask parece no estar configurada. Asegúrate de reemplazar 'TU_URL_DE_FLASK_LOGIN_ENDPOINT' con tu URL real.");
             toast({
                title: "Configuración Requerida",
                description: "La URL del backend no está configurada. Por favor, edita el archivo LoginPage.jsx.",
                variant: "destructive",
                className: "bg-destructive text-destructive-foreground"
            });
            setIsLoading(false);
            return;
        }

        console.log("Enviando solicitud a:", FLASK_LOGIN_URL);
        try {
          const response = await fetch(FLASK_LOGIN_URL, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username: username, password: password }),
          });

          console.log("Respuesta recibida del servidor:", response);
          
          let data;
          try {
            data = await response.json();
            console.log("Datos JSON de la respuesta:", data);
          } catch (jsonError) {
            console.error("Error al parsear JSON de la respuesta:", jsonError);
            const responseText = await response.text();
            console.error("Texto de la respuesta (no JSON):", responseText);
            toast({
              title: "Error de Respuesta del Servidor",
              description: `El servidor respondió con un formato inesperado. Código: ${response.status}. Respuesta: ${responseText.substring(0,100)}...`,
              variant: "destructive",
              className: "bg-destructive text-destructive-foreground"
            });
            setIsLoading(false);
            return;
          }


          if (response.ok) {
            toast({
              title: "Inicio de Sesión Exitoso",
              description: data.message || "Redirigiendo...",
              variant: "default",
              className: "bg-primary text-primary-foreground"
            });
            setTimeout(() => {
              navigate('/dashboard');
            }, 1500);
          } else {
            console.error("Error de autenticación - Respuesta no OK:", response.status, data);
            toast({
              title: "Error de Autenticación",
              description: data.message || `Error ${response.status}: Credenciales incorrectas o error del servidor.`,
              variant: "destructive",
              className: "bg-destructive text-destructive-foreground"
            });
          }
        } catch (error) {
          console.error("Error en la solicitud de inicio de sesión (catch principal):", error);
          toast({
            title: "Error de Red o Conexión",
            description: `No se pudo conectar al servidor. Verifica la URL del backend y que el servidor Flask esté corriendo. Detalles: ${error.message}`,
            variant: "destructive",
            className: "bg-destructive text-destructive-foreground"
          });
        } finally {
          setIsLoading(false);
        }
      };

      return (
        <div className="min-h-screen flex flex-col items-center justify-center bg-gradient-to-br from-background via-secondary/30 to-background p-6">
           <motion.div
            initial={{ opacity: 0, y: -50 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="absolute top-6 left-6"
          >
            <Link to="/" className="flex items-center text-foreground hover:text-primary transition-colors">
              <Leaf className="h-7 w-7 mr-2 text-primary" />
              <span className="text-xl font-semibold">Sistema IoT UPB</span>
            </Link>
          </motion.div>
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.5 }}
            className="w-full max-w-md p-8 space-y-8 bg-card rounded-xl shadow-2xl border border-border"
          >
            <div className="text-center">
              <LogIn className="mx-auto h-12 w-12 text-primary" />
              <h1 className="mt-6 text-3xl font-extrabold text-card-foreground">
                Accede a tu Cuenta
              </h1>
              <p className="mt-2 text-sm text-muted-foreground">
                Ingresa tus credenciales para continuar.
              </p>
            </div>
            <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
              <div className="rounded-md -space-y-px">
                <div>
                  <Label htmlFor="username-field" className="sr-only">
                    Usuario
                  </Label>
                  <Input
                    id="username-field"
                    name="username"
                    type="text"
                    autoComplete="username"
                    required
                    className="appearance-none rounded-none relative block w-full px-3 py-3 border border-input placeholder-muted-foreground text-card-foreground bg-background rounded-t-md focus:outline-none focus:ring-ring focus:border-ring focus:z-10 sm:text-sm"
                    placeholder="Usuario"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    disabled={isLoading}
                  />
                </div>
                <div>
                  <Label htmlFor="password" className="sr-only">
                    Contraseña
                  </Label>
                  <Input
                    id="password"
                    name="password"
                    type="password"
                    autoComplete="current-password"
                    required
                    className="appearance-none rounded-none relative block w-full px-3 py-3 border border-input placeholder-muted-foreground text-card-foreground bg-background rounded-b-md focus:outline-none focus:ring-ring focus:border-ring focus:z-10 sm:text-sm"
                    placeholder="Contraseña"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    disabled={isLoading}
                  />
                </div>
              </div>

              <div>
                <Button
                  type="submit"
                  className="group relative w-full flex justify-center py-3 px-4 border border-transparent text-sm font-medium rounded-md text-primary-foreground bg-primary hover:bg-primary/90 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-ring transition-transform transform hover:scale-105 disabled:opacity-75"
                  disabled={isLoading}
                >
                  {isLoading ? 'Iniciando Sesión...' : 'Iniciar Sesión'}
                </Button>
              </div>
            </form>
            <p className="mt-6 text-center text-sm text-muted-foreground">
              ¿No tienes una cuenta? El registro se maneja internamente.
            </p>
          </motion.div>
        </div>
      );
    };

    export default LoginPage;