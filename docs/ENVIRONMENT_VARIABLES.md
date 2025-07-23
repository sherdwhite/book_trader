# Environment Variables Guide

This document explains all environment variables used in the BookTrader application and how to set them up for different environments.

## Environment Files

### 1. `.env.example` (Root directory)
- **Purpose**: Template for general local development
- **Usage**: Copy to `.env` and customize for local development
- **Suitable for**: Running Django locally without Docker

### 2. `.devcontainer/.env.example`
- **Purpose**: Template for VS Code DevContainer development
- **Usage**: Copy to `.devcontainer/.env` and customize
- **Suitable for**: Development using VS Code DevContainer

### 3. `.env.production.example`
- **Purpose**: Template for production deployment
- **Usage**: Copy to `.env.production` and customize for production
- **Suitable for**: Production server deployment

## Environment Variable Reference

### Django Core Settings

| Variable | Default | Description | Required |
|----------|---------|-------------|----------|
| `DJANGO_SECRET_KEY` | Auto-generated | Django secret key for cryptographic signing | ✅ Yes |
| `DJANGO_DEBUG` | `True` | Enable/disable debug mode | ✅ Yes |
| `DJANGO_ALLOWED_HOSTS` | `*` | Comma-separated list of allowed hosts | ✅ Yes |
| `DJANGO_ENV` | `development` | Environment type (development/production) | ❌ No |

### Database Settings

| Variable | Default | Description | Required |
|----------|---------|-------------|----------|
| `DB_ENGINE` | `django.db.backends.postgresql` | Database engine | ❌ No |
| `DB_NAME` | `postgres` | Database name | ✅ Yes |
| `DB_USER` | `postgres` | Database username | ✅ Yes |
| `DB_PASSWORD` | `postgres` | Database password | ✅ Yes |
| `DB_HOST` | `db` | Database host | ✅ Yes |
| `DB_PORT` | `5432` | Database port | ❌ No |

### Database Connection Pooling

| Variable | Default | Description | Required |
|----------|---------|-------------|----------|
| `DB_CONN_MAX_AGE` | `600` (production) / `300` (development) | Connection max age in seconds | ❌ No |
| `DB_CONNECT_TIMEOUT` | `30` (production) / `10` (development) | Connection timeout in seconds | ❌ No |

### Development Tools

| Variable | Default | Description | Required |
|----------|---------|-------------|----------|
| `ENABLE_DEBUG_TOOLBAR` | `True` | Enable Django Debug Toolbar | ❌ No |
| `LOG_LEVEL` | `INFO` | Logging level (DEBUG/INFO/WARNING/ERROR) | ❌ No |

### Static Files & Media

| Variable | Default | Description | Required |
|----------|---------|-------------|----------|
| `STATIC_URL` | `/static/` | URL prefix for static files | ❌ No |
| `MEDIA_URL` | `/media/` | URL prefix for media files | ❌ No |

## Setup Instructions

### 1. Local Development (Without Docker)

```bash
# Copy the example file
cp .env.example .env

# Edit the .env file with your local database settings
# Make sure PostgreSQL is running locally
# Create a database: createdb booktrader_dev

# Run migrations
cd booktrader
python manage.py migrate

# Start development server
python manage.py runserver
```

### 2. Docker Compose Development

```bash
# The docker-compose.yml already has environment variables set
# Just run:
docker-compose up
```

### 3. VS Code DevContainer

```bash
# Copy the devcontainer example
cp .devcontainer/.env.example .devcontainer/.env

# Open in VS Code and rebuild container
# The environment will be automatically configured
```

### 4. Production Deployment

```bash
# Copy the production example
cp .env.production.example .env.production

# Edit .env.production with your production settings:
# - Generate a new SECRET_KEY
# - Set DEBUG=False
# - Configure your domain in ALLOWED_HOSTS
# - Set up production database credentials
# - Configure static file serving

# Deploy using your preferred method
```

## Security Notes

### Development
- ✅ Default secret keys are fine
- ✅ DEBUG=True is acceptable
- ✅ ALLOWED_HOSTS=* is acceptable

### Production
- ⚠️  **NEVER** use default secret keys
- ⚠️  **ALWAYS** set DEBUG=False
- ⚠️  **ALWAYS** specify exact domains in ALLOWED_HOSTS
- ⚠️  **ALWAYS** use strong database passwords
- ⚠️  **ALWAYS** use HTTPS in production

## Troubleshooting

### Database Connection Issues
1. Verify `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD` are correct
2. Ensure PostgreSQL is running and accessible
3. Check if the database exists: `createdb booktrader_dev`

### Secret Key Issues
1. Generate a new secret key at https://djecrety.ir/
2. Set it in your environment file
3. Restart the application

### Allowed Hosts Issues
1. Add your domain to `DJANGO_ALLOWED_HOSTS`
2. Use comma-separated values: `domain1.com,domain2.com`
3. For development, `localhost,127.0.0.1` is usually sufficient
