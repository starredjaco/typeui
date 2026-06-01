# TypeUI Antigravity Plugin

TypeUI connects Antigravity to the TypeUI MCP server so it can use curated design systems, UI prompts, and layout variations while building interfaces.

## Install

Install TypeUI directly from the public repository:

```bash
agy plugin install https://github.com/bergside/typeui
```

After installation, Antigravity will connect to TypeUI through the bundled MCP configuration. Sign in with TypeUI if Antigravity asks you to authorize the connection.

## MCP server

This plugin registers the TypeUI Streamable HTTP MCP server:

```text
https://mcp.typeui.sh/mcp
```

Antigravity uses `serverUrl` for remote MCP servers, so the plugin ships this MCP configuration:

```json
{
  "mcpServers": {
    "typeui": {
      "serverUrl": "https://mcp.typeui.sh/mcp"
    }
  }
}
```

## Directory preparation

To submit TypeUI to an Antigravity plugin directory, use the repository root if the directory expects a GitHub install URL, or use `plugins/antigravity/typeui` if it expects a package folder. Both include the required `plugin.json` marker file, MCP server definition, and TypeUI usage rules.

## Links

- Website: https://www.typeui.sh
- Documentation: https://www.typeui.sh/docs
- Antigravity setup guide: https://www.typeui.sh/docs/guides/antigravity
- Privacy policy: https://www.typeui.sh/privacy
- Terms of service: https://www.typeui.sh/terms
