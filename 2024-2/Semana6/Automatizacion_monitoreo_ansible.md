### **Actividad: Automatización de tareas de monitoreo y solución de problemas con Ansible**

**Objetivo:** Implementar y automatizar tareas de monitoreo y solución de problemas en una máquina virtual Linux utilizando Ansible y Vagrant. Aprenderás a detectar y resolver problemas comunes de rendimiento y disponibilidad en sistemas Linux mediante la ejecución de comandos y scripts automatizados.

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
$ mkdir proyecto_monitoreo
$ cd proyecto_monitoreo
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
  Vagrant.configure("2") do |config|
    config.vm.box = "ubuntu/focal64"

    config.vm.network "private_network", type: "dhcp"

    config.vm.provider "virtualbox" do |vb|
      vb.memory = "1024"
      vb.name = "vm_monitoreo"
    end

    config.vm.provision "ansible" do |ansible|
      ansible.playbook = "playbook.yml"
    end
  end
  ```

#### **4. Crear el playbook de Ansible `playbook.yml`**

Crea un archivo llamado `playbook.yml` y agrega el siguiente contenido:

```yaml
---
- name: Aprovisionar y monitorear VM
  hosts: all
  become: yes
  become_method: sudo
  remote_user: vagrant
  tasks:
    - name: Instalar herramientas de monitoreo y solución de problemas
      apt:
        name:
          - htop
          - iotop
          - sysstat
          - lsof
          - tcpdump
          - strace
          - net-tools
        update_cache: yes
        state: present

    - name: Copiar scripts de monitoreo
      copy:
        src: scripts/
        dest: /home/vagrant/scripts/
        mode: '0755'
        owner: vagrant
        group: vagrant

    - name: Programar tareas de monitoreo
      cron:
        name: "Ejecutar monitoreo de recursos"
        user: vagrant
        minute: "*/5"
        job: "/home/vagrant/scripts/monitoreo.sh >> /home/vagrant/monitoreo.log 2>&1"

    - name: Configurar alerta por uso de disco
      copy:
        src: scripts/alerta_espacio_disco.sh
        dest: /usr/local/bin/alerta_espacio_disco.sh
        mode: '0755'
        owner: root
        group: root

    - name: Configurar cron para alerta de espacio en disco
      cron:
        name: "Alerta de espacio en disco"
        user: root
        hour: "*/1"
        job: "/usr/local/bin/alerta_espacio_disco.sh"
```

#### **5. Crear el directorio de scripts**

Crea un directorio llamado `scripts` donde almacenaremos nuestros scripts de monitoreo:

```bash
$ mkdir scripts
```

#### **6. Crear el script `monitoreo.sh`**

Dentro del directorio `scripts`, crea el archivo `monitoreo.sh` con el siguiente contenido:

```bash
#!/bin/bash

echo "Fecha y hora: $(date)"
echo "----------------------------------------"

echo "Tiempo de actividad del sistema:"
uptime
echo "----------------------------------------"

echo "Uso de CPU y procesos:"
top -b -n1 | head -15
echo "----------------------------------------"

echo "Uso de memoria:"
free -hm
echo "----------------------------------------"

echo "Estadísticas de E/S:"
vmstat 1 5
echo "----------------------------------------"

echo "Uso de disco:"
df -h
echo "----------------------------------------"

echo "Procesos con mayor consumo de memoria:"
ps -eo pid,ppid,cmd,%mem,%cpu --sort=-%mem | head
echo "----------------------------------------"

echo "Estadísticas de red:"
ss -tuna
echo "----------------------------------------"

echo "Fin del reporte"
```

#### **7. Crear el script `alerta_espacio_disco.sh`**

En el directorio `scripts`, crea el archivo `alerta_espacio_disco.sh` con el siguiente contenido:

```bash
#!/bin/bash

THRESHOLD=80

PARTITIONS=$(df -h | grep '^/dev/' | awk '{print $1}')

for PART in $PARTITIONS; do
  USAGE=$(df -h | grep $PART | awk '{print $5}' | sed 's/%//g')
  if [ $USAGE -ge $THRESHOLD ]; then
    echo "Alerta: La partición $PART está al $USAGE% de uso."
    # Aquí podrías agregar envío de correo o notificación
  fi
done
```

#### **8. Volver a copiar los scripts al directorio de Ansible**

Como has creado los scripts en tu máquina host, asegúrate de que estén dentro del directorio `scripts/` que Ansible copiará a la VM.

#### **9. Levantar y aprovisionar la máquina virtual**

Ejecuta el siguiente comando para crear y configurar la VM:

```bash
$ vagrant up
```

Este comando:

- Creará la VM según el `Vagrantfile`.
- Ejecutará el playbook de Ansible, aplicando las tareas definidas.

#### **10. Verificar la configuración**

#### **10.1. Conectar a la VM**

Conéctate a la VM:

```bash
$ vagrant ssh
```

#### **10.2. Verificar los scripts y cron jobs**

Comprueba que los scripts están en el directorio correcto:

```bash
vagrant@vm_monitoreo:~$ ls -l ~/scripts/
```

Verifica que los cron jobs están configurados:

```bash
vagrant@vm_monitoreo:~$ crontab -l
```

Deberías ver la tarea programada para ejecutar `monitoreo.sh` cada 5 minutos.

#### **10.3. Verificar el archivo de log de monitoreo**

Después de unos minutos, verifica el archivo `monitoreo.log`:

```bash
vagrant@vm_monitoreo:~$ cat ~/monitoreo.log
```

Deberías ver los reportes generados por el script `monitoreo.sh`.

#### **11. Probar situaciones de solución de problemas**

Ahora, generarás situaciones que puedan desencadenar problemas y utilizarás los comandos y scripts para identificarlos.

#### **11.1. Simular alto uso de CPU**

Ejecuta en la VM:

```bash
vagrant@vm_monitoreo:~$ yes > /dev/null &
```

Este comando generará un proceso que consume CPU.

- **Identificar el proceso con `top` o `htop`**:

  ```bash
  vagrant@vm_monitoreo:~$ top
  ```

- **Detener el proceso**:

  ```bash
  vagrant@vm_monitoreo:~$ pkill yes
  ```

#### **11.2. Simular alto uso de memoria**

Ejecuta en la VM:

```bash
vagrant@vm_monitoreo:~$ stress --vm 1 --vm-bytes 900M --vm-hang 5 &
```

- **Verificar uso de memoria con `free` y `vmstat`**:

  ```bash
  vagrant@vm_monitoreo:~$ free -hm
  vagrant@vm_monitoreo:~$ vmstat 1 5
  ```

- **Detener el proceso**:

  ```bash
  vagrant@vm_monitoreo:~$ pkill stress
  ```

#### **11.3. Simular llenado de disco**

Ejecuta en la VM:

```bash
vagrant@vm_monitoreo:~$ dd if=/dev/zero of=~/archivo_grande bs=1M count=1024
```

Esto creará un archivo de 1GB.

- **Verificar uso de disco con `df`**:

  ```bash
  vagrant@vm_monitoreo:~$ df -h
  ```

- **Esperar a que el script `alerta_espacio_disco.sh` se ejecute** y ver si muestra alguna alerta.

- **Eliminar el archivo**:

  ```bash
  vagrant@vm_monitoreo:~$ rm ~/archivo_grande
  ```

#### **11.4. Simular problemas de red**

- **Bloquear una dirección IP usando `iptables`**:

  ```bash
  vagrant@vm_monitoreo:~$ sudo iptables -A INPUT -s 8.8.8.8 -j DROP
  ```

- **Intentar hacer ping a la dirección bloqueada**:

  ```bash
  vagrant@vm_monitoreo:~$ ping 8.8.8.8
  ```

- **Usar `ss` y `tcpdump` para verificar conexiones de red**:

  ```bash
  vagrant@vm_monitoreo:~$ sudo ss -tuna
  vagrant@vm_monitoreo:~$ sudo tcpdump -ni any icmp
  ```

- **Remover la regla de `iptables`**:

  ```bash
  vagrant@vm_monitoreo:~$ sudo iptables -D INPUT -s 8.8.8.8 -j DROP
  ```

#### **12. Analizar registros y procesos**

Utiliza los comandos mencionados en el texto para analizar y solucionar problemas:

- **`journalctl`**: Revisa los registros del sistema.

  ```bash
  vagrant@vm_monitoreo:~$ sudo journalctl -r
  ```

- **`grep` y `awk`**: Busca patrones en los registros.

  ```bash
  vagrant@vm_monitoreo:~$ sudo grep "error" /var/log/syslog
  ```

- **`lsof`**: Lista archivos abiertos.

  ```bash
  vagrant@vm_monitoreo:~$ sudo lsof -i TCP:22
  ```

- **`strace`**: Traza llamadas del sistema.

  ```bash
  vagrant@vm_monitoreo:~$ sudo strace -p $(pidof sshd)
  ```

#### **13. Documentar tus hallazgos**

Mantén un registro de los comandos utilizados y los resultados obtenidos. Esto te ayudará a entender mejor el comportamiento del sistema y a desarrollar buenas prácticas de documentación.

#### **14. Destruir la máquina virtual (opcional)**

Si deseas liberar recursos:

```bash
$ vagrant destroy
```
