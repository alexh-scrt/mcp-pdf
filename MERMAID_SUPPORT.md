# Mermaid Diagram Support

## ✅ IMPLEMENTED: Mermaid Diagrams in PDFs

The MCP-PDF server now supports **Mermaid diagrams**! When Claude Desktop sends Mermaid code, the server automatically converts it to a PNG image and embeds it in the PDF.

## Overview

- **Page Type**: `mermaid`
- **Conversion Tool**: `mmdc` (mermaid-cli via npx)
- **Output Format**: PNG with transparent background
- **Supported Diagrams**: All Mermaid diagram types (flowchart, sequence, class, gantt, etc.)

## How It Works

### 1. Claude Desktop Sends Mermaid Code

When a user provides Mermaid code, Claude Desktop calls the `generate_pdf` tool with:

```json
{
  "page_type": "mermaid",
  "title": "System Sequence Diagram",
  "mermaid_code": "sequenceDiagram\n    Client->>Server: Request\n    Server-->>Client: Response",
  "description": ["Optional description bullets"]
}
```

### 2. Server Converts to Image

The server:
1. Writes the Mermaid code to a temporary `.mmd` file
2. Calls `npx -p @mermaid-js/mermaid-cli mmdc -i input.mmd -o output.png -b transparent`
3. Waits for conversion (max 30 seconds)
4. Embeds the PNG image in the PDF
5. Cleans up temporary files

### 3. Result: Rendered Diagram in PDF

The PDF contains the **rendered Mermaid diagram** as a high-quality PNG image, not as text code.

## Supported Mermaid Diagram Types

All Mermaid diagram types are supported:

- **Flowcharts**: `flowchart TD`, `flowchart LR`
- **Sequence Diagrams**: `sequenceDiagram`
- **Class Diagrams**: `classDiagram`
- **State Diagrams**: `stateDiagram-v2`
- **Entity Relationship**: `erDiagram`
- **Gantt Charts**: `gantt`
- **Pie Charts**: `pie`
- **Git Graphs**: `gitGraph`
- **And more...**

## Usage Examples

### Example 1: Simple Sequence Diagram

```json
{
  "page_type": "mermaid",
  "title": "API Request Flow",
  "mermaid_code": "sequenceDiagram\n    Client->>Server: GET /users\n    Server-->>Client: 200 OK"
}
```

### Example 2: Flowchart with Description

```json
{
  "page_type": "mermaid",
  "title": "User Authentication Flow",
  "mermaid_code": "flowchart TD\n    Start[Start] --> Login[Login Page]\n    Login --> Auth{Valid?}\n    Auth -->|Yes| Dashboard[Dashboard]\n    Auth -->|No| Error[Error Page]",
  "description": [
    "Shows the authentication decision flow",
    "Redirects to dashboard on success",
    "Shows error page on failure"
  ]
}
```

### Example 3: Class Diagram

```json
{
  "page_type": "mermaid",
  "title": "Data Model",
  "mermaid_code": "classDiagram\n    class User {\n        +String name\n        +String email\n        +login()\n    }\n    class Post {\n        +String title\n        +String content\n    }\n    User \"1\" --> \"*\" Post : creates",
  "caption": "Blog platform data model"
}
```

### Example 4: Gantt Chart

```json
{
  "page_type": "mermaid",
  "title": "Project Timeline",
  "mermaid_code": "gantt\n    title Project Schedule\n    dateFormat YYYY-MM-DD\n    section Phase 1\n    Requirements :done, 2024-01-01, 2024-01-15\n    Design :active, 2024-01-16, 2024-02-01\n    section Phase 2\n    Implementation :2024-02-02, 2024-03-15"
}
```

## Full Example: API Documentation

Here's a complete example showing how Claude Desktop would create a PDF with a Mermaid diagram:

```json
{
  "document_spec": {
    "title": "API Documentation",
    "theme": {},
    "pages": [
      {
        "page_type": "title",
        "title": "API Documentation",
        "subtitle": "HTTP Request/Response Examples"
      },
      {
        "page_type": "mermaid",
        "title": "API Sequence Diagram",
        "mermaid_code": "sequenceDiagram\n    participant Client\n    participant Server\n    participant Database\n    \n    Client->>Server: HTTP GET /api/users/123\n    activate Server\n    Server->>Database: Query user by ID\n    activate Database\n    Database-->>Server: Return user data\n    deactivate Database\n    Server-->>Client: HTTP 200 OK (JSON response)\n    deactivate Server",
        "description": [
          "Shows Client-Server-Database interactions",
          "Includes activation boxes",
          "Displays response codes"
        ]
      },
      {
        "page_type": "code",
        "title": "Mermaid Source Code",
        "code": "sequenceDiagram...",
        "language": "mermaid",
        "line_numbers": true
      }
    ],
    "output": {
      "filename": "api_docs.pdf",
      "directory": "./output"
    }
  }
}
```

## Requirements

### Server-Side

The `@mermaid-js/mermaid-cli` package must be available:

```bash
# Test if mmdc is available
npx -p @mermaid-js/mermaid-cli mmdc --version

# If needed, install globally (optional)
npm install -g @mermaid-js/mermaid-cli
```

The server uses `npx` to run `mmdc`, so no global installation is required. The package will be downloaded automatically on first use.

### Dependencies

- Node.js and npm (for npx)
- `@mermaid-js/mermaid-cli` (installed automatically via npx)
- Chromium/Puppeteer (bundled with mermaid-cli)

## Claude Desktop Instructions

When using the MCP-PDF server in Claude Desktop, you can now say:

> **User:** "Create a PDF with this Mermaid sequence diagram: [paste Mermaid code]"

> **Claude:** I'll create a PDF with that Mermaid diagram rendered as an image.
>
> *[Calls generate_pdf tool with page_type="mermaid"]*
>
> ✅ I've created your PDF! The Mermaid diagram has been converted to an image and embedded in the document.

## Implementation Details

### Code References

- **Model**: `src/mcp_pdf/models/document_spec.py:25` (PageType.MERMAID)
- **Rendering**: `src/mcp_pdf/rendering/pdf_generator.py:492-562` (_render_mermaid_to_png)
- **Page Handler**: `src/mcp_pdf/rendering/pdf_generator.py:451-478` (_add_mermaid_page)
- **Server Schema**: `src/mcp_pdf/server.py:199` (includes mermaid in enum)

### Conversion Process

```python
def _render_mermaid_to_png(self, mermaid_code: str) -> Optional[str]:
    """
    1. Write Mermaid code to temporary .mmd file
    2. Call: npx -p @mermaid-js/mermaid-cli mmdc -i input.mmd -o output.png -b transparent
    3. Return path to generated PNG
    4. Track file for cleanup
    """
```

### Error Handling

If Mermaid conversion fails:
- PDF generation continues
- Error message is displayed in place of diagram: "[Failed to render Mermaid diagram]"
- Error is logged with details
- User is informed to check mmdc installation

## Testing

Run the test suite:

```bash
# Test Mermaid functionality
python tests/test_mermaid.py

# Test with user's exact example
python test_user_example.py
```

### Test Results

```
✅ test_mermaid_sequence_diagram - PASSED (output/mermaid_test.pdf, 36KB)
✅ test_multiple_mermaid_diagrams - PASSED (output/multiple_mermaid_test.pdf, 53KB)
✅ test_mermaid_with_code_page - PASSED (output/mermaid_with_code_test.pdf, 37KB)
✅ test_user_example - PASSED (output/api_documentation.pdf, 84KB)
```

## Before and After

### ❌ Before (Problem)

When Claude Desktop sent Mermaid code, it appeared as **plain text code** in the PDF:

```
sequenceDiagram
    Client->>Server: Request
    Server-->>Client: Response
```

### ✅ After (Solution)

Now the Mermaid code is **converted to a rendered diagram image**:

![Rendered Sequence Diagram]

The diagram appears as a professional, high-quality image in the PDF.

## Benefits

1. **Automatic Conversion**: No manual steps required
2. **All Diagram Types**: Supports all Mermaid syntax
3. **High Quality**: PNG output with transparent background
4. **Error Handling**: Graceful failure if mmdc unavailable
5. **Easy Integration**: Works seamlessly with existing page types
6. **Claude Desktop Ready**: Fully compatible with MCP protocol

## Troubleshooting

### mmdc Not Found

If you see errors about mmdc not being found:

```bash
# Verify npx works
npx -p @mermaid-js/mermaid-cli mmdc --version

# If that fails, check Node.js installation
node --version
npm --version
```

### Conversion Timeout

If diagrams are very complex and timeout:
- Simplify the diagram
- Check server logs for details
- Verify system resources (memory, CPU)

### Image Not Appearing

If the PDF generates but image is missing:
- Check server logs for mmdc errors
- Verify Mermaid syntax is valid
- Test with simple diagram first

## Future Enhancements

Possible future improvements:

- [ ] Support for Mermaid themes (dark, forest, etc.)
- [ ] Custom background colors
- [ ] Size/scale customization
- [ ] SVG output option
- [ ] Batch conversion optimization

## Conclusion

The MCP-PDF server now fully supports Mermaid diagrams! Users can provide Mermaid code through Claude Desktop, and the server automatically converts it to high-quality images in the generated PDFs.

**Status**: ✅ Fully Implemented and Tested
