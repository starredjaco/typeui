# TypeUI for OpenClaw

TypeUI connects OpenClaw-managed agents to the hosted TypeUI MCP server so they can use project design skills, brand kits, UI prompts, and layout variations while building interfaces.

This folder is also a ClawHub-ready OpenClaw plugin package. It includes:

- `openclaw.plugin.json` for native OpenClaw plugin discovery.
- `package.json` with ClawHub package, install, compatibility, and build metadata.
- `index.js` as the runtime entrypoint that installs TypeUI MCP into OpenClaw config.
- `skills/typeui/SKILL.md` with TypeUI usage guidance for OpenClaw.
- `config.json` with the OpenClaw MCP server definition for TypeUI.

## Install TypeUI MCP

After installing the plugin package, run:

```bash
openclaw typeui install-mcp
```

The plugin writes this OpenClaw-managed MCP server entry:

```bash
openclaw mcp set typeui '{"url":"https://mcp.typeui.sh","transport":"streamable-http","auth":"oauth"}'
```

This folder includes the same server definition in `config.json`.

You can also ask an OpenClaw agent to call the `typeui_install_mcp` tool.

Start the TypeUI OAuth flow:

```bash
openclaw mcp login typeui
```

OpenClaw prints an authorization URL. Open it, sign in with TypeUI, and authorize the connection. If OpenClaw asks you to finish with a code, pass it back to the same server:

```bash
openclaw mcp login typeui --code <code>
```

Check the saved server and live connection:

```bash
openclaw mcp status --verbose
openclaw mcp doctor typeui --probe
```

If OpenClaw is already running with cached MCP runtimes, reload MCP servers or restart the agent process:

```bash
openclaw mcp reload
```

## Package for ClawHub

Validate the plugin package before upload:

```bash
clawhub package validate plugins/openclaw/typeui
clawhub package publish plugins/openclaw/typeui --dry-run
```

Create a local package artifact from this folder:

```bash
cd plugins/openclaw/typeui
npm pack
```

Upload the package artifact or ZIP this folder for ClawHub submission.

## Links

- Website: https://www.typeui.sh
- Documentation: https://www.typeui.sh/docs
- OpenClaw setup guide: https://www.typeui.sh/docs/guides/openclaw
- TypeUI MCP server: https://mcp.typeui.sh
- Privacy policy: https://www.typeui.sh/privacy
- Terms of service: https://www.typeui.sh/terms
