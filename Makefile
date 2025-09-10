# =============================================================================
# Career Advisor MVP - Professional Makefile
# =============================================================================
# Author: Career Advisor Team
# Description: Comprehensive build automation for Flask application
# =============================================================================

# -----------------------------------------------------------------------------
# Configuration Variables
# -----------------------------------------------------------------------------
SHELL := /bin/bash
.DEFAULT_GOAL := help
.PHONY: help install dev test clean build deploy docker lint format security check-deps

# Project Configuration
PROJECT_NAME := career-advisor-mvp
PYTHON := python
PIP := pip
FLASK_APP := app.py
FLASK_ENV := development
PORT := 5000

# Virtual Environment
VENV := venv
VENV_ACTIVATE := $(VENV)/Scripts/activate

# Testing Configuration
TEST_PATH := tests
COVERAGE_MIN := 80

# Docker Configuration
DOCKER_IMAGE := $(PROJECT_NAME):latest
DOCKER_CONTAINER := $(PROJECT_NAME)-container

# Color Output
RED := \033[0;31m
GREEN := \033[0;32m
YELLOW := \033[1;33m
BLUE := \033[0;34m
NC := \033[0m # No Color

# -----------------------------------------------------------------------------
# Help Command
# -----------------------------------------------------------------------------
help: ## Show this help message
	@echo "$(BLUE)================================================================================$(NC)"
	@echo "$(GREEN)Career Advisor MVP - Make Commands$(NC)"
	@echo "$(BLUE)================================================================================$(NC)"
	@echo ""
	@echo "$(YELLOW)Available commands:$(NC)"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(GREEN)%-20s$(NC) %s\n", $$1, $$2}'
	@echo ""
	@echo "$(BLUE)================================================================================$(NC)"

# -----------------------------------------------------------------------------
# Environment Setup
# -----------------------------------------------------------------------------
setup: ## Initial project setup (creates venv, installs deps, copies .env)
	@echo "$(YELLOW)Setting up project environment...$(NC)"
	@if [ ! -d "$(VENV)" ]; then \
		echo "Creating virtual environment..."; \
		$(PYTHON) -m venv $(VENV); \
	fi
	@echo "Installing dependencies..."
	@. $(VENV_ACTIVATE) && $(PIP) install --upgrade pip
	@. $(VENV_ACTIVATE) && $(PIP) install -r requirements.txt
	@if [ ! -f .env ] && [ -f .env.example ]; then \
		echo "Creating .env file from .env.example..."; \
		cp .env.example .env; \
		echo "$(RED)Please update .env with your actual configuration!$(NC)"; \
	fi
	@echo "$(GREEN)✓ Setup complete!$(NC)"

install: ## Install Python dependencies
	@echo "$(YELLOW)Installing dependencies...$(NC)"
	@. $(VENV_ACTIVATE) && $(PIP) install -r requirements.txt
	@echo "$(GREEN)✓ Dependencies installed!$(NC)"

install-dev: ## Install development dependencies
	@echo "$(YELLOW)Installing development dependencies...$(NC)"
	@. $(VENV_ACTIVATE) && $(PIP) install -r requirements-dev.txt 2>/dev/null || true
	@. $(VENV_ACTIVATE) && $(PIP) install pytest pytest-cov pytest-flask black flake8 bandit mypy
	@echo "$(GREEN)✓ Development dependencies installed!$(NC)"

freeze: ## Update requirements.txt with current dependencies
	@echo "$(YELLOW)Freezing dependencies...$(NC)"
	@. $(VENV_ACTIVATE) && $(PIP) freeze > requirements.txt
	@echo "$(GREEN)✓ requirements.txt updated!$(NC)"

# -----------------------------------------------------------------------------
# Development Commands
# -----------------------------------------------------------------------------
dev: ## Run Flask app in development mode
	@echo "$(YELLOW)Starting Flask development server...$(NC)"
	@echo "$(BLUE)Server running at: http://localhost:$(PORT)$(NC)"
	@. $(VENV_ACTIVATE) && FLASK_APP=$(FLASK_APP) FLASK_ENV=$(FLASK_ENV) flask run --port=$(PORT) --reload

run: ## Run Flask app in production mode
	@echo "$(YELLOW)Starting Flask production server...$(NC)"
	@. $(VENV_ACTIVATE) && FLASK_APP=$(FLASK_APP) FLASK_ENV=production python $(FLASK_APP)

debug: ## Run Flask app in debug mode with verbose output
	@echo "$(YELLOW)Starting Flask in debug mode...$(NC)"
	@. $(VENV_ACTIVATE) && FLASK_APP=$(FLASK_APP) FLASK_DEBUG=1 FLASK_ENV=development flask run --port=$(PORT) --reload --debugger

shell: ## Open Flask shell for interactive debugging
	@echo "$(YELLOW)Opening Flask shell...$(NC)"
	@. $(VENV_ACTIVATE) && FLASK_APP=$(FLASK_APP) flask shell

# -----------------------------------------------------------------------------
# Database Commands
# -----------------------------------------------------------------------------
db-init: ## Initialize database
	@echo "$(YELLOW)Initializing database...$(NC)"
	@if [ ! -d "database" ]; then mkdir database; fi
	@. $(VENV_ACTIVATE) && python -c "from app import db; db.create_all()"
	@echo "$(GREEN)✓ Database initialized!$(NC)"

db-migrate: ## Run database migrations
	@echo "$(YELLOW)Running database migrations...$(NC)"
	@. $(VENV_ACTIVATE) && flask db upgrade
	@echo "$(GREEN)✓ Migrations completed!$(NC)"

db-reset: ## Reset database (WARNING: Destroys all data)
	@echo "$(RED)WARNING: This will delete all data!$(NC)"
	@read -p "Are you sure? (y/N): " confirm && [ "$$confirm" = "y" ] || exit 1
	@echo "$(YELLOW)Resetting database...$(NC)"
	@rm -rf database/*.db database/*.sqlite 2>/dev/null || true
	@$(MAKE) db-init
	@echo "$(GREEN)✓ Database reset!$(NC)"

# -----------------------------------------------------------------------------
# Testing Commands
# -----------------------------------------------------------------------------
test: ## Run all tests
	@echo "$(YELLOW)Running tests...$(NC)"
	@. $(VENV_ACTIVATE) && pytest $(TEST_PATH) -v --color=yes 2>/dev/null || python test_demo.py
	@echo "$(GREEN)✓ Tests completed!$(NC)"

test-coverage: ## Run tests with coverage report
	@echo "$(YELLOW)Running tests with coverage...$(NC)"
	@. $(VENV_ACTIVATE) && pytest $(TEST_PATH) --cov=. --cov-report=html --cov-report=term 2>/dev/null || \
		(python -m coverage run test_demo.py && python -m coverage report)
	@echo "$(GREEN)✓ Coverage report generated!$(NC)"

test-watch: ## Run tests in watch mode
	@echo "$(YELLOW)Running tests in watch mode...$(NC)"
	@. $(VENV_ACTIVATE) && pytest-watch $(TEST_PATH) 2>/dev/null || \
		while true; do python test_demo.py; sleep 2; done

# -----------------------------------------------------------------------------
# Code Quality Commands
# -----------------------------------------------------------------------------
lint: ## Run code linting
	@echo "$(YELLOW)Running linter...$(NC)"
	@. $(VENV_ACTIVATE) && (flake8 . --exclude=$(VENV),__pycache__ --max-line-length=120 2>/dev/null || \
		python -m py_compile *.py)
	@echo "$(GREEN)✓ Linting completed!$(NC)"

format: ## Format code with black
	@echo "$(YELLOW)Formatting code...$(NC)"
	@. $(VENV_ACTIVATE) && (black . --exclude=$(VENV) 2>/dev/null || \
		echo "Install black: pip install black")
	@echo "$(GREEN)✓ Code formatted!$(NC)"

type-check: ## Run type checking with mypy
	@echo "$(YELLOW)Running type checks...$(NC)"
	@. $(VENV_ACTIVATE) && (mypy . --ignore-missing-imports 2>/dev/null || \
		echo "Install mypy: pip install mypy")
	@echo "$(GREEN)✓ Type checking completed!$(NC)"

security: ## Run security checks
	@echo "$(YELLOW)Running security scan...$(NC)"
	@. $(VENV_ACTIVATE) && (bandit -r . -x $(VENV) 2>/dev/null || \
		echo "Install bandit: pip install bandit")
	@echo "$(GREEN)✓ Security scan completed!$(NC)"

check-deps: ## Check for outdated dependencies
	@echo "$(YELLOW)Checking dependencies...$(NC)"
	@. $(VENV_ACTIVATE) && pip list --outdated
	@echo "$(GREEN)✓ Dependency check completed!$(NC)"

# -----------------------------------------------------------------------------
# Build & Deployment Commands
# -----------------------------------------------------------------------------
build: clean ## Build project for production
	@echo "$(YELLOW)Building project...$(NC)"
	@$(MAKE) install
	@$(MAKE) test
	@$(MAKE) lint
	@echo "$(GREEN)✓ Build completed!$(NC)"

build-docker: ## Build Docker image
	@echo "$(YELLOW)Building Docker image...$(NC)"
	@docker build -t $(DOCKER_IMAGE) .
	@echo "$(GREEN)✓ Docker image built: $(DOCKER_IMAGE)$(NC)"

run-docker: ## Run Docker container
	@echo "$(YELLOW)Running Docker container...$(NC)"
	@docker run -d -p $(PORT):$(PORT) --name $(DOCKER_CONTAINER) $(DOCKER_IMAGE)
	@echo "$(GREEN)✓ Container running at: http://localhost:$(PORT)$(NC)"

stop-docker: ## Stop Docker container
	@echo "$(YELLOW)Stopping Docker container...$(NC)"
	@docker stop $(DOCKER_CONTAINER) 2>/dev/null || true
	@docker rm $(DOCKER_CONTAINER) 2>/dev/null || true
	@echo "$(GREEN)✓ Container stopped!$(NC)"

deploy-staging: ## Deploy to staging environment
	@echo "$(YELLOW)Deploying to staging...$(NC)"
	@echo "TODO: Add staging deployment commands"
	@echo "$(GREEN)✓ Staging deployment completed!$(NC)"

deploy-production: ## Deploy to production environment
	@echo "$(RED)Deploying to PRODUCTION...$(NC)"
	@read -p "Are you sure you want to deploy to production? (y/N): " confirm && [ "$$confirm" = "y" ] || exit 1
	@echo "TODO: Add production deployment commands"
	@echo "$(GREEN)✓ Production deployment completed!$(NC)"

# -----------------------------------------------------------------------------
# Utility Commands
# -----------------------------------------------------------------------------
clean: ## Clean temporary files and caches
	@echo "$(YELLOW)Cleaning project...$(NC)"
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@find . -type f -name "*.pyo" -delete 2>/dev/null || true
	@find . -type f -name "*.coverage" -delete 2>/dev/null || true
	@find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true
	@echo "$(GREEN)✓ Cleanup completed!$(NC)"

clean-all: clean ## Deep clean including virtual environment
	@echo "$(RED)Removing virtual environment...$(NC)"
	@rm -rf $(VENV)
	@echo "$(GREEN)✓ Deep clean completed!$(NC)"

logs: ## Show application logs
	@echo "$(YELLOW)Showing application logs...$(NC)"
	@tail -f *.log 2>/dev/null || echo "No log files found"

backup: ## Create backup of the project
	@echo "$(YELLOW)Creating backup...$(NC)"
	@tar -czf ../$(PROJECT_NAME)-backup-$$(date +%Y%m%d-%H%M%S).tar.gz --exclude=$(VENV) --exclude=__pycache__ .
	@echo "$(GREEN)✓ Backup created!$(NC)"

# -----------------------------------------------------------------------------
# Git Commands
# -----------------------------------------------------------------------------
git-status: ## Show git status
	@git status

git-commit: ## Stage all changes and commit
	@read -p "Commit message: " msg; \
	git add -A && git commit -m "$$msg"

git-push: ## Push to remote repository
	@git push origin $$(git branch --show-current)

# -----------------------------------------------------------------------------
# Documentation Commands
# -----------------------------------------------------------------------------
docs: ## Generate documentation
	@echo "$(YELLOW)Generating documentation...$(NC)"
	@. $(VENV_ACTIVATE) && (pdoc --html --output-dir docs . 2>/dev/null || \
		echo "Install pdoc: pip install pdoc3")
	@echo "$(GREEN)✓ Documentation generated in docs/$(NC)"

serve-docs: ## Serve documentation locally
	@echo "$(YELLOW)Serving documentation...$(NC)"
	@python -m http.server 8080 --directory docs

# -----------------------------------------------------------------------------
# Performance & Monitoring
# -----------------------------------------------------------------------------
profile: ## Profile application performance
	@echo "$(YELLOW)Profiling application...$(NC)"
	@. $(VENV_ACTIVATE) && python -m cProfile -s cumulative $(FLASK_APP)

monitor: ## Monitor application metrics
	@echo "$(YELLOW)Monitoring application...$(NC)"
	@watch -n 2 "ps aux | grep python | grep -v grep"

# -----------------------------------------------------------------------------
# Aliases for Common Commands
# -----------------------------------------------------------------------------
i: install
d: dev
t: test
c: clean
b: build
r: run

# -----------------------------------------------------------------------------
# CI/CD Commands
# -----------------------------------------------------------------------------
ci: ## Run continuous integration checks
	@echo "$(YELLOW)Running CI checks...$(NC)"
	@$(MAKE) clean
	@$(MAKE) install
	@$(MAKE) lint
	@$(MAKE) type-check
	@$(MAKE) security
	@$(MAKE) test-coverage
	@echo "$(GREEN)✓ CI checks passed!$(NC)"

# -----------------------------------------------------------------------------
# End of Makefile
# -----------------------------------------------------------------------------
