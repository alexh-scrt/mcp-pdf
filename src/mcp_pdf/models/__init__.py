"""Models for MCP-PDF."""

from .theme_spec import ThemeSpec, ColorPalette, FontPalette
from .document_spec import (
    DocumentSpec,
    PageSpec,
    PageType,
    ContentItem,
    TitlePageSpec,
    TOCPageSpec,
    SectionPageSpec,
    ContentPageSpec,
    CodePageSpec,
    ImagePageSpec,
    SummaryPageSpec,
    ReferencesPageSpec,
)

__all__ = [
    "ThemeSpec",
    "ColorPalette",
    "FontPalette",
    "DocumentSpec",
    "PageSpec",
    "PageType",
    "ContentItem",
    "TitlePageSpec",
    "TOCPageSpec",
    "SectionPageSpec",
    "ContentPageSpec",
    "CodePageSpec",
    "ImagePageSpec",
    "SummaryPageSpec",
    "ReferencesPageSpec",
]
