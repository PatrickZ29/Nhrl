# Juez Logit
### *Sistema de Arbitraje Inteligente para Combates de Robótica*

[![Status](https://img.shields.io/badge/System-Active-10b981?style=for-the-badge)](https://github.com/tu-usuario/juez-logit)
[![Hardware](https://img.shields.io/badge/Hardware-Raspberry_Pi-C51A4A?style=for-the-badge&logo=raspberry-pi)](https://github.com/tu-usuario/juez-logit)
[![Interface](https://img.shields.io/badge/UI-Cyberpunk_Dark-00c6ff?style=for-the-badge)](https://github.com/tu-usuario/juez-logit)

**Juez Logit** es una plataforma de gestión y análisis técnico para competencias de robótica. Permite la integración directa con sistemas de captura de video en tiempo real, ofreciendo un veredicto automatizado basado en el análisis de los combates.

---

## Características Principales

* **Monitoreo en Vivo:** Panel de estado con polling automático para verificar la conexión con la cámara y el sistema de grabación.
* **Control Remoto:** Botones integrados para iniciar y detener grabaciones en la Raspberry Pi directamente desde la web.
* **Análisis Técnico:** Formulario especializado para cargar datos de los robots, imágenes de referencia (inicio/fin) y video en formato MP4.
* **Tarjeta de Resultados:** Despliegue dinámico del ganador con efectos visuales, tiempo de duración y detalles del análisis técnico.
* **Historial de Peleas:** Base de datos persistente con tabla de resultados históricos consultable sin recarga de página.

---

## Stack Tecnológico

| Componente | Tecnología |
| :--- | :--- |
| **Backend** | Python / Flask |
| **Frontend** | HTML5, CSS3 (Custom Variables), JS Vanilla |
| **Estética** | Cyber-Dark Mode / Glassmorphism |
| **Hardware** | Raspberry Pi (Control de cámara y almacenamiento) |

---

## Estructura del Repositorio

```text
juez-logit/
├── app.py                
├── static/               
├── templates/
│   └── index.html        #
├── recordings/           # Almacenamiento de videos capturados
└── history/              # Logs y base de datos de combates
