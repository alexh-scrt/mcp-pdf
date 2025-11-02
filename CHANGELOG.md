# Changelog

All notable changes to the mcp-pdf project will be documented in this file.

## [0.1.1] - 2024-11-02

### Fixed
- **Smart Directory Fallback**: PDF generator now intelligently handles inaccessible output directories
  - Checks if requested directory exists and is writable
  - Automatically falls back to OUTPUT_DIR if requested directory is not accessible
  - Creates fallback directory if it doesn't exist
  - Returns clear message to user indicating where file was actually saved
  - Prevents errors when Claude suggests paths like `/mnt/user-data/outputs` that don't exist on the system

### Added
- Test suite for directory fallback mechanism (`test_directory_fallback.py`)
- Comprehensive OUTPUT_DIRECTORY.md documentation explaining fallback behavior

## [0.1.0] - 2024-11-02

### Added
- Initial release of MCP-PDF server
- Support for 9 page types: Title, TOC, Section, Content, Code, Diagram, Image, Summary, References
- Default Secret AI theme (red/cyan color scheme)
- Full theme customization support (colors, fonts, typography, spacing)
- Rich content support (text, bullets, tables, images, code blocks)
- Code syntax highlighting with optional line numbers
- MCP protocol implementation with `generate_pdf` tool
- Handlers for `list_prompts` and `list_resources` (return empty lists)
- Comprehensive documentation (README, usage examples, configuration guide)
- Test suite with pytest (11 unit tests)
- Example PDF generation test demonstrating all features

### Fixed
- Added missing `list_prompts()` and `list_resources()` handlers to prevent "Method not found" errors in Claude Desktop logs
- Organized tests in proper `tests/` folder structure
- Added pytest configuration in `conftest.py`

### Project Structure
```
mcp-pdf/
├── src/mcp_pdf/          # Main package
│   ├── models/           # Data models (theme, document specs)
│   ├── rendering/        # PDF generation logic
│   └── server.py         # MCP server implementation
├── tests/                # Test suite
│   ├── conftest.py       # Pytest configuration
│   ├── test_models.py    # Unit tests for data models
│   └── test_pdf_generation.py  # Integration test
├── output/               # Generated PDFs
├── run_server.py         # Server entry point
├── requirements.txt      # Dependencies
└── Documentation files
```

### Dependencies
- Python 3.9+
- mcp >= 1.0.0
- pydantic >= 2.0.0
- reportlab >= 4.0.0
- pillow >= 10.0.0
- python-dotenv >= 1.0.0
- pytest >= 7.0.0 (dev)
- pytest-asyncio >= 0.21.0 (dev)

### Testing
- 11 unit tests covering all data models
- Integration test generating a 9-page sample PDF
- All tests passing ✅

### Known Limitations
- Image URLs not yet supported (only local paths)
- No custom font embedding
- No chart generation
- No PDF encryption/password protection

### Future Enhancements
- Image URL downloading and embedding
- Chart generation support
- Custom font embedding
- Header/footer customization
- PDF encryption
- Template system
- Batch PDF generation
