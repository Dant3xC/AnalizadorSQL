/* Archivo de prueba VALIDO.
  Contiene una sentencia CREATE y una SELECT...HAVING.
*/

CREATE TABLE empleados (
    id INT,
    nombre CHAR,
    salario DECIMAL
);

SELECT departamento, COUNT(id)
FROM empleados
HAVING COUNT(id) > 10;