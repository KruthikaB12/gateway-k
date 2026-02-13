#!/bin/bash

echo "🚀 Starting Student Gateway Backend..."
echo ""

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install
    echo ""
fi

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚠️  Warning: .env file not found. Using defaults."
    echo ""
fi

echo "✅ Starting server..."
npm start
