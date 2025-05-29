import React from 'react';
    import { motion } from 'framer-motion';
    import { Users, Leaf, Brain, Settings } from 'lucide-react';
    import { Link } from 'react-router-dom';
    import { Button } from '@/components/ui/button';

    const GlobalHeader = () => (
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
                <Users className="h-5 w-5 mr-2" />
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

    const AuthorProfileCard = ({ name, role, description, imageUrl, icon, delay }) => (
      <motion.div
        initial={{ opacity: 0, y: 50 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, delay: delay }}
        className="bg-card p-8 rounded-xl shadow-xl border border-border flex flex-col items-center text-center transform hover:scale-105 transition-transform duration-300"
      >
        <div className="mb-6">
          <img  className="w-32 h-32 rounded-full object-cover shadow-lg mx-auto border-4 border-primary" alt={`Foto de perfil de ${name}`} src={imageUrl} />
        </div>
        <div className="flex items-center text-accent mb-2">
          {icon}
          <h3 className="text-2xl font-semibold ml-2 text-card-foreground">{name}</h3>
        </div>
        <p className="text-lg font-medium text-primary mb-4">{role}</p>
        <p className="text-muted-foreground text-sm leading-relaxed">{description}</p>
      </motion.div>
    );


    const AboutPage = () => {
      const authors = [
        {
          name: "Antony Sanchez",
          role: "Analista de Datos",
          description: "Antony es un apasionado analista de datos con experiencia en la interpretación de grandes volúmenes de información para extraer insights valiosos. En Sistema IoT UPB, se enfoca en transformar los datos de los sensores en conocimiento accionable para la toma de decisiones ambientales.",
          icon: <Brain className="w-8 h-8" />,
          imageUrl: "https://storage.googleapis.com/hostinger-horizons-assets-prod/a33f7010-563b-45c1-9865-c3c88d7a05a1/8939ad516c89ba6981df830de40a7fd0.jpg",
          altText: "Foto de Antony Sanchez, Analista de Datos",
          delay: 0.2
        },
        {
          name: "Sebastian Franco",
          role: "Ingeniero en Diseño de Entretenimiento Digital",
          description: "Sebastian es un ingeniero de entretenimiento digital con una sólida trayectoria en el desarrollo y la implementación de soluciones creativas y visuales funcionales. En el proyecto Sistema IoT UPB, es responsable de la arquitectura del sistema, la integración de los sensores y el desarrollo de la plataforma.",
          icon: <Settings className="w-8 h-8" />,
          imageUrl: "/20240212_093617.jpg",
          altText: "Foto de Sebastian Franco, Ingeniero de Sistemas",
          delay: 0.4
        }
      ];

      return (
        <div className="min-h-screen bg-background text-foreground">
          <GlobalHeader />
          <main className="pt-32 pb-20">
            <div className="container mx-auto px-6">
              <motion.div
                initial={{ opacity: 0, y: -20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.7 }}
              >
                <h1 className="text-5xl font-extrabold text-center text-primary mb-6">
                  <Users className="inline-block h-12 w-12 mr-4 text-primary" />
                  Conoce a Nuestro Equipo
                </h1>
                <p className="text-xl text-center text-muted-foreground mb-16 max-w-3xl mx-auto">
                  Somos un dúo dinámico comprometido con la innovación en el monitoreo ambiental. Conoce a las mentes detrás del Sistema IoT UPB:
                </p>
              </motion.div>

              <div className="grid md:grid-cols-2 gap-12">
                {authors.map((author) => (
                  <AuthorProfileCard
                    key={author.name}
                    name={author.name}
                    role={author.role}
                    description={author.description}
                    icon={author.icon}
                    imageUrl={author.imageUrl}
                    delay={author.delay}
                  />
                ))}
              </div>

              <motion.div
                className="mt-20 text-center max-w-4xl mx-auto"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.8, delay: 0.5 }}
              >
                <h2 className="text-3xl font-bold text-foreground mb-6">Nuestra Misión Compartida</h2>
                <p className="text-lg text-muted-foreground mb-4">
                  Juntos, Antony y Sebastian combinan su experiencia para hacer del Sistema IoT UPB una herramienta poderosa y accesible. Antony se asegura de que los datos cuenten una historia clara, mientras Sebastian garantiza que la plataforma que entrega esos datos sea sólida y confiable.
                </p>
                <p className="text-lg text-muted-foreground">
                  Creemos que la tecnología puede ser una fuerza para el bien ambiental, y estamos dedicados a proporcionar las herramientas necesarias para entender y proteger nuestro planeta. Gracias por ser parte de la comunidad del Sistema IoT UPB.
                </p>
              </motion.div>
            </div>
          </main>
          <footer className="bg-secondary/50 text-secondary-foreground py-8 mt-auto">
            <div className="container mx-auto px-6 text-center">
              <p className="text-sm">&copy; {new Date().getFullYear()} Sistema IoT UPB. Todos los derechos reservados.</p>
              <p className="text-xs mt-1">Desarrollado con pasión por Antony Sanchez y Sebastian Franco.</p>
            </div>
          </footer>
        </div>
      );
    };

    export default AboutPage;