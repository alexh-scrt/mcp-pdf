# MCP-PDF Usage Examples

This document provides comprehensive examples of how to generate various types of PDF documents using the MCP-PDF server.

## Example 1: Simple Document

A minimal PDF with just a few pages:

```json
{
  "document_spec": {
    "title": "Getting Started",
    "theme": {},
    "pages": [
      {
        "page_type": "title",
        "title": "Getting Started with MCP-PDF",
        "subtitle": "A Quick Introduction"
      },
      {
        "page_type": "content",
        "title": "Welcome",
        "content": [
          {
            "type": "text",
            "text": "This is a simple example of generating PDFs with MCP-PDF."
          }
        ]
      }
    ]
  }
}
```

## Example 2: Technical Documentation

A complete technical document with multiple sections:

```json
{
  "document_spec": {
    "title": "REST API Documentation",
    "theme": {},
    "pages": [
      {
        "page_type": "title",
        "title": "REST API Documentation",
        "subtitle": "Version 2.0",
        "author": "Engineering Team",
        "date": "November 2024"
      },
      {
        "page_type": "toc",
        "title": "Table of Contents",
        "entries": [
          "1. Introduction",
          "2. Authentication",
          "3. Endpoints",
          "4. Error Handling",
          "5. Examples",
          "6. References"
        ]
      },
      {
        "page_type": "section",
        "title": "Introduction",
        "subtitle": "API Overview"
      },
      {
        "page_type": "content",
        "title": "API Overview",
        "content": [
          {
            "type": "text",
            "text": "Our REST API provides programmatic access to all platform features."
          },
          {
            "type": "bullet",
            "items": [
              "RESTful architecture",
              "JSON request/response format",
              "OAuth 2.0 authentication",
              "Rate limiting: 1000 requests/hour",
              "HTTPS required for all endpoints"
            ]
          }
        ]
      },
      {
        "page_type": "section",
        "title": "Authentication"
      },
      {
        "page_type": "content",
        "title": "OAuth 2.0 Authentication",
        "content": [
          {
            "type": "text",
            "text": "All API requests require authentication using OAuth 2.0 bearer tokens."
          }
        ]
      },
      {
        "page_type": "code",
        "title": "Authentication Example",
        "code": "import requests\n\nheaders = {\n    'Authorization': 'Bearer YOUR_ACCESS_TOKEN',\n    'Content-Type': 'application/json'\n}\n\nresponse = requests.get(\n    'https://api.example.com/v2/users',\n    headers=headers\n)\n\nif response.status_code == 200:\n    users = response.json()\n    print(f\"Found {len(users)} users\")",
        "language": "python",
        "line_numbers": true
      },
      {
        "page_type": "summary",
        "title": "Key Takeaways",
        "key_points": [
          "Use OAuth 2.0 for authentication",
          "Include bearer token in all requests",
          "Rate limit is 1000 requests per hour",
          "All communication must use HTTPS",
          "Comprehensive error codes provided"
        ],
        "conclusion": "This API provides secure, efficient access to all platform features with comprehensive documentation and support."
      },
      {
        "page_type": "references",
        "title": "References",
        "references": [
          "OAuth 2.0 RFC 6749 - https://tools.ietf.org/html/rfc6749",
          "REST API Best Practices - https://restfulapi.net/",
          "HTTP Status Codes - https://httpstatuses.com/"
        ],
        "style": "numbered"
      }
    ],
    "output": {
      "filename": "api_documentation.pdf",
      "directory": "./output"
    }
  }
}
```

## Example 3: Report with Custom Theme

A business report with custom branding:

```json
{
  "document_spec": {
    "title": "Q4 2024 Sales Report",
    "theme": {
      "colors": {
        "primary": "#1E40AF",
        "secondary": "#10B981",
        "accent": "#F59E0B",
        "background": "#FFFFFF",
        "text": "#1F2937",
        "code_bg": "#F3F4F6"
      },
      "fonts": {
        "heading": "Helvetica-Bold",
        "body": "Helvetica",
        "code": "Courier"
      },
      "title_font_size": 28,
      "h1_font_size": 20,
      "body_font_size": 11
    },
    "pages": [
      {
        "page_type": "title",
        "title": "Q4 2024 Sales Report",
        "subtitle": "Performance Analysis and Insights",
        "author": "Sales Analytics Team",
        "date": "November 2, 2024",
        "additional_info": "Confidential - Internal Use Only"
      },
      {
        "page_type": "toc",
        "title": "Contents",
        "entries": [
          "Executive Summary",
          "Q4 Performance Overview",
          "Regional Analysis",
          "Product Performance",
          "Key Insights",
          "Recommendations"
        ]
      },
      {
        "page_type": "content",
        "title": "Executive Summary",
        "content": [
          {
            "type": "text",
            "text": "Q4 2024 demonstrated strong performance across all regions, with revenue exceeding targets by 15%."
          },
          {
            "type": "bullet",
            "items": [
              "Total Revenue: $12.5M (↑ 15% vs. target)",
              "New Customers: 450 (↑ 22% YoY)",
              "Customer Retention: 94%",
              "Average Deal Size: $27,800 (↑ 8%)",
              "Sales Cycle: 42 days (↓ 12%)"
            ]
          }
        ]
      },
      {
        "page_type": "summary",
        "title": "Key Insights",
        "key_points": [
          "Enterprise segment drove 60% of revenue growth",
          "Product line expansion contributed to higher deal sizes",
          "Improved sales processes reduced cycle time",
          "Customer satisfaction scores at all-time high (9.2/10)",
          "Strong pipeline entering Q1 2025 ($18M qualified)"
        ],
        "conclusion": "Q4 2024 exceeded expectations across all metrics. The team's focus on enterprise clients and operational efficiency improvements has positioned us well for continued growth in 2025."
      }
    ],
    "output": {
      "filename": "q4_2024_sales_report.pdf"
    }
  }
}
```

## Example 4: Tutorial with Code Examples

A programming tutorial with multiple code snippets:

```json
{
  "document_spec": {
    "title": "Python Async Programming Tutorial",
    "theme": {},
    "pages": [
      {
        "page_type": "title",
        "title": "Async Programming in Python",
        "subtitle": "A Practical Guide to asyncio",
        "author": "Python Learning Center"
      },
      {
        "page_type": "content",
        "title": "Introduction to Async/Await",
        "content": [
          {
            "type": "text",
            "text": "Asynchronous programming allows you to write concurrent code that can handle multiple operations without blocking."
          },
          {
            "type": "bullet",
            "items": [
              "Non-blocking I/O operations",
              "Efficient handling of multiple tasks",
              "Better resource utilization",
              "Improved application responsiveness"
            ]
          }
        ]
      },
      {
        "page_type": "code",
        "title": "Basic Async Function",
        "code": "import asyncio\n\nasync def fetch_data(url):\n    \"\"\"Fetch data from a URL asynchronously.\"\"\"\n    print(f\"Fetching {url}...\")\n    await asyncio.sleep(2)  # Simulate network delay\n    return f\"Data from {url}\"\n\nasync def main():\n    # Run multiple fetch operations concurrently\n    tasks = [\n        fetch_data(\"https://api1.com\"),\n        fetch_data(\"https://api2.com\"),\n        fetch_data(\"https://api3.com\")\n    ]\n    results = await asyncio.gather(*tasks)\n    for result in results:\n        print(result)\n\n# Run the async main function\nasyncio.run(main())",
        "language": "python",
        "line_numbers": true
      },
      {
        "page_type": "code",
        "title": "Error Handling in Async Code",
        "code": "import asyncio\n\nasync def fetch_with_retry(url, max_retries=3):\n    \"\"\"Fetch data with retry logic.\"\"\"\n    for attempt in range(max_retries):\n        try:\n            # Simulate fetch operation\n            if attempt < 2:\n                raise ConnectionError(\"Network error\")\n            return f\"Success: {url}\"\n        except ConnectionError as e:\n            if attempt == max_retries - 1:\n                raise\n            print(f\"Retry {attempt + 1}/{max_retries}\")\n            await asyncio.sleep(1)\n\nasync def main():\n    try:\n        result = await fetch_with_retry(\"https://api.com\")\n        print(result)\n    except ConnectionError:\n        print(\"Failed after retries\")\n\nasyncio.run(main())",
        "language": "python",
        "line_numbers": true
      },
      {
        "page_type": "summary",
        "title": "Best Practices",
        "key_points": [
          "Always use 'await' with async functions",
          "Use asyncio.gather() for concurrent operations",
          "Implement proper error handling",
          "Avoid blocking operations in async code",
          "Use asyncio.run() as the entry point"
        ],
        "conclusion": "Mastering async programming in Python enables you to build high-performance, scalable applications that efficiently handle I/O-bound operations."
      }
    ]
  }
}
```

## Example 5: Research Paper

An academic-style document:

```json
{
  "document_spec": {
    "title": "Machine Learning in Healthcare",
    "theme": {},
    "pages": [
      {
        "page_type": "title",
        "title": "Machine Learning Applications in Healthcare",
        "subtitle": "A Comprehensive Review",
        "author": "Dr. Jane Smith, PhD",
        "date": "November 2024",
        "additional_info": "Department of Computer Science, University Example"
      },
      {
        "page_type": "content",
        "title": "Abstract",
        "content": [
          {
            "type": "text",
            "text": "Machine learning has revolutionized healthcare by enabling early disease detection, personalized treatment plans, and improved patient outcomes. This paper reviews recent applications of ML in clinical settings and discusses future directions."
          }
        ]
      },
      {
        "page_type": "toc",
        "title": "Table of Contents",
        "entries": [
          "1. Introduction",
          "2. Diagnostic Applications",
          "3. Treatment Optimization",
          "4. Patient Monitoring",
          "5. Challenges and Limitations",
          "6. Future Directions",
          "7. Conclusion",
          "8. References"
        ]
      },
      {
        "page_type": "section",
        "title": "1. Introduction"
      },
      {
        "page_type": "content",
        "title": "Background",
        "content": [
          {
            "type": "text",
            "text": "The integration of machine learning in healthcare has grown exponentially over the past decade. With the availability of large-scale medical datasets and increased computational power, ML algorithms can now identify patterns and make predictions that support clinical decision-making."
          },
          {
            "type": "bullet",
            "items": [
              "Image analysis for radiology and pathology",
              "Predictive models for disease progression",
              "Natural language processing for medical records",
              "Drug discovery and development",
              "Personalized medicine recommendations"
            ]
          }
        ]
      },
      {
        "page_type": "section",
        "title": "2. Diagnostic Applications"
      },
      {
        "page_type": "content",
        "title": "Medical Image Analysis",
        "content": [
          {
            "type": "text",
            "text": "Deep learning models, particularly convolutional neural networks (CNNs), have achieved remarkable accuracy in analyzing medical images:"
          },
          {
            "type": "bullet",
            "items": [
              "Chest X-ray analysis for pneumonia detection (98% accuracy)",
              "MRI scan interpretation for brain tumor classification",
              "Retinal imaging for diabetic retinopathy screening",
              "Mammography analysis for breast cancer detection",
              "CT scan evaluation for stroke identification"
            ]
          }
        ]
      },
      {
        "page_type": "references",
        "title": "References",
        "references": [
          "Esteva, A., et al. (2019). A guide to deep learning in healthcare. Nature Medicine, 25(1), 24-29.",
          "Topol, E. J. (2019). High-performance medicine: the convergence of human and artificial intelligence. Nature Medicine, 25(1), 44-56.",
          "Jiang, F., et al. (2017). Artificial intelligence in healthcare: past, present and future. Stroke and Vascular Neurology, 2(4), 230-243.",
          "Rajkomar, A., et al. (2019). Machine learning in medicine. New England Journal of Medicine, 380(14), 1347-1358.",
          "Yu, K. H., et al. (2018). Artificial intelligence in healthcare. Nature Biomedical Engineering, 2(10), 719-731."
        ],
        "style": "numbered"
      }
    ],
    "output": {
      "filename": "ml_healthcare_review.pdf"
    }
  }
}
```

## Tips for Creating Great PDFs

1. **Structure Your Content**
   - Always start with a title page
   - Include a table of contents for longer documents
   - Use section pages to separate major topics
   - End with a summary or conclusion

2. **Use Appropriate Page Types**
   - Use `code` pages for code examples (not content pages with code items)
   - Use `section` pages as dividers between major sections
   - Use `summary` pages for key takeaways

3. **Keep Content Readable**
   - Break long text into paragraphs
   - Use bullet points for lists
   - Keep code examples focused and well-commented
   - Add line numbers to longer code blocks

4. **Customize Themes**
   - Use your brand colors for consistency
   - Adjust font sizes for readability
   - Maintain good contrast between text and background

5. **Output Organization**
   - Specify meaningful filenames
   - Use a consistent output directory
   - Include dates in filenames for versioning

## Common Patterns

### Meeting Minutes
```
Title Page → TOC → Section (per topic) → Content Pages → Summary → Action Items
```

### Technical Proposal
```
Title Page → Executive Summary → TOC → Problem Statement → Solution → Architecture (with diagrams) → Implementation Plan → Budget → References
```

### User Manual
```
Title Page → TOC → Introduction → Installation → Configuration → Usage Examples (with code) → Troubleshooting → FAQ → References
```

### Training Material
```
Title Page → TOC → Section (per module) → Content (theory) → Code Examples → Exercises → Summary → Resources
```
