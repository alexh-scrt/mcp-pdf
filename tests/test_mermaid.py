#!/usr/bin/env python3
"""Test Mermaid diagram functionality."""

from mcp_pdf.models.document_spec import DocumentSpec, PageSpec, PageType
from mcp_pdf.models.theme_spec import ThemeSpec
from mcp_pdf.rendering.pdf_generator import PDFGenerator


def test_mermaid_sequence_diagram():
    """Test Mermaid page with sequence diagram."""

    mermaid_code = """sequenceDiagram
    participant Client
    participant Server
    participant Database

    Note over Client,Server: HTTP Request/Response Cycle

    Client->>Server: HTTP GET /api/users/123
    activate Server

    Server->>Database: Query user by ID
    activate Database
    Database-->>Server: Return user data
    deactivate Database

    Server-->>Client: HTTP 200 OK (JSON response)
    deactivate Server
"""

    doc_spec = DocumentSpec(
        title="Mermaid Diagram Test",
        theme=ThemeSpec(),
        pages=[
            PageSpec(
                page_type=PageType.TITLE,
                title="Mermaid Diagram Test",
                subtitle="Testing Mermaid to PNG Conversion"
            ),
            PageSpec(
                page_type=PageType.MERMAID,
                title="HTTP Request/Response Sequence",
                mermaid_code=mermaid_code,
                description=[
                    "Illustrates typical HTTP request/response cycle",
                    "Shows interaction between Client, Server, and Database",
                    "Includes activation boxes and notes"
                ]
            )
        ],
        output={
            "filename": "mermaid_test.pdf",
            "directory": "./output"
        }
    )

    # Generate PDF
    generator = PDFGenerator()
    result = generator.generate_pdf(doc_spec)

    print(f"\n✅ PDF Generation with Mermaid Diagram:")
    print(f"   OK: {result['ok']}")
    print(f"   Output: {result['output']}")
    print(f"   Pages: {result['pages_generated']}")

    assert result['ok'] is True, "PDF generation should succeed"
    assert result['pages_generated'] == 2, "Should generate 2 pages"

    print(f"✅ Successfully generated PDF with Mermaid diagram")


def test_multiple_mermaid_diagrams():
    """Test PDF with multiple Mermaid diagrams."""

    flowchart_code = """flowchart TD
    Start[Start] --> Input[Get User Input]
    Input --> Validate{Valid?}
    Validate -->|Yes| Process[Process Data]
    Validate -->|No| Error[Show Error]
    Process --> Save[Save to DB]
    Save --> Success[Show Success]
    Error --> Input
    Success --> End[End]
"""

    gantt_code = """gantt
    title Project Timeline
    dateFormat YYYY-MM-DD
    section Phase 1
    Requirements :done, req, 2024-01-01, 2024-01-15
    Design :done, design, 2024-01-16, 2024-02-01
    section Phase 2
    Implementation :active, impl, 2024-02-02, 2024-03-15
    Testing :test, 2024-03-16, 2024-04-01
    section Phase 3
    Deployment :deploy, 2024-04-02, 2024-04-15
"""

    doc_spec = DocumentSpec(
        title="Multiple Mermaid Diagrams",
        theme=ThemeSpec(),
        pages=[
            PageSpec(
                page_type=PageType.TITLE,
                title="Multiple Mermaid Diagrams",
                subtitle="Flowchart and Gantt Chart Examples"
            ),
            PageSpec(
                page_type=PageType.MERMAID,
                title="User Input Flowchart",
                mermaid_code=flowchart_code,
                description=[
                    "Shows decision flow for user input validation",
                    "Includes error handling loop"
                ]
            ),
            PageSpec(
                page_type=PageType.MERMAID,
                title="Project Timeline",
                mermaid_code=gantt_code,
                caption="Q1-Q2 2024 Project Schedule"
            )
        ],
        output={
            "filename": "multiple_mermaid_test.pdf",
            "directory": "./output"
        }
    )

    # Generate PDF
    generator = PDFGenerator()
    result = generator.generate_pdf(doc_spec)

    print(f"\n✅ PDF Generation with Multiple Mermaid Diagrams:")
    print(f"   OK: {result['ok']}")
    print(f"   Output: {result['output']}")
    print(f"   Pages: {result['pages_generated']}")

    assert result['ok'] is True, "PDF generation should succeed"
    assert result['pages_generated'] == 3, "Should generate 3 pages"

    print(f"✅ Successfully generated PDF with multiple Mermaid diagrams")


def test_mermaid_with_code_page():
    """Test document with both Mermaid diagram and code page."""

    mermaid_code = """classDiagram
    class User {
        +String username
        +String email
        +login()
        +logout()
    }
    class Post {
        +String title
        +String content
        +Date created_at
        +publish()
    }
    class Comment {
        +String text
        +Date created_at
        +approve()
    }
    User "1" --> "*" Post : creates
    Post "1" --> "*" Comment : has
    User "1" --> "*" Comment : writes
"""

    python_code = """class User:
    def __init__(self, username, email):
        self.username = username
        self.email = email

    def login(self):
        print(f"{self.username} logged in")

    def logout(self):
        print(f"{self.username} logged out")


class Post:
    def __init__(self, title, content, author):
        self.title = title
        self.content = content
        self.author = author
        self.created_at = datetime.now()

    def publish(self):
        print(f"Published: {self.title}")
"""

    doc_spec = DocumentSpec(
        title="System Design Document",
        theme=ThemeSpec(),
        pages=[
            PageSpec(
                page_type=PageType.TITLE,
                title="System Design Document",
                subtitle="Blog Platform Architecture",
                author="Engineering Team",
                date="November 2024"
            ),
            PageSpec(
                page_type=PageType.SECTION,
                title="Data Model",
                subtitle="Class Diagram"
            ),
            PageSpec(
                page_type=PageType.MERMAID,
                title="Class Relationships",
                mermaid_code=mermaid_code,
                description=[
                    "Users create Posts and Comments",
                    "Posts contain multiple Comments",
                    "Relationships shown with multiplicity"
                ]
            ),
            PageSpec(
                page_type=PageType.SECTION,
                title="Implementation",
                subtitle="Python Code"
            ),
            PageSpec(
                page_type=PageType.CODE,
                title="User and Post Classes",
                code=python_code,
                language="python",
                line_numbers=True
            )
        ],
        output={
            "filename": "mermaid_with_code_test.pdf",
            "directory": "./output"
        }
    )

    # Generate PDF
    generator = PDFGenerator()
    result = generator.generate_pdf(doc_spec)

    print(f"\n✅ PDF Generation with Mermaid and Code:")
    print(f"   OK: {result['ok']}")
    print(f"   Output: {result['output']}")
    print(f"   Pages: {result['pages_generated']}")

    assert result['ok'] is True, "PDF generation should succeed"
    assert result['pages_generated'] == 5, "Should generate 5 pages"

    print(f"✅ Successfully generated PDF with Mermaid diagram and code")


if __name__ == "__main__":
    print("=" * 70)
    print("Testing Mermaid Diagram Functionality")
    print("=" * 70)

    print("\n📝 Test 1: Mermaid Sequence Diagram")
    print("-" * 70)
    test_mermaid_sequence_diagram()

    print("\n📝 Test 2: Multiple Mermaid Diagrams")
    print("-" * 70)
    test_multiple_mermaid_diagrams()

    print("\n📝 Test 3: Mermaid with Code Page")
    print("-" * 70)
    test_mermaid_with_code_page()

    print("\n" + "=" * 70)
    print("✅ All Mermaid tests passed!")
    print("=" * 70)
