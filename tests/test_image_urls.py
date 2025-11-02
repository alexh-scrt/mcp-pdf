#!/usr/bin/env python3
"""Test image URL downloading functionality."""

from mcp_pdf.models.document_spec import DocumentSpec, PageSpec, PageType
from mcp_pdf.models.theme_spec import ThemeSpec
from mcp_pdf.rendering.pdf_generator import PDFGenerator


def test_diagram_page_with_image_url():
    """Test diagram page with image URL (using 'image' field shorthand)."""

    # Use a simple test image URL
    test_image_url = "https://via.placeholder.com/800x600.png?text=Test+Diagram"

    doc_spec = DocumentSpec(
        title="Image URL Test",
        theme=ThemeSpec(),
        pages=[
            PageSpec(
                page_type=PageType.TITLE,
                title="Image URL Test",
                subtitle="Testing Image Download from URLs"
            ),
            PageSpec(
                page_type=PageType.DIAGRAM,
                title="Test Diagram with URL",
                image=test_image_url,  # Using 'image' shorthand
                description=["This diagram was downloaded from a URL"]
            )
        ],
        output={
            "filename": "image_url_test.pdf",
            "directory": "./output"
        }
    )

    # Generate PDF
    generator = PDFGenerator()
    result = generator.generate_pdf(doc_spec)

    print(f"\n✅ PDF Generation with Image URL:")
    print(f"   OK: {result['ok']}")
    print(f"   Output: {result['output']}")
    print(f"   Pages: {result['pages_generated']}")

    assert result['ok'] is True, "PDF generation should succeed"
    assert result['pages_generated'] == 2, "Should generate 2 pages"

    print(f"✅ Successfully generated PDF with image downloaded from URL")


def test_image_field_mapping():
    """Test that 'image' field is correctly mapped to diagram_url."""

    page_data = {
        "page_type": "diagram",
        "title": "Test",
        "image": "https://example.com/diagram.png"
    }

    page = PageSpec(**page_data)

    # Verify it was mapped to diagram_url
    assert page.diagram_url == "https://example.com/diagram.png"
    assert page.diagram_path is None
    print("✅ 'image' field correctly mapped to diagram_url")


def test_image_field_local_path():
    """Test that 'image' field works with local paths too."""

    page_data = {
        "page_type": "diagram",
        "title": "Test",
        "image": "/local/path/to/image.png"
    }

    page = PageSpec(**page_data)

    # Verify it was mapped to diagram_path (not URL)
    assert page.diagram_path == "/local/path/to/image.png"
    assert page.diagram_url is None
    print("✅ 'image' field correctly mapped to diagram_path for local files")


if __name__ == "__main__":
    print("=" * 70)
    print("Testing Image URL Functionality")
    print("=" * 70)

    print("\n📝 Test 1: 'image' Field Mapping (URL)")
    print("-" * 70)
    test_image_field_mapping()

    print("\n📝 Test 2: 'image' Field Mapping (Local Path)")
    print("-" * 70)
    test_image_field_local_path()

    print("\n📝 Test 3: Diagram Page with Image URL Download")
    print("-" * 70)
    test_diagram_page_with_image_url()

    print("\n" + "=" * 70)
    print("✅ All image URL tests passed!")
    print("=" * 70)
