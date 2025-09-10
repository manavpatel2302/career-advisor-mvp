# Career Advisor MVP - Professional Build System Guide

## 🚀 Overview

This project includes a comprehensive build automation system with professional-grade features for development, testing, deployment, and maintenance. The system provides consistent commands across different platforms.

## 📋 Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Available Commands](#available-commands)
- [Platform Support](#platform-support)
- [Advanced Features](#advanced-features)
- [CI/CD Integration](#cicd-integration)
- [Best Practices](#best-practices)

## 💻 Installation

### Windows Users

For Windows, we provide three options:

1. **Batch File (Recommended for Windows)**
   ```cmd
   make.bat [command]
   ```

2. **PowerShell Script**
   ```powershell
   .\Makefile.ps1 [command]
   ```

3. **GNU Make (requires make installation)**
   ```cmd
   make [command]
   ```

### Unix/Linux/Mac Users

Use the standard Makefile:
```bash
make [command]
```

## 🎯 Quick Start

1. **Initial Setup**
   ```cmd
   make.bat setup
   ```
   This will:
   - Create a Python virtual environment
   - Install all dependencies
   - Set up configuration files

2. **Run Development Server**
   ```cmd
   make.bat dev
   ```

3. **Run Tests**
   ```cmd
   make.bat test
   ```

## 📦 Available Commands

### Setup & Installation

| Command | Alias | Description |
|---------|-------|-------------|
| `setup` | - | Complete project setup (venv, deps, config) |
| `install` | `i` | Install Python dependencies |
| `install-dev` | - | Install development dependencies |
| `freeze` | - | Update requirements.txt |

### Development

| Command | Alias | Description |
|---------|-------|-------------|
| `dev` | `d` | Run Flask in development mode |
| `run` | `r` | Run Flask in production mode |
| `debug` | - | Run with debugging enabled |
| `shell` | - | Open Flask interactive shell |

### Database Management

| Command | Description |
|---------|-------------|
| `db-init` | Initialize database |
| `db-migrate` | Run database migrations |
| `db-reset` | Reset database (⚠️ destroys data) |

### Testing

| Command | Alias | Description |
|---------|-------|-------------|
| `test` | `t` | Run all tests |
| `test-coverage` | - | Run tests with coverage report |
| `test-watch` | - | Run tests in watch mode |

### Code Quality

| Command | Description |
|---------|-------------|
| `lint` | Run code linting (flake8) |
| `format` | Format code with black |
| `type-check` | Type checking with mypy |
| `security` | Security scan with bandit |
| `check-deps` | Check for outdated dependencies |

### Build & Deployment

| Command | Alias | Description |
|---------|-------|-------------|
| `build` | `b` | Complete production build |
| `build-docker` | - | Build Docker image |
| `deploy-staging` | - | Deploy to staging |
| `deploy-production` | - | Deploy to production |

### Utilities

| Command | Alias | Description |
|---------|-------|-------------|
| `clean` | `c` | Clean temp files and caches |
| `clean-all` | - | Deep clean (including venv) |
| `logs` | - | View application logs |
| `backup` | - | Create project backup |

### Documentation

| Command | Description |
|---------|-------------|
| `docs` | Generate documentation |
| `serve-docs` | Serve docs locally |

### Git Integration

| Command | Description |
|---------|-------------|
| `git-status` | Show git status |
| `git-commit` | Stage and commit changes |
| `git-push` | Push to remote |

### Performance

| Command | Description |
|---------|-------------|
| `profile` | Profile application performance |
| `monitor` | Monitor application metrics |

### CI/CD

| Command | Description |
|---------|-------------|
| `ci` | Run all CI checks |

## 🔧 Advanced Features

### 1. **Professional Project Structure**
The Makefile system enforces a professional project structure with:
- Virtual environment isolation
- Dependency management
- Environment configuration (.env files)
- Test organization
- Documentation generation

### 2. **Color-Coded Output**
All commands provide clear, color-coded output:
- 🟨 Yellow: Operations in progress
- 🟩 Green: Successful completion
- 🔴 Red: Errors or warnings
- 🔵 Blue: Information

### 3. **Error Handling**
- Graceful degradation when tools aren't installed
- Clear error messages
- Automatic fallbacks

### 4. **Cross-Platform Support**
- Windows batch files
- PowerShell scripts
- Unix/Linux Makefiles
- Consistent command interface

### 5. **Development Workflow**
Complete development workflow support:
```cmd
# Morning routine
make.bat clean
make.bat install
make.bat test
make.bat dev

# Before commit
make.bat format
make.bat lint
make.bat test
make.bat build

# Deployment
make.bat build
make.bat deploy-staging
# After testing...
make.bat deploy-production
```

## 🔄 CI/CD Integration

### GitHub Actions Example
```yaml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run CI checks
        run: make ci
```

### Jenkins Pipeline Example
```groovy
pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                sh 'make build'
            }
        }
        stage('Test') {
            steps {
                sh 'make test-coverage'
            }
        }
        stage('Deploy') {
            steps {
                sh 'make deploy-staging'
            }
        }
    }
}
```

## 📚 Best Practices

### 1. **Daily Development**
```cmd
# Start of day
make.bat clean
make.bat install
make.bat dev
```

### 2. **Before Committing**
```cmd
make.bat format
make.bat lint
make.bat test
```

### 3. **Regular Maintenance**
```cmd
# Weekly
make.bat check-deps
make.bat security

# Monthly
make.bat clean-all
make.bat setup
```

### 4. **Production Deployment**
```cmd
make.bat build
make.bat test-coverage
make.bat deploy-production
```

## 🛠️ Customization

### Adding New Commands

#### For Windows (make.bat)
```batch
:mycommand
echo Running my custom command...
REM Your command logic here
exit /b 0
```

#### For Unix (Makefile)
```makefile
mycommand: ## Description of my command
	@echo "Running my custom command..."
	# Your command logic here
```

### Modifying Configuration

Edit the configuration section in your preferred file:
- `make.bat` - Lines 12-18
- `Makefile.ps1` - Lines 20-27
- `Makefile` - Lines 15-33

## 🐛 Troubleshooting

### Common Issues

1. **"make" not recognized**
   - Use `make.bat` instead on Windows
   - Or install GNU Make via Scoop: `scoop install make`

2. **Virtual environment not found**
   - Run `make.bat setup` first

3. **Permission errors**
   - Run as Administrator if needed
   - Check file permissions

4. **Python not found**
   - Ensure Python is installed and in PATH
   - Update PYTHON variable in configuration

## 📄 License

This build system is part of the Career Advisor MVP project.

## 🤝 Contributing

To contribute to the build system:
1. Test your changes with `make.bat test`
2. Ensure code quality with `make.bat lint`
3. Update this documentation if needed

## 📞 Support

For issues or questions about the build system:
- Check this guide first
- Review error messages carefully
- Create an issue in the project repository

---

**Pro Tip:** Use command aliases for faster development:
- `make.bat i` instead of `make.bat install`
- `make.bat d` instead of `make.bat dev`
- `make.bat t` instead of `make.bat test`
