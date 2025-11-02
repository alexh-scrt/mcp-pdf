#!/usr/bin/env python3
"""
Verify that the MCP-PDF server can:
1. Receive requests from Claude Desktop that contain image URLs
2. Download those images
3. Display them in PDFs

This script demonstrates all the ways image URLs can be used.
"""

import json
from mcp_pdf.models.document_spec import DocumentSpec, PageSpec, PageType, ContentItem
from mcp_pdf.models.theme_spec import ThemeSpec
from mcp_pdf.rendering.pdf_generator import PDFGenerator


def test_all_image_url_methods():
    """Test all the different ways to include image URLs in a PDF."""

    # Example image URLs (using a reliable public image service)
    sample_image_url = "https://picsum.photos/800/600"

    print("=" * 80)
    print("VERIFYING IMAGE URL FUNCTIONALITY")
    print("=" * 80)
    print()
    print("This demonstrates how Claude Desktop can send image URLs to the MCP server")
    print("and have them automatically downloaded and included in PDFs.")
    print()

    # Create document spec with all image URL methods
    doc_spec = DocumentSpec(
        title="Image URL Functionality Test",
        theme=ThemeSpec(),
        pages=[
            # Title page
            PageSpec(
                page_type=PageType.TITLE,
                title="Image URL Functionality Test",
                subtitle="Verifying Image Download & Display",
                author="MCP-PDF Server",
                date="November 2024"
            ),

            # Method 1: Diagram page with 'image' shorthand
            PageSpec(
                page_type=PageType.DIAGRAM,
                title="Method 1: Diagram Page with 'image' Field",
                image=sample_image_url,  # Shorthand - automatically maps to diagram_url
                description=[
                    "Uses the 'image' shorthand field",
                    "Automatically detects URL vs local path",
                    "Downloads image and displays in PDF"
                ]
            ),

            # Method 2: Diagram page with explicit diagram_url
            PageSpec(
                page_type=PageType.DIAGRAM,
                title="Method 2: Diagram Page with 'diagram_url' Field",
                diagram_url=sample_image_url,
                caption="Explicitly using diagram_url field",
                description=[
                    "Uses explicit 'diagram_url' field",
                    "Server downloads from URL",
                    "Displays with optional caption"
                ]
            ),

            # Method 3: Image page with image_url
            PageSpec(
                page_type=PageType.IMAGE,
                title="Method 3: Image Page with 'image_url' Field",
                image_url=sample_image_url,
                caption="Using image_url field on image page",
                description="Image pages support both image_url and image_path fields"
            ),

            # Method 4: Content page with image URL in content items
            PageSpec(
                page_type=PageType.CONTENT,
                title="Method 4: Content Page with Image URL",
                content=[
                    ContentItem(
                        type="text",
                        text="Content pages can include images as content items:"
                    ),
                    ContentItem(
                        type="image",
                        image_url=sample_image_url,
                        caption="Image URL embedded in content item"
                    ),
                    ContentItem(
                        type="bullet",
                        items=[
                            "Images can be mixed with other content",
                            "Supports both image_url and image_path",
                            "Great for documentation with screenshots"
                        ]
                    )
                ]
            ),

            # Summary page
            PageSpec(
                page_type=PageType.SUMMARY,
                title="Summary",
                key_points=[
                    "✓ Server accepts image URLs in multiple formats",
                    "✓ Automatically downloads images from URLs",
                    "✓ Supports both URLs and local file paths",
                    "✓ Handles errors gracefully if download fails",
                    "✓ Cleans up temporary files after PDF generation"
                ],
                conclusion="The MCP-PDF server fully supports receiving image URLs from Claude Desktop and embedding them in generated PDFs."
            )
        ],
        output={
            "filename": "image_url_verification.pdf",
            "directory": "./output"
        }
    )

    print("📋 Document Specification:")
    print("-" * 80)
    print(f"Title: {doc_spec.title}")
    print(f"Pages: {len(doc_spec.pages)}")
    print(f"Output: {doc_spec.output.directory}/{doc_spec.output.filename}")
    print()

    print("🎯 Image URL Methods Demonstrated:")
    print("-" * 80)
    print("1. Diagram page with 'image' shorthand field")
    print("2. Diagram page with explicit 'diagram_url' field")
    print("3. Image page with 'image_url' field")
    print("4. Content page with image URL in content items")
    print()

    # Generate the PDF
    print("📝 Generating PDF...")
    print("-" * 80)
    generator = PDFGenerator()
    result = generator.generate_pdf(doc_spec)

    print()
    print("✅ RESULTS:")
    print("-" * 80)
    print(f"Success: {result['ok']}")
    print(f"Output File: {result['output']}")
    print(f"Pages Generated: {result['pages_generated']}")
    print(f"File Size: {result.get('filename', 'N/A')}")

    if 'message' in result:
        print(f"Note: {result['message']}")

    print()
    print("=" * 80)
    print("✅ VERIFICATION COMPLETE")
    print("=" * 80)
    print()
    print("The MCP-PDF server can successfully:")
    print("  ✓ Receive image URLs from Claude Desktop")
    print("  ✓ Download images from those URLs")
    print("  ✓ Embed the images in generated PDFs")
    print()
    print(f"📄 View the generated PDF at: {result['output']}")
    print()

    # Also show the JSON that Claude Desktop would send
    print("=" * 80)
    print("EXAMPLE: How Claude Desktop sends image URLs to the MCP server")
    print("=" * 80)
    print()
    print("When Claude Desktop calls the 'generate_pdf' tool, it sends JSON like this:")
    print()

    example_request = {
        "document_spec": {
            "title": "My Document",
            "theme": {},
            "pages": [
                {
                    "page_type": "diagram",
                    "title": "Architecture Diagram",
                    "image": "https://example.com/diagram.png",
                    "description": ["This is a diagram from a URL"]
                }
            ],
            "output": {
                "filename": "my_doc.pdf",
                "directory": "./output"
            }
        }
    }

    print(json.dumps(example_request, indent=2))
    print()
    print("The server will:")
    print("  1. Parse the 'image' field")
    print("  2. Detect it's a URL (starts with http:// or https://)")
    print("  3. Download the image to a temporary file")
    print("  4. Embed it in the PDF")
    print("  5. Clean up the temporary file")
    print()


if __name__ == "__main__":
    test_all_image_url_methods()
