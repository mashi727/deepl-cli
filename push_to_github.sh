#!/bin/bash

# Script to create and push to GitHub repository
# Usage: ./push_to_github.sh [github-username]

GITHUB_USER=${1:-$GITHUB_USERNAME}
REPO_NAME="deepl-cli"

if [ -z "$GITHUB_USER" ]; then
    echo "Error: Please provide GitHub username"
    echo "Usage: $0 <github-username>"
    exit 1
fi

echo "Creating GitHub repository for $GITHUB_USER/$REPO_NAME..."

# Check if gh CLI is installed
if ! command -v gh &> /dev/null; then
    echo "GitHub CLI (gh) is not installed."
    echo "Please install it from: https://cli.github.com/"
    echo ""
    echo "Or manually create the repository and run:"
    echo "  git remote add origin git@github.com:$GITHUB_USER/$REPO_NAME.git"
    echo "  git branch -M main"
    echo "  git push -u origin main"
    exit 1
fi

# Create repository using GitHub CLI
gh repo create "$REPO_NAME" \
    --public \
    --description "A command-line interface for DeepL translation API" \
    --homepage "https://github.com/$GITHUB_USER/$REPO_NAME" \
    --license MIT \
    --push \
    --source=.

# Add topics
gh repo edit "$GITHUB_USER/$REPO_NAME" \
    --add-topic deepl \
    --add-topic translation \
    --add-topic cli \
    --add-topic python

echo "Repository created successfully!"
echo "Visit: https://github.com/$GITHUB_USER/$REPO_NAME"
echo ""
echo "Next steps:"
echo "1. Add your DeepL API key to GitHub Secrets as DEEPL_API_KEY for tests"
echo "2. Get PyPI API token and add as PYPI_API_TOKEN for publishing"
echo "3. Update README.md with your information"
echo "4. Create first release to trigger PyPI publish"
