# 🤖 Bot de Automatización: Apertura y Asignación de Siniestros (Atlas)

Este proyecto es una herramienta de automatización que desarrollé utilizando **Python** y **Selenium**. Su objetivo principal es realizar el flujo completo de "End-to-End" (E2E) en el portal de pruebas (Prometeo QA) para la apertura de siniestros y la asignación de ajustadores.

El script automatiza desde el inicio de sesión hasta la asignación manual de un ajustador, pasando por el llenado de múltiples formularios y búsquedas dinámicas.

## 🚀 Funcionalidades Principales

El bot realiza las siguientes tareas de forma secuencial:

1. **Inicio de Sesión Automático:** Ingresa credenciales en el portal `prometeo-qa-demo`.
2. **Llenado de Formularios:** Completa automáticamente los datos del:
* Reportante (Nombre, Teléfonos, Causa).
* Conductor.
* Ubicación del Siniestro (Interacción con Google Maps inputs).
* Detalles del Siniestro (Fecha, Hora, Hechos, Color del vehículo).
* Ajuste Remoto (Selección de opciones negativas).


3. **Búsqueda Dinámica de Póliza:** Implementé un patrón de estrategia para buscar el siniestro por diferentes criterios según la necesidad del momento:
* `PLACAS`
* `POLIZA` (Tradicional)
* `SERIE`
* `SANTANDER`
* `INCISO`


4. **Asignación de Ajustador:** Navega al menú de seguimiento, filtra por "Por Asignar" y realiza la asignación manual del ajustador en la tabla.

## 📂 Estructura del Proyecto

Organicé el código de manera modular para facilitar el mantenimiento:

* `main.py`: Es el orquestador principal. Configura el driver de Chrome, contiene la clase `Atlas` con todos los métodos de navegación (Page Object Model simplificado) y ejecuta el flujo.
* `busquedas/`: Paquete que contiene la lógica específica para cada tipo de búsqueda.
* `busqueda_placas.py`, `busqueda_poliza.py`, etc.: Cada archivo maneja los selectores y pasos únicos para ese criterio de búsqueda.



## 🛠️ Requisitos e Instalación

Para correr este proyecto necesitas tener instalado Python y las siguientes librerías.

1. **Clona este repositorio o descarga los archivos.**
2. **Instala las dependencias:**
```bash
pip install selenium

```


3. **Driver:** Asegúrate de tener Google Chrome instalado. El script usa `webdriver.Chrome`, por lo que Selenium manager debería encargarse del driver automáticamente en versiones recientes.

## ▶️ Ejecución

Para iniciar el bot, simplemente ejecuta el archivo principal desde tu terminal:

```bash
python main.py

```

Al iniciar, el script te preguntará en la consola qué criterio de búsqueda quieres utilizar:

```text
--- CONFIGURACIÓN INICIAL ---
Opciones disponibles: POLIZA, SERIE, PLACAS, SANTANDER, INCISO
Ingrese el criterio de búsqueda deseado en mayusculas:

```

Si presionas `Enter` sin escribir nada, por defecto utilizará la búsqueda por **PLACAS**.

## ⚙️ Configuración Adicional

* **Modo Headless:** En la clase `Atlas` dentro de `main.py`, puedes cambiar `headless=False` a `True` si deseas que el navegador se ejecute en segundo plano sin interfaz gráfica.
* **Credenciales:** Actualmente las credenciales de prueba (`Testing` / `123456*`) están definidas como constantes al inicio de `main.py`.
