#!/usr/bin/env python3
"""Test directory fallback mechanism."""

import os
from pathlib import Path

from mcp_pdf.models.document_spec import DocumentSpec, PageSpec, PageType
from mcp_pdf.models.theme_spec import ThemeSpec
from mcp_pdf.rendering.pdf_generator import PDFGenerator


def test_inaccessible_directory_fallback():
    """Test that PDF generation falls back when directory is not accessible."""

    # Set a valid fallback directory
    os.environ['OUTPUT_DIR'] = './output'

    # Create a document spec with an inaccessible directory
    doc_spec = DocumentSpec(
        title="Fallback Test",
        theme=ThemeSpec(),
        pages=[
            PageSpec(
                page_type=PageType.TITLE,
                title="Test Document",
                subtitle="Testing Directory Fallback"
            )
        ],
        output={
            "filename": "fallback_test.pdf",
            "directory": "/mnt/user-data/outputs"  # This directory doesn't exist
        }
    )

    # Generate PDF
    generator = PDFGenerator()
    result = generator.generate_pdf(doc_spec)

    print(f"\n✅ PDF Generation Result:")
    print(f"   OK: {result['ok']}")
    print(f"   Output: {result['output']}")
    print(f"   Pages: {result['pages_generated']}")
    print(f"   Filename: {result['filename']}")

    # Check if we got a message about the fallback
    if 'message' in result:
        print(f"   ⚠️  Message: {result['message']}")

    # Verify the file was created
    output_path = Path(result['output'])
    assert output_path.exists(), f"PDF file not created at {output_path}"
    print(f"\n✅ PDF file created successfully at: {output_path}")

    # Verify it's in the fallback directory (not /mnt/user-data/outputs)
    assert "/mnt/user-data/outputs" not in str(output_path), "PDF should not be in inaccessible directory"
    print(f"✅ Correctly used fallback directory instead of inaccessible /mnt/user-data/outputs")

    # Clean up
    output_path.unlink()


def test_valid_directory():
    """Test that PDF generation uses the requested directory when it's accessible."""

    doc_spec = DocumentSpec(
        title="Valid Directory Test",
        theme=ThemeSpec(),
        pages=[
            PageSpec(
                page_type=PageType.TITLE,
                title="Test Document",
                subtitle="Testing Valid Directory"
            )
        ],
        output={
            "filename": "valid_dir_test.pdf",
            "directory": "./output"  # This directory should be accessible
        }
    )

    # Generate PDF
    generator = PDFGenerator()
    result = generator.generate_pdf(doc_spec)

    print(f"\n✅ PDF Generation Result (Valid Directory):")
    print(f"   OK: {result['ok']}")
    print(f"   Output: {result['output']}")

    # Should NOT have a message field (no fallback needed)
    assert 'message' not in result, "Should not have fallback message for valid directory"
    print(f"✅ Used requested directory without fallback")

    # Verify the file was created in the requested location
    output_path = Path(result['output'])
    assert output_path.exists(), f"PDF file not created at {output_path}"
    assert "output" in str(output_path), "PDF should be in requested ./output directory"
    print(f"✅ PDF correctly saved to requested directory: {output_path}")

    # Clean up
    output_path.unlink()


if __name__ == "__main__":
    print("=" * 70)
    print("Testing Directory Fallback Mechanism")
    print("=" * 70)

    print("\n📝 Test 1: Inaccessible Directory Fallback")
    print("-" * 70)
    test_inaccessible_directory_fallback()

    print("\n📝 Test 2: Valid Directory (No Fallback)")
    print("-" * 70)
    test_valid_directory()

    print("\n" + "=" * 70)
    print("✅ All tests passed!")
    print("=" * 70)
