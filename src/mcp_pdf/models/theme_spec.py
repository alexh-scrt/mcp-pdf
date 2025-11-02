"""Theme specification models for PDF documents."""

from typing import Optional
from pydantic import BaseModel, Field


class ColorPalette(BaseModel):
    """Color palette for PDF theme."""

    primary: str = Field("#E3342F", description="Primary color (hex)")
    secondary: str = Field("#1CCBD0", description="Secondary color (hex)")
    accent: str = Field("#F59E0B", description="Accent color (hex)")
    background: str = Field("#FFFFFF", description="Background color (hex)")
    text: str = Field("#111827", description="Text color (hex)")
    code_bg: str = Field("#F5F5F5", description="Code background color (hex)")


class FontPalette(BaseModel):
    """Font palette for PDF theme."""

    heading: str = Field("Helvetica-Bold", description="Heading font")
    body: str = Field("Helvetica", description="Body font")
    code: str = Field("Courier", description="Code font")


class ThemeSpec(BaseModel):
    """Theme specification for PDF documents."""

    colors: ColorPalette = Field(default_factory=ColorPalette, description="Color palette")
    fonts: FontPalette = Field(default_factory=FontPalette, description="Font palette")
    logo_path: Optional[str] = Field(None, description="Path to logo image")

    # Typography settings
    title_font_size: int = Field(24, description="Title font size")
    subtitle_font_size: int = Field(16, description="Subtitle font size")
    h1_font_size: int = Field(18, description="H1 heading font size")
    h2_font_size: int = Field(14, description="H2 heading font size")
    h3_font_size: int = Field(12, description="H3 heading font size")
    body_font_size: int = Field(10, description="Body text font size")
    code_font_size: int = Field(9, description="Code font size")

    # Spacing settings
    line_spacing: float = Field(1.2, description="Line spacing multiplier")
    paragraph_spacing: float = Field(6, description="Space after paragraphs (points)")

    # Page settings
    page_width: float = Field(612, description="Page width in points (letter: 612)")
    page_height: float = Field(792, description="Page height in points (letter: 792)")
    margin_top: float = Field(72, description="Top margin in points")
    margin_bottom: float = Field(72, description="Bottom margin in points")
    margin_left: float = Field(72, description="Left margin in points")
    margin_right: float = Field(72, description="Right margin in points")
