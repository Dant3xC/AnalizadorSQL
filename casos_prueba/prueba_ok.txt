/* Ejemplo válido */
CREATE TABLE alumnos (id INT, nombre CHAR, promedio DECIMAL);
SELECT id, SUM(promedio) FROM alumnos HAVING SUM(promedio) > 6;
