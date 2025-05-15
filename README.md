# ProyectoIoT2025_10MJ

## Sistema de Gestión de Sensores IoT

Este proyecto implementa una plataforma completa para el monitoreo de sensores IoT, conectándose al Orion Context Broker y almacenando datos históricos en CrateDB.

## Estructura del Proyecto

- **Web App (Django)**: Interfaz de usuario para visualizar y gestionar sensores
- **Agentes**: Componentes para recolectar datos de los sensores 
- **Brokers**: Intermediarios para la comunicación entre componentes
- **Orion Context Broker**: Gestión de entidades y contexto
- **CrateDB**: Base de datos para almacenamiento de series temporales
- **QuantumLeap**: Conector entre Orion y CrateDB para históricos

## Requisitos

- Docker y Docker Compose
- Python 3.8+

## Instrucciones de Instalación

1. Clonar el repositorio:
```
git clone [URL_del_repositorio]
cd ProyectoIoT2025_10MJ
```

2. Ejecutar con Docker Compose:
```
docker-compose up -d
```

3. Acceder a la aplicación web:
- URL: http://localhost:8000
- Credenciales por defecto: admin / admin

## Componentes del Sistema

### Orion Context Broker
- **Puerto**: 1026
- **Interfaz de gestión**: http://localhost:1026/version

### CrateDB 
- **Puerto**: 4200
- **Interfaz de gestión**: http://localhost:4200/

### QuantumLeap
- **Puerto**: 8668
- **Documentación API**: http://localhost:8668/v2

### Web App Django
- **Puerto**: 8000
- **Panel de administración**: http://localhost:8000/admin

### Agentes y Brokers
- **Agente_W_RS**: Puerto 4451
- **Broker_D_W_RS**: Puerto 4450

## Gestión de Sensores

La plataforma permite:

1. Ver todos los sensores registrados
2. Agregar nuevos sensores
3. Editar información de sensores
4. Eliminar sensores
5. Visualizar datos históricos

## Seguridad

- La interfaz web requiere autenticación
- Solo usuarios registrados pueden acceder al panel de sensores
- Comunicación segura entre componentes

## Resolución de Problemas

Si encuentras problemas al iniciar el sistema:

1. Verifica los logs de Docker: `docker-compose logs`
2. Asegúrate de que todos los puertos requeridos estén disponibles
3. Revisa las conexiones entre servicios con `docker-compose ps`
