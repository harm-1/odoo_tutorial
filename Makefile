DC := docker-compose
D := docker

psql:
	$(DC) exec db psql -d odoo_db -U odoo

mod_up:
	$(DC) run --rm web odoo -u estate 

init:
	$(DC) run --rm web odoo -i base

up-detach:
	$(DC) up -d $(service)

up:
	$(DC) up $(service)
