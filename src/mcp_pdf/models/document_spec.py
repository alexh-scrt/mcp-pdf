"""Document specification models for PDF generation."""

import os
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, Field, model_validator

from .theme_spec import ThemeSpec

# Default output directory
DEFAULT_OUTPUT_DIR = os.getenv('OUTPUT_DIR', str(Path.home() / 'pdf-output'))


class PageType(str, Enum):
    """Available page types."""

    TITLE = "title"
    TOC = "toc"
    SECTION = "section"
    CONTENT = "content"
    CODE = "code"
    DIAGRAM = "diagram"
    IMAGE = "image"
    MERMAID = "mermaid"
    SUMMARY = "summary"
    REFERENCES = "references"


class ContentItem(BaseModel):
    """Content item for a page."""

    type: str = Field("text", description="Content type: text, bullet, image, code, table")
    text: Optional[str] = Field(None, description="Text content")
    items: Optional[List[str]] = Field(None, description="List items for bullets")
    code: Optional[str] = Field(None, description="Code content")
    language: Optional[str] = Field(None, description="Programming language for code")
    image_path: Optional[str] = Field(None, description="Path to image file")
    image_url: Optional[str] = Field(None, description="URL to image")
    caption: Optional[str] = Field(None, description="Image caption")
    table_data: Optional[List[List[str]]] = Field(None, description="Table data (rows x columns)")
    table_headers: Optional[List[str]] = Field(None, description="Table headers")


class TitlePageSpec(BaseModel):
    """Title page specification."""

    title: str = Field(..., description="Document title")
    subtitle: Optional[str] = Field(None, description="Document subtitle")
    author: Optional[str] = Field(None, description="Document author")
    date: Optional[str] = Field(None, description="Document date")
    additional_info: Optional[str] = Field(None, description="Additional information")


class TOCPageSpec(BaseModel):
    """Table of Contents page specification."""

    title: str = Field("Table of Contents", description="TOC title")
    entries: List[str] = Field(..., description="TOC entries")


class SectionPageSpec(BaseModel):
    """Section divider page specification."""

    title: str = Field(..., description="Section title")
    subtitle: Optional[str] = Field(None, description="Section subtitle")


class ContentPageSpec(BaseModel):
    """Content page specification."""

    title: str = Field(..., description="Page title")
    content: List[ContentItem] = Field(..., description="Page content items")


class CodePageSpec(BaseModel):
    """Code page specification."""

    title: str = Field(..., description="Page title")
    code: str = Field(..., description="Code content")
    language: Optional[str] = Field("python", description="Programming language")
    line_numbers: bool = Field(False, description="Show line numbers")


class DiagramPageSpec(BaseModel):
    """Diagram page specification."""

    title: str = Field(..., description="Page title")
    diagram_path: Optional[str] = Field(None, description="Path to diagram image")
    diagram_url: Optional[str] = Field(None, description="URL to diagram image")
    caption: Optional[str] = Field(None, description="Diagram caption")
    description: Optional[List[str]] = Field(None, description="Diagram description bullets")


class ImagePageSpec(BaseModel):
    """Image page specification."""

    title: str = Field(..., description="Page title")
    image_path: Optional[str] = Field(None, description="Path to image file")
    image_url: Optional[str] = Field(None, description="URL to image")
    caption: Optional[str] = Field(None, description="Image caption")
    description: Optional[str] = Field(None, description="Image description")


class SummaryPageSpec(BaseModel):
    """Summary page specification."""

    title: str = Field("Summary", description="Summary page title")
    key_points: List[str] = Field(..., description="Key summary points")
    conclusion: Optional[str] = Field(None, description="Concluding remarks")


class ReferencesPageSpec(BaseModel):
    """References page specification."""

    title: str = Field("References", description="References page title")
    references: List[str] = Field(..., description="List of references")
    style: str = Field("numbered", description="Reference style: numbered, bulleted, plain")


class PageSpec(BaseModel):
    """Generic page specification."""

    page_type: PageType = Field(..., description="Type of page")

    # Title page fields
    title: Optional[str] = Field(None, description="Page/Document title")
    subtitle: Optional[str] = Field(None, description="Subtitle")
    author: Optional[str] = Field(None, description="Author (for title page)")
    date: Optional[str] = Field(None, description="Date (for title page)")
    additional_info: Optional[str] = Field(None, description="Additional info (for title page)")

    # TOC fields
    entries: Optional[List[str]] = Field(None, description="TOC entries")

    # Content fields
    content: Optional[List[ContentItem]] = Field(None, description="Content items")

    # Code fields
    code: Optional[str] = Field(None, description="Code content")
    language: Optional[str] = Field(None, description="Programming language")
    line_numbers: bool = Field(False, description="Show line numbers")

    # Image/Diagram fields
    image_path: Optional[str] = Field(None, description="Path to image file")
    image_url: Optional[str] = Field(None, description="URL to image")
    diagram_path: Optional[str] = Field(None, description="Path to diagram image")
    diagram_url: Optional[str] = Field(None, description="URL to diagram image")
    caption: Optional[str] = Field(None, description="Image/Diagram caption")
    description: Optional[Union[str, List[str]]] = Field(None, description="Description")

    # Mermaid diagram fields
    mermaid_code: Optional[str] = Field(None, description="Mermaid diagram code")

    # Summary fields
    key_points: Optional[List[str]] = Field(None, description="Key summary points")
    conclusion: Optional[str] = Field(None, description="Conclusion")

    # References fields
    references: Optional[List[str]] = Field(None, description="List of references")
    style: str = Field("numbered", description="Reference style")

    @model_validator(mode='before')
    @classmethod
    def handle_image_field(cls, values: Any) -> Any:
        """Handle 'image' field as shorthand for image_url/image_path/diagram_url/diagram_path."""
        if isinstance(values, dict) and 'image' in values:
            image_value = values.pop('image')
            page_type = values.get('page_type')

            # Determine if it's a URL or local path
            is_url = isinstance(image_value, str) and image_value.startswith(('http://', 'https://'))

            # Map 'image' to the appropriate field based on page_type
            if page_type == 'diagram' or page_type == PageType.DIAGRAM:
                if is_url:
                    values['diagram_url'] = image_value
                else:
                    values['diagram_path'] = image_value
            else:
                # For image page type or generic image
                if is_url:
                    values['image_url'] = image_value
                else:
                    values['image_path'] = image_value

        return values


class OutputSpec(BaseModel):
    """Output specification."""

    filename: Optional[str] = Field(None, description="Output filename (auto-generated if not provided)")
    directory: str = Field(default_factory=lambda: DEFAULT_OUTPUT_DIR, description="Output directory")


class DocumentSpec(BaseModel):
    """Complete PDF document specification."""

    title: str = Field(..., description="Document title")
    theme: ThemeSpec = Field(default_factory=ThemeSpec, description="Theme specification")
    pages: List[PageSpec] = Field(..., min_length=1, description="Page specifications")
    output: OutputSpec = Field(default_factory=OutputSpec, description="Output specification")
