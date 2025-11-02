"""MCP-PDF Server implementation."""

import asyncio
import json
import logging
import os
import sys
from typing import Any, Dict, Optional

from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.types import ServerCapabilities
from mcp.types import (
    CallToolResult,
    ListToolsResult,
    ListPromptsResult,
    ListResourcesResult,
    Tool,
    TextContent,
)

from .models.document_spec import DocumentSpec
from .rendering.pdf_generator import PDFGenerator

logger = logging.getLogger(__name__)


class MCPPDFServer:
    """MCP server for PDF document generation."""

    def __init__(self) -> None:
        logger.info("Initializing MCP-PDF Server...")
        self.server = Server("mcp-pdf")
        logger.info("Created MCP server instance")

        self.pdf_generator = PDFGenerator()
        logger.info("Initialized PDFGenerator")

        self._setup_handlers()
        logger.info("MCP-PDF Server initialization complete")

    def _setup_handlers(self) -> None:
        """Set up MCP server handlers."""
        logger.info("Setting up MCP server handlers...")

        @self.server.list_tools()
        async def handle_list_tools() -> ListToolsResult:
            """List available tools."""
            logger.info("Received list_tools request")
            tools_result = ListToolsResult(
                tools=[
                    Tool(
                        name="generate_pdf",
                        description="""Generate a themed PDF document with various page types.

SUPPORTED PAGE TYPES:
- title: Title page with title, subtitle, author, date, and additional info
- toc: Table of Contents page with entries
- section: Section divider page with title and optional subtitle
- content: Content page with title and various content items (text, bullets, images, tables, code)
- code: Code page with syntax highlighting and optional line numbers
- diagram: Diagram page with image and optional description bullets
- image: Image page with caption and description
- mermaid: Mermaid diagram page - converts Mermaid code to image and displays in PDF
- summary: Summary page with key points and conclusion
- references: References page with list of references (numbered, bulleted, or plain)

THEME CUSTOMIZATION:
The theme object allows you to customize:
- colors: primary, secondary, accent, background, text, code_bg (all hex colors)
- fonts: heading, body, code (font names like Helvetica-Bold, Courier)
- Typography: title_font_size, subtitle_font_size, h1/h2/h3_font_size, body_font_size, code_font_size
- Spacing: line_spacing, paragraph_spacing
- Page settings: page dimensions and margins

DEFAULT THEME (Secret AI style):
- Primary color: #E3342F (red)
- Secondary color: #1CCBD0 (cyan)
- Accent color: #F59E0B (orange)
- Background: #FFFFFF (white)
- Text: #111827 (dark gray)

CONTENT ITEMS (for content pages):
- text: Plain text paragraphs
- bullet: Bulleted list items
- image: Images with optional captions
- code: Code blocks with syntax highlighting
- table: Tables with headers and data

EXAMPLE USAGE:
{
  "document_spec": {
    "title": "My Technical Report",
    "theme": {},  // Uses default Secret AI theme
    "pages": [
      {
        "page_type": "title",
        "title": "Technical Report",
        "subtitle": "A Comprehensive Guide",
        "author": "John Doe",
        "date": "November 2024"
      },
      {
        "page_type": "toc",
        "title": "Table of Contents",
        "entries": ["1. Introduction", "2. Architecture", "3. Implementation"]
      },
      {
        "page_type": "section",
        "title": "Introduction",
        "subtitle": "Overview and Background"
      },
      {
        "page_type": "content",
        "title": "System Architecture",
        "content": [
          {"type": "text", "text": "The system consists of..."},
          {"type": "bullet", "items": ["Component A", "Component B", "Component C"]}
        ]
      },
      {
        "page_type": "code",
        "title": "Example Implementation",
        "code": "def hello():\\n    print('Hello World')",
        "language": "python",
        "line_numbers": true
      },
      {
        "page_type": "mermaid",
        "title": "System Sequence Diagram",
        "mermaid_code": "sequenceDiagram\\n    Client->>Server: Request\\n    Server-->>Client: Response",
        "description": ["Mermaid diagrams are automatically converted to images"]
      },
      {
        "page_type": "summary",
        "title": "Key Takeaways",
        "key_points": ["Point 1", "Point 2", "Point 3"],
        "conclusion": "In conclusion..."
      },
      {
        "page_type": "references",
        "title": "References",
        "references": ["Reference 1", "Reference 2"],
        "style": "numbered"
      }
    ],
    "output": {
      "filename": "technical_report.pdf",
      "directory": "/path/to/output"
    }
  }
}

OUTPUT:
Returns a JSON object with:
- ok: true/false
- output: Full path to generated PDF
- pages_generated: Number of pages created
- filename: Output filename
""",
                        inputSchema={
                            "type": "object",
                            "properties": {
                                "document_spec": {
                                    "type": "object",
                                    "description": "Complete PDF document specification",
                                    "properties": {
                                        "title": {
                                            "type": "string",
                                            "description": "Document title"
                                        },
                                        "theme": {
                                            "type": "object",
                                            "description": "Theme specification (colors, fonts, sizes). Leave empty {} for default Secret AI theme.",
                                            "properties": {
                                                "colors": {
                                                    "type": "object",
                                                    "properties": {
                                                        "primary": {"type": "string"},
                                                        "secondary": {"type": "string"},
                                                        "accent": {"type": "string"},
                                                        "background": {"type": "string"},
                                                        "text": {"type": "string"},
                                                        "code_bg": {"type": "string"}
                                                    }
                                                },
                                                "fonts": {
                                                    "type": "object",
                                                    "properties": {
                                                        "heading": {"type": "string"},
                                                        "body": {"type": "string"},
                                                        "code": {"type": "string"}
                                                    }
                                                }
                                            }
                                        },
                                        "pages": {
                                            "type": "array",
                                            "description": "Array of page specifications",
                                            "items": {
                                                "type": "object",
                                                "properties": {
                                                    "page_type": {
                                                        "type": "string",
                                                        "enum": ["title", "toc", "section", "content", "code", "diagram", "image", "mermaid", "summary", "references"],
                                                        "description": "Type of page"
                                                    },
                                                    "title": {"type": "string"},
                                                    "subtitle": {"type": "string"},
                                                    "author": {"type": "string"},
                                                    "date": {"type": "string"},
                                                    "entries": {
                                                        "type": "array",
                                                        "items": {"type": "string"}
                                                    },
                                                    "content": {
                                                        "type": "array",
                                                        "items": {"type": "object"}
                                                    },
                                                    "code": {"type": "string"},
                                                    "language": {"type": "string"},
                                                    "line_numbers": {"type": "boolean"},
                                                    "mermaid_code": {"type": "string"},
                                                    "key_points": {
                                                        "type": "array",
                                                        "items": {"type": "string"}
                                                    },
                                                    "conclusion": {"type": "string"},
                                                    "references": {
                                                        "type": "array",
                                                        "items": {"type": "string"}
                                                    },
                                                    "style": {"type": "string"}
                                                },
                                                "required": ["page_type"]
                                            }
                                        },
                                        "output": {
                                            "type": "object",
                                            "properties": {
                                                "filename": {"type": "string"},
                                                "directory": {"type": "string"}
                                            }
                                        }
                                    },
                                    "required": ["title", "pages"]
                                }
                            },
                            "required": ["document_spec"]
                        }
                    ),
                ]
            )
            logger.info(f"Returning {len(tools_result.tools)} available tools")
            return tools_result

        @self.server.list_prompts()
        async def handle_list_prompts() -> ListPromptsResult:
            """List available prompts (none for this server)."""
            logger.info("Received list_prompts request")
            return ListPromptsResult(prompts=[])

        @self.server.list_resources()
        async def handle_list_resources() -> ListResourcesResult:
            """List available resources (none for this server)."""
            logger.info("Received list_resources request")
            return ListResourcesResult(resources=[])

        @self.server.call_tool()
        async def handle_call_tool(
            name: str, arguments: Optional[Dict[str, Any]]
        ) -> CallToolResult:
            """Handle tool calls."""
            logger.info(f"Received tool call: {name}")
            logger.debug(f"Tool arguments: {arguments}")
            try:
                if name == "generate_pdf":
                    logger.info("Executing generate_pdf tool")
                    result = await self._generate_pdf(arguments or {})
                    logger.info("generate_pdf tool completed successfully")
                    return result
                else:
                    logger.error(f"Unknown tool requested: {name}")
                    raise ValueError(f"Unknown tool: {name}")
            except Exception as e:
                logger.exception(f"Error calling tool {name}")
                return CallToolResult(
                    content=[
                        TextContent(
                            type="text",
                            text=json.dumps({
                                "ok": False,
                                "error": str(e),
                                "tool": name
                            })
                        )
                    ]
                )

    async def _generate_pdf(self, arguments: Dict[str, Any]) -> CallToolResult:
        """Generate PDF document."""
        doc_spec_data = arguments["document_spec"]

        logger.info("Starting PDF document generation")
        logger.debug(f"Doc spec data keys: {list(doc_spec_data.keys()) if isinstance(doc_spec_data, dict) else 'Not a dict'}")

        try:
            doc_spec = DocumentSpec.model_validate(doc_spec_data)
            logger.info(f"Starting generation of PDF with {len(doc_spec.pages)} pages")
            result = self.pdf_generator.generate_pdf(doc_spec)
            logger.info(f"PDF generation completed successfully. Output: {result.get('output', 'Unknown')}")

            return CallToolResult(
                content=[
                    TextContent(
                        type="text",
                        text=json.dumps(result, indent=2)
                    )
                ]
            )
        except Exception as e:
            logger.error(f"PDF generation failed: {str(e)}")
            return CallToolResult(
                content=[
                    TextContent(
                        type="text",
                        text=json.dumps({
                            "ok": False,
                            "error": str(e),
                            "output": None,
                            "pages_generated": 0,
                        }, indent=2)
                    )
                ]
            )

    async def run(self) -> None:
        """Run the MCP server."""
        from mcp.server.stdio import stdio_server

        logger.info("Starting MCP-PDF server...")

        try:
            async with stdio_server() as (read_stream, write_stream):
                logger.info("STDIO server started, beginning MCP communication")
                await self.server.run(
                    read_stream,
                    write_stream,
                    InitializationOptions(
                        server_name="mcp-pdf",
                        server_version="0.1.1",
                        capabilities=ServerCapabilities(
                            tools={}
                        )
                    )
                )
                logger.info("MCP server finished running")
        except BaseException as e:
            # Handle both regular exceptions and ExceptionGroups
            if isinstance(e, BaseExceptionGroup):
                # Check if all exceptions are BrokenPipeError or ConnectionError
                is_disconnect = all(
                    isinstance(exc, (BrokenPipeError, ConnectionError))
                    for exc in e.exceptions
                )
                if is_disconnect:
                    logger.debug("Client disconnected during shutdown")
                    return
            elif isinstance(e, (BrokenPipeError, ConnectionError)):
                # Single BrokenPipeError or ConnectionError
                logger.debug("Client disconnected")
                return
            # Re-raise if it's not a disconnect error
            raise


def suppress_broken_pipe_errors() -> None:
    """Suppress BrokenPipeError during stdout/stderr cleanup."""
    if sys.stdout is not None:
        try:
            original_flush = sys.stdout.flush
            def safe_flush():
                try:
                    original_flush()
                except (BrokenPipeError, OSError):
                    pass
            sys.stdout.flush = safe_flush
        except AttributeError:
            pass

    if sys.stderr is not None:
        try:
            original_flush = sys.stderr.flush
            def safe_flush():
                try:
                    original_flush()
                except (BrokenPipeError, OSError):
                    pass
            sys.stderr.flush = safe_flush
        except AttributeError:
            pass


async def main() -> None:
    """Main entry point."""
    suppress_broken_pipe_errors()

    log_level = logging.DEBUG if os.getenv('MCP_PDF_DEBUG', '').lower() in ('1', 'true', 'yes') else logging.INFO

    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    if log_level == logging.DEBUG:
        logger.info("=== MCP-PDF Server Starting (DEBUG MODE) ===")
        logger.debug("Debug logging enabled via MCP_PDF_DEBUG environment variable")
    else:
        logger.info("=== MCP-PDF Server Starting ===")
        logger.info("Set MCP_PDF_DEBUG=1 for debug logging")

    try:
        server = MCPPDFServer()
        await server.run()
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except BaseException as e:
        if isinstance(e, BaseExceptionGroup):
            is_disconnect = all(
                isinstance(exc, (BrokenPipeError, ConnectionError))
                for exc in e.exceptions
            )
            if is_disconnect:
                logger.debug("Client disconnected during shutdown")
            else:
                logger.exception(f"Server failed with error: {e}")
                raise
        elif isinstance(e, (BrokenPipeError, ConnectionError)):
            logger.debug("Client disconnected")
        elif isinstance(e, KeyboardInterrupt):
            pass
        else:
            logger.exception(f"Server failed with error: {e}")
            raise
    finally:
        logger.info("=== MCP-PDF Server Shutdown ===")


if __name__ == "__main__":
    asyncio.run(main())
