"""
Esta es la expresion regular para el ejercicio 0, que se facilita
a modo de ejemplo:
"""
RE0 = "[a-zA-Z]+"

"""
Completa a continuacion las expresiones regulares para los
ejercicios 1-5:
"""
RE1 = "[a-zA-Z0-9_]+\.py"
RE2 = "-?(([1-9][0-9]*)|0)?(\.?|\.[0-9]*)"
RE3 = "[a-z]+\.[a-z]+@(estudiante\.)?uam.es"
RE4 = "([a-zA-Z ]*\([a-zA-Z ]*\))+[a-zA-Z ]*"
RE5 = "([a-zA-Z ]*\([a-zA-Z ]*(\([a-zA-Z ]*\))*\))+[a-zA-Z ]*"

"""
Recuerda que puedes usar el fichero prueba.py para probar tus
expresiones regulares.
"""

""" 
EJERCICIO 6:
Incluye a continuacion, dentro de esta cadena, tu respuesta 
al ejercicio 6.

La razón por la cual no es posible crear una expresión regular
que reconozca todas las secuencias de paréntesis bien anidadas
sin límite de profundidad es debido a que, para realizar una
secuencia sin límite es necesario definir esa secuencia de manera
recursiva; sin embargo, no hay forma de producir una expresión 
regular de manera recursiva. Sería necesaria una expresión regular
infinita.

"""
