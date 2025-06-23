# Chatbot con Groq

## Requisitos previos
- Python 3.8 o superior
- Cuenta en Groq y API key (https://console.groq.com/)

## Instalación

1. Crear entorno virtual:
```bash
python -m venv venv
```

## Despliegue

### Opción 1: Streamlit Cloud
1. Subir a un repositorio GitHub
2. Conectar a Streamlit Cloud

### Opción 2: Auto-hospedaje
1. Instalar dependencias en servidor
2. Ejecutar con:
```bash
streamlit run chat-groq.py --server.port=8501