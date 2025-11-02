# MCP-PDF

MCP server for generating themed PDF documents with various page types.

## Features

- **Multiple Page Types**: Title, Table of Contents, Section, Content, Code, Diagram, Image, **Mermaid**, Summary, References
- **Mermaid Diagram Support**: Automatically converts Mermaid code to PNG images using mmdc
- **Theme Customization**: Customize colors, fonts, typography, and spacing
- **Default Secret AI Theme**: Professional red/cyan color scheme
- **Rich Content**: Support for text, bullets, images, tables, and code blocks
- **Syntax Highlighting**: Code pages with optional line numbers
- **Image URL Support**: Download and embed images from URLs
- **Smart Directory Fallback**: Automatically uses configured fallback directory when requested path is not accessible

## Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Or install in development mode
pip install -e .
```

## Usage

### Running the Server

```bash
python run_server.py
```

### Generating PDFs

The server exposes a `generate_pdf` tool that accepts a document specification:

```json
{
  "document_spec": {
    "title": "My Technical Report",
    "theme": {},
    "pages": [
      {
        "page_type": "title",
        "title": "Technical Report",
        "subtitle": "A Comprehensive Guide",
        "author": "John Doe",
        "date": "November 2024"
      },
      {
        "page_type": "content",
        "title": "Introduction",
        "content": [
          {"type": "text", "text": "This document..."},
          {"type": "bullet", "items": ["Point 1", "Point 2"]}
        ]
      }
    ],
    "output": {
      "filename": "report.pdf",
      "directory": "./output"
    }
  }
}
```

## Page Types

### 1. Title Page
- **Fields**: title, subtitle, author, date, additional_info
- **Use**: Document cover page

### 2. Table of Contents (TOC)
- **Fields**: title, entries (list)
- **Use**: Document navigation

### 3. Section Page
- **Fields**: title, subtitle
- **Use**: Section dividers

### 4. Content Page
- **Fields**: title, content (list of items)
- **Content Types**: text, bullet, image, code, table
- **Use**: Main content pages

### 5. Code Page
- **Fields**: title, code, language, line_numbers
- **Use**: Code examples with syntax highlighting

### 6. Diagram Page
- **Fields**: title, diagram_path/diagram_url, caption, description
- **Use**: Technical diagrams with explanations

### 7. Image Page
- **Fields**: title, image_path/image_url, caption, description
- **Use**: Images with captions

### 8. Mermaid Diagram Page
- **Fields**: title, mermaid_code, caption, description
- **Use**: Mermaid diagrams automatically converted to PNG images
- **Requirements**: Node.js and npm (mmdc installed via npx)

### 9. Summary Page
- **Fields**: title, key_points (list), conclusion
- **Use**: Key takeaways and conclusions

### 10. References Page
- **Fields**: title, references (list), style (numbered/bulleted/plain)
- **Use**: Citations and references

## Theme Customization

```json
{
  "theme": {
    "colors": {
      "primary": "#E3342F",
      "secondary": "#1CCBD0",
      "accent": "#F59E0B",
      "background": "#FFFFFF",
      "text": "#111827",
      "code_bg": "#F5F5F5"
    },
    "fonts": {
      "heading": "Helvetica-Bold",
      "body": "Helvetica",
      "code": "Courier"
    },
    "title_font_size": 24,
    "h1_font_size": 18,
    "body_font_size": 10,
    "code_font_size": 9
  }
}
```

## Development

### Project Structure

```
mcp-pdf/
├── src/
│   └── mcp_pdf/
│       ├── __init__.py
│       ├── __main__.py
│       ├── server.py           # MCP server implementation
│       ├── models/
│       │   ├── __init__.py
│       │   ├── theme_spec.py   # Theme models
│       │   └── document_spec.py # Document models
│       └── rendering/
│           ├── __init__.py
│           └── pdf_generator.py # PDF generation logic
├── run_server.py               # Server entry point
├── pyproject.toml
├── requirements.txt
└── README.md
```

### Running Tests

```bash
# Run all tests with pytest
pytest tests/ -v

# Run specific test file
pytest tests/test_models.py -v

# Run the example PDF generation test
python tests/test_pdf_generation.py
```

## License

MIT License
