
### **Actividad: Gestión de usuarios y seguridad en Linux con Ansible**

**Objetivo:** Automatizar la configuración de políticas de contraseñas, gestión de usuarios y grupos, y permisos de archivos y directorios en una máquina virtual Ubuntu utilizando Ansible y Vagrant.

#### **Requisitos previos**

- **Vagrant** instalado en tu sistema.
- **VirtualBox** instalado.
- **Ansible** instalado en tu máquina host.
- Conocimientos básicos de línea de comandos y edición de archivos de texto.
- Familiaridad con YAML y los conceptos básicos de Ansible.

### **Pasos de la actividad**

#### **1. Crear el entorno de trabajo**

Crea un nuevo directorio para tu proyecto y navega a él:

```bash
$ mkdir proyecto_seguridad
$ cd proyecto_seguridad
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
    vb.name = "vm_seguridad"
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
- name: Aprovisionar VM con políticas de seguridad
  hosts: all
  become: yes
  become_method: sudo
  remote_user: vagrant
  tasks:
    - import_tasks: tasks/pam_pwquality.yml
    - import_tasks: tasks/user_and_group.yml
```

#### **5. Crear el directorio de tareas**

Crea un directorio llamado `tasks` donde almacenaremos nuestras tareas:

```bash
$ mkdir tasks
```

#### **6. Crear la tarea `pam_pwquality.yml`**

Dentro del directorio `tasks`, crea el archivo `pam_pwquality.yml` con el siguiente contenido:

```yaml
---
- name: Instalar libpam-pwquality
  apt:
    name: libpam-pwquality
    state: present

- name: Configurar pam_pwquality
  lineinfile:
    path: "/etc/pam.d/common-password"
    regexp: "pam_pwquality.so"
    line: "password requisite pam_pwquality.so retry=3 minlen=12 lcredit=-1 ucredit=-1 dcredit=-1 ocredit=-1 enforce_for_root"
    state: present
```

**Descripción de las tareas:**

- **Instalar `libpam-pwquality`**: Utiliza el módulo `apt` para instalar el paquete que permite configurar políticas de contraseñas complejas.
- **Configurar `pam_pwquality`**: Utiliza el módulo `lineinfile` para modificar el archivo de configuración y establecer políticas de contraseña más estrictas.

#### **7. Crear la tarea `user_and_group.yml`**

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
    password: "{{ 'TuContraseñaSegura' | password_hash('sha512') }}"

- name: Asignar 'bender' al grupo 'desarrolladores'
  user:
    name: bender
    groups: desarrolladores
    append: yes

- name: Crear un directorio llamado 'ingenieria'
  file:
    path: /opt/ingenieria
    state: directory
    mode: '0750'
    group: desarrolladores

- name: Crear un archivo en el directorio de 'ingenieria'
  file:
    path: /opt/ingenieria/privado.txt
    state: touch
    mode: '0770'
    group: desarrolladores
```

**Nota:** Reemplaza `"TuContraseñaSegura"` por una contraseña que cumpla con los requisitos de complejidad establecidos.

**Descripción de las tareas:**

- **Crear el grupo 'desarrolladores'**: Asegura que el grupo exista en el sistema.
- **Crear el usuario 'bender'**: Crea un usuario con un shell de bash y una contraseña segura.
- **Asignar 'bender' al grupo 'desarrolladores'**: Añade el usuario al grupo.
- **Crear el directorio '/opt/ingenieria'**: Crea un directorio con permisos restringidos al grupo.
- **Crear el archivo 'privado.txt'**: Crea un archivo dentro del directorio con permisos específicos.

#### **8. Levantar y aprovisionar la máquina virtual**

Ejecuta el siguiente comando para crear y configurar la VM:

```bash
$ vagrant up
```

Este comando:

- Creará la VM según el `Vagrantfile`.
- Ejecutará el playbook de Ansible, aplicando las tareas definidas.

#### **9. Verificar la configuración**

Una vez finalizado el aprovisionamiento:

- **Conéctate a la VM**:

  ```bash
  $ vagrant ssh
  ```

- **Verifica que el usuario 'bender' exista**:

  ```bash
  $ getent passwd bender
  ```

  Deberías ver una salida similar a:

  ```
  bender:x:1001:1001::/home/bender:/bin/bash
  ```

- **Verifica que el grupo 'desarrolladores' exista y que 'bender' sea miembro**:

  ```bash
  $ getent group desarrolladores
  ```

  Deberías ver:

  ```
  desarrolladores:x:1002:bender
  ```

- **Prueba los permisos del directorio y archivo**:

  - Como usuario `vagrant`, intenta acceder al directorio:

    ```bash
    $ ls -la /opt/ingenieria
    ```

    Deberías recibir un mensaje de "Permiso denegado".

  - **Cambiar al usuario 'bender'**:

    ```bash
    $ sudo su - bender
    ```

  - Como `bender`, lista el contenido del directorio:

    ```bash
    $ ls -la /opt/ingenieria
    ```

    Ahora deberías ver el contenido sin problemas.

  - **Salir de la sesión de 'bender'**:

    ```bash
    $ exit
    ```

- **Probar la política de contraseñas**:

  - Intenta cambiar la contraseña de `bender` a una contraseña sencilla:

    ```bash
    $ sudo su - bender
    $ passwd
    ```

    Introduce una contraseña que no cumpla con los requisitos y verifica que el sistema no la acepta.

#### **10. Opcional: Añadir Ansible Vault para proteger contraseñas**

Para mejorar la seguridad y evitar almacenar contraseñas en texto plano:

- **Crear un archivo de variables cifradas**:

  ```bash
  $ ansible-vault create vars/secret.yml
  ```

- **Añadir la variable de contraseña** en el archivo `secret.yml`:

  ```yaml
  ---
  bender_password: "TuContraseñaSegura"
  ```

- **Modificar la tarea de creación de usuario** en `user_and_group.yml`:

  ```yaml
  password: "{{ bender_password | password_hash('sha512') }}"
  ```

- **Modificar el `site.yml` para incluir las variables**:

  ```yaml
  vars_files:
    - vars/secret.yml
  ```

- **Ejecutar Vagrant con la contraseña de Vault**:

  ```bash
  $ vagrant provision --extra-vars="@vars/secret.yml" --ask-vault-pass
  ```

#### **11. Destruir la máquina virtual (opcional)**

Si deseas liberar recursos:

```bash
$ vagrant destroy
```
**Nota**: Utiliza  este comando para generar el hash SHA512 que se usa en la tarea "crear usuario".

```bash
sudo apt update
sudo apt install pwgen whois
pass=`pwgen --secure --capitalize --numerals --symbols 12 1`
echo $pass | mkpasswd --stdin --method=sha-512; echo $pass
```
