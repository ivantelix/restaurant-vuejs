.PHONY: migrations superuser

# Obtener todas las apps dinámicamente del directorio apps
APPS := $(shell find backend/apps -maxdepth 1 -mindepth 1 -type d -exec basename {} \;)

# Comando para generar migraciones
migrations:
	@echo "Generando migraciones para todas las apps..."
	@for app in $(APPS); do \
		echo "Generando migraciones para $$app..."; \
		python backend/manage.py makemigrations $$app; \
	done
	@echo "¡Migraciones completadas!"

# Comando para aplicar las migraciones
migrate:
	@echo "Aplicando migraciones..."
	python backend/manage.py migrate

# Comando para listar las apps detectadas
list-apps:
	@echo "Apps detectadas:"
	@for app in $(APPS); do \
		echo "- $$app"; \
	done

# Comando para crear un superusuario
superuser:
	@echo "Creando superusuario..."
	python backend/manage.py createsuperuser

# Comando para crear un superusuario no interactivo (requiere variables de entorno)
superuser-auto:
	@echo "Creando superusuario automáticamente..."
	@if [ -z "$$DJANGO_SUPERUSER_USERNAME" ] || [ -z "$$DJANGO_SUPERUSER_EMAIL" ] || [ -z "$$DJANGO_SUPERUSER_PASSWORD" ]; then \
		echo "Error: Necesitas definir DJANGO_SUPERUSER_USERNAME, DJANGO_SUPERUSER_EMAIL y DJANGO_SUPERUSER_PASSWORD"; \
		exit 1; \
	fi
	python backend/manage.py createsuperuser --noinput 