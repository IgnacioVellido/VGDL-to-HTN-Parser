# Siadex_Planner_ROS

Para hacer que funcione:
- Cambiar en Makefile y archivos de Cmake la ruta de la carpeta
- Cambiar INT_MAX por INT32_MAX en fluentVar.hh
- Instalar GNU Readline (no lo consigo, ni con libreadline6, ni libreadline7, ni lib32readline-dev, ni lib32readline7) -> Tras reinstalar Ubunutu, instalando libreadline-dev, y añadiendo línea inutil en CMakeList.txt, parece que funciona
- Instalar python-dev package
- Cambiar #include "structmember.h" por #include <python2.7/structmember.h> en archivos en src

https://stackoverflow.com/questions/34176416/error-compiling-structmember-h-from-python2-7-library
Según stack falta una definición de preprocesamiento 
