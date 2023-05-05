# ST0263 Tópicos Especiales en Telematica

# Estudiantes: 
- Mauricio Escudero, mescude1@eafit.edu.co
- Jose Alejandro Sánchez Sánchez, jasanchez@eafit.edu.co
- Edison Alejandro Torres Muñoz, eatorresm@eafit.edu.co
#
# Profesor: Edwin Nelson Montoya Munera, emontoya@eafit.edu.co

# Proyecto 2
#
# 1. Breve descripción de la actividad
Desplegar una aplicación open source LAMP de comunidad que represente un sistema de
información del tipo Sistema de Gestión de Aprendizaje y para eso se selecciono Moodle.
#
# 1.1. Que aspectos cumplió o desarrolló de la actividad propuesta por el profesor (requerimientos funcionales y no funcionales)


# 1.2. Que aspectos NO cumplió o desarrolló de la actividad propuesta por el profesor (requerimientos funcionales y no funcionales)

Todos los requerimientos fueron implementados.

# 2. Información general de diseño de alto nivel, arquitectura, patrones, mejores prácticas utilizadas.
![Arquitectura](./assets/Arquitectura.png)

La arquitectura descrita tiene un cliente que envía solicitudes HTTP a través de Internet. Terraform se utiliza para describir y configurar la infraestructura de GCP, que incluye la creación de recursos como instancias de máquinas virtuales, redes y equilibradores de carga. El equilibrador de carga distribuye el tráfico entre las instancias de la aplicación web que se ejecutan en GCP. La aplicación web está creada con Moddle y utiliza NFS para compartir datos entre las instancias. Por último, la base de datos de la aplicación web se aloja en Cloud SQL.

A continuacion se explicara cada uno y su relacion en la arquitectura:
- *Cliente:* Es el usuario final que interactúa con la aplicación web. El cliente envía solicitudes HTTP a través de Internet.

- *Terraform:* Es una herramienta de infraestructura como código que permite a los desarrolladores definir y administrar su infraestructura en la nube de forma programática. En este caso, Terraform se utiliza para describir y configurar la infraestructura de GCP, lo que incluye la creación de recursos como instancias de máquinas virtuales, redes y equilibradores de carga.

- *Load balancer:* Es un servicio que distribuye el tráfico de entrada entre varias instancias de la aplicación. En este caso, se utiliza un equilibrador de carga para distribuir el tráfico entre las instancias de la aplicación web que se ejecutan en GCP.

- *Moodle:* Es un software de gestión del aprendizaje que se utiliza para crear cursos en línea y contenido educativo.

- *NFS:* Es un protocolo de sistema de archivos de red que permite a los usuarios acceder y compartir archivos y directorios de forma remota. En este caso, se utiliza NFS para compartir datos entre las instancias de la aplicación web.

- *Cloud SQL:* Es un servicio de bases de datos relacionales completamente administrado en la nube que se utiliza para alojar la base de datos de la aplicación web.


# 3. Descripción del ambiente de desarrollo y técnico: lenguaje de programación, librerias, paquetes, etc, con sus numeros de versiones.

# 3.1. Como se compila y ejecuta.


# 3.2. Detalles del desarrollo.


# 3.3. Detalles técnicos
Dentro del main.tf se puede encontrar los siguientes detalles:

- Modulo de nfs:

        module "nfs" {
        source      = "DeimosCloud/nfs/google"
        name_prefix = "moodle-nfs"
        labels      = {}
        project     = "reto4-moodle"
        network     = google_compute_network.reto4_network.name
        export_paths = [
            "/mnt/moodle",
            "/mnt/moodledata"
        ]
        capacity_gb = "10"
        attach_public_ip = true
        }

            resource "google_sql_database_instance" "moodle_db_primary" {
                name             = "moodle-db-primary"
                database_version = "POSTGRES_14"
                region           = "us-central1"

                settings {
                    # Second-generation instance tiers are based on the machine
                    # type. See argument reference below.
                    tier = "db-f1-micro"
                }
            }

            resource "google_sql_database" "moodle_db" {
            name     = "bitnami_moodle"
            instance = google_sql_database_instance.moodle_db_primary.name
            }

            resource "google_sql_user" "users" {
            name     = "bn_moodle"
            instance = google_sql_database_instance.moodle_db_primary.name
            password = "password"
            }

            resource "google_compute_target_pool" "reto4_target_pool" {
                name = "reto4-target-pool"
                project = "reto4-moodle"
                region = "us-central1"
            }

- Modulo de load balancer:

        module "lb" {
            source = "GoogleCloudPlatform/lb/google"
            version = "2.2.0"
            region = "us-central1"
            name = "load-balancer"
            service_port = 80
            target_tags = ["reto4-target-pool"]
            network = google_compute_network.reto4_network.name
        }

        resource "google_compute_autoscaler" "reto4_autoscaler" {
            name = "reto4-autoscaler"
            project = "reto4-moodle"
            zone = "us-central1-c"
            target = google_compute_instance_group_manager.reto_4_group_manager.self_link

            autoscaling_policy {
            max_replicas = 5
            min_replicas = 1
            cooldown_period = 60

                cpu_utilization {
                target = 0.5    
                }
            }
        }

        resource "google_compute_instance_template" "reto4_moodle_template" {
        name = "reto4-instance-template"
        machine_type = "e2-micro"
        can_ip_forward = false
        project = "reto4-moodle"
        tags = ["allow-lb-service"]

            disk {
                source_image = data.google_compute_image.reto4_moodle_image.self_link
            }

            network_interface {
                network = google_compute_network.reto4_network.name
            }

            service_account {
                scopes = ["userinfo-email", "compute-ro", "storage-ro"]
            }
        }


        resource "google_compute_instance_group_manager" "reto_4_group_manager" {
            name = "reto4-igm"
            zone = "us-central1-c"
            project = "reto4-moodle"
            version {
                instance_template = google_compute_instance_template.reto4_moodle_template.self_link
                name = "primary"
            }

            target_pools = [google_compute_target_pool.reto4_target_pool.self_link]
            base_instance_name = "st263"
        }

        data "google_compute_image" "reto4_moodle_image" {
            name = "reto4-seed"
            project = "reto4-moodle"
        }


# 3.4. Descripción y como se configura los parámetros del proyecto (ej: ip, puertos, conexión a bases de datos, variables de ambiente, parámetros, etc)
A continuacion se mostrarán las instancias que se tienen en GCP:

- SQL
![SQL](./assets/SQL.png)
- DISK
![DISK](./assets/DISK.jpeg)
- Group
![GROUP](./assets/GROUP.jpeg)
- Virtual Machines Instances
![VM](./assets/VM.jpeg)
- Load balancer
![LB](./assets/LB.jpeg)
- Templates
![Templates](./assets/Templates.jpeg)


# 3.5. Detalles de la organización del código por carpetas o descripción de algún archivo. (ESTRUCTURA DE DIRECTORIOS Y ARCHIVOS IMPORTANTE DEL PROYECTO, comando 'tree' de linux)
![tree](./assets/tree.jpeg)

# 4. Descripción del ambiente de EJECUCIÓN (en producción) lenguaje de programación, librerias, paquetes, etc, con sus numeros de versiones.

- Terraform: Terraform es una herramienta de infraestructura como código (IaC) que permite a los usuarios describir y gestionar la infraestructura de sus aplicaciones de manera declarativa. En lugar de crear y configurar manualmente los recursos de la infraestructura en la nube, los usuarios pueden definirlos en un archivo de configuración de Terraform y aplicar los cambios con un solo comando. Además, Terraform proporciona una interfaz para interactuar con los servicios y recursos de GCP, lo que permite a los usuarios definir su infraestructura en términos de recursos de GCP y gestionarlos de manera consistente y escalable. Con Terraform, los usuarios pueden crear y administrar fácilmente sus recursos de GCP, como instancias de máquinas virtuales, redes y bases de datos, entre otros.

Sabiendo ya que es Terraform, se utilizó un Script en el cual se ejecuta el init y terraform crea las instancias y las configura, terraform evita algunos trabajos, sin embargo, hay que hacer unas configraciones manuales para el proyecto.