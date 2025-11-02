# MCP-PDF Project Summary

## Overview

MCP-PDF is a Model Context Protocol (MCP) server that enables AI assistants like Claude to generate professional, themed PDF documents with various page types. It follows the same architectural pattern as the mcp-pptx project but focuses on PDF generation using the ReportLab library.

## Project Structure

```
mcp-pdf/
├── src/
│   └── mcp_pdf/
│       ├── __init__.py              # Package initialization
│       ├── __main__.py              # Entry point for python -m mcp_pdf
│       ├── server.py                # MCP server implementation
│       ├── models/
│       │   ├── __init__.py
│       │   ├── theme_spec.py        # Theme color/font/typography models
│       │   └── document_spec.py     # Document and page specification models
│       └── rendering/
│           ├── __init__.py
│           └── pdf_generator.py     # Core PDF generation logic
├── output/                          # Generated PDFs
├── run_server.py                    # Server entry point
├── test_example.py                  # Standalone test script
├── pyproject.toml                   # Python project configuration
├── requirements.txt                 # Python dependencies
├── README.md                        # Main documentation
├── MCP_CONFIGURATION.md             # Claude Desktop setup guide
├── USAGE_EXAMPLES.md                # Comprehensive usage examples
├── PROJECT_SUMMARY.md               # This file
├── .env                             # Environment configuration
└── .gitignore                       # Git ignore patterns
```

## Key Features

### 1. Nine Page Types

- **Title Page**: Document cover with title, subtitle, author, date, and additional info
- **Table of Contents (TOC)**: Structured navigation with entries
- **Section Page**: Section dividers with title and subtitle
- **Content Page**: Rich content with text, bullets, tables, images, and code
- **Code Page**: Dedicated code blocks with syntax highlighting and optional line numbers
- **Diagram Page**: Technical diagrams with captions and description bullets
- **Image Page**: Images with captions and descriptions
- **Summary Page**: Key points and conclusions
- **References Page**: Citations and bibliography (numbered, bulleted, or plain)

### 2. Theme Customization

**Default Secret AI Theme:**
- Primary: #E3342F (Red)
- Secondary: #1CCBD0 (Cyan)
- Accent: #F59E0B (Orange)
- Background: #FFFFFF (White)
- Text: #111827 (Dark Gray)
- Code Background: #F5F5F5 (Light Gray)

**Customizable Elements:**
- Color palette (primary, secondary, accent, background, text, code_bg)
- Font families (heading, body, code)
- Font sizes (title, subtitle, h1, h2, h3, body, code)
- Spacing (line spacing, paragraph spacing)
- Page settings (dimensions, margins)

### 3. Rich Content Support

- Plain text paragraphs
- Bulleted lists
- Code blocks with syntax highlighting
- Tables with headers
- Images (local paths)
- Multiple content types per page

## Architecture

The project follows a clean, modular architecture:

### Models Layer (`models/`)
- **theme_spec.py**: Defines theme configuration (ColorPalette, FontPalette, ThemeSpec)
- **document_spec.py**: Defines document structure (PageSpec, ContentItem, DocumentSpec)
- Uses Pydantic for data validation and type safety

### Rendering Layer (`rendering/`)
- **pdf_generator.py**: Core PDF generation logic using ReportLab
- Implements all page type generators
- Handles theme application and styling
- Manages the PDF story building process

### Server Layer (`server.py`)
- Implements MCP protocol handlers
- Exposes `generate_pdf` tool
- Handles request/response serialization
- Provides comprehensive error handling
- Supports debug logging

## Technologies Used

- **Python 3.9+**: Core language
- **MCP SDK**: Model Context Protocol implementation
- **Pydantic**: Data validation and settings management
- **ReportLab**: PDF generation library
- **Pillow**: Image processing
- **python-dotenv**: Environment configuration

## MCP Tool: generate_pdf

The server exposes a single, comprehensive tool that handles all PDF generation:

### Input Schema

```typescript
{
  document_spec: {
    title: string,
    theme?: ThemeSpec,  // Optional, uses default if not provided
    pages: PageSpec[],  // Array of page specifications
    output?: {
      filename?: string,
      directory?: string
    }
  }
}
```

### Output

```json
{
  "ok": true,
  "output": "/path/to/generated.pdf",
  "pages_generated": 9,
  "filename": "document.pdf"
}
```

## Comparison with mcp-pptx

| Feature | mcp-pptx | mcp-pdf |
|---------|----------|---------|
| Output Format | PowerPoint (.pptx) | PDF (.pdf) |
| Library | python-pptx | reportlab |
| Theme Extraction | Web scraping with Playwright | Manual theme specification |
| Primary Use Case | Presentations | Documents, reports, manuals |
| Page Types | Slides | Document pages |
| Tools | 5 (scrape, list, validate, generate, merge) | 1 (generate) |
| Complexity | Higher (web scraping, assets) | Lower (direct generation) |

## Usage Scenarios

1. **Technical Documentation**
   - API documentation with code examples
   - User manuals with diagrams
   - Architecture documents

2. **Business Reports**
   - Sales reports with executive summaries
   - Quarterly business reviews
   - Project status reports

3. **Academic Papers**
   - Research papers with references
   - Course materials with examples
   - Study guides

4. **Training Materials**
   - Tutorial documents with code
   - Workshop materials
   - Learning resources

## Testing

The project includes a comprehensive test example (`test_example.py`) that demonstrates:
- All 9 page types
- Theme usage (default Secret AI theme)
- Various content types
- Code with line numbers
- Proper document structure

### Running the Test

```bash
python test_example.py
```

This generates a complete PDF demonstrating all features.

## Configuration

### Environment Variables

- `MCP_PDF_DEBUG`: Enable debug logging (0/1, false/true, no/yes)
- `OUTPUT_DIR`: Directory for generated PDFs (default: ~/pdf-output)

### Claude Desktop Integration

Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "mcp-pdf": {
      "command": "python",
      "args": ["/path/to/mcp-pdf/run_server.py"],
      "env": {
        "OUTPUT_DIR": "/path/to/output"
      }
    }
  }
}
```

## Development Status

### ✅ Completed

- [x] Project structure and configuration
- [x] Data models (theme, document, pages)
- [x] PDF generator with all page types
- [x] MCP server implementation with all required handlers
- [x] Default Secret AI theme
- [x] Theme customization support
- [x] Rich content support (text, bullets, code, tables)
- [x] Code syntax highlighting
- [x] Comprehensive documentation
- [x] Test suite with pytest (11 unit tests, all passing)
- [x] Integration test for PDF generation
- [x] Configuration guides
- [x] Added `list_prompts` and `list_resources` handlers
- [x] Proper tests/ folder structure

### 🚀 Potential Enhancements

- [ ] Image URL support (download and embed)
- [ ] More font options (embed custom fonts)
- [ ] Chart generation support
- [ ] Header/footer customization
- [ ] Page numbering options
- [ ] Watermark support
- [ ] PDF encryption/password protection
- [ ] Batch PDF generation
- [ ] Template system
- [ ] Web theme extraction (like mcp-pptx)

## Performance

- Fast PDF generation (< 1 second for typical documents)
- Efficient memory usage
- Handles documents with dozens of pages
- Minimal dependencies

## Security Considerations

- No external network requests (unlike mcp-pptx web scraping)
- Local file system access only
- No code execution from user input
- Pydantic validation for all inputs
- Safe path handling for output files

## License

MIT License - Free to use, modify, and distribute

## Acknowledgments

- Based on architectural patterns from mcp-pptx
- Uses ReportLab for PDF generation
- Follows MCP specification from Anthropic
- Default theme inspired by Secret AI branding

## Getting Started

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Test the server:**
   ```bash
   python test_example.py
   ```

3. **Configure Claude Desktop:**
   - Edit `claude_desktop_config.json`
   - Add mcp-pdf server configuration
   - Restart Claude Desktop

4. **Generate PDFs:**
   - Ask Claude to create documents
   - Specify page types and content
   - Customize themes as needed

## Support

For issues, questions, or contributions:
- Review README.md for basic usage
- Check USAGE_EXAMPLES.md for detailed examples
- See MCP_CONFIGURATION.md for setup help
- Test with test_example.py to verify installation

## Version

Current Version: 0.1.0
Last Updated: November 2, 2024
