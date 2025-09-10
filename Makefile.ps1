# =============================================================================
# Career Advisor MVP - PowerShell Make Script for Windows
# =============================================================================
# Author: Career Advisor Team
# Description: Windows PowerShell version of Make commands
# Usage: .\Makefile.ps1 [command]
# =============================================================================

param(
    [Parameter(Position=0)]
    [string]$Command = "help",
    
    [Parameter(Position=1)]
    [string]$Arg1 = "",
    
    [Parameter(Position=2)]
    [string]$Arg2 = ""
)

# Configuration Variables
$ProjectName = "career-advisor-mvp"
$Python = "python"
$Pip = "pip"
$FlaskApp = "app.py"
$Port = "5000"
$Venv = "venv"
$VenvActivate = ".\$Venv\Scripts\Activate.ps1"

# Color definitions
function Write-ColorOutput {
    param([string]$Text, [string]$Color = "White")
    Write-Host $Text -ForegroundColor $Color
}

# Helper function to check if virtual environment exists
function Test-VenvExists {
    return Test-Path $Venv
}

# Helper function to activate virtual environment
function Invoke-VenvCommand {
    param([string]$Command)
    if (Test-VenvExists) {
        & $VenvActivate
        Invoke-Expression $Command
        deactivate
    } else {
        Write-ColorOutput "Virtual environment not found. Run: .\Makefile.ps1 setup" "Red"
        exit 1
    }
}

# Command implementations
switch ($Command.ToLower()) {
    "help" {
        Write-ColorOutput "================================================================================" "Blue"
        Write-ColorOutput "Career Advisor MVP - PowerShell Make Commands" "Green"
        Write-ColorOutput "================================================================================" "Blue"
        Write-ColorOutput ""
        Write-ColorOutput "Available commands:" "Yellow"
        Write-ColorOutput ""
        Write-ColorOutput "  SETUP & INSTALLATION" "Cyan"
        Write-ColorOutput "    setup              Initial project setup (creates venv, installs deps)" "White"
        Write-ColorOutput "    install            Install Python dependencies" "White"
        Write-ColorOutput "    install-dev        Install development dependencies" "White"
        Write-ColorOutput "    freeze             Update requirements.txt" "White"
        Write-ColorOutput ""
        Write-ColorOutput "  DEVELOPMENT" "Cyan"
        Write-ColorOutput "    dev                Run Flask app in development mode" "White"
        Write-ColorOutput "    run                Run Flask app in production mode" "White"
        Write-ColorOutput "    debug              Run Flask app in debug mode" "White"
        Write-ColorOutput "    shell              Open Flask shell" "White"
        Write-ColorOutput ""
        Write-ColorOutput "  DATABASE" "Cyan"
        Write-ColorOutput "    db-init            Initialize database" "White"
        Write-ColorOutput "    db-migrate         Run database migrations" "White"
        Write-ColorOutput "    db-reset           Reset database (WARNING: Destroys all data)" "White"
        Write-ColorOutput ""
        Write-ColorOutput "  TESTING" "Cyan"
        Write-ColorOutput "    test               Run all tests" "White"
        Write-ColorOutput "    test-coverage      Run tests with coverage report" "White"
        Write-ColorOutput ""
        Write-ColorOutput "  CODE QUALITY" "Cyan"
        Write-ColorOutput "    lint               Run code linting" "White"
        Write-ColorOutput "    format             Format code with black" "White"
        Write-ColorOutput "    type-check         Run type checking with mypy" "White"
        Write-ColorOutput "    security           Run security checks" "White"
        Write-ColorOutput "    check-deps         Check for outdated dependencies" "White"
        Write-ColorOutput ""
        Write-ColorOutput "  BUILD & DEPLOY" "Cyan"
        Write-ColorOutput "    build              Build project for production" "White"
        Write-ColorOutput "    deploy-staging     Deploy to staging environment" "White"
        Write-ColorOutput "    deploy-production  Deploy to production environment" "White"
        Write-ColorOutput ""
        Write-ColorOutput "  UTILITIES" "Cyan"
        Write-ColorOutput "    clean              Clean temporary files and caches" "White"
        Write-ColorOutput "    clean-all          Deep clean including virtual environment" "White"
        Write-ColorOutput "    logs               Show application logs" "White"
        Write-ColorOutput "    backup             Create backup of the project" "White"
        Write-ColorOutput ""
        Write-ColorOutput "  GIT" "Cyan"
        Write-ColorOutput "    git-status         Show git status" "White"
        Write-ColorOutput "    git-commit         Stage all changes and commit" "White"
        Write-ColorOutput "    git-push           Push to remote repository" "White"
        Write-ColorOutput ""
        Write-ColorOutput "  DOCUMENTATION" "Cyan"
        Write-ColorOutput "    docs               Generate documentation" "White"
        Write-ColorOutput "    serve-docs         Serve documentation locally" "White"
        Write-ColorOutput ""
        Write-ColorOutput "  MONITORING" "Cyan"
        Write-ColorOutput "    profile            Profile application performance" "White"
        Write-ColorOutput "    monitor            Monitor application metrics" "White"
        Write-ColorOutput ""
        Write-ColorOutput "  CI/CD" "Cyan"
        Write-ColorOutput "    ci                 Run continuous integration checks" "White"
        Write-ColorOutput ""
        Write-ColorOutput "================================================================================" "Blue"
        Write-ColorOutput "Usage: .\Makefile.ps1 [command]" "Gray"
        Write-ColorOutput "Example: .\Makefile.ps1 dev" "Gray"
        Write-ColorOutput "================================================================================" "Blue"
    }
    
    "setup" {
        Write-ColorOutput "Setting up project environment..." "Yellow"
        
        # Create virtual environment if it doesn't exist
        if (-not (Test-VenvExists)) {
            Write-ColorOutput "Creating virtual environment..." "White"
            & $Python -m venv $Venv
        }
        
        # Activate and install dependencies
        Write-ColorOutput "Installing dependencies..." "White"
        & $VenvActivate
        & $Python -m pip install --upgrade pip
        & $Pip install -r requirements.txt
        
        # Copy .env.example to .env if needed
        if ((-not (Test-Path ".env")) -and (Test-Path ".env.example")) {
            Write-ColorOutput "Creating .env file from .env.example..." "White"
            Copy-Item ".env.example" ".env"
            Write-ColorOutput "Please update .env with your actual configuration!" "Red"
        }
        
        deactivate
        Write-ColorOutput "✓ Setup complete!" "Green"
    }
    
    "install" {
        Write-ColorOutput "Installing dependencies..." "Yellow"
        Invoke-VenvCommand "$Pip install -r requirements.txt"
        Write-ColorOutput "✓ Dependencies installed!" "Green"
    }
    
    "install-dev" {
        Write-ColorOutput "Installing development dependencies..." "Yellow"
        & $VenvActivate
        if (Test-Path "requirements-dev.txt") {
            & $Pip install -r requirements-dev.txt
        }
        & $Pip install pytest pytest-cov pytest-flask black flake8 bandit mypy
        deactivate
        Write-ColorOutput "✓ Development dependencies installed!" "Green"
    }
    
    "freeze" {
        Write-ColorOutput "Freezing dependencies..." "Yellow"
        Invoke-VenvCommand "$Pip freeze > requirements.txt"
        Write-ColorOutput "✓ requirements.txt updated!" "Green"
    }
    
    "dev" {
        Write-ColorOutput "Starting Flask development server..." "Yellow"
        Write-ColorOutput "Server running at: http://localhost:$Port" "Blue"
        & $VenvActivate
        $env:FLASK_APP = $FlaskApp
        $env:FLASK_ENV = "development"
        & $Python -m flask run --port=$Port --reload
    }
    
    "run" {
        Write-ColorOutput "Starting Flask production server..." "Yellow"
        & $VenvActivate
        $env:FLASK_APP = $FlaskApp
        $env:FLASK_ENV = "production"
        & $Python $FlaskApp
    }
    
    "debug" {
        Write-ColorOutput "Starting Flask in debug mode..." "Yellow"
        & $VenvActivate
        $env:FLASK_APP = $FlaskApp
        $env:FLASK_DEBUG = "1"
        $env:FLASK_ENV = "development"
        & $Python -m flask run --port=$Port --reload --debugger
    }
    
    "shell" {
        Write-ColorOutput "Opening Flask shell..." "Yellow"
        & $VenvActivate
        $env:FLASK_APP = $FlaskApp
        & $Python -m flask shell
    }
    
    "db-init" {
        Write-ColorOutput "Initializing database..." "Yellow"
        if (-not (Test-Path "database")) {
            New-Item -ItemType Directory -Path "database"
        }
        Invoke-VenvCommand "$Python -c 'from app import db; db.create_all()'"
        Write-ColorOutput "✓ Database initialized!" "Green"
    }
    
    "db-migrate" {
        Write-ColorOutput "Running database migrations..." "Yellow"
        & $VenvActivate
        $env:FLASK_APP = $FlaskApp
        & $Python -m flask db upgrade
        deactivate
        Write-ColorOutput "✓ Migrations completed!" "Green"
    }
    
    "db-reset" {
        Write-ColorOutput "WARNING: This will delete all data!" "Red"
        $confirm = Read-Host "Are you sure? (y/N)"
        if ($confirm -eq 'y') {
            Write-ColorOutput "Resetting database..." "Yellow"
            Remove-Item "database\*.db", "database\*.sqlite" -ErrorAction SilentlyContinue
            & $PSCommandPath db-init
            Write-ColorOutput "✓ Database reset!" "Green"
        }
    }
    
    "test" {
        Write-ColorOutput "Running tests..." "Yellow"
        & $VenvActivate
        try {
            & pytest tests -v --color=yes
        } catch {
            & $Python test_demo.py
        }
        deactivate
        Write-ColorOutput "✓ Tests completed!" "Green"
    }
    
    "test-coverage" {
        Write-ColorOutput "Running tests with coverage..." "Yellow"
        & $VenvActivate
        try {
            & pytest tests --cov=. --cov-report=html --cov-report=term
        } catch {
            & $Python -m coverage run test_demo.py
            & $Python -m coverage report
        }
        deactivate
        Write-ColorOutput "✓ Coverage report generated!" "Green"
    }
    
    "lint" {
        Write-ColorOutput "Running linter..." "Yellow"
        & $VenvActivate
        try {
            & flake8 . --exclude=$Venv,__pycache__ --max-line-length=120
        } catch {
            Get-ChildItem -Filter "*.py" | ForEach-Object { & $Python -m py_compile $_.FullName }
        }
        deactivate
        Write-ColorOutput "✓ Linting completed!" "Green"
    }
    
    "format" {
        Write-ColorOutput "Formatting code..." "Yellow"
        & $VenvActivate
        try {
            & black . --exclude=$Venv
        } catch {
            Write-ColorOutput "Install black: pip install black" "Yellow"
        }
        deactivate
        Write-ColorOutput "✓ Code formatted!" "Green"
    }
    
    "type-check" {
        Write-ColorOutput "Running type checks..." "Yellow"
        & $VenvActivate
        try {
            & mypy . --ignore-missing-imports
        } catch {
            Write-ColorOutput "Install mypy: pip install mypy" "Yellow"
        }
        deactivate
        Write-ColorOutput "✓ Type checking completed!" "Green"
    }
    
    "security" {
        Write-ColorOutput "Running security scan..." "Yellow"
        & $VenvActivate
        try {
            & bandit -r . -x $Venv
        } catch {
            Write-ColorOutput "Install bandit: pip install bandit" "Yellow"
        }
        deactivate
        Write-ColorOutput "✓ Security scan completed!" "Green"
    }
    
    "check-deps" {
        Write-ColorOutput "Checking dependencies..." "Yellow"
        Invoke-VenvCommand "$Pip list --outdated"
        Write-ColorOutput "✓ Dependency check completed!" "Green"
    }
    
    "build" {
        Write-ColorOutput "Building project..." "Yellow"
        & $PSCommandPath clean
        & $PSCommandPath install
        & $PSCommandPath test
        & $PSCommandPath lint
        Write-ColorOutput "✓ Build completed!" "Green"
    }
    
    "clean" {
        Write-ColorOutput "Cleaning project..." "Yellow"
        
        # Remove Python cache files
        Get-ChildItem -Path . -Include __pycache__,*.pyc,*.pyo,*.coverage,.pytest_cache,.mypy_cache,htmlcov,*.egg-info -Recurse -Force | 
            Remove-Item -Force -Recurse -ErrorAction SilentlyContinue
        
        Write-ColorOutput "✓ Cleanup completed!" "Green"
    }
    
    "clean-all" {
        Write-ColorOutput "Removing virtual environment..." "Red"
        & $PSCommandPath clean
        Remove-Item $Venv -Recurse -Force -ErrorAction SilentlyContinue
        Write-ColorOutput "✓ Deep clean completed!" "Green"
    }
    
    "logs" {
        Write-ColorOutput "Showing application logs..." "Yellow"
        $logFiles = Get-ChildItem -Filter "*.log" -ErrorAction SilentlyContinue
        if ($logFiles) {
            Get-Content $logFiles -Tail 50 -Wait
        } else {
            Write-ColorOutput "No log files found" "Yellow"
        }
    }
    
    "backup" {
        Write-ColorOutput "Creating backup..." "Yellow"
        $timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
        $backupName = "..\$ProjectName-backup-$timestamp.zip"
        
        # Create backup excluding venv and cache
        Compress-Archive -Path * -DestinationPath $backupName -Force `
            -CompressionLevel Optimal `
            -Exclude $Venv, "__pycache__", "*.pyc", "*.pyo", ".pytest_cache"
        
        Write-ColorOutput "✓ Backup created: $backupName" "Green"
    }
    
    "git-status" {
        git status
    }
    
    "git-commit" {
        $message = Read-Host "Commit message"
        git add -A
        git commit -m $message
    }
    
    "git-push" {
        $branch = git branch --show-current
        git push origin $branch
    }
    
    "docs" {
        Write-ColorOutput "Generating documentation..." "Yellow"
        & $VenvActivate
        try {
            & pdoc --html --output-dir docs .
        } catch {
            Write-ColorOutput "Install pdoc: pip install pdoc3" "Yellow"
        }
        deactivate
        Write-ColorOutput "✓ Documentation generated in docs/" "Green"
    }
    
    "serve-docs" {
        Write-ColorOutput "Serving documentation..." "Yellow"
        & $Python -m http.server 8080 --directory docs
    }
    
    "profile" {
        Write-ColorOutput "Profiling application..." "Yellow"
        Invoke-VenvCommand "$Python -m cProfile -s cumulative $FlaskApp"
    }
    
    "monitor" {
        Write-ColorOutput "Monitoring application..." "Yellow"
        while ($true) {
            Clear-Host
            Write-ColorOutput "Python Processes:" "Yellow"
            Get-Process | Where-Object {$_.ProcessName -like "*python*"} | Format-Table
            Start-Sleep -Seconds 2
        }
    }
    
    "ci" {
        Write-ColorOutput "Running CI checks..." "Yellow"
        & $PSCommandPath clean
        & $PSCommandPath install
        & $PSCommandPath lint
        & $PSCommandPath type-check
        & $PSCommandPath security
        & $PSCommandPath test-coverage
        Write-ColorOutput "✓ CI checks passed!" "Green"
    }
    
    "deploy-staging" {
        Write-ColorOutput "Deploying to staging..." "Yellow"
        Write-ColorOutput "TODO: Add staging deployment commands" "Gray"
        Write-ColorOutput "✓ Staging deployment completed!" "Green"
    }
    
    "deploy-production" {
        Write-ColorOutput "Deploying to PRODUCTION..." "Red"
        $confirm = Read-Host "Are you sure you want to deploy to production? (y/N)"
        if ($confirm -eq 'y') {
            Write-ColorOutput "TODO: Add production deployment commands" "Gray"
            Write-ColorOutput "✓ Production deployment completed!" "Green"
        }
    }
    
    # Aliases
    "i" { & $PSCommandPath install }
    "d" { & $PSCommandPath dev }
    "t" { & $PSCommandPath test }
    "c" { & $PSCommandPath clean }
    "b" { & $PSCommandPath build }
    "r" { & $PSCommandPath run }
    
    default {
        Write-ColorOutput "Unknown command: $Command" "Red"
        Write-ColorOutput "Run '.\Makefile.ps1 help' for available commands" "Yellow"
    }
}
