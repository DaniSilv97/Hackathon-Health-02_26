.PHONY: help build up down logs shell-backend shell-frontend db-shell clean

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-20s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

build: ## Build all containers
	docker-compose build

up: ## Start all containers
	docker-compose up -d

up-logs: ## Start all containers with logs
	docker-compose up

down: ## Stop all containers
	docker-compose down

logs: ## View logs from all containers
	docker-compose logs -f

logs-backend: ## View backend logs
	docker-compose logs -f backend

logs-frontend: ## View frontend logs
	docker-compose logs -f frontend

shell-backend: ## Open shell in backend container
	docker-compose exec backend sh

shell-frontend: ## Open shell in frontend container
	docker-compose exec frontend sh

db-shell: ## Open MySQL shell
	docker-compose exec database mysql -u health_user -phealth_password health_db

clean: ## Remove all containers, volumes and images
	docker-compose down -v --rmi all

restart: ## Restart all containers
	docker-compose restart

rebuild: ## Rebuild and restart all containers
	docker-compose down
	docker-compose build --no-cache
	docker-compose up -d

ollama-pull: ## Pull llama2 model for Ollama
	docker-compose exec ollama ollama pull llama2
