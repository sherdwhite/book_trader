#!/bin/bash

# BookTrader Environment Setup Script
# This script helps you set up environment files for different deployment scenarios

set -e

echo "🚀 BookTrader Environment Setup"
echo "================================"
echo

# Function to create .env file from template
setup_env_file() {
    local template_file=$1
    local target_file=$2
    local description=$3

    if [ -f "$target_file" ]; then
        echo "⚠️  $target_file already exists. Skipping..."
        return
    fi

    if [ ! -f "$template_file" ]; then
        echo "❌ Template file $template_file not found!"
        return 1
    fi

    cp "$template_file" "$target_file"
    echo "✅ Created $target_file for $description"
}

echo "Select your deployment scenario:"
echo "1) Local development (without Docker)"
echo "2) Docker Compose development"
echo "3) VS Code DevContainer"
echo "4) Production deployment"
echo "5) Set up all environments"
echo

read -p "Enter your choice (1-5): " choice

case $choice in
    1)
        echo "Setting up for local development..."
        setup_env_file ".env.example" ".env" "local development"
        echo
        echo "📝 Next steps:"
        echo "1. Edit .env and configure your local database settings"
        echo "2. Make sure PostgreSQL is running"
        echo "3. Create database: createdb booktrader_dev"
        echo "4. Run: cd booktrader && python manage.py migrate"
        echo "5. Start server: python manage.py runserver"
        ;;
    2)
        echo "Setting up for Docker Compose development..."
        echo "✅ Docker Compose environment variables are already configured in docker-compose.yml"
        echo
        echo "📝 Next steps:"
        echo "1. Run: docker-compose up"
        echo "2. Your app will be available at http://localhost:8000"
        ;;
    3)
        echo "Setting up for VS Code DevContainer..."
        setup_env_file ".devcontainer/.env.example" ".devcontainer/.env" "VS Code DevContainer"
        echo
        echo "📝 Next steps:"
        echo "1. Open this project in VS Code"
        echo "2. Click 'Reopen in Container' when prompted"
        echo "3. The environment will be automatically configured"
        ;;
    4)
        echo "Setting up for production deployment..."
        setup_env_file ".env.production.example" ".env.production" "production deployment"
        echo
        echo "🔐 IMPORTANT SECURITY STEPS:"
        echo "1. Edit .env.production and:"
        echo "   - Generate a new SECRET_KEY at https://djecrety.ir/"
        echo "   - Set DEBUG=False"
        echo "   - Configure your actual domain(s) in ALLOWED_HOSTS"
        echo "   - Set secure database credentials"
        echo "2. Never commit .env.production to version control!"
        echo "3. Use HTTPS in production"
        ;;
    5)
        echo "Setting up all environments..."
        setup_env_file ".env.example" ".env" "local development"
        setup_env_file ".devcontainer/.env.example" ".devcontainer/.env" "VS Code DevContainer"
        setup_env_file ".env.production.example" ".env.production" "production deployment"
        echo
        echo "✅ All environment files created!"
        echo "📖 See docs/ENVIRONMENT_VARIABLES.md for detailed configuration guide"
        ;;
    *)
        echo "❌ Invalid choice. Please run the script again."
        exit 1
        ;;
esac

echo
echo "📖 For detailed information about all environment variables,"
echo "   see: docs/ENVIRONMENT_VARIABLES.md"
echo
echo "🎉 Setup complete!"
