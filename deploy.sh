#!/bin/bash
# deploy.sh - Simple Docker deployment

set -e

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Default values
export DOCKERHUB_USERNAME=${DOCKERHUB_USERNAME:-"username"}
COMPOSE_FILE="docker-compose.yml"

echo -e "${GREEN}🚀 Deploying OmniPass...${NC}"

# Function to show usage
usage() {
    echo "Usage: ./deploy.sh [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  up      - Build and start containers"
    echo "  down    - Stop and remove containers"
    echo "  restart - Restart containers"
    echo "  logs    - Show logs"
    echo "  status  - Show container status"
    echo "  clean   - Remove containers and images"
    echo ""
    echo "Examples:"
    echo "  ./deploy.sh up"
    echo "  ./deploy.sh down"
    echo "  ./deploy.sh logs"
}

# Start containers
up() {
    echo -e "${YELLOW}📦 Building and starting containers...${NC}"
    docker compose -f $COMPOSE_FILE up -d --build
    echo -e "${GREEN}✅ Containers started!${NC}"
    echo ""
    echo "🌐 Frontend: http://localhost:80"
    echo "🔧 Backend:  http://localhost:8000"
    echo ""
    docker compose -f $COMPOSE_FILE ps
}

# Stop containers
down() {
    echo -e "${YELLOW}🛑 Stopping containers...${NC}"
    docker compose -f $COMPOSE_FILE down
    echo -e "${GREEN}✅ Containers stopped${NC}"
}

# Restart containers
restart() {
    echo -e "${YELLOW}🔄 Restarting containers...${NC}"
    docker compose -f $COMPOSE_FILE restart
    echo -e "${GREEN}✅ Containers restarted${NC}"
}

# Show logs
logs() {
    docker compose -f $COMPOSE_FILE logs -f
}

# Show status
status() {
    docker compose -f $COMPOSE_FILE ps
}

# Clean everything
clean() {
    echo -e "${RED}⚠️  This will remove all containers and images!${NC}"
    read -p "Are you sure? (y/N) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        docker compose -f $COMPOSE_FILE down -v
        docker rmi -f ${DOCKERHUB_USERNAME}/omnipass-backend:latest 2>/dev/null || true
        docker rmi -f ${DOCKERHUB_USERNAME}/omnipass-frontend:latest 2>/dev/null || true
        echo -e "${GREEN}✅ Cleaned up${NC}"
    fi
}

# Main
case "$1" in
    up)
        up
        ;;
    down)
        down
        ;;
    restart)
        restart
        ;;
    logs)
        logs
        ;;
    status)
        status
        ;;
    clean)
        clean
        ;;
    help|--help|-h)
        usage
        ;;
    *)
        echo -e "${RED}❌ Unknown command: $1${NC}"
        usage
        exit 1
        ;;
esac
