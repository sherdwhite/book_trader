# Environment-specific database settings
import os

# Base connection pool settings
BASE_DB_OPTIONS = {
    "connect_timeout": int(os.environ.get("DB_CONNECT_TIMEOUT", "30")),
    "options": "-c default_transaction_isolation=read committed"
}

# Development settings (smaller pool for local development)
DEVELOPMENT_DB_POOL = {
    "MAX_CONNS": int(os.environ.get("DB_MAX_CONNS_DEV", "10")),
    "MIN_CONNS": int(os.environ.get("DB_MIN_CONNS_DEV", "2")),
}

# Production settings (larger pool for production workloads)
PRODUCTION_DB_POOL = {
    "MAX_CONNS": int(os.environ.get("DB_MAX_CONNS_PROD", "50")),
    "MIN_CONNS": int(os.environ.get("DB_MIN_CONNS_PROD", "10")),
}

# Get environment-specific pool settings
def get_db_pool_settings():
    """Return appropriate connection pool settings based on environment"""
    if os.environ.get('DJANGO_ENV') == 'production':
        pool_settings = PRODUCTION_DB_POOL.copy()
    else:
        pool_settings = DEVELOPMENT_DB_POOL.copy()

    pool_settings.update(BASE_DB_OPTIONS)
    return pool_settings
