DC := docker-compose
D := docker

psql:
	$(DC) exec db psql -d odoo_db -U odoo

init:
	$(DC) run --rm web odoo -i base

debug:
	$(DC) run --rm --service-ports web

up:
	$(DC) up $(service)

up-detach:
	$(DC) up -d $(service)

down:
	$(DC) down $(service)
