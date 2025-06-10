CREATE DATABASE IF NOT EXISTS salonesdb;
USE salonesdb;

CREATE TABLE aulas (
    id_aula INT PRIMARY KEY,
    ip_aula VARCHAR(15) NOT NULL,
    estado TINYINT NOT NULL
);