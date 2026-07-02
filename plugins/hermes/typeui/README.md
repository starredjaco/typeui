# TypeUI for Hermes Agent

TypeUI connects Hermes Agent to the hosted TypeUI MCP server so it can use project design skills, brand kits, UI prompts, and layout variations while building interfaces.

This folder is a Hermes plugin package. It includes:

- `plugin.yaml` for Hermes directory-plugin discovery.
- `typeui_hermes/` with the plugin registration, tool schemas, and MCP install handlers.
- `pyproject.toml` with a `hermes_agent.plugins` entry point for pip installs.
- `typeui_hermes/skills/typeui/SKILL.md` with TypeUI usage guidance for Hermes.
- `config.yaml` with the Hermes MCP server definition for TypeUI.

## Install as a Hermes directory plugin

Copy this folder into Hermes' user plugin directory:

```bash
mkdir -p ~/.hermes/plugins/typeui
cp -R plugins/hermes/typeui/. ~/.hermes/plugins/typeui/
```

Enable the plugin:

```bash
hermes plugins enable typeui
```

## Install as a pip entry-point plugin

From this repository:

```bash
cd plugins/hermes/typeui
pip install .
hermes plugins enable typeui
```

The package exposes this Hermes entry point:

```toml
[project.entry-points."hermes_agent.plugins"]
typeui = "typeui_hermes"
```

## Install TypeUI MCP

After installing and enabling the plugin, run:

```bash
hermes typeui install-mcp
```

The plugin writes this server into your Hermes configuration at `~/.hermes/config.yaml`:

```yaml
mcp_servers:
  typeui:
    url: "https://mcp.typeui.sh"
    auth: oauth
```

This folder includes the same snippet in `config.yaml`.

You can also ask a Hermes agent to call the `typeui_install_mcp` tool, or run the slash command inside a session:

```text
/typeui install-mcp
```

Start the TypeUI OAuth flow:

```bash
hermes mcp login typeui
```

Sign in with TypeUI when Hermes asks you to authorize the connection.

If Hermes Agent is already running, reload MCP servers inside the session:

```text
/reload-mcp
```

Check the saved server:

```bash
hermes typeui mcp-status
```

## Package for distribution

Build a local wheel or source distribution from this folder:

```bash
cd plugins/hermes/typeui
python -m build
```

Or create a ZIP artifact from `plugins/hermes/typeui` for users who want the directory-plugin install path.

For plugin discovery debugging, Hermes supports:

```bash
HERMES_PLUGINS_DEBUG=1 hermes plugins list
```

## Links

- Website: https://www.typeui.sh
- Documentation: https://www.typeui.sh/docs
- Hermes setup guide: https://www.typeui.sh/docs/guides/hermes
- TypeUI MCP server: https://mcp.typeui.sh
- Privacy policy: https://www.typeui.sh/privacy
- Terms of service: https://www.typeui.sh/terms
