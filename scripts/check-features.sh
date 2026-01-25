#!/bin/bash

# Check if code uses features not available in project version
# Usage: ./scripts/check-features.sh [version]
# If no version provided, reads from .4d-metadata.json

set -e

# Get version from metadata or argument
if [ -n "$1" ]; then
    VERSION="$1"
elif [ -f ".4d-metadata.json" ]; then
    VERSION=$(grep '"4d"' .4d-metadata.json | cut -d'"' -f4)
else
    echo "Error: No version specified and .4d-metadata.json not found"
    echo "Usage: $0 [version]"
    echo "   or: Run ./scripts/init-metadata.sh first"
    exit 1
fi

echo "Checking features against 4D version $VERSION"
echo "=============================================="
echo ""
echo "This script will use WebFetch to check the changelog."
echo "Claude will analyze: https://developer.4d.com/docs/Notes/updates"
echo ""
echo "Instructions for Claude:"
echo "1. Use WebFetch to fetch: https://developer.4d.com/docs/Notes/updates"
echo "2. Extract all features introduced AFTER version $VERSION"
echo "3. List them in a clear format"
echo "4. Return ONLY the features list (minimal context)"
echo ""
echo "Note: WebFetch runs in a separate context and returns sanitized output."
echo "This keeps your main context clean."
