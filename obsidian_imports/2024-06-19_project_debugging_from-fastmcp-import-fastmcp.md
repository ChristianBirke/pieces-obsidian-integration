---\n\ncontent_category: debugging
content_category: debugging
created: 2025-06-19 19:31:56.687540
pieces_id: 10a12af2-c1df-4ec9-95bd-4b05a5c0f737
source: pieces
tags:
- pieces-import
- workstream
- debugging
- '#project'
- from
- fastmcp
- import
title: From Fastmcp Import Fastmcp
type: project
workstream_activity: from-fastmcp-import-FastMCP
---\n\n\n\n# The error message indicates that there should be t...

The error message indicates that there should be two blank lines before the function definition. This is a common style guideline in Python to improve code readability. Here’s the corrected code snippet with the appropriate number of blank lines:

```python
import asyncio

from fastmcp import FastMCP

mcp = FastMCP("My MCP Server")


@mcp.tool
def greet(name: str) -> str:
    """Greet a person by name"""
    return f"Hello, {name}!"


if __name__ == "__main__":
    mcp.run()
```

Now, there are two blank lines before the `greet` function definition, which should resolve the error.

---
*Imported from Pieces Workstream Activity*  
*Import Date: 2025-06-19 19:31:56*