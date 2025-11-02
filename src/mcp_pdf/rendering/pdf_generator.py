"""PDF generator using reportlab."""

import os
import logging
import tempfile
import urllib.request
import subprocess
from pathlib import Path
from typing import List, Optional
from datetime import datetime
from urllib.parse import urlparse

from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    PageBreak,
    Table,
    TableStyle,
    Image,
    Preformatted,
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib import colors
from reportlab.lib.colors import HexColor

from ..models.document_spec import DocumentSpec, PageSpec, PageType, ContentItem
from ..models.theme_spec import ThemeSpec

logger = logging.getLogger(__name__)


class PDFGenerator:
    """Generates PDF documents with themed pages."""

    def __init__(self):
        """Initialize the PDF generator."""
        self.story = []
        self.theme = None
        self.styles = {}
        self.downloaded_images = []  # Track downloaded images for cleanup

    def generate_pdf(self, doc_spec: DocumentSpec) -> dict:
        """
        Generate a PDF document from a document specification.

        Args:
            doc_spec: Document specification

        Returns:
            Dictionary with generation results
        """
        logger.info(f"Starting PDF generation for: {doc_spec.title}")

        # Setup theme
        self.theme = doc_spec.theme
        self._setup_styles()

        # Setup output - handle directory validation and fallback
        requested_dir = Path(doc_spec.output.directory)
        output_dir = None
        directory_message = None

        # Try to use the requested directory
        try:
            # Check if directory exists or can be created
            if not requested_dir.exists():
                requested_dir.mkdir(parents=True, exist_ok=True)
                logger.info(f"Created output directory: {requested_dir}")

            # Test if directory is writable
            test_file = requested_dir / ".write_test"
            test_file.touch()
            test_file.unlink()

            output_dir = requested_dir
            logger.info(f"Using requested output directory: {output_dir}")

        except (OSError, PermissionError) as e:
            # Directory doesn't exist, can't be created, or isn't writable
            logger.warning(f"Cannot use requested directory {requested_dir}: {e}")

            # Fall back to OUTPUT_DIR from environment
            fallback_dir = Path(os.getenv('OUTPUT_DIR', str(Path.home() / 'pdf-output')))
            logger.info(f"Falling back to configured output directory: {fallback_dir}")

            try:
                if not fallback_dir.exists():
                    fallback_dir.mkdir(parents=True, exist_ok=True)
                    logger.info(f"Created fallback output directory: {fallback_dir}")

                output_dir = fallback_dir
                directory_message = f"Note: Saved to {fallback_dir} (requested directory {requested_dir} was not accessible)"

            except (OSError, PermissionError) as e2:
                logger.error(f"Cannot use fallback directory {fallback_dir}: {e2}")
                raise RuntimeError(f"Cannot write to requested directory '{requested_dir}' or fallback directory '{fallback_dir}'. Please check permissions and configuration.") from e2

        # Generate filename
        if doc_spec.output.filename:
            filename = doc_spec.output.filename
        else:
            # Auto-generate filename from title
            safe_title = "".join(c if c.isalnum() or c in (' ', '-', '_') else '_' for c in doc_spec.title)
            safe_title = safe_title.replace(' ', '_').lower()
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{safe_title}_{timestamp}.pdf"

        output_path = output_dir / filename
        logger.info(f"Output path: {output_path}")

        # Create PDF document
        doc = SimpleDocTemplate(
            str(output_path),
            pagesize=(self.theme.page_width, self.theme.page_height),
            rightMargin=self.theme.margin_right,
            leftMargin=self.theme.margin_left,
            topMargin=self.theme.margin_top,
            bottomMargin=self.theme.margin_bottom,
        )

        # Reset story
        self.story = []

        # Generate pages
        pages_generated = 0
        for page in doc_spec.pages:
            try:
                self._generate_page(page)
                pages_generated += 1
            except Exception as e:
                logger.error(f"Error generating page {pages_generated + 1}: {e}")
                raise

        # Build PDF
        doc.build(self.story)
        logger.info(f"PDF generated successfully: {output_path}")

        # Clean up downloaded images
        self._cleanup_downloaded_images()

        result = {
            "ok": True,
            "output": str(output_path),
            "pages_generated": pages_generated,
            "filename": filename,
        }

        # Include directory message if we fell back to a different location
        if directory_message:
            result["message"] = directory_message
            logger.warning(directory_message)

        return result

    def _setup_styles(self):
        """Setup paragraph styles based on theme."""
        base_styles = getSampleStyleSheet()

        # Title style (for title pages)
        self.styles['title'] = ParagraphStyle(
            'Title',
            parent=base_styles['Heading1'],
            fontSize=self.theme.title_font_size,
            textColor=HexColor(self.theme.colors.primary),
            spaceAfter=self.theme.paragraph_spacing * 5,
            alignment=TA_CENTER,
            fontName=self.theme.fonts.heading,
        )

        # Subtitle style
        self.styles['subtitle'] = ParagraphStyle(
            'Subtitle',
            parent=base_styles['Heading2'],
            fontSize=self.theme.subtitle_font_size,
            textColor=HexColor(self.theme.colors.secondary),
            spaceAfter=self.theme.paragraph_spacing * 3,
            alignment=TA_CENTER,
            fontName=self.theme.fonts.body,
        )

        # H1 style
        self.styles['h1'] = ParagraphStyle(
            'H1',
            parent=base_styles['Heading1'],
            fontSize=self.theme.h1_font_size,
            textColor=HexColor(self.theme.colors.primary),
            spaceAfter=self.theme.paragraph_spacing * 2,
            spaceBefore=self.theme.paragraph_spacing * 2,
            fontName=self.theme.fonts.heading,
        )

        # H2 style
        self.styles['h2'] = ParagraphStyle(
            'H2',
            parent=base_styles['Heading2'],
            fontSize=self.theme.h2_font_size,
            textColor=HexColor(self.theme.colors.secondary),
            spaceAfter=self.theme.paragraph_spacing,
            spaceBefore=self.theme.paragraph_spacing,
            fontName=self.theme.fonts.heading,
        )

        # H3 style
        self.styles['h3'] = ParagraphStyle(
            'H3',
            parent=base_styles['Heading3'],
            fontSize=self.theme.h3_font_size,
            textColor=HexColor(self.theme.colors.text),
            spaceAfter=self.theme.paragraph_spacing * 0.8,
            spaceBefore=self.theme.paragraph_spacing * 0.8,
            fontName=self.theme.fonts.heading,
        )

        # Body style
        self.styles['body'] = ParagraphStyle(
            'Body',
            parent=base_styles['BodyText'],
            fontSize=self.theme.body_font_size,
            textColor=HexColor(self.theme.colors.text),
            alignment=TA_JUSTIFY,
            spaceAfter=self.theme.paragraph_spacing,
            fontName=self.theme.fonts.body,
        )

        # Bullet style
        self.styles['bullet'] = ParagraphStyle(
            'Bullet',
            parent=base_styles['BodyText'],
            fontSize=self.theme.body_font_size,
            textColor=HexColor(self.theme.colors.text),
            leftIndent=20,
            spaceAfter=self.theme.paragraph_spacing,
            fontName=self.theme.fonts.body,
        )

        # Code style
        self.styles['code'] = ParagraphStyle(
            'Code',
            parent=base_styles['Code'],
            fontSize=self.theme.code_font_size,
            textColor=HexColor(self.theme.colors.text),
            fontName=self.theme.fonts.code,
            leftIndent=10,
            rightIndent=10,
            spaceAfter=self.theme.paragraph_spacing,
        )

    def _generate_page(self, page: PageSpec):
        """Generate a page based on its type."""
        if page.page_type == PageType.TITLE:
            self._add_title_page(page)
        elif page.page_type == PageType.TOC:
            self._add_toc_page(page)
        elif page.page_type == PageType.SECTION:
            self._add_section_page(page)
        elif page.page_type == PageType.CONTENT:
            self._add_content_page(page)
        elif page.page_type == PageType.CODE:
            self._add_code_page(page)
        elif page.page_type == PageType.DIAGRAM:
            self._add_diagram_page(page)
        elif page.page_type == PageType.IMAGE:
            self._add_image_page(page)
        elif page.page_type == PageType.MERMAID:
            self._add_mermaid_page(page)
        elif page.page_type == PageType.SUMMARY:
            self._add_summary_page(page)
        elif page.page_type == PageType.REFERENCES:
            self._add_references_page(page)
        else:
            raise ValueError(f"Unknown page type: {page.page_type}")

    def _add_title_page(self, page: PageSpec):
        """Add a title page."""
        logger.debug(f"Adding title page: {page.title}")

        # Add spacing at top
        self.story.append(Spacer(1, 2 * inch))

        # Add title
        self.story.append(Paragraph(page.title, self.styles['title']))

        # Add subtitle if present
        if page.subtitle:
            self.story.append(Paragraph(page.subtitle, self.styles['subtitle']))
            self.story.append(Spacer(1, 0.3 * inch))

        # Add author if present
        if page.author:
            self.story.append(Paragraph(page.author, self.styles['body']))

        # Add date if present
        if page.date:
            self.story.append(Paragraph(page.date, self.styles['body']))

        # Add additional info if present
        if page.additional_info:
            self.story.append(Spacer(1, 0.5 * inch))
            self.story.append(Paragraph(page.additional_info, self.styles['body']))

        self.story.append(PageBreak())

    def _add_toc_page(self, page: PageSpec):
        """Add a table of contents page."""
        logger.debug("Adding TOC page")

        self.story.append(Paragraph(page.title or "Table of Contents", self.styles['h1']))
        self.story.append(Spacer(1, 0.2 * inch))

        if page.entries:
            for entry in page.entries:
                self.story.append(Paragraph(entry, self.styles['bullet']))

        self.story.append(PageBreak())

    def _add_section_page(self, page: PageSpec):
        """Add a section divider page."""
        logger.debug(f"Adding section page: {page.title}")

        # Add spacing at top
        self.story.append(Spacer(1, 2.5 * inch))

        # Add section title (centered and large)
        self.story.append(Paragraph(page.title, self.styles['title']))

        # Add subtitle if present
        if page.subtitle:
            self.story.append(Paragraph(page.subtitle, self.styles['subtitle']))

        self.story.append(PageBreak())

    def _add_content_page(self, page: PageSpec):
        """Add a content page."""
        logger.debug(f"Adding content page: {page.title}")

        # Add title
        self.story.append(Paragraph(page.title, self.styles['h1']))
        self.story.append(Spacer(1, 0.2 * inch))

        # Add content items
        if page.content:
            for item in page.content:
                self._add_content_item(item)

        self.story.append(PageBreak())

    def _add_content_item(self, item: ContentItem):
        """Add a content item to the story."""
        if item.type == "text":
            if item.text:
                self.story.append(Paragraph(item.text, self.styles['body']))

        elif item.type == "bullet":
            if item.items:
                for bullet in item.items:
                    self.story.append(Paragraph(f"• {bullet}", self.styles['bullet']))

        elif item.type == "image":
            if item.image_path or item.image_url:
                self._add_image(item.image_path or item.image_url, item.caption)

        elif item.type == "code":
            if item.code:
                self._add_code_block(item.code, item.language)

        elif item.type == "table":
            if item.table_data:
                self._add_table(item.table_data, item.table_headers)

    def _add_code_page(self, page: PageSpec):
        """Add a code page."""
        logger.debug(f"Adding code page: {page.title}")

        # Add title
        self.story.append(Paragraph(page.title, self.styles['h1']))
        self.story.append(Spacer(1, 0.2 * inch))

        # Add code block
        if page.code:
            self._add_code_block(page.code, page.language, page.line_numbers)

        self.story.append(PageBreak())

    def _add_code_block(self, code: str, language: Optional[str] = None, line_numbers: bool = False):
        """Add a code block with optional line numbers."""
        if line_numbers:
            lines = code.split('\n')
            numbered_code = '\n'.join(f"{i+1:4d}  {line}" for i, line in enumerate(lines))
            code = numbered_code

        # Create a code block with background
        code_para = Preformatted(
            code,
            style=self.styles['code'],
            bulletText=None,
            maxLineLength=100,
        )

        self.story.append(code_para)
        self.story.append(Spacer(1, 0.2 * inch))

    def _add_diagram_page(self, page: PageSpec):
        """Add a diagram page."""
        logger.debug(f"Adding diagram page: {page.title}")

        # Add title
        self.story.append(Paragraph(page.title, self.styles['h1']))
        self.story.append(Spacer(1, 0.2 * inch))

        # Add diagram image
        image_path = page.diagram_path or page.diagram_url
        if image_path:
            self._add_image(image_path, page.caption)

        # Add description bullets if present
        if page.description:
            self.story.append(Spacer(1, 0.2 * inch))
            if isinstance(page.description, list):
                for desc in page.description:
                    self.story.append(Paragraph(f"• {desc}", self.styles['bullet']))
            else:
                self.story.append(Paragraph(page.description, self.styles['body']))

        self.story.append(PageBreak())

    def _add_image_page(self, page: PageSpec):
        """Add an image page."""
        logger.debug(f"Adding image page: {page.title}")

        # Add title
        self.story.append(Paragraph(page.title, self.styles['h1']))
        self.story.append(Spacer(1, 0.2 * inch))

        # Add image
        image_path = page.image_path or page.image_url
        if image_path:
            self._add_image(image_path, page.caption)

        # Add description if present
        if page.description:
            self.story.append(Spacer(1, 0.2 * inch))
            desc_text = page.description if isinstance(page.description, str) else '\n'.join(page.description)
            self.story.append(Paragraph(desc_text, self.styles['body']))

        self.story.append(PageBreak())

    def _add_mermaid_page(self, page: PageSpec):
        """Add a Mermaid diagram page."""
        logger.debug(f"Adding Mermaid diagram page: {page.title}")

        # Add title
        self.story.append(Paragraph(page.title, self.styles['h1']))
        self.story.append(Spacer(1, 0.2 * inch))

        # Render Mermaid code to PNG
        if page.mermaid_code:
            png_path = self._render_mermaid_to_png(page.mermaid_code)
            if png_path:
                self._add_image(png_path, page.caption)
            else:
                error_msg = "[Failed to render Mermaid diagram. Please ensure @mermaid-js/mermaid-cli is installed]"
                self.story.append(Paragraph(error_msg, self.styles['body']))
                logger.error("Failed to render Mermaid diagram")

        # Add description if present
        if page.description:
            self.story.append(Spacer(1, 0.2 * inch))
            if isinstance(page.description, list):
                for desc in page.description:
                    self.story.append(Paragraph(f"• {desc}", self.styles['bullet']))
            else:
                self.story.append(Paragraph(page.description, self.styles['body']))

        self.story.append(PageBreak())

    def _download_image(self, url: str) -> Optional[str]:
        """
        Download an image from a URL to a temporary file.

        Args:
            url: The URL of the image to download

        Returns:
            Path to the downloaded temporary file, or None if download failed
        """
        try:
            logger.info(f"Downloading image from URL: {url}")

            # Parse URL to get file extension
            parsed_url = urlparse(url)
            path = parsed_url.path
            ext = os.path.splitext(path)[1] or '.png'  # Default to .png if no extension

            # Create temporary file
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=ext)
            temp_path = temp_file.name
            temp_file.close()

            # Download the image
            headers = {'User-Agent': 'Mozilla/5.0 (MCP-PDF/0.1.1)'}
            req = urllib.request.Request(url, headers=headers)

            with urllib.request.urlopen(req, timeout=30) as response:
                with open(temp_path, 'wb') as out_file:
                    out_file.write(response.read())

            logger.info(f"Successfully downloaded image to: {temp_path}")
            self.downloaded_images.append(temp_path)
            return temp_path

        except Exception as e:
            logger.error(f"Failed to download image from {url}: {e}")
            return None

    def _is_url(self, path: str) -> bool:
        """Check if a path is a URL."""
        return path.startswith(('http://', 'https://'))

    def _render_mermaid_to_png(self, mermaid_code: str) -> Optional[str]:
        """
        Render Mermaid diagram code to PNG using mmdc (mermaid-cli).

        Args:
            mermaid_code: Mermaid diagram code

        Returns:
            Path to the rendered PNG file, or None if rendering failed
        """
        try:
            logger.info("Rendering Mermaid diagram to PNG...")

            # Create temporary files for input and output
            temp_input = tempfile.NamedTemporaryFile(
                mode='w',
                delete=False,
                suffix='.mmd',
                encoding='utf-8'
            )
            temp_input.write(mermaid_code)
            temp_input.close()

            temp_output = tempfile.NamedTemporaryFile(
                delete=False,
                suffix='.png'
            )
            temp_output_path = temp_output.name
            temp_output.close()

            # Call mmdc via npx
            cmd = [
                'npx',
                '-p', '@mermaid-js/mermaid-cli',
                'mmdc',
                '-i', temp_input.name,
                '-o', temp_output_path,
                '-b', 'transparent'
            ]

            logger.debug(f"Running command: {' '.join(cmd)}")
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )

            # Clean up input file
            os.unlink(temp_input.name)

            if result.returncode != 0:
                logger.error(f"mmdc failed with exit code {result.returncode}")
                logger.error(f"stderr: {result.stderr}")
                if os.path.exists(temp_output_path):
                    os.unlink(temp_output_path)
                return None

            logger.info(f"Successfully rendered Mermaid diagram to: {temp_output_path}")
            self.downloaded_images.append(temp_output_path)
            return temp_output_path

        except subprocess.TimeoutExpired:
            logger.error("mmdc command timed out after 30 seconds")
            return None
        except FileNotFoundError:
            logger.error("mmdc not found. Please install: npm install -g @mermaid-js/mermaid-cli")
            return None
        except Exception as e:
            logger.error(f"Failed to render Mermaid diagram: {e}")
            return None

    def _cleanup_downloaded_images(self):
        """Clean up any downloaded temporary image files."""
        for temp_path in self.downloaded_images:
            try:
                if os.path.exists(temp_path):
                    os.unlink(temp_path)
                    logger.debug(f"Cleaned up temporary image: {temp_path}")
            except Exception as e:
                logger.warning(f"Failed to clean up temporary image {temp_path}: {e}")

        self.downloaded_images.clear()

    def _add_image(self, image_path: str, caption: Optional[str] = None):
        """Add an image with optional caption. Supports both local paths and URLs."""
        try:
            actual_path = image_path

            # If it's a URL, download it first
            if self._is_url(image_path):
                logger.info(f"Image path is a URL, downloading: {image_path}")
                downloaded_path = self._download_image(image_path)
                if downloaded_path:
                    actual_path = downloaded_path
                else:
                    logger.error(f"Failed to download image from URL: {image_path}")
                    self.story.append(Paragraph(f"[Failed to download image from: {image_path}]", self.styles['body']))
                    return

            # Check if file exists
            if os.path.exists(actual_path):
                img = Image(actual_path, width=4 * inch, height=3 * inch)
                self.story.append(img)

                if caption:
                    self.story.append(Spacer(1, 0.1 * inch))
                    caption_style = ParagraphStyle(
                        'Caption',
                        parent=self.styles['body'],
                        alignment=TA_CENTER,
                        fontSize=9,
                        textColor=HexColor("#666666"),
                    )
                    self.story.append(Paragraph(caption, caption_style))
            else:
                logger.warning(f"Image not found: {actual_path}")
                self.story.append(Paragraph(f"[Image not found: {image_path}]", self.styles['body']))
        except Exception as e:
            logger.error(f"Error adding image {image_path}: {e}")
            self.story.append(Paragraph(f"[Error loading image: {e}]", self.styles['body']))

    def _add_summary_page(self, page: PageSpec):
        """Add a summary page."""
        logger.debug("Adding summary page")

        # Add title
        self.story.append(Paragraph(page.title or "Summary", self.styles['h1']))
        self.story.append(Spacer(1, 0.2 * inch))

        # Add key points
        if page.key_points:
            for point in page.key_points:
                self.story.append(Paragraph(f"• {point}", self.styles['bullet']))

        # Add conclusion
        if page.conclusion:
            self.story.append(Spacer(1, 0.3 * inch))
            self.story.append(Paragraph(page.conclusion, self.styles['body']))

        self.story.append(PageBreak())

    def _add_references_page(self, page: PageSpec):
        """Add a references page."""
        logger.debug("Adding references page")

        # Add title
        self.story.append(Paragraph(page.title or "References", self.styles['h1']))
        self.story.append(Spacer(1, 0.2 * inch))

        # Add references
        if page.references:
            for i, ref in enumerate(page.references, 1):
                if page.style == "numbered":
                    self.story.append(Paragraph(f"{i}. {ref}", self.styles['body']))
                elif page.style == "bulleted":
                    self.story.append(Paragraph(f"• {ref}", self.styles['bullet']))
                else:  # plain
                    self.story.append(Paragraph(ref, self.styles['body']))

        self.story.append(PageBreak())

    def _add_table(self, data: List[List[str]], headers: Optional[List[str]] = None):
        """Add a table to the story."""
        if headers:
            table_data = [headers] + data
        else:
            table_data = data

        table = Table(table_data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), HexColor(self.theme.colors.primary)),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), self.theme.fonts.heading),
            ('FONTSIZE', (0, 0), (-1, 0), self.theme.body_font_size),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), self.theme.body_font_size - 1),
        ]))

        self.story.append(table)
        self.story.append(Spacer(1, 0.2 * inch))
