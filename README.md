# mcp-guard

A high-performance, fail-closed interception proxy for Model Context Protocol (MCP) servers.

## Overview
As AI agents gain access to local file systems and shell execution via MCP, the attack surface expands exponentially. mcp-guard sits between the LLM client (e.g., Claude Desktop, Cursor) and the MCP server, applying deterministic AST-based pre-flight inspection to intercept and block destructive tool calls.

## Quick Start
```bash
pip install xpleon-mcp-guard
```

```python
from mcp_guard import Interceptor, Policy

policy = Policy(
    allowed_programs=["echo", "ls", "grep"],
    block_paths=["/etc/", "/var/"]
)

interceptor = Interceptor(policy=policy)

@interceptor.guard
def execute_shell(command: str):
    import os
    os.system(command)
```

## Architecture and Limitations
mcp-guard utilizes a fast, static analysis engine to parse shell commands and JSON-RPC payloads. It enforces strict capability allowlists and blocks known exfiltration patterns.

The Open Source Limitation:
Static regex and AST parsing cannot detect complex prompt injection or emergent state-based threats. If an agent's context shifts maliciously, a static policy may be bypassed.

## Enterprise Runtime
If you are deploying agents into production (fintech, healthcare, SaaS), static rules are insufficient.

For dynamic state-aware governance, cryptographic Write-Ahead Logging (WAL), and multi-tenant isolation, explore the commercial Xpleon Runtime. It provides a deterministic policy engine based on real-time telemetry and native REST/MCP gateway support.

Live Demo: https://huggingface.co/spaces/Nambi23/Xpleon-Labs
