"""Tool schemas for the TypeUI Hermes plugin."""

TYPEUI_INSTALL_MCP = {
    "name": "typeui_install_mcp",
    "description": (
        "Install or repair the hosted TypeUI MCP server in Hermes Agent config. "
        "Use when the user wants Hermes to connect to TypeUI, enable TypeUI design "
        "skills, or add TypeUI MCP to ~/.hermes/config.yaml."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "force": {
                "type": "boolean",
                "description": "Overwrite the existing typeui MCP server entry if it is already configured.",
            },
            "config_path": {
                "type": "string",
                "description": "Optional path to Hermes config.yaml. Defaults to $HERMES_HOME/config.yaml or ~/.hermes/config.yaml.",
            },
        },
    },
}

TYPEUI_MCP_STATUS = {
    "name": "typeui_mcp_status",
    "description": (
        "Show whether the hosted TypeUI MCP server is configured in Hermes Agent. "
        "Use before installing or when troubleshooting TypeUI MCP availability."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "config_path": {
                "type": "string",
                "description": "Optional path to Hermes config.yaml. Defaults to $HERMES_HOME/config.yaml or ~/.hermes/config.yaml.",
            },
        },
    },
}
