FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# Actualizar los paquetes e instalar herramientas esenciales y Python 3.10
RUN apt-get update && \
    apt-get install -y sudo vim git zip tree curl wget python3.10 python3.10-dev python3-pip && \
    update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.10 1 && \
    apt-get autoremove -y && \
    apt-get clean -y

# Crear un usuario para desarrollo
ARG USERNAME=kapumota
ARG USER_UID=1000
ARG USER_GID=$USER_UID

# Crear el usuario con privilegios sudo sin contraseña
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME -s /bin/bash \
    && usermod -aG sudo $USERNAME \
    && echo "$USERNAME ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

# Configurar el entorno de desarrollo de Python
WORKDIR /project
RUN python3 -m pip install --upgrade pip && \
    pip3 install --upgrade wheel

# Habilitar colores en la terminal
ENV TERM=xterm-256color

EXPOSE 5000

# Cambiar al usuario normal para desarrollo
USER $USERNAME

