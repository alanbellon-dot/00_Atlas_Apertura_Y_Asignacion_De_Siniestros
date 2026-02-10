

# 🤖 Bot de Automatización de Siniestros (Versión Playwright)

Este proyecto es una herramienta de automatización de alto rendimiento migrada de Selenium a **Playwright**. Automatiza el ciclo completo de apertura, búsqueda y asignación de siniestros en el portal de "Aseguradora Digital".

Gracias a Playwright, esta versión es **más rápida, estable y resistente** a problemas de red o renderizado (como los mapas de Google o tablas dinámicas).

## 🚀 Características Clave

* **Page Object Model (POM):** Código organizado y modular en la carpeta `pages/`.
* **Manejo Inteligente de Esperas:** Adiós a los `time.sleep` fijos; el bot espera automáticamente a que los elementos estén listos.
* **Google Maps Blindado:** Estrategia híbrida (Click + Teclado) para asegurar que las direcciones se seleccionen correctamente.
* **Búsqueda Avanzada de Pólizas:** Detecta automáticamente la fila "ACTIVA" en tablas dinámicas.
* **Autorecuperación:** Si una iteración falla, el bot toma una **captura de pantalla del error**, refresca la página e intenta con la siguiente.

## 📂 Estructura del Proyecto

```text
PROYECTO/
├── pages/                  # Lógica de cada pantalla (Page Objects)
│   ├── login_page.py       # Inicio de sesión
│   ├── apertura_page.py    # Formularios, Mapas y Búsqueda de Póliza
│   └── asignacion_page.py  # Lógica de asignación a proveedores
├── venv/                   # Entorno virtual (no se sube al repo)
├── main.py                 # Script principal (Ejecutor)
├── requirements.txt        # Dependencias del proyecto
└── README.md               # Documentación

```

## 📋 Requisitos Previos

* **Python 3.8+**: [Descargar Python](https://www.python.org/downloads/)
* **Sistema Operativo**: Windows, Mac o Linux.

## ⚙️ Instalación

1. **Clonar o descargar** el proyecto.
2. **Crear un entorno virtual** (recomendado):
```bash
python -m venv venv

```


* *Windows:* `.\venv\Scripts\activate`
* *Mac/Linux:* `source venv/bin/activate`


3. **Instalar dependencias**:
```bash
pip install -r requirements.txt

```


4. **Instalar navegadores de Playwright**:
Este paso es vital para que funcione el motor de automatización.
```bash
playwright install

```



## ▶️ Cómo Ejecutar

Asegúrate de tener tu entorno virtual activado y ejecuta:

```bash
python main.py

```

### Interacción

El bot te hará dos preguntas en la consola:

1. **Cantidad de iteraciones:** ¿Cuántos siniestros quieres crear?
2. **Búsqueda Avanzada:** Escribe `si` para usar el flujo complejo de "Gestor de Póliza" o `no` para usar la limpieza estándar.

## 🛠 Solución de Problemas

* **Error "Strict Mode Violation":** Significa que el bot encontró múltiples elementos iguales. El código ya está parcheado con `.first` para evitar esto.
* **El formulario no avanza:** El bot tomará una foto llamada `error_apertura_X.png`. Revisa la imagen para ver qué campo obligatorio faltó (usualmente dirección o teléfono).
* **Login fallido:** Verifica que las credenciales en `pages/login_page.py` sean las correctas.

---

*Desarrollado con 🎭 Playwright y Python*