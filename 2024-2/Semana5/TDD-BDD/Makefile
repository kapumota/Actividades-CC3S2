# Construye un entorno para Behave y Selenium

.PHONY: all help bdd app

help: ## Muestra esta ayuda
        @awk 'BEGIN {FS = ":.*##"; printf "\nUso:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z_0-9-\.]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

all: help

bdd: ## Instalar software necesario para BDD
        $(info Instalando software pre-requisito para BDD...)
        sudo apt-get update
        sudo apt-get install -y sqlite3 chromium-driver python3-selenium

app: ## Ejecuta la aplicación BDD
        $(info Ejecutando la aplicación BDD...)
        docker run -d --name bdd \
                -p 5000:5000 \
                -e DATABASE_URI=sqlite:///test.db \
                rofrano/lab-flask-bdd:1.0

