#!/bin/bash

# Initialize .4d-metadata.json for a 4D project
# Usage: ./scripts/init-metadata.sh

set -e

echo "4D Project Metadata Initialization"
echo "==================================="
echo ""

# Check if we're in a project root
if [ ! -d "Project" ]; then
    echo "Error: No 'Project' folder found. Are you in the 4D project root?"
    exit 1
fi

# Check if metadata already exists
if [ -f ".4d-metadata.json" ]; then
    echo "Warning: .4d-metadata.json already exists."
    read -p "Overwrite? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Cancelled."
        exit 0
    fi
fi

# Prompt for version
echo ""
echo "Enter your 4D version information:"
echo "(You can find this in 4D: Help > About 4D)"
echo ""
read -p "4D version (e.g., 20.5.0): " version
read -p "Build number (e.g., 20R5.123456): " build

# Create metadata file
cat > .4d-metadata.json << EOF
{
  "version": {
    "4d": "$version",
    "build": "$build",
    "lastUpdated": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
  },
  "feedback": []
}
EOF

echo ""
echo "✓ Created .4d-metadata.json"
echo ""
echo "Next steps:"
echo "1. Commit .4d-metadata.json to git"
echo "2. Update this file when you upgrade 4D"
echo "3. The 4D development skill will use this to check feature compatibility"
echo ""
cat .4d-metadata.json
