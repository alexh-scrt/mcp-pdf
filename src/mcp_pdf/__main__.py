"""Main entry point for mcp-pdf package."""

import asyncio
from .server import main

if __name__ == "__main__":
    asyncio.run(main())
