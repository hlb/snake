# Documentation Directory

This directory contains the project presentation slides and related documentation.

## Files

- `presentation.md` - English version of the presentation
- `presentation-zh.md` - Chinese version of the presentation
- `screenshot.png` - Game screenshot used in presentations
- `generate-pdf.sh` - Script to generate PDF versions of the presentations

## Generating PDFs

To generate PDF versions of the presentations, you'll need:

1. Node.js installed on your system
2. Marp CLI (will be installed automatically via npx)

### Steps to generate PDFs:

1. Open terminal in the `docs` directory
2. Make the script executable (if not already):
   ```bash
   chmod +x generate-pdf.sh
   ```
3. Run the script:
   ```bash
   ./generate-pdf.sh
   ```

The script will generate:
- `presentation.pdf` (English version)
- `presentation-zh.pdf` (Chinese version)

### About the Presentations

The presentations are created using [Marp](https://marp.app/), a markdown presentation ecosystem. They use the Gaia theme and include:
- Responsive layouts
- Custom styling
- Embedded screenshots
- Bilingual versions (English and Chinese)

### Customizing the Presentations

To modify the presentations:
1. Edit the markdown files (`presentation.md` or `presentation-zh.md`)
2. Run `./generate-pdf.sh` to update the PDFs
3. Preview changes in your markdown editor with Marp preview support
