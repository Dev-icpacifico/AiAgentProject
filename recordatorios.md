# 📌 Recordatorios Rápidos para Desarrollo

Este documento contiene comandos y procedimientos útiles para el desarrollo de software en Python y el manejo de Git.

---

## 🐍 Configuración de Entorno Virtual en Python

### 📌 Crear un entorno virtual
```bash
python -m venv venv
```

### 📌 Activar el entorno virtual
- **Windows:**
  ```bash
  venv\Scripts\activate
  ```
- **Mac/Linux:**
  ```bash
  source venv/bin/activate
  ```

### 📌 Desactivar el entorno virtual
```bash
deactivate
```

---

## 📦 Manejo de Dependencias en Python

### 📌 Crear un `requirements.txt`
```bash
pip freeze > requirements.txt
```

### 📌 Instalar dependencias desde `requirements.txt`
```bash
pip install -r requirements.txt
```

### 📌 Instalar una librería específica y guardarla en `requirements.txt`
```bash
pip install nombre_libreria
pip freeze > requirements.txt
```

---

## 🔧 Comandos Básicos de Git

### 📌 Configurar Git (solo la primera vez)
```bash
git config --global user.name "Tu Nombre"
git config --global user.email "tuemail@example.com"
```

### 📌 Inicializar un repositorio
```bash
git init
```

### 📌 Clonar un repositorio
```bash
git clone https://github.com/usuario/repositorio.git
```

### 📌 Agregar cambios y hacer commit
```bash
git add .
git commit -m "Descripción del cambio"
```

### 📌 Subir cambios al repositorio remoto
```bash
git push origin main
```

### 📌 Obtener los últimos cambios del repositorio
```bash
git pull origin main
```

### 📌 Crear y cambiar de rama
```bash
git checkout -b nueva_rama
```

---
