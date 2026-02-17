@echo off
title Bot de Automatización - Seguros Atlas
echo === 1. ACTUALIZANDO CODIGO (GIT PULL) ===
git pull

echo.
echo === 2. VERIFICANDO ENTORNO VIRTUAL ===
if not exist venv (
    echo Creando entorno virtual...
    python -m venv venv
)

echo === 3. INSTALANDO DEPENDENCIAS Y NAVEGADORES ===
call venv\Scripts\activate
pip install -r requirements.txt
playwright install

echo.
echo === 4. INICIANDO BOT DE ATLAS ===
:: Usamos test_flujo.py ya que es el que contiene la lógica de interacción
python test_flujo.py

echo.
echo Proceso terminado.
pause