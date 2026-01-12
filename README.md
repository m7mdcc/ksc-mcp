# Kaspersky Security Center (KSC) MCP Server

This is a Model Context Protocol (MCP) server that exposes the Kaspersky Security Center Web API as tools for LLMs.

## Features
- **Async Architecture**: Uses `anyio` to wrap the synchronous `KlAkOAPI` library.
- **Tools**:
  - `ksc_ping`: Check connection.
  - `ksc_list_hosts`: Find managed devices.
  - `ksc_get_host_details`: Get device info.
  - `ksc_list_tasks`: Enum tasks.
  - `ksc_run_task`: Execute tasks.
  - `ksc_get_task_state`: Check task status.

## Installation

### Prerequisites
- Python 3.12+
- `uv` (recommended)
- KSC Server Credentials
- KlAkOAPI 15.1 package (included in `packages/`)

### Setup
1. **Clone the repository.**
2. **Create a `.env` file** in the root directory:
   ```env
   KSC_HOST=https://your-ksc-server.com:13299
   KSC_USERNAME=your_username
   KSC_PASSWORD=your_password
   KSC_VERIFY_SSL=false
   ```
3. **Install dependencies**:
   ```bash
   uv sync
   ```

## Usage

### Running the Server
```bash
uv run ksc-mcp
```
Or directly:
```bash
uv run app/main.py
```

### Using with Claude Desktop
Add the following to your `claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "ksc": {
      "command": "uv",
      "args": [
        "--directory",
        "C:\\path\\to\\ksc-mcp",
        "run",
        "ksc-mcp"
      ]
    }
  }
}
```

## Development Workflow

This project uses `uv` for dependency management and `ruff` for linting.

### Common Commands
- **Install Dependencies**: `uv sync`
    - *Note:* This only installs packages. It does not run tests or linters.
- **Run Server**: `uv run ksc-mcp` (or `make dev`)
- **Run Tests**: `uv run pytest` (or `make test`)
- **Lint & Fix**: `uv run ruff check --fix .` (or `make lint`)
- **Format Code**: `uv run ruff format .` (or `make format`)

### Makefile
For convenience, a `Makefile` is included:
```bash
make install
make dev
make test
make lint    # Runs ruff check
make format  # Runs ruff format
```

## Implementation Details
The server wraps the official `KlAkOAPI` Python package. Since `KlAkOAPI` uses synchronous `requests`, we offload these calls to a threadpool to ensure the MCP server remains responsive and async.
