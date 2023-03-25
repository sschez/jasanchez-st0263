# ST02363 Tópicos Especiales en Telemática

# Estudiante: Jose Alejandro Sánchez Sánchez, jasanchez@eafit.edu.co

# Profesor: Edwin Nelson Montoya Munera, emontoya@eafit.edu.co


# Reto 3


# 1. breve descripción de la actividad

  

## 1.1. Qué aspectos cumplió o desarrolló de la actividad propuesta por el profesor (requerimientos funcionales y no funcionales)



## 1.2. Que aspectos NO cumplió o desarrolló de la actividad propuesta por el profesor (requerimientos funcionales y no funcionales)

Todos los requerimientos fueron implementados.

# 2. información general de diseño de alto nivel, arquitectura, patrones, mejores prácticas utilizadas.

![Arquitectura](./images/Arquitectura.png)


# 3. Descripción del ambiente de desarrollo y técnico: lenguaje de programación, librerias, paquetes, etc, con sus numeros de versiones.



# 3.1 Como se compila y ejecuta.
Para cada maquina se tiene que verificar de que los contenedores esten *up* y para eso se tiene que subir los docker-compose para cada una de la maquina.

1. Para la maquina de la base de datos:
    - **Entrar a la maquina por SSH->sschez-st0263-jasanchez->Reto 3->Wordpress-db**
    - **Después utilizar el siguiente comando:**
        - *docker-compose -f docker-compose-solo-wordpress-db.yml up -d*


2. Para la maquina de Wordpress-1:
    - **Entrar a la maquina por SSH->sschez-st0263-jasanchez->Reto 3->Wordpress-1**
    - **Después utilizar el siguiente comando:**
        - *docker-compose -f docker-compose-solo-wordpress-with-nfsclient.yml up -d*


3. Para la maquina de Wordpress-2:
    - **Entrar a la maquina por SSH->sschez-st0263-jasanchez->Reto 3->Wordpress-2**
    - **Después utilizar el siguiente comando:**
        - *docker-compose -f docker-compose-solo-wordpress-with-nfsclient.yml up -d*

4. Para la maquina de NGINX:
    - **Entrar a la maquina por SSH->wordpress**
    - **Después utilizar el siguiente comando:**
        - *docker-compose -f docker-compose-solo-nginx up -d*

Despues ya solo es ingresar al dominio: https://www.jasanchez.online y se veran los resultados.

# 3.2 Detalles del desarrollo.
Los detalles mas importantes en el desarrollo fueron: 
1. En la maquina virtual de NGINX se tuvo que hacer un proceso mas largo, debido a que se debia de sacar la certificación para poder que el dominio corriera por *https*. Luego se tuvo que modificar el *nginx.config* para que actuara como *LOAD BALANCER* y que redireccionara la carga a los wordpress.

2. En la maquina del NFS, se tuvo que colocar la siguiente linea en /etc/exports

        /var/nfs/general    10.128.0.0/16(rw,sync,no_root_squash,no_subtree_check)

    Para poder tener la comunicacion con ambos wordpres y poder guardar los archivos en su respectiva carpeta.

3. Para los Wordpress, se tuvo que agregar la dirección IP de la base de datos para cada docker-compose y ademas de eso se tuvo que realizar el comando

        sudo mount 10.128.0.5:/var/nfs/general /mnt/wordpress

    Para poder montar los datos en el nfs y que ambos wordpress recogieran la misma información.


# 3.3 Detalles técnicos:
- **Plataforma y servicios en nube:** Amazon GCP (Ubuntu 22.04 LTS)
- **Orquestación del proyecto:** Docker

# 3.4 Descripción y como se configura los parámetros del proyecto (ej: ip, puertos, conexión a bases de datos, variables de ambiente, parámetros, etc)

En primer lugar se comenzo creando 5 maquinas virtuales (NGINX, WP1,WP2,BD,NFS). Para la maquina de 


# 3.5 Detalles de la organización del código por carpetas o descripción de algún archivo. (ESTRUCTURA DE DIRECTORIOS Y ARCHIVOS IMPORTANTE DEL PROYECTO, comando 'tree' de linux)

![](./assets/tree.png)

# 4. Descripción del ambiente de EJECUCIÓN (en producción) lenguaje de programación, librerias, paquetes, etc, con sus numeros de versiones.

El proyecto se realizo en 5 maquinas virtuales:

1. Ngnix: Como un balanceador de cargas.

2. Wordpress-1: Wordpress aislado.

        nfs-common

3. Wordpress-2: Wordpress aislado.

        nfs-common

4. Base de Datos: Base de datos mysql aislada pero conectada con ambos Wordpress.

5. NFS-Server: Servidor que sirve para que los cambios que se hagan en ambos wordpress se vean reflejados en la misma base de datos y no sean diferentes sino que cada uno tenga la misma copia en tiempo real. 

        nfs-kernel-server

# IP o nombres de dominio en nube o en la máquina servidor.
- https://www.jasanchez.online : Es el dominio donde esta el Reto 3 completo.

## Descripción y como se configura los parámetros del proyecto (ej: ip, puertos, conexión a bases de datos, variables de ambiente, parámetros, etc)

  Puesto que el proyecto se construyó utilizando docker-compose, el ambiente de ejecucion tanto en desarrollo como en producción es el mismo. Lo que se debe tener presente es que deben habilitar los puertos necesarios en AWS para permitir las comunicaciones.


## Como se lanza el servidor.



## Una mini guia de como un usuario utilizaría el software o la aplicación


## Resultados

![](./assets/Resultado.png)


# referencias:

#### versión README.md -> 1.0 (2022-agosto)