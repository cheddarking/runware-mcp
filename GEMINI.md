# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Model Context Protocol (MCP) server that provides AI-powered image and video generation tools using the Runware API. The server supports both SSE (Server-Sent Events) transport for custom integrations and direct Claude Desktop installation.

## Architecture

The codebase follows a layered architecture:

```
Client (Claude Desktop / MCP Client)
    ↓ (SSE over HTTP)
Uvicorn ASGI Server
    ↓
Starlette Web Framework
    ↓
FastMCP Server (mcp.server.fastmcp)
    ↓
MCP Tools (@mcp.tool() decorators)
    ↓
Runware API (https://api.runware.ai/v1)
```

### Key Files

- **runware_mcp_server.py**: Main server file containing all MCP tool definitions and SSE server setup
- **utils/runwareUtils.py**: Utility functions for API communication, video model management, and polling
- **pyproject.toml**: Project metadata and dependencies
- **Dockerfile**: Container configuration for deployment

## Development Commands

### Setup

```bash
# Install dependencies using uv (recommended)
uv venv
source .venv/bin/activate
uv pip install .

# Or using pip
pip install -r requirements.txt
```

### Running the Server

```bash
# Run SSE server (default: http://0.0.0.0:8081)
python runware_mcp_server.py

# Run with custom host/port
python runware_mcp_server.py --host 127.0.0.1 --port 8080
```

### Docker Deployment

```bash
# Build Docker image
docker build -t runware-mcp .

# Run container
docker run --rm -p 8081:8081 runware-mcp
```

### MCP Installation

```bash
# Install in Claude Desktop from project directory
mcp install --with-editable . runware_mcp_server.py
```

## Environment Configuration

Create a `.env` file in the project root:

```bash
RUNWARE_API_KEY=your_api_key_here
```

The API key is required for all operations. Get it from https://my.runware.ai

## MCP Tool Categories

### Image Generation
- **imageInference**: Full-featured image generation with advanced parameters (LoRA, ControlNet, IP-Adapters, etc.)
- **photoMaker**: Subject personalization using PhotoMaker technology
- **imageUpscale**: High-quality upscaling (2-4x factor, max 4096x4096)
- **imageBackgroundRemoval**: Background removal with multiple AI models
- **imageCaption**: AI-powered image description
- **imageMasking**: Auto mask generation for faces, hands, people

### Video Generation
- **videoInference**: Text-to-video and image-to-video generation
- **listVideoModels**: List all available video models
- **getVideoModelInfo**: Get model specifications

### Utilities
- **imageUpload**: Upload local images to get Runware UUIDs
- **modelSearch**: Search and discover AI models

## Critical Implementation Details

### Input Validation for Claude Upload URLs

All image input tools reject Claude upload URLs (`https://files.*`) to prevent context pollution. When Claude pastes images, it generates base64 strings during reasoning that rapidly fill the context window. Instead:

1. Use `imageUpload` tool first with local file paths
2. Use the returned Runware UUID in subsequent tools
3. Or use publicly accessible URLs with proper file extensions

See validation functions in runware_mcp_server.py:
- `isClaudeUploadURL()` - line 61
- `validateImageInputs()` - line 72

### Video Model Dimension Requirements

Each video model has strict dimension requirements defined in `utils/runwareUtils.py` (MODEL_DIMENSIONS dict, line 71). The `validateVideoDimensions()` function enforces these constraints before API calls.

Default model recommendations:
- Image-to-Video: `klingai:5@2` (1920x1080)
- Text-to-Video: `google:3@1` (1280x720)

### Async Video Generation

Video generation uses asynchronous processing with polling:
1. Initial request returns a `taskUUID`
2. `pollVideoCompletion()` polls every 2 seconds
3. Returns when status != "processing"

See `pollVideoCompletion()` in utils/runwareUtils.py:261

### PhotoMaker Trigger Word

The `photoMaker` tool automatically prepends "rwre" trigger word if not present in the prompt (line 377). This is required by the PhotoMaker model architecture.

## Default Models

```python
DEFAULT_IMAGE_MODEL = "civitai:943001@1055701"  # SDXL-based
DEFAULT_PHOTO_MAKER_MODEL = "civitai:139562@344487"  # RealVisXL V4.0
DEFAULT_BG_REMOVAL_MODEL = "runware:109@1"  # RemBG 1.4
DEFAULT_MASKING_MODEL = "runware:35@1"  # face_yolov8n
```

## API Communication

All tools use `inferenceRequest()` from utils/runwareUtils.py which:
- Constructs requests to `https://api.runware.ai/v1`
- Adds Bearer token authentication
- Wraps config in array: `[genConfig]`
- Handles errors via `errors[0].message` field
- Has 300-second timeout

## Important Notes

- Image retention: 30 days after last use, but indefinite while actively used
- Max upscale output: 4096x4096 pixels (auto-resizes input if needed)
- Video output: Only URL delivery supported (not dataURI or base64)
- SSE transport uses `/sse` endpoint for connections and `/messages/` for POST communication
