### **Actividad: Seguridad de acceso SSH con Ansible y Vagrant**

**Objetivo:** Implementar y automatizar mejoras de seguridad en el acceso SSH a una máquina virtual Ubuntu utilizando Ansible y Vagrant. Configurarás la autenticación de clave pública y habilitarás la autenticación de dos factores (2FA) para un usuario específico.

### **Requisitos previos**

- **Vagrant** instalado en tu sistema.
- **VirtualBox** instalado.
- **Ansible** instalado en tu máquina host.
- Conocimientos básicos de línea de comandos y edición de archivos de texto.
- Familiaridad con YAML y los conceptos básicos de Ansible.
- **Nota:** Las instrucciones están diseñadas para sistemas Linux o macOS.

### **Pasos de la actividad**

#### **1. Crear el entorno de trabajo**

Crea un nuevo directorio para tu proyecto y navega a él:

```bash
$ mkdir proyecto_ssh_seguridad
$ cd proyecto_ssh_seguridad
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
    vb.name = "vm_ssh_seguridad"
  end
  ```

- **Configurar el aprovisionador Ansible**:

  ```ruby
  config.vm.provision "ansible" do |ansible|
    ansible.playbook = "site.yml"
  end
  ```

#### **4. Generar un par de claves SSH**

En tu máquina host, genera un nuevo par de claves SSH específico para este proyecto:

```bash
$ ssh-keygen -t rsa -f ~/.ssh/dftd -C "dftd"
```

- **Explicación**:
  - `-t rsa`: Especifica el tipo de clave RSA.
  - `-f ~/.ssh/dftd`: Define el nombre y ubicación del archivo de clave.
  - `-C "dftd"`: Agrega un comentario para identificar la clave.

Cuando se te solicite, ingresa una **frase de contraseña segura** para proteger tu clave privada.

#### **5. Crear el playbook de Ansible `site.yml`**

Crea un archivo llamado `site.yml` y agrega el siguiente contenido:

```yaml
---
- name: Aprovisionar VM con seguridad SSH
  hosts: all
  become: yes
  become_method: sudo
  remote_user: vagrant
  vars:
    ssh_public_key_path: "{{ lookup('env','HOME') }}/.ssh/dftd.pub"
  tasks:
    - import_tasks: tasks/authorized_keys.yml
    - import_tasks: tasks/two_factor.yml
  handlers:
    - import_tasks: handlers/restart_ssh.yml
```

#### **6. Crear el directorio de tareas**

Crea un directorio llamado `tasks` donde almacenaremos nuestras tareas:

```bash
$ mkdir tasks
```

#### **7. Crear la tarea `authorized_keys.yml`**

Dentro del directorio `tasks`, crea el archivo `authorized_keys.yml` con el siguiente contenido:

```yaml
---
- name: Establecer el archivo de clave autorizada para el usuario 'bender'
  authorized_key:
    user: bender
    state: present
    key: "{{ lookup('file', ssh_public_key_path) }}"
```

#### **8. Crear la tarea `two_factor.yml`**

En el directorio `tasks`, crea el archivo `two_factor.yml` con el siguiente contenido:

```yaml
---
- name: Instalar libpam-google-authenticator
  apt:
    name: libpam-google-authenticator
    update_cache: yes
    state: present

- name: Copiar configuración preconfigurada de Google Authenticator
  copy:
    src: files/google_authenticator
    dest: /home/bender/.google_authenticator
    mode: '0600'
    owner: bender

- name: Deshabilitar autenticación de contraseña para SSH en PAM
  lineinfile:
    path: "/etc/pam.d/sshd"
    regexp: '^@include common-auth'
    state: absent

- name: Configurar PAM para usar Google Authenticator para SSH
  lineinfile:
    path: "/etc/pam.d/sshd"
    line: "auth required pam_google_authenticator.so nullok"
    insertafter: EOF

- name: Establecer ChallengeResponseAuthentication a yes
  lineinfile:
    path: "/etc/ssh/sshd_config"
    regexp: "^ChallengeResponseAuthentication (yes|no)"
    line: "ChallengeResponseAuthentication yes"
    state: present

- name: Establecer métodos de autenticación para usuarios
  blockinfile:
    path: "/etc/ssh/sshd_config"
    block: |
      Match User vagrant
        AuthenticationMethods publickey

      Match User bender
        AuthenticationMethods publickey,keyboard-interactive
  notify: Reiniciar servidor SSH
```

**Nota:** Crearás el archivo `google_authenticator` en el siguiente paso.

#### **9. Crear el directorio de archivos y el archivo `google_authenticator`**

Crea un directorio llamado `files` dentro de `tasks` y luego crea el archivo `google_authenticator` con contenido preconfigurado:

```bash
$ mkdir tasks/files
$ touch tasks/files/google_authenticator
```

Abre `tasks/files/google_authenticator` y agrega el siguiente contenido:

```
YOUR_BASE32_SECRET_KEY
" WINDOW_SIZE 17
" TOTP_AUTH
12345678
87654321
...
```

**Nota:** Reemplaza `YOUR_BASE32_SECRET_KEY` por una clave secreta generada para este propósito. Puedes generar una clave usando `google-authenticator` o herramientas en línea. Los números como `12345678` y `87654321` son tokens de emergencia; puedes generar 10 números aleatorios de 8 dígitos.

**Advertencia:** No utilices información sensible real en este archivo, ya que es solo para fines educativos.

#### **10. Crear el controlador `restart_ssh.yml`**

Crea un directorio llamado `handlers` y dentro de él el archivo `restart_ssh.yml`:

```bash
$ mkdir handlers
$ touch handlers/restart_ssh.yml
```

Agrega el siguiente contenido a `handlers/restart_ssh.yml`:

```yaml
---
- name: Reiniciar servidor SSH
  service:
    name: sshd
    state: restarted
```

#### **11. Levantar y aprovisionar la máquina virtual**

Ejecuta el siguiente comando para crear y configurar la VM:

```bash
$ vagrant up
```

Este comando:

- Creará la VM según el `Vagrantfile`.
- Ejecutará el playbook de Ansible, aplicando las tareas definidas.

#### **12. Verificar la configuración**

#### **12.1. Probar acceso SSH con autenticación de clave pública y 2FA**

En tu máquina host, intenta conectarte a la VM como el usuario `bender`:

```bash
$ ssh -i ~/.ssh/dftd -p 2222 bender@localhost
```

- **Notas**:
  - `-i ~/.ssh/dftd`: Especifica la clave privada para autenticación.
  - `-p 2222`: Especifica el puerto que Vagrant usa para SSH.

Se te solicitará:

1. **Frase de contraseña** de tu clave privada (la que ingresaste al generarla).
2. **Código de verificación** (2FA). Usa uno de los tokens de emergencia que agregaste en el archivo `google_authenticator`.

Si todo está configurado correctamente, deberías iniciar sesión como `bender`.

#### **12.2. Verificar que usuarios sin clave pública no puedan acceder**

Intenta conectarte sin especificar la clave privada:

```bash
$ ssh -p 2222 bender@localhost
```

Deberías recibir un mensaje de "Permission denied" o similar, ya que no se permite la autenticación por contraseña ni sin clave.

#### **13. Opcional: Generar tokens TOTP con `oathtool`**

Si deseas generar tokens TOTP basados en tiempo:

- **Instala `oathtool`** en tu máquina host:

  ```bash
  $ sudo apt-get install oathtool    # Para sistemas basados en Debian/Ubuntu
  ```

- **Genera un token usando la clave secreta**:

  ```bash
  $ oathtool --totp --base32 "YOUR_BASE32_SECRET_KEY"
  ```

  Reemplaza `"YOUR_BASE32_SECRET_KEY"` por la clave secreta que utilizaste en el archivo `google_authenticator`.

#### **14. Destruir la máquina virtual (opcional)**

Si deseas liberar recursos:

```bash
$ vagrant destroy
```
**Nota:** Crea el archivo de Google Authenticator utilizando el siguiente comando.

```bash
google-authenticator -f -t -d -r 3 -R 30 -w 17 -e 10
```


