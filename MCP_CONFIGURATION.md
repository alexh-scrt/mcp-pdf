# MCP-PDF Configuration Guide

## Claude Desktop Configuration

To use the MCP-PDF server with Claude Desktop, add the following configuration to your Claude Desktop config file:

### macOS
Edit: `~/Library/Application Support/Claude/claude_desktop_config.json`

### Windows
Edit: `%APPDATA%\Claude\claude_desktop_config.json`

### Configuration

```json
{
  "mcpServers": {
    "mcp-pdf": {
      "command": "python",
      "args": [
        "/Users/ki11erc0der/Workspace/mcp-pdf/run_server.py"
      ],
      "env": {
        "MCP_PDF_DEBUG": "0",
        "OUTPUT_DIR": "/Users/ki11erc0der/Workspace/mcp-pdf/output"
      }
    }
  }
}
```

**Note**: Replace `/Users/ki11erc0der/Workspace/mcp-pdf` with the actual path to your mcp-pdf installation.

## Using Python Virtual Environment

If you're using a Python virtual environment, use the python executable from that environment:

```json
{
  "mcpServers": {
    "mcp-pdf": {
      "command": "/path/to/venv/bin/python",
      "args": [
        "/path/to/mcp-pdf/run_server.py"
      ],
      "env": {
        "OUTPUT_DIR": "/path/to/output"
      }
    }
  }
}
```

## Environment Variables

- `MCP_PDF_DEBUG`: Set to `1`, `true`, or `yes` to enable debug logging
- `OUTPUT_DIR`: Directory where generated PDFs will be saved (default: `~/pdf-output`)

## Testing the Server

After configuring Claude Desktop, restart the application. Then you can test the server by asking Claude to generate a PDF:

```
Can you generate a PDF with a title page, table of contents, and a few content pages about Python programming?
```

## Example Usage in Claude Desktop

Here's what you can ask Claude to do:

1. **Simple PDF**:
   ```
   Create a PDF document titled "Quick Start Guide" with:
   - A title page
   - A content page explaining the basics
   - A summary page with key points
   ```

2. **Technical Documentation**:
   ```
   Generate a PDF for API documentation with:
   - Title page: "REST API Documentation"
   - TOC with sections
   - Content pages for each endpoint
   - Code examples
   - References
   ```

3. **Report**:
   ```
   Create a professional report PDF about cloud computing with:
   - Title page with author and date
   - Executive summary
   - Multiple sections with content
   - Diagrams (if you have image paths)
   - Conclusion and references
   ```

## Troubleshooting

### Server Not Connecting
1. Check that the path to `run_server.py` is correct
2. Verify Python is in your PATH or use the full path to Python
3. Check the Claude Desktop logs for error messages

### PDFs Not Generating
1. Verify the `OUTPUT_DIR` exists and is writable
2. Check server logs by setting `MCP_PDF_DEBUG=1`
3. Ensure all dependencies are installed: `pip install -r requirements.txt`

### Permission Errors
Ensure the output directory has write permissions:
```bash
mkdir -p ~/pdf-output
chmod 755 ~/pdf-output
```

## Server Capabilities

The MCP-PDF server provides one main tool:

### `generate_pdf`

Generates a themed PDF document with various page types.

**Supported Page Types:**
- `title`: Title page with metadata
- `toc`: Table of contents
- `section`: Section divider pages
- `content`: Rich content pages (text, bullets, tables, images, code)
- `code`: Dedicated code pages with syntax highlighting
- `diagram`: Diagram pages with descriptions
- `image`: Image pages with captions
- `summary`: Summary pages with key points
- `references`: Reference/bibliography pages

**Theme Options:**
- Default Secret AI theme (red/cyan professional theme)
- Custom colors (primary, secondary, accent, background, text)
- Custom fonts (heading, body, code)
- Custom typography settings (font sizes, spacing)
- Custom page settings (dimensions, margins)

## Advanced Configuration

### Using with uv (Python Package Manager)

```json
{
  "mcpServers": {
    "mcp-pdf": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/mcp-pdf",
        "run",
        "run_server.py"
      ]
    }
  }
}
```

### Using with Conda Environment

```json
{
  "mcpServers": {
    "mcp-pdf": {
      "command": "/Users/yourusername/miniconda/envs/mcp-pdf/bin/python",
      "args": [
        "/path/to/mcp-pdf/run_server.py"
      ]
    }
  }
}
```

## Output

Generated PDFs are saved to the configured `OUTPUT_DIR` with:
- Auto-generated filename if not specified (e.g., `document_title_20241102_121530.pdf`)
- Custom filename if provided in the document specification

The server returns the full path to the generated PDF file.
