# Output Directory Handling

## Overview

The MCP-PDF server intelligently handles output directory paths with automatic fallback to ensure PDFs are always saved successfully, even when Claude suggests a directory that doesn't exist or isn't accessible.

## How It Works

### 1. Primary Directory (Requested)

When Claude generates a PDF, it specifies an output directory in the document specification:

```json
{
  "output": {
    "filename": "report.pdf",
    "directory": "/path/to/output"
  }
}
```

The server will **attempt to use this directory first**:
- If the directory exists and is writable → Use it ✅
- If the directory doesn't exist but can be created → Create and use it ✅
- If the directory cannot be accessed or created → Fall back ⚠️

### 2. Fallback Directory (Configured)

If the requested directory is not accessible, the server automatically falls back to the configured `OUTPUT_DIR` environment variable.

**Configuration:**
```bash
# In .env file or environment
OUTPUT_DIR=./output
```

**Default fallback:** If `OUTPUT_DIR` is not set, the fallback is `~/pdf-output`

### 3. User Notification

When a fallback occurs, the response includes a message informing Claude (and the user) where the file was actually saved:

```json
{
  "ok": true,
  "output": "/Users/username/workspace/mcp-pdf/output/report.pdf",
  "pages_generated": 15,
  "filename": "report.pdf",
  "message": "Note: Saved to /Users/username/workspace/mcp-pdf/output (requested directory /mnt/user-data/outputs was not accessible)"
}
```

## Common Scenarios

### Scenario 1: Claude Suggests `/mnt/user-data/outputs`

This is a common path that Claude might suggest, but it doesn't exist on macOS/Linux desktop systems.

**What happens:**
1. Server tries to create `/mnt/user-data/outputs` → Fails (read-only filesystem)
2. Server falls back to `OUTPUT_DIR` (e.g., `./output`)
3. PDF is saved successfully
4. Response includes message about the fallback

**Claude is informed:**
```
Note: Saved to ./output (requested directory /mnt/user-data/outputs was not accessible)
```

### Scenario 2: Valid Custom Directory

Claude suggests a valid, accessible directory like `./reports`.

**What happens:**
1. Server checks if `./reports` exists
2. If not, creates the directory
3. PDF is saved to `./reports/document.pdf`
4. No fallback message (everything worked as requested)

### Scenario 3: Relative Path

Claude suggests a relative path like `../documents`.

**What happens:**
1. Server resolves the relative path
2. Attempts to create/access the directory
3. Uses it if successful, falls back if not

## Configuration Examples

### For Claude Desktop (macOS)

```json
{
  "mcpServers": {
    "mcp-pdf": {
      "command": "python",
      "args": ["/path/to/mcp-pdf/run_server.py"],
      "env": {
        "OUTPUT_DIR": "/Users/username/Documents/pdfs"
      }
    }
  }
}
```

### For Claude Desktop (Windows)

```json
{
  "mcpServers": {
    "mcp-pdf": {
      "command": "python",
      "args": ["C:\\path\\to\\mcp-pdf\\run_server.py"],
      "env": {
        "OUTPUT_DIR": "C:\\Users\\username\\Documents\\pdfs"
      }
    }
  }
}
```

### For Development/Testing

```bash
# In .env file
OUTPUT_DIR=./output
```

## Logs

The fallback behavior is logged for troubleshooting:

```
2024-11-02 12:36:45 - WARNING - Cannot use requested directory /mnt/user-data/outputs: [Errno 30] Read-only file system: '/mnt'
2024-11-02 12:36:45 - INFO - Falling back to configured output directory: output
2024-11-02 12:36:45 - INFO - Created fallback output directory: output
2024-11-02 12:36:45 - WARNING - Note: Saved to output (requested directory /mnt/user-data/outputs was not accessible)
```

## Best Practices

1. **Set OUTPUT_DIR** in your Claude Desktop configuration to a reliable, writable directory
2. **Use absolute paths** for OUTPUT_DIR to avoid ambiguity
3. **Ensure the directory exists** or that the server has permissions to create it
4. **Monitor logs** if you're experiencing issues with file saving

## Testing the Fallback

Run the test script to verify fallback behavior:

```bash
python tests/test_directory_fallback.py
```

This will:
1. Test fallback when directory is not accessible
2. Verify normal operation when directory is valid
3. Confirm messages are sent correctly

## Troubleshooting

### Problem: PDFs not being saved

**Check:**
- Is `OUTPUT_DIR` set and valid?
- Does the server have write permissions?
- Check logs for error messages

### Problem: PDFs saved to unexpected location

**Check:**
- What directory did Claude request?
- What is your `OUTPUT_DIR` configuration?
- Look for fallback messages in the response

### Problem: Permission errors

**Solution:**
```bash
# Make sure the output directory exists and is writable
mkdir -p ~/pdf-output
chmod 755 ~/pdf-output

# Update your configuration
export OUTPUT_DIR=~/pdf-output
```

## Technical Details

The fallback mechanism:

1. **Path Resolution**: Converts relative paths to absolute paths
2. **Directory Testing**: Creates a temporary file to verify write access
3. **Graceful Degradation**: Falls back through multiple options:
   - Requested directory
   - OUTPUT_DIR environment variable
   - Default ~/pdf-output
4. **Clear Communication**: Always tells the user where the file was actually saved
5. **Logging**: Comprehensive logging for troubleshooting

## Error Handling

If both the requested directory AND the fallback directory fail, the server returns an error:

```json
{
  "ok": false,
  "error": "Cannot write to requested directory '/invalid/path' or fallback directory '~/pdf-output'. Please check permissions and configuration.",
  "output": null,
  "pages_generated": 0
}
```

This ensures the user is always informed when PDF generation fails.
