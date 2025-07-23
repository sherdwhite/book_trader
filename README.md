# Book Trader

A Django-based book trading platform that allows users to list, discover, and trade books with other users. The application features user authentication, book management, auction functionality, and a RESTful API.

## Features

- **User Management**: Registration, authentication, and user profiles
- **Book Catalog**: Add, edit, and browse books with detailed information
- **Trading System**: Post books for trade and negotiate with other users
- **Auction System**: Bid on books through an auction mechanism
- **REST API**: Full API access for all major functionality
- **Admin Interface**: Django admin for content management

## Quick Start

Choose your preferred development environment:

### Option 1: VS Code DevContainer (Recommended)

**Prerequisites**: VS Code with Dev Containers extension

1. Clone the repository
2. Open in VS Code
3. When prompted, click "Reopen in Container" or use Command Palette: "Dev Containers: Reopen in Container"
4. Wait for the container to build (first time only)
5. Run migrations and start the server:
   ```bash
   cd booktrader
   python manage.py migrate
   python manage.py loaddata initial_data_MANUAL
   python manage.py createsuperuser
   python manage.py runserver 0.0.0.0:8000
   ```

The DevContainer automatically configures:
- Python environment with all dependencies
- PostgreSQL database
- VS Code extensions for Django development
- Debug configurations

### Option 2: Docker Compose

**Prerequisites**: Docker and Docker Compose

#### Install Docker

* [Docker For Linux](https://docs.docker.com/engine/installation/linux/ubuntu/)
* [Docker For Mac](https://docs.docker.com/docker-for-mac/)
* [Docker For Windows](https://docs.docker.com/docker-for-windows/)

#### Setup and Run

```bash
# Build and start services
docker compose build
docker compose up -d

# Run initial setup
docker compose exec booktrader python manage.py migrate
docker compose exec booktrader python manage.py loaddata initial_data_MANUAL
docker compose exec booktrader python manage.py createsuperuser

# View logs
docker compose logs -f booktrader
```

### Option 3: Local Development

**Prerequisites**: Python 3.12+, PostgreSQL

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   cd booktrader
   pip install -r requirements.txt
   ```
4. Set up environment variables:
   ```bash
   cp .env.local .env
   # Edit .env with your local database settings
   ```
5. Run setup:
   ```bash
   python manage.py migrate
   python manage.py loaddata initial_data_MANUAL
   python manage.py createsuperuser
   python manage.py runserver
   ```

## Environment Configuration

The project supports multiple environment configurations:

- **DevContainer**: Automatic setup with PostgreSQL in Docker
- **Docker Compose**: Full containerized development environment
- **Local Development**: Use local Python and PostgreSQL installation

See the [Environment Variables Guide](docs/ENVIRONMENT_VARIABLES.md) for detailed configuration options.

## Accessing the Application

Once running, the application will be available at:
- **Web Interface**: http://localhost:8000/
- **Admin Interface**: http://localhost:8000/admin/
- **API Endpoints**: http://localhost:8000/api/

## API Documentation

The project includes a RESTful API with endpoints for:
- Books: `/api/v1/books/`
- Authors: `/api/v1/authors/`
- Publishers: `/api/v1/publishers/`

API versioning is implemented - see [API Versioning Guide](docs/API_VERSIONING.md) for details.

## Development

### VS Code Integration

The project includes VS Code configuration for optimal development experience:

- **Launch Configurations**: Debug Django server and shell
- **Task Configurations**: Common Django management commands
- **Extensions**: Recommended extensions for Django development
- **DevContainer**: Complete development environment setup

### Database Management

The application uses PostgreSQL in development and production. Connection pooling is configured automatically based on the environment. See [Database Pooling Guide](docs/DATABASE_POOLING.md) for details.

### Running Tests

Multiple options for running tests:

```bash
# Using Docker Compose
docker compose exec booktrader python manage.py test

# In DevContainer or local environment
python manage.py test

# Run specific app tests
python manage.py test books.tests
```

### Management Commands

```bash
# Generate random book ratings (development only)
python manage.py generate_random_ratings

# Apply database migrations
python manage.py migrate

# Create admin user
python manage.py createsuperuser

# Collect static files (production)
python manage.py collectstatic
```

## Project Structure

```
booktrader/
├── api/                    # REST API application
├── auctions/              # Auction functionality
├── books/                 # Book catalog management
├── booktrader/            # Django project settings
├── core/                  # Shared utilities
├── templates/             # HTML templates
├── trades/                # Trading system
├── users/                 # User management
├── static/                # Static files (CSS, JS)
└── manage.py              # Django management script

docs/                      # Documentation
├── API_VERSIONING.md
├── DATABASE_POOLING.md
└── ENVIRONMENT_VARIABLES.md

.devcontainer/             # VS Code DevContainer configuration
├── devcontainer.json
├── docker-compose.yml
└── .env.example
```

## Production Deployment

For production deployment:

1. Copy production environment template:
   ```bash
   cp .env.production.example .env.production
   ```

2. Update production settings:
   - Generate new `DJANGO_SECRET_KEY`
   - Set `DJANGO_DEBUG=False`
   - Configure domain in `DJANGO_ALLOWED_HOSTS`
   - Set secure database credentials
   - Configure static file serving

3. Use production Docker Compose:
   ```bash
   docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d
   ```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests to ensure everything works
5. Submit a pull request

## Documentation

- [Environment Variables Guide](docs/ENVIRONMENT_VARIABLES.md)
- [Database Pooling Configuration](docs/DATABASE_POOLING.md)
- [API Versioning](docs/API_VERSIONING.md)

## License

This project is licensed under the Creative Commons Attribution-NonCommercial 4.0 International License - see the [LICENSE](LICENSE) file for details.

**Non-Commercial Use Only**: This project is available for personal and educational use. Commercial use requires express permission from the repository owner.

For commercial licensing inquiries, please contact the repository owner.
