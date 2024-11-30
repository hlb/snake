#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
NC='\033[0m' # No Color

echo -e "${GREEN}Generating PDFs from Markdown presentations...${NC}"

# Generate Chinese version
echo "Converting presentation-zh.md to PDF..."
npx @marp-team/marp-cli presentation-zh.md --pdf --allow-local-files

# Generate English version
echo "Converting presentation.md to PDF..."
npx @marp-team/marp-cli presentation.md --pdf --allow-local-files

echo -e "${GREEN}Done! PDFs have been generated:${NC}"
echo "- presentation-zh.pdf"
echo "- presentation.pdf"
