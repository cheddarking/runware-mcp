# Runware MCP Server

A powerful Model Context Protocol (MCP) server that provides lightning fast image and video generation tools using the [Runware API](https://runware.ai). This server supports both SSE (Server-Sent Events) transport for custom claude connector and direct claude desktop installation as well.

## Features

### **Image Generation Tools**
- **`imageInference`**: Full-featured image generation with advanced parameters
- **`photoMaker`**: Subject personalization with PhotoMaker technology
- **`imageUpscale`**: High-quality image resolution enhancement
- **`imageBackgroundRemoval`**: Background removal with multiple AI models
- **`imageCaption`**: AI-powered image description generation
- **`imageMasking`**: Automatic mask generation for faces, hands, and people

### **Video Generation Tools**
- **`videoInference`**: Text-to-video and image-to-video generation
- **`listVideoModels`**: Discover available video models
- **`getVideoModelInfo`**: Get detailed model specifications

### **Utility Tools**
- **`imageUpload`**: Upload local images to get Runware UUIDs
- **`modelSearch`**: Search and discover AI models on the platform

### **Smart Features**
- **Automatic Model Selection**: I2V uses `klingai:5@2`, T2V uses `google:3@1`
- **Input Validation**: Prevents Claude upload URL pasting and validates dimensions
- **Comprehensive Error Handling**: Clear error messages and guidance

## Demo

Watch the demo video to see the Runware MCP server in action:


https://github.com/user-attachments/assets/9732096b-8513-455c-9759-cc88363c42f9


## Architecture

```
[ MCP Client / AI Assistant ]
           |
    (connects via SSE over HTTP)
           |
    [ Uvicorn Server ]
           |
    [ Starlette App ]
           |
    [ FastMCP Server ]
           |
    [ Runware API ]
```

- **Transport**: SSE (Server-Sent Events) for real-time communication
- **Framework**: [FastMCP](https://github.com/jlowin/fastmcp) with [Starlette](https://www.starlette.io/) web framework
- **Server**: [Uvicorn](https://www.uvicorn.org/) ASGI server
- **API**: Direct integration with [Runware's AI services](https://runware.ai)

## Prerequisites

- **Runware API Key**: Get your API key from [Runware Dashboard](https://my.runware.ai)
- **Docker** (for Method 1) or **Python 3.10+** (for Method 2)
- **MCP Client**: Claude Desktop, Claude Code, or Cursor

## Quick Start

### **Method 1: Docker (Recommended)**

Pull and run the pre-built Docker image:

```bash
# Pull from Docker Hub
docker pull bicharri/runware-mcp:latest

# Run the container with your API key
docker run --rm -p 8081:8081 \
  -e RUNWARE_API_KEY=your_api_key_here \
  bicharri/runware-mcp:latest
```

Or build from source:
```bash
# Clone and build
git clone https://github.com/Runware/MCP-Runware.git
cd MCP-Runware
docker build -t runware-mcp .

# Run the container
docker run --rm -p 8081:8081 \
  -e RUNWARE_API_KEY=your_api_key_here \
  runware-mcp
```

### **Method 2: Local Python Installation**

```bash
# Clone the repository
git clone https://github.com/Runware/MCP-Runware.git
cd MCP-Runware

# Install dependencies
uv venv
source .venv/bin/activate
uv pip install .

# Create .env file with your API key
echo "RUNWARE_API_KEY=your_api_key_here" > .env

# Run the server
python runware_mcp_server.py
```

### **Method 3: MCP Install (Direct Integration)**

For direct integration with Claude Desktop:
```bash
# From the project directory
mcp install --with-editable . runware_mcp_server.py
```

## Connecting to MCP Clients

Configure your MCP client to automatically start and stop the Docker container.

### **Claude Desktop**

Add to your Claude Desktop configuration file:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "runware": {
      "command": "docker",
      "args": [
        "run",
        "--rm",
        "-i",
        "-p",
        "8081:8081",
        "-e",
        "RUNWARE_API_KEY=your_api_key_here",
        "bicharri/runware-mcp:latest"
      ]
    }
  }
}
```

**Important**: Replace `your_api_key_here` with your actual Runware API key.

Restart Claude Desktop after saving the configuration.

### **Claude Code**

Create a `.mcp.json` file in your project directory:

```json
{
  "mcpServers": {
    "runware": {
      "command": "docker",
      "args": [
        "run",
        "--rm",
        "-i",
        "-p",
        "8081:8081",
        "-e",
        "RUNWARE_API_KEY=your_api_key_here",
        "bicharri/runware-mcp:latest"
      ]
    }
  }
}
```

**Important**: Replace `your_api_key_here` with your actual Runware API key.

Claude Code will detect the `.mcp.json` file and prompt you to enable the MCP server. Once enabled, restart Claude Code to activate the connection.

### **Cursor**

Add to your Cursor MCP settings file:

**macOS**: `~/Library/Application Support/Cursor/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json`
**Windows**: `%APPDATA%\Cursor\User\globalStorage\saoudrizwan.claude-dev\settings\cline_mcp_settings.json`

```json
{
  "mcpServers": {
    "runware": {
      "command": "docker",
      "args": [
        "run",
        "--rm",
        "-i",
        "-p",
        "8081:8081",
        "-e",
        "RUNWARE_API_KEY=your_api_key_here",
        "bicharri/runware-mcp:latest"
      ]
    }
  }
}
```

**Important**: Replace `your_api_key_here` with your actual Runware API key.

Restart Cursor after saving the configuration.

### **Alternative: Manual Server Mode**

If you prefer to run the server manually (without automatic start/stop), start the Docker container:

```bash
docker run --rm -p 8081:8081 \
  -e RUNWARE_API_KEY=your_api_key_here \
  bicharri/runware-mcp:latest
```

Then configure your MCP client with a URL connection:

```json
{
  "mcpServers": {
    "runware": {
      "url": "http://localhost:8081/sse"
    }
  }
}
```

## Model Recommendations

### **Image Generation**
- **Default**: `civitai:943001@1055701` (SDXL-based)
- **PhotoMaker**: `civitai:139562@344487` (RealVisXL V4.0)
- **Background Removal**: `runware:109@1` (RemBG 1.4)

### **Video Generation**
- **Image-to-Video (I2V)**: `klingai:5@2` (1920x1080)
- **Text-to-Video (T2V)**: `google:3@1` (1280x720)

You can find all additional models here: [Runware Models](https://my.runware.ai/models/all)

## Configuration

### **Environment Variables**
- `RUNWARE_API_KEY`: Your Runware API key (required)

### **Input Validation**
- Rejects Claude upload URLs (`https://files.*`). Claude tends to include base64 strings in its reasoning/thinking process, which rapidly fills the context window with garbage data. [Learn more about this issue](https://claude.ai/public/artifacts/0f28d79d-47bd-4fb8-bc25-e2699d78479f)
- Supports local file paths, public accessible URLs (make sure it has proper file extension such as JPG, PNG, WEBP, etc), and Runware UUIDs


## Support

- **Documentation**: [Runware API Docs](https://runware.ai/docs)
- **Models**: [Browse All Models](https://my.runware.ai/models/all)
- **Dashboard**: [Runware Dashboard](https://my.runware.ai)
- **Issues**: Create an issue in this repository
- **Email**: support@runware.ai
