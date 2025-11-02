#!/usr/bin/env python3
"""Test example for MCP-PDF server."""

from mcp_pdf.models.document_spec import DocumentSpec, PageSpec, PageType, ContentItem
from mcp_pdf.models.theme_spec import ThemeSpec
from mcp_pdf.rendering.pdf_generator import PDFGenerator


def create_test_document():
    """Create a test PDF document."""

    doc_spec = DocumentSpec(
        title="MCP-PDF Test Document",
        theme=ThemeSpec(),  # Use default Secret AI theme
        pages=[
            # Title page
            PageSpec(
                page_type=PageType.TITLE,
                title="MCP-PDF Test Document",
                subtitle="A Comprehensive Test of PDF Generation",
                author="MCP-PDF Server",
                date="November 2024",
                additional_info="Version 1.0.0 | Test Build"
            ),

            # Table of Contents
            PageSpec(
                page_type=PageType.TOC,
                title="Table of Contents",
                entries=[
                    "1. Introduction",
                    "2. Features Overview",
                    "3. Page Types",
                    "4. Code Examples",
                    "5. Summary",
                    "6. References"
                ]
            ),

            # Section page
            PageSpec(
                page_type=PageType.SECTION,
                title="Introduction",
                subtitle="Getting Started with MCP-PDF"
            ),

            # Content page
            PageSpec(
                page_type=PageType.CONTENT,
                title="Features Overview",
                content=[
                    ContentItem(
                        type="text",
                        text="MCP-PDF is a powerful server for generating themed PDF documents. It supports various page types and rich content formatting."
                    ),
                    ContentItem(
                        type="bullet",
                        items=[
                            "Multiple page types (Title, TOC, Section, Content, Code, etc.)",
                            "Customizable themes with colors and fonts",
                            "Support for text, bullets, images, tables, and code",
                            "Professional default Secret AI theme",
                            "Easy integration with MCP clients"
                        ]
                    )
                ]
            ),

            # Another section
            PageSpec(
                page_type=PageType.SECTION,
                title="Page Types",
                subtitle="Comprehensive Page Type Support"
            ),

            # Content page with more details
            PageSpec(
                page_type=PageType.CONTENT,
                title="Available Page Types",
                content=[
                    ContentItem(
                        type="text",
                        text="MCP-PDF supports the following page types:"
                    ),
                    ContentItem(
                        type="bullet",
                        items=[
                            "Title: Document cover page with title, subtitle, author",
                            "TOC: Table of contents with entries",
                            "Section: Section divider pages",
                            "Content: Main content with rich formatting",
                            "Code: Code blocks with syntax highlighting",
                            "Diagram: Technical diagrams with descriptions",
                            "Image: Image pages with captions",
                            "Summary: Key points and conclusions",
                            "References: Citations and bibliography"
                        ]
                    )
                ]
            ),

            # Code page
            PageSpec(
                page_type=PageType.CODE,
                title="Python Example",
                code='''def generate_pdf(document_spec):
    """Generate a PDF from document specification."""
    generator = PDFGenerator()
    result = generator.generate_pdf(document_spec)
    return result

# Example usage
spec = DocumentSpec(
    title="My Document",
    theme=ThemeSpec(),
    pages=[...]
)
result = generate_pdf(spec)
print(f"PDF generated: {result['output']}")''',
                language="python",
                line_numbers=True
            ),

            # Summary page
            PageSpec(
                page_type=PageType.SUMMARY,
                title="Summary",
                key_points=[
                    "MCP-PDF provides a comprehensive PDF generation solution",
                    "Supports 9 different page types for various content needs",
                    "Highly customizable with theme support",
                    "Easy to integrate with MCP ecosystem",
                    "Professional output with Secret AI default theme"
                ],
                conclusion="MCP-PDF is the ideal solution for generating professional, themed PDF documents through the Model Context Protocol."
            ),

            # References page
            PageSpec(
                page_type=PageType.REFERENCES,
                title="References",
                references=[
                    "Model Context Protocol - https://github.com/anthropics/mcp",
                    "ReportLab - https://www.reportlab.com/",
                    "Pydantic - https://docs.pydantic.dev/",
                    "Python Pillow - https://python-pillow.org/"
                ],
                style="numbered"
            )
        ],
        output={
            "filename": "mcp_pdf_test.pdf",
            "directory": "./output"
        }
    )

    return doc_spec


def main():
    """Main test function."""
    print("Creating test document specification...")
    doc_spec = create_test_document()

    print(f"Generating PDF with {len(doc_spec.pages)} pages...")
    generator = PDFGenerator()
    result = generator.generate_pdf(doc_spec)

    print(f"\nPDF Generation Complete!")
    print(f"Output: {result['output']}")
    print(f"Pages Generated: {result['pages_generated']}")
    print(f"Filename: {result['filename']}")


if __name__ == "__main__":
    main()
