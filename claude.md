# QFieldCloud Setup and Management Guide

QFieldCloud is a synchronization service for QField that provides change tracking and team management capabilities for GIS field data collection.

## Architecture Overview

- **Backend**: Django-based Python application
- **Database**: PostgreSQL with PostGIS extension
- **Storage**: MinIO (S3-compatible) or external S3 storage
- **Web Server**: Nginx reverse proxy
- **Containerization**: Docker Compose orchestration

## Prerequisites

### System Requirements
- Docker 20.10+
- Docker Compose 2.0+
- 4GB+ RAM
- 20GB+ disk space
- Git

### Port Requirements (Local Development)
- 8080: QFieldCloud application
- 5432: PostgreSQL database
- 9000: MinIO console
- 8000: Django admin interface

## Local Development Setup

### 1. Repository Setup
```bash
# Clone with submodules
git clone --recurse-submodules git@github.com:opengisch/QFieldCloud.git
cd QFieldCloud

# If submodules weren't initialized
git submodule update --init --recursive
```

### 2. Environment Configuration
```bash
# Copy environment template
cp .env.example .env

# Edit the environment file
nano .env
```

### 3. Key Environment Variables (.env)
```bash
# Development mode
ENVIRONMENT=development
DEBUG=true
COMPOSE_FILE=docker-compose.yml

# Database (development defaults)
POSTGRES_DB=qfieldcloud
POSTGRES_USER=qfieldcloud
POSTGRES_PASSWORD=qfieldcloud
DATABASE_URL=postgres://qfieldcloud:qfieldcloud@db:5432/qfieldcloud

# Storage (development defaults)
AWS_ACCESS_KEY_ID=minioadmin
AWS_SECRET_ACCESS_KEY=minioadmin
AWS_STORAGE_BUCKET_NAME=qfieldcloud
S3_ENDPOINT_URL=http://minio:9000

# Security
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1

# Email (optional for development)
EMAIL_HOST=mailhog
EMAIL_PORT=1025
```

### 4. Building and Starting Services
```bash
# Build and start all services
docker compose up -d --build

# Check service status
docker compose ps

# View logs
docker compose logs -f app
```

### 5. Database Setup
```bash
# Run migrations
docker compose exec app python manage.py migrate

# Create superuser
docker compose run --rm app python manage.py createsuperuser

# Collect static files
docker compose exec app python manage.py collectstatic --no-input
```

### 6. Accessing Services
- **QFieldCloud App**: http://localhost:8080
- **Django Admin**: http://localhost:8080/admin
- **MinIO Console**: http://localhost:9000 (minioadmin/minioadmin)

## Development Workflow

### Common Commands
```bash
# Restart specific service
docker compose restart app

# Access app container
docker compose exec app bash

# View logs for specific service
docker compose logs -f db

# Stop all services
docker compose down

# Remove volumes (reset database)
docker compose down -v
```

### Code Changes
```bash
# Rebuild after code changes
docker compose up -d --build app

# Hot reload (if configured)
# Changes should auto-reload in development mode
```

### Database Management
```bash
# Create new migrations
docker compose exec app python manage.py makemigrations

# Apply migrations
docker compose exec app python manage.py migrate

# Reset database (DANGEROUS)
docker compose down -v
docker compose up -d db
docker compose exec app python manage.py migrate
```

## Testing

### Running Tests
```bash
# Run all tests
docker compose exec app python manage.py test

# Run specific app tests
docker compose exec app python manage.py test core.tests

# Run with coverage
docker compose exec app coverage run --source='.' manage.py test
docker compose exec app coverage report
```

### Test Environment
```bash
# Use test environment
ENVIRONMENT=test docker compose -f docker-compose.test.yml up -d --build
```

## Production Deployment (VPS)

### 1. Server Preparation
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Install Docker Compose
sudo apt install docker-compose-plugin -y

# Configure firewall
sudo ufw allow 22
sudo ufw allow 80
sudo ufw allow 443
sudo ufw enable
```

### 2. Production Environment Configuration
```bash
# Production .env configuration
ENVIRONMENT=production
DEBUG=false
COMPOSE_FILE=docker-compose.yml:docker-compose.override.production.yml

# Production database (external recommended)
DATABASE_URL=postgres://user:password@external-db:5432/qfieldcloud

# Production storage (S3 or external MinIO)
AWS_ACCESS_KEY_ID=your-production-key
AWS_SECRET_ACCESS_KEY=your-production-secret
AWS_STORAGE_BUCKET_NAME=your-production-bucket
S3_ENDPOINT_URL=https://your-s3-compatible-storage.com

# Domain configuration
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
SECRET_KEY=very-strong-production-secret-key

# Email configuration
EMAIL_HOST=smtp.yourprovider.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@yourdomain.com
EMAIL_HOST_PASSWORD=your-email-password
```

### 3. SSL/TLS Configuration
```bash
# Using Let's Encrypt with Nginx
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Auto-renewal
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

### 4. Production Deployment Commands
```bash
# Clone repository
git clone --recurse-submodules git@github.com:opengisch/QFieldCloud.git
cd QFieldCloud

# Configure production environment
cp .env.example .env
# Edit .env with production values

# Deploy production services
docker compose -f docker-compose.yml -f docker-compose.override.production.yml up -d --build

# Run production migrations
docker compose exec app python manage.py migrate

# Create superuser
docker compose exec app python manage.py createsuperuser

# Collect static files
docker compose exec app python manage.py collectstatic --no-input
```

## Monitoring and Maintenance

### Health Checks
```bash
# Check service health
docker compose ps
curl http://localhost:8080/health/

# Database connection test
docker compose exec app python manage.py dbshell
```

### Backup Strategy
```bash
# Database backup
docker compose exec db pg_dump -U qfieldcloud qfieldcloud > backup.sql

# Restore database
docker compose exec -T db psql -U qfieldcloud qfieldcloud < backup.sql

# Backup files (if using local storage)
docker compose exec minio mc mirror qfieldcloud /backup/minio/
```

### Log Management
```bash
# View application logs
docker compose logs -f --tail=100 app

# Rotate logs (configure in docker-compose.yml)
# Add logging configuration to services
```

### Updates and Maintenance
```bash
# Update code
git pull origin main
git submodule update --remote

# Rebuild and restart
docker compose up -d --build

# Run migrations after updates
docker compose exec app python manage.py migrate
```

## Troubleshooting

### Common Issues

1. **Database Connection Errors**
   ```bash
   # Check database container
   docker compose ps db
   docker compose logs db

   # Test connection
   docker compose exec app python manage.py dbshell
   ```

2. **Storage/MinIO Issues**
   ```bash
   # Check MinIO container
   docker compose ps minio
   docker compose logs minio

   # Test S3 connection
   docker compose exec app python manage.py shell
   >>> from storages.backends.s3boto3 import S3Boto3Storage
   >>> storage = S3Boto3Storage()
   >>> storage.exists('test')
   ```

3. **Permission Issues**
   ```bash
   # Fix file permissions
   sudo chown -R $USER:$USER .

   # Docker permission issues
   sudo usermod -aG docker $USER
   # Log out and back in
   ```

4. **Port Conflicts**
   ```bash
   # Check port usage
   sudo netstat -tulpn | grep :8080

   # Kill conflicting processes
   sudo kill -9 <PID>
   ```

### Performance Optimization

1. **Database Optimization**
   ```bash
   # Connect to database
   docker compose exec db psql -U qfieldcloud qfieldcloud

   # Check slow queries
   SELECT query, mean_time, calls FROM pg_stat_statements ORDER BY mean_time DESC LIMIT 10;
   ```

2. **Resource Monitoring**
   ```bash
   # Monitor container resources
   docker stats

   # Check disk usage
   docker system df
   docker system prune -f
   ```

## Security Considerations

1. **Change default passwords** in production
2. **Use environment variables** for secrets
3. **Enable SSL/TLS** in production
4. **Regular updates** of Docker images
5. **Backup strategy** for data protection
6. **Firewall configuration** for port access
7. **Database security** with strong passwords

## API Documentation

Once running, API documentation is available at:
- **Swagger UI**: http://localhost:8080/api/docs/
- **ReDoc**: http://localhost:8080/api/redoc/

## Support and Resources

- **GitHub Repository**: https://github.com/opengisch/QFieldCloud
- **Issues**: https://github.com/opengisch/QFieldCloud/issues
- **QField Documentation**: https://qfield.org/docs/
- **Docker Documentation**: https://docs.docker.com/