### **Actividad: Automatización de implementación y configuración de políticas de sudo con Ansible**

**Objetivo:** Implementar y automatizar la configuración de una aplicación web Python Flask en una máquina virtual Ubuntu utilizando Ansible y Vagrant. Configurarás políticas de **sudoers** para controlar los permisos de usuarios y permitirás que un usuario específico ejecute comandos elevados de manera segura.

#### **Requisitos previos**

- **Vagrant** instalado en tu sistema.
- **VirtualBox** instalado.
- **Ansible** instalado en tu máquina host.
- Conocimientos básicos de línea de comandos y edición de archivos de texto.
- Familiaridad con YAML, Ansible y conceptos básicos de Linux.

#### **Pasos de la actividad**

#### **1. Crear el entorno de trabajo**

Crea un nuevo directorio para tu proyecto y navega a él:

```bash
$ mkdir proyecto_sudoers
$ cd proyecto_sudoers
```

#### **2. Inicializar un Vagrantfile**

Inicializa un `Vagrantfile` para una máquina virtual Ubuntu:

```bash
$ vagrant init ubuntu/focal64
```

#### **3. Modificar el Vagrantfile**

Edita el `Vagrantfile` para agregar las siguientes configuraciones:

- **Configurar la red privada**:

  ```ruby
  config.vm.network "private_network", type: "dhcp"
  ```

- **Configurar el proveedor VirtualBox**:

  ```ruby
  config.vm.provider "virtualbox" do |vb|
    vb.memory = "1024"
    vb.name = "vm_sudoers"
  end
  ```

- **Configurar el aprovisionador Ansible**:

  ```ruby
  config.vm.provision "ansible" do |ansible|
    ansible.playbook = "site.yml"
  end
  ```

#### **4. Crear el playbook de Ansible `site.yml`**

Crea un archivo llamado `site.yml` y agrega el siguiente contenido:

```yaml
---
- name: Aprovisionar VM
  hosts: all
  become: yes
  become_method: sudo
  remote_user: vagrant
  tasks:
    - import_tasks: tasks/user_and_group.yml
    - import_tasks: tasks/web_application.yml
    - import_tasks: tasks/sudoers.yml
```

#### **5. Crear el directorio de tareas**

Crea un directorio llamado `tasks` donde almacenaremos nuestras tareas:

```bash
$ mkdir tasks
```

#### **6. Crear la tarea `user_and_group.yml`**

En el directorio `tasks`, crea el archivo `user_and_group.yml` con el siguiente contenido:

```yaml
---
- name: Asegurar que el grupo 'desarrolladores' exista
  group:
    name: desarrolladores
    state: present

- name: Crear el usuario 'bender'
  user:
    name: bender
    shell: /bin/bash
    groups: desarrolladores
    append: yes
```

#### **7. Crear la tarea `web_application.yml`**

Crea el archivo `web_application.yml` en el directorio `tasks`:

```yaml
---
- name: Instalar python3-flask, gunicorn3 y nginx
  apt:
    name:
      - python3-flask
      - gunicorn3
      - nginx
    update_cache: yes

- name: Crear directorio para la aplicación
  file:
    path: /opt/engineering
    state: directory
    mode: '0750'
    owner: bender
    group: desarrolladores

- name: Copiar aplicación de muestra de Flask
  copy:
    src: "{{ item }}"
    dest: "/opt/engineering/"
    mode: '0750'
    owner: bender
    group: desarrolladores
  loop:
    - files/greeting.py
    - files/wsgi.py

- name: Copiar el archivo de la unidad Systemd para el saludo
  copy:
    src: files/greeting.service
    dest: "/etc/systemd/system/greeting.service"
    mode: '0644'

- name: Iniciar y habilitar la aplicación de saludo
  systemd:
    name: greeting.service
    state: started
    enabled: yes
    daemon_reload: yes
```

#### **8. Crear los archivos de la aplicación Flask**

Crea un directorio llamado `files` dentro de `tasks` y añade los archivos necesarios:

```bash
$ mkdir tasks/files
```

#### **8.1. Crear `greeting.py`**

Crea el archivo `greeting.py` en `tasks/files/` con el siguiente contenido:

```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return "<h1 style='color:green'>¡Greetings!</h1>"

if __name__ == '__main__':
    app.run(host='0.0.0.0')
```

#### **8.2. Crear `wsgi.py`**

Crea el archivo `wsgi.py` en `tasks/files/` con el siguiente contenido:

```python
from greeting import app

if __name__ == "__main__":
    app.run()
```

#### **8.3. Crear `greeting.service`**

Crea el archivo `greeting.service` en `tasks/files/` con el siguiente contenido:

```ini
[Unit]
Description=Greeting Application

[Service]
WorkingDirectory=/opt/engineering
ExecStart=/usr/bin/gunicorn3 --access-logfile - --error-logfile - wsgi:app
Restart=always
User=bender
Group=desarrolladores

[Install]
WantedBy=multi-user.target
```

#### **9. Crear la tarea `sudoers.yml`**

Crea el archivo `sudoers.yml` en el directorio `tasks`:

```yaml
---
- name: Establecer variable para el archivo de la aplicación
  set_fact:
    greeting_application_file: "/opt/engineering/greeting.py"

- name: Crear archivo sudoers para el grupo de desarrolladores
  template:
    src: "developers.j2"
    dest: "/etc/sudoers.d/developers"
    validate: "/usr/sbin/visudo -cf %s"
  owner: root
  group: root
  mode: '0440'
```

#### **10. Crear la plantilla `developers.j2`**

Crea un directorio llamado `templates` y añade la plantilla:

```bash
$ mkdir templates
```

Crea el archivo `developers.j2` en `templates/` con el siguiente contenido:

```jinja
Cmnd_Alias GREETING_STOP = /bin/systemctl stop greeting, /bin/systemctl stop greeting.service
Cmnd_Alias GREETING_START = /bin/systemctl start greeting, /bin/systemctl start greeting.service
Cmnd_Alias GREETING_RESTART = /bin/systemctl restart greeting, /bin/systemctl restart greeting.service

Host_Alias LOCAL_VM = {{ ansible_default_ipv4.address }}

%desarrolladores LOCAL_VM=(root) NOPASSWD: GREETING_STOP, GREETING_START, GREETING_RESTART, sudoedit {{ greeting_application_file }}
```

#### **11. Actualizar el playbook para incluir la plantilla**

Edita el `site.yml` para agregar la ruta a las plantillas:

```yaml
---
- name: Aprovisionar VM
  hosts: all
  become: yes
  become_method: sudo
  remote_user: vagrant
  vars:
    ansible_python_interpreter: /usr/bin/python3
  tasks:
    - import_tasks: tasks/user_and_group.yml
    - import_tasks: tasks/web_application.yml
    - import_tasks: tasks/sudoers.yml
  vars_files:
    - templates/developers.j2
```

#### **12. Levantar y aprovisionar la máquina virtual**

Ejecuta el siguiente comando para crear y configurar la VM:

```bash
$ vagrant up
```

Este comando:

- Creará la VM según el `Vagrantfile`.
- Ejecutará el playbook de Ansible, aplicando las tareas definidas.

#### **13. Verificar la configuración**

#### **13.1. Iniciar sesión como `bender`**

Conéctate a la VM como el usuario `bender`:

```bash
$ vagrant ssh
vagrant@vm_sudoers:~$ sudo su - bender
```

#### **13.2. Probar la aplicación web**

Ejecuta el siguiente comando para verificar que la aplicación está en funcionamiento:

```bash
bender@vm_sudoers:~$ curl http://localhost:5000
```

Deberías ver:

```
<h1 style='color:green'>¡Greetings!</h1>
```

#### **13.3. Editar `greeting.py` usando `sudoedit`**

Edita el archivo `greeting.py`:

```bash
bender@vm_sudoers:~$ sudoedit /opt/engineering/greeting.py
```

Realiza el cambio sugerido en el texto de saludo:

```python
return "<h1 style='color:green'>¡Greetings and Salutations!</h1>"
```

Guarda el archivo y cierra el editor.

#### **13.4. Reiniciar la aplicación**

Detén la aplicación:

```bash
bender@vm_sudoers:~$ sudo systemctl stop greeting
```

Inicia la aplicación:

```bash
bender@vm_sudoers:~$ sudo systemctl start greeting
```

#### **13.5. Verificar los cambios**

Ejecuta nuevamente el comando `curl`:

```bash
bender@vm_sudoers:~$ curl http://localhost:5000
```

Ahora deberías ver:

```
<h1 style='color:green'>¡Greetings and Salutations!</h1>
```

#### **13.6. Probar comandos no permitidos**

Intenta ejecutar un comando no autorizado:

```bash
bender@vm_sudoers:~$ sudo tail /var/log/auth.log
```

Deberías recibir un mensaje de "command not allowed" o similar, indicando que no tienes permisos para ejecutar ese comando.

#### **14. Verificar los registros de auditoría**

Como usuario `vagrant`, revisa el archivo de registros:

```bash
bender@vm_sudoers:~$ exit
vagrant@vm_sudoers:~$ sudo tail /var/log/auth.log
```

Observa las entradas relacionadas con los comandos `sudo` ejecutados por `bender`.

#### **15. Destruir la máquina virtual (opcional)**

Si deseas liberar recursos:

```bash
$ vagrant destroy
```


Con esta actividad, has aprendido a:

- **Automatizar la implementación de una aplicación web** utilizando Ansible.
- **Configurar políticas de sudoers** para controlar los permisos de usuarios.
- **Gestionar servicios con systemd** y controlarlos mediante comandos privilegiados.
- **Aplicar principios de Infraestructura como Código (IaC)** para mejorar la seguridad y consistencia en la gestión de sistemas.
- **Auditar comandos ejecutados con sudo** y entender la importancia del rastro de auditoría.



¡Felicidades por completar la actividad! Has dado un paso importante en el dominio de la Infraestructura como Código y la gestión segura de sistemas Linux.
