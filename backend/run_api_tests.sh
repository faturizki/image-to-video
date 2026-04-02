#!/bin/bash
# Quick API Key Test Runner
# This script helps run API key tests with different configurations

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_header() {
    echo -e "${BLUE}================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}================================${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

# Function to run test without keys (mock mode)
test_without_keys() {
    print_header "Testing Without API Keys (Mock Mode)"
    unset GEMINI_API_KEY
    unset HUGGINGFACE_API_KEY
    python test_api_keys.py || true
}

# Function to run test with provided keys
test_with_keys() {
    print_header "Testing With Provided API Keys"
    
    if [ -z "$GEMINI_API_KEY" ] && [ -z "$HUGGINGFACE_API_KEY" ]; then
        print_warning "No API keys provided in environment"
        return 1
    fi
    
    if [ -n "$GEMINI_API_KEY" ]; then
        print_success "GEMINI_API_KEY is set"
    fi
    
    if [ -n "$HUGGINGFACE_API_KEY" ]; then
        print_success "HUGGINGFACE_API_KEY is set"
    fi
    
    python test_api_keys.py || true
}

# Function to load keys from .env
test_with_env_file() {
    print_header "Testing With .env File"
    
    if [ ! -f .env ]; then
        print_error ".env file not found"
        return 1
    fi
    
    print_success ".env file found, loading keys..."
    source .env
    python test_api_keys.py || true
}

# Main menu
show_menu() {
    print_header "API Key Test Runner"
    echo ""
    echo "1) Test without keys (mock mode)"
    echo "2) Test with environment variables"
    echo "3) Test with .env file"
    echo "4) Run all tests"
    echo "5) Exit"
    echo ""
}

# Main loop
while true; do
    show_menu
    read -p "Select option [1-5]: " choice
    
    case $choice in
        1)
            test_without_keys
            ;;
        2)
            test_with_keys
            ;;
        3)
            test_with_env_file
            ;;
        4)
            test_without_keys
            echo ""
            test_with_keys
            echo ""
            test_with_env_file
            ;;
        5)
            print_success "Exiting..."
            exit 0
            ;;
        *)
            print_error "Invalid option, please select 1-5"
            ;;
    esac
    
    echo ""
    read -p "Press Enter to continue..."
    clear
done
