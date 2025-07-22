# Database Connection Pooling Configuration

This document explains the database connection pooling settings added to the BookTrader application.

## What is Connection Pooling?

Connection pooling is a technique used to manage database connections efficiently by:
- Reusing existing connections instead of creating new ones for each request
- Maintaining a pool of active connections ready for use
- Automatically closing idle connections after a timeout period

## Configuration

### Environment Variables

The following environment variables control database connection pooling:

- `DJANGO_ENV`: Set to `production` for production-level pooling settings
- `DB_CONN_MAX_AGE`: Connection lifetime in seconds (default: 600 = 10 minutes)
- `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`: Standard database connection settings

### Pool Sizes

**Development (DJANGO_ENV=development or not set):**
- Maximum connections: 10
- Minimum connections: 2

**Production (DJANGO_ENV=production):**
- Maximum connections: 50
- Minimum connections: 10

## Usage

### Development
```bash
docker-compose up
```

### Production
```bash
# Using production settings with larger connection pool
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up
```
## Monitoring

Monitor your connection pool with these Django management commands:
```bash
# Check database connectivity
python manage.py check --database default

# Monitor active connections (requires database access)
python manage.py dbshell
# Then run: SELECT count(*) FROM pg_stat_activity;
```
