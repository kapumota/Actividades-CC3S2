### **Actividad: Configuración y aprovisionamiento de una máquina virtual Ubuntu con Vagrant y Ansible**

**Objetivo:** Crear y configurar una máquina virtual Ubuntu utilizando Vagrant y Ansible, automatizando el proceso de instalación y configuración de software en la VM.

### **Requisitos previos**

- **Vagrant** instalado en tu sistema. Puedes descargarlo desde [aquí](https://www.vagrantup.com/downloads).
- **VirtualBox** instalado. Descárgalo desde [aquí](https://www.virtualbox.org/wiki/Downloads).
- **Ansible** instalado en tu máquina host. Instrucciones de instalación [aquí](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html).
- Conocimientos básicos de línea de comandos y edición de archivos de texto.

### **Pasos de la actividad**

### **1. Crear un directorio de trabajo**

Crea un nuevo directorio para tu proyecto y navega a él en la terminal:

```bash
$ mkdir proyecto_iac
$ cd proyecto_iac
```

#### **2. Inicializar un Vagrantfile**

Ejecuta el siguiente comando para inicializar un `Vagrantfile` en el directorio actual:

```bash
$ vagrant init ubuntu/focal64
```

Este comando crea un archivo `Vagrantfile` con la configuración básica para una VM de Ubuntu 20.04.

#### **3. Modificar el Vagrantfile**

Edita el `Vagrantfile` para agregar configuraciones adicionales. Abre el archivo en tu editor de texto preferido y realiza los siguientes cambios:

- Configura la **red privada** para que la VM obtenga una IP mediante DHCP:

  ```ruby
  config.vm.network "private_network", type: "dhcp"
  ```

- Configura el **proveedor** VirtualBox para asignar más memoria a la VM y cambiar el nombre:

  ```ruby
  config.vm.provider "virtualbox" do |vb|
    vb.memory = "1024"
    vb.name = "vm_iac"
  end
  ```

- Configura Vagrant para utilizar **Ansible** como aprovisionador:

  ```ruby
  config.vm.provision "ansible" do |ansible|
    ansible.playbook = "playbook.yml"
  end
  ```

#### **4. Crear un playbook de Ansible**

Crea un archivo llamado `playbook.yml` en el mismo directorio y agrega el siguiente contenido:

```yaml
---
- name: Configurar VM
  hosts: all
  become: yes
  become_method: sudo
  remote_user: vagrant
  tasks:
    - name: Actualizar e instalar paquetes
      apt:
        update_cache: yes
        name:
          - git
          - curl
        state: present

    - name: Crear un usuario y grupo
      user:
        name: "usuario_dev"
        groups: "sudo"
        append: yes
        shell: "/bin/bash"
        create_home: yes
```

**Descripción de las tareas:**

- **Actualizar la caché de paquetes e instalar `git` y `curl`:**
  Utiliza el módulo `apt` para actualizar los repositorios e instalar los paquetes necesarios.

- **Crear un nuevo usuario llamado `usuario_dev` y agregarlo al grupo `sudo`:**
  Utiliza el módulo `user` para crear un usuario con privilegios administrativos.

#### **5. Levantar la máquina virtual y aprovisionarla**

Ejecuta el siguiente comando para crear y configurar la VM:

```bash
$ vagrant up
```

Este comando:

- Descargará la caja `ubuntu/focal64` si no la tienes ya.
- Creará y configurará la VM según el `Vagrantfile`.
- Ejecutará el playbook de Ansible para aprovisionar la VM.

#### **6. Verificar la configuración**

Una vez que el comando anterior haya finalizado:

- Conéctate a la VM mediante SSH:

  ```bash
  $ vagrant ssh
  ```

- **Dentro de la VM**, verifica que los paquetes se hayan instalado:

  ```bash
  $ git --version
  $ curl --version
  ```

- Verifica que el usuario `usuario_dev` exista:

  ```bash
  $ cat /etc/passwd | grep usuario_dev
  ```

- Sal de la VM:

  ```bash
  $ exit
  ```

#### **7. Opcional: modificar y reprovisionar**

- **Añade más tareas** al `playbook.yml`, como instalar más paquetes o configurar servicios adicionales.

- Para aplicar los cambios, puedes reprovisionar la VM sin recrearla:

  ```bash
  $ vagrant provision
  ```

#### **8. Destruir la máquina virtual (opcional)**

Una vez que hayas terminado, puedes destruir la VM para liberar recursos:

```bash
$ vagrant destroy
```

¡Felicidades por completar la actividad!
