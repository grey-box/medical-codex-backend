#!/bin/bash

# Iterative testing script for medical codex backend
# This script runs tests in Docker and returns to shell for iterative development

set -e

echo "🚀 Starting Medical Codex Backend Iterative Testing"
echo "=================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to cleanup on exit
cleanup() {
    print_status "🧹 Cleaning up Docker containers..."
    docker-compose -f docker-compose.test.yml down -v --remove-orphans 2>/dev/null || true
    print_success "✅ Cleanup completed"
}

# Set trap to cleanup on script exit
trap cleanup EXIT

# Function to check if Docker is running
check_docker() {
    if ! docker info >/dev/null 2>&1; then
        print_error "Docker is not running. Please start Docker first."
        exit 1
    fi
    print_success "✅ Docker is running"
}

# Function to run tests
run_tests() {
    print_status "🏃‍♂️ Running tests in Docker..."
    
    # Run tests and capture output, then automatically return to shell
    docker-compose -f docker-compose.test.yml up --build
    local exit_code=$?
    
    if [ $exit_code -eq 0 ]; then
        print_success "✅ Tests completed successfully"
    else
        print_warning "⚠️ Tests completed with issues (exit code: $exit_code)"
    fi
    
    return $exit_code
}

# Function to show test results
show_results() {
    if [ -f "test-results/junit.xml" ]; then
        print_status "📄 Test results available in: test-results/junit.xml"
        print_status "🔍 You can view detailed results in the test-results/ directory"
    fi
}

# Function to analyze test results
analyze_results() {
    if [ -f "test-results/junit.xml" ]; then
        # Count errors and failures in the junit.xml file
        local errors=$(grep -c "error message=" test-results/junit.xml 2>/dev/null || echo "0")
        local failures=$(grep -c "type=\"failure\"" test-results/junit.xml 2>/dev/null || echo "0")
        
        if [ "$errors" = "0" ] && [ "$failures" = "0" ]; then
            print_success "🎉 All tests passed!"
            return 0
        else
            print_warning "🔧 Test results: $errors errors, $failures failures"
            return 1
        fi
    else
        # If no junit.xml, assume based on exit code
        if [ $1 -eq 0 ]; then
            print_success "🎉 All tests passed!"
            return 0
        else
            print_warning "🔧 Tests completed with issues (exit code: $1)"
            return 1
        fi
    fi
}

# Main execution
main() {
    print_status "🔍 Checking prerequisites..."
    check_docker
    
    print_status "🏗️  Building and running tests..."
    run_tests
    local test_exit_code=$?
    
    show_results
    
    if analyze_results $test_exit_code; then
        # Tests passed
        :
    else
        # Tests failed
        print_status "💡 Common issues to check:"
        print_status "   - Database tables and views exist"
        print_status "   - SQLAlchemy models are properly defined"
        print_status "   - No circular imports in application code"
        print_status "   - All dependencies are installed"
    fi
    
    print_status "🔄 Iterative testing session completed"
    print_status "👉 Make your changes and run './test_iterative.sh' again to test"
}

# Run main function
main "$@"