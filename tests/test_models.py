"""Tests for MCP-PDF data models."""

import pytest
from pydantic import ValidationError

from mcp_pdf.models.theme_spec import ThemeSpec, ColorPalette, FontPalette
from mcp_pdf.models.document_spec import (
    DocumentSpec,
    PageSpec,
    PageType,
    ContentItem,
)


class TestThemeSpec:
    """Tests for theme specification models."""

    def test_default_theme(self):
        """Test default theme values."""
        theme = ThemeSpec()

        assert theme.colors.primary == "#E3342F"
        assert theme.colors.secondary == "#1CCBD0"
        assert theme.colors.accent == "#F59E0B"
        assert theme.fonts.heading == "Helvetica-Bold"
        assert theme.fonts.body == "Helvetica"
        assert theme.title_font_size == 24

    def test_custom_theme(self):
        """Test custom theme values."""
        theme = ThemeSpec(
            colors=ColorPalette(
                primary="#FF0000",
                secondary="#00FF00"
            ),
            fonts=FontPalette(
                heading="Times-Bold"
            ),
            title_font_size=28
        )

        assert theme.colors.primary == "#FF0000"
        assert theme.colors.secondary == "#00FF00"
        assert theme.fonts.heading == "Times-Bold"
        assert theme.title_font_size == 28


class TestPageSpec:
    """Tests for page specification models."""

    def test_title_page(self):
        """Test title page specification."""
        page = PageSpec(
            page_type=PageType.TITLE,
            title="Test Document",
            subtitle="A Test",
            author="Test Author"
        )

        assert page.page_type == PageType.TITLE
        assert page.title == "Test Document"
        assert page.subtitle == "A Test"
        assert page.author == "Test Author"

    def test_content_page(self):
        """Test content page specification."""
        page = PageSpec(
            page_type=PageType.CONTENT,
            title="Content Page",
            content=[
                ContentItem(type="text", text="Hello world"),
                ContentItem(type="bullet", items=["Item 1", "Item 2"])
            ]
        )

        assert page.page_type == PageType.CONTENT
        assert len(page.content) == 2
        assert page.content[0].text == "Hello world"
        assert page.content[1].items == ["Item 1", "Item 2"]

    def test_code_page(self):
        """Test code page specification."""
        page = PageSpec(
            page_type=PageType.CODE,
            title="Code Example",
            code="print('Hello')",
            language="python",
            line_numbers=True
        )

        assert page.page_type == PageType.CODE
        assert page.code == "print('Hello')"
        assert page.language == "python"
        assert page.line_numbers is True


class TestDocumentSpec:
    """Tests for document specification models."""

    def test_minimal_document(self):
        """Test minimal valid document."""
        doc = DocumentSpec(
            title="Test Doc",
            pages=[
                PageSpec(
                    page_type=PageType.TITLE,
                    title="Test"
                )
            ]
        )

        assert doc.title == "Test Doc"
        assert len(doc.pages) == 1
        assert doc.theme is not None  # Should have default theme

    def test_document_requires_pages(self):
        """Test that document requires at least one page."""
        with pytest.raises(ValidationError):
            DocumentSpec(
                title="Test Doc",
                pages=[]
            )

    def test_complete_document(self):
        """Test complete document with all features."""
        doc = DocumentSpec(
            title="Complete Document",
            theme=ThemeSpec(),
            pages=[
                PageSpec(page_type=PageType.TITLE, title="Title"),
                PageSpec(page_type=PageType.TOC, entries=["Section 1"]),
                PageSpec(page_type=PageType.SECTION, title="Section"),
                PageSpec(
                    page_type=PageType.CONTENT,
                    title="Content",
                    content=[ContentItem(type="text", text="Text")]
                ),
                PageSpec(
                    page_type=PageType.CODE,
                    title="Code",
                    code="print('hi')",
                    language="python"
                ),
                PageSpec(
                    page_type=PageType.SUMMARY,
                    key_points=["Point 1", "Point 2"]
                ),
                PageSpec(
                    page_type=PageType.REFERENCES,
                    references=["Ref 1"]
                )
            ],
            output={
                "filename": "test.pdf",
                "directory": "./output"
            }
        )

        assert doc.title == "Complete Document"
        assert len(doc.pages) == 7
        assert doc.output.filename == "test.pdf"


class TestContentItem:
    """Tests for content item models."""

    def test_text_content(self):
        """Test text content item."""
        item = ContentItem(type="text", text="Hello")
        assert item.type == "text"
        assert item.text == "Hello"

    def test_bullet_content(self):
        """Test bullet list content item."""
        item = ContentItem(type="bullet", items=["A", "B", "C"])
        assert item.type == "bullet"
        assert item.items == ["A", "B", "C"]

    def test_code_content(self):
        """Test code content item."""
        item = ContentItem(
            type="code",
            code="x = 1",
            language="python"
        )
        assert item.type == "code"
        assert item.code == "x = 1"
        assert item.language == "python"
