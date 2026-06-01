# TypeUI Antigravity CLI Plugin

TypeUI connects Antigravity CLI to the TypeUI MCP server so it can use curated design systems, UI prompts, and layout variations while building interfaces.

## Install

Install TypeUI from a local checkout of the public repository:

```bash
git clone https://github.com/bergside/typeui.git
agy plugin install ./typeui/plugins/antigravity/typeui
```

After installation, Antigravity CLI will connect to TypeUI through the bundled MCP configuration. Sign in with TypeUI if Antigravity asks you to authorize the connection.

## MCP server

This plugin registers the TypeUI Streamable HTTP MCP server:

```text
https://mcp.typeui.sh/mcp
```

Antigravity CLI uses `serverUrl` for remote MCP servers, so the plugin ships this MCP configuration:

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

To submit TypeUI to an Antigravity plugin directory, use the `plugins/antigravity/typeui` folder as the plugin package root. It contains the required `plugin.json` marker file, the optional `mcp_config.json` server definition, and TypeUI usage rules.

## Links

- Website: https://www.typeui.sh
- Documentation: https://www.typeui.sh/docs
- Antigravity CLI setup guide: https://www.typeui.sh/docs/guides/antigravity-cli
- Privacy policy: https://www.typeui.sh/privacy
- Terms of service: https://www.typeui.sh/terms
