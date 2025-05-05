# Product Requirements Document (PRD): Sistema IoT de Monitoreo Temperatura-Humedad

## Información del Proyecto
- **Nombre del Proyecto**: ProyectoIoT2025_10MJ
- **Fecha**: Mayo 5, 2025
- **Versión**: 1.0
- **Autor**: [Tu Nombre]

## Resumen Ejecutivo
Este proyecto implementa una solución completa de Internet de las Cosas (IoT) para el monitoreo de temperatura y humedad en tiempo real. Utiliza el framework FIWARE para gestionar los datos y proporcionar una arquitectura escalable basada en microservicios con Docker.

## Contexto y Alcance
El sistema está diseñado para capturar datos de sensores de temperatura y humedad, procesarlos a través de varios brokers para garantizar seguridad y disponibilidad, y finalmente almacenarlos en una base de datos que permite su posterior análisis y visualización.

## Descripción General del Sistema
El sistema emplea una arquitectura de microservicios con los siguientes componentes principales:

1. **Agente de Hardware (agente_w_ht)**:
   - Conecta directamente con los sensores físicos a través de comunicación serial
   - Proporciona una API REST para acceder a los datos más recientes
   - Almacena temporalmente las lecturas en formato JSON

2. **Broker de Datos (broker_d_w_ht)**:
   - Recolecta periódicamente los datos del agente
   - Maneja la transferencia de datos hacia el siguiente componente en la cadena

3. **Broker de Seguridad (broker_s_l_rs)**:
   - Actúa como intermediario para garantizar la seguridad en la transferencia de datos
   - Reenvía los datos al Context Broker Orion de FIWARE

4. **Infraestructura FIWARE**:
   - Context Broker Orion: gestiona el contexto de datos
   - QuantumLeap: permite la persistencia de datos históricos
   - MongoDB: almacena datos de contexto actual
   - CrateDB: almacena series temporales para análisis histórico

## Requisitos Funcionales

### RF-1: Captura de Datos
- El sistema debe leer datos de temperatura y humedad desde un dispositivo conectado por puerto serial
- Frecuencia de muestreo: cada 0.5 segundos verificar disponibilidad de nuevos datos
- Formato de datos: JSON con campos timestamp, temperatura y humedad

### RF-2: Almacenamiento y Transferencia de Datos
- Los datos deben almacenarse temporalmente en formato JSON
- El broker de datos debe enviar actualizaciones cada 10 segundos
- El sistema debe implementar una arquitectura de transferencia en cascada para garantizar la seguridad

### RF-3: Exposición de Datos
- API REST para consultar el último dato capturado
- Los datos históricos deben ser accesibles a través de la API de QuantumLeap
- Posibilidad de integración con herramientas de visualización (comentado en el código actual)

### RF-4: Integración con FIWARE
- Compatibilidad con el Context Broker Orion-LD
- Persistencia histórica a través de QuantumLeap
- Las entidades deben seguir el modelo de datos NGSI-LD

## Requisitos No Funcionales

### RNF-1: Escalabilidad
- Implementación basada en contenedores Docker para facilitar el escalado
- Arquitectura distribuida con componentes independientes

### RNF-2: Disponibilidad
- El sistema debe continuar funcionando incluso si hay caídas temporales en alguno de los componentes
- Reintentos automáticos en caso de fallos en la comunicación

### RNF-3: Seguridad
- Uso de un broker dedicado a la seguridad para la transferencia de datos
- Control de acceso a las APIs expuestas

### RNF-4: Mantenibilidad
- Código organizado en microservicios independientes
- Estructura modular para facilitar actualizaciones

### RNF-5: Rendimiento
- Tiempo máximo de respuesta para consultas en tiempo real: < 1 segundo
- Capacidad de procesar al menos 1 medición cada 10 segundos

## Arquitectura Técnica
```
[Sensor] → [Agente (agente_w_ht)] → [Broker Datos (broker_d_w_ht)] → 
[Broker Seguridad (broker_s_l_rs)] → [Orion Context Broker] → 
[QuantumLeap] → [CrateDB]
```

### Tecnologías Utilizadas
- **Backend**: Python, Flask
- **Comunicación**: REST APIs, Serial
- **Almacenamiento**: MongoDB, CrateDB
- **Contenedorización**: Docker, Docker Compose
- **Plataforma IoT**: FIWARE (Orion-LD, QuantumLeap)

## Interfaz de Usuario
El sistema actual está enfocado principalmente en el backend, pero incluye comentarios para una futura integración con un frontend basado en Streamlit.

## Consideraciones de Despliegue
- Requisitos de sistema: Docker, Docker Compose
- Necesidad de configurar correctamente el puerto serial según el sistema operativo (COM4 en Windows, /dev/ttyUSB0 en Linux)
- Ajuste de vm.max_map_count para optimizar el rendimiento de Elasticsearch (como se comenta en docker-compose.yml)

## Plan de Implementación Propuesto
1. Completar los archivos Dockerfile faltantes para los componentes:
   - agente_w_ht
   - broker_d_w_ht
   - broker_s_l_rs
2. Implementar un frontend para visualización de datos (posiblemente con Streamlit)
3. Configurar correctamente la integración entre el broker de seguridad y Orion
4. Desarrollo de dashboard para visualizar tendencias históricas de temperatura y humedad

## Dependencias del Sistema
- Python 3.x
- Flask 2.3.0 o superior
- pyserial
- Docker y Docker Compose
- FIWARE Orion-LD
- QuantumLeap
- MongoDB
- CrateDB

## Métricas de Éxito
- Captación continua de datos sin pérdidas durante al menos 24 horas
- Tiempo de respuesta promedio de las APIs < 500ms
- Correcta persistencia de datos históricos accesibles para análisis

## Apéndice: Diagrama de Flujo de Datos
```
┌─────────┐       ┌────────────┐       ┌─────────────┐       ┌─────────────┐
│         │       │            │       │             │       │             │
│ Sensores├──────►│ Agente IoT ├──────►│Broker Datos ├──────►│Broker Segur.│
│         │Serial │            │ JSON  │             │ JSON  │             │
└─────────┘       └────────────┘       └─────────────┘       └──────┬──────┘
                                                                    │
                     ┌───────────┐       ┌────────────┐       ┌─────▼─────┐
                     │           │       │            │       │           │
                     │  CrateDB  │◄──────┤QuantumLeap │◄──────┤   Orion   │
                     │           │       │            │       │           │
                     └───────────┘       └────────────┘       └───────────┘
                           ▲                                        │
                           │                                        │
                           │            ┌────────────┐              │
                           │            │            │              │
                           └────────────┤  MongoDB   │◄─────────────┘
                                        │            │
                                        └────────────┘
```