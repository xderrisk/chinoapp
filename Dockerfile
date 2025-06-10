# docker build -t salonesdb .

# Usar la imagen oficial de MySQL
FROM mysql

# Establecer variables de entorno para MySQL
ENV MYSQL_ROOT_PASSWORD=root
ENV MYSQL_DATABASE=salonesdb

# Copiar el archivo SQL de inicialización al contenedor
COPY sql/setup.sql /docker-entrypoint-initdb.d/

# Exponer el puerto de MySQL
EXPOSE 3306