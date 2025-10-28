/* Archivo de prueba con ERROR LÉXICO.
  El carácter '@' no está definido en los tokens.
*/

SELECT nombre FROM usuarios WHERE email = @email_usuario;