# Como utilizar el proyecto
# 1. Crear la base de datos
- Crear la base de datos vacia, por ejemplo "idatos2022"
- Configurar el contenido de los archivos `utils/db.py` con las credenciales de la base nueva
- Usar el comando `psql idatos2022 < utils/init_database.sql` para inicializar las tablas
- Usar el comando `python3 utils/csv_loader.py` para cargar las tablas recien creadas

# 2. Iniciar el servidor
- Configurar el contenido de los archivos `application/api/config.py` con las credenciales de la base
- Instalar dependencias `pip3 install requirements.txt`
- Dentro de `application/api` ejecutar `python3 api.py`

# 3. Iniciar el frontend
- Dentro de `application` ejecutar `npm install` para instalar las dependencias
- Ejecutar `npm start`
