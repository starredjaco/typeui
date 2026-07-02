"""TypeUI plugin registration for Hermes Agent."""

from __future__ import annotations

import json
import shlex
from pathlib import Path

from . import schemas, tools


def _format_json_result(payload: str, *, status: bool = False) -> str:
    try:
        data = json.loads(payload)
    except json.JSONDecodeError:
        return payload

    if data.get("error"):
        return f"TypeUI MCP error: {data['error']}"

    if status:
        if data.get("configured"):
            return "\n".join(
                [
                    "TypeUI MCP is configured in Hermes.",
                    f"Config: {data.get('config_path')}",
                    "",
                    json.dumps(data.get("server", {}), indent=2),
                ]
            )

        return "\n".join(
            [
                "TypeUI MCP is not configured in Hermes yet.",
                f"Config: {data.get('config_path')}",
                "",
                "Install it with:",
                "hermes typeui install-mcp",
            ]
        )

    changed = bool(data.get("changed"))
    first_line = (
        "TypeUI MCP has been installed in Hermes config."
        if changed
        else "TypeUI MCP is already installed in Hermes config."
    )
    lines = [
        first_line,
        f"Config: {data.get('config_path')}",
    ]

    if data.get("backup_path"):
        lines.append(f"Backup: {data['backup_path']}")

    lines.extend(
        [
            "",
            "Next, authorize TypeUI OAuth:",
            "hermes mcp login typeui",
            "",
            "If Hermes is already running, reload MCP servers in the session:",
            "/reload-mcp",
        ]
    )

    return "\n".join(lines)


def _cli_command(args) -> None:
    subcommand = getattr(args, "typeui_command", None)
    config_path = getattr(args, "config_path", None)

    if subcommand == "install-mcp":
        result = tools.install_mcp(
            {
                "force": bool(getattr(args, "force", False)),
                "config_path": config_path,
            }
        )
        print(_format_json_result(result))
        return

    if subcommand == "mcp-status":
        result = tools.mcp_status({"config_path": config_path})
        print(_format_json_result(result, status=True))
        return

    print("Usage: hermes typeui <install-mcp|mcp-status>")


def _setup_argparse(subparser) -> None:
    subcommands = subparser.add_subparsers(dest="typeui_command")

    install = subcommands.add_parser(
        "install-mcp",
        help="Install the hosted TypeUI MCP server into Hermes config.",
    )
    install.add_argument(
        "--force",
        action="store_true",
        help="Overwrite the existing typeui MCP server entry.",
    )
    install.add_argument(
        "--config",
        dest="config_path",
        help="Path to Hermes config.yaml. Defaults to $HERMES_HOME/config.yaml or ~/.hermes/config.yaml.",
    )

    status = subcommands.add_parser(
        "mcp-status",
        help="Show whether TypeUI MCP is installed in Hermes config.",
    )
    status.add_argument(
        "--config",
        dest="config_path",
        help="Path to Hermes config.yaml. Defaults to $HERMES_HOME/config.yaml or ~/.hermes/config.yaml.",
    )

    subparser.set_defaults(func=_cli_command)


def _slash_command(raw_args: str) -> str:
    try:
        parts = shlex.split(raw_args or "")
    except ValueError as exc:
        return f"Invalid /typeui arguments: {exc}"

    subcommand = parts[0] if parts else "mcp-status"
    force = "--force" in parts

    if subcommand in {"help", "-h", "--help"}:
        return "\n".join(
            [
                "Usage:",
                "/typeui install-mcp [--force]",
                "/typeui mcp-status",
            ]
        )

    if subcommand in {"install", "install-mcp"}:
        result = tools.install_mcp({"force": force})
        return _format_json_result(result)

    if subcommand in {"status", "mcp-status"}:
        result = tools.mcp_status({})
        return _format_json_result(result, status=True)

    return "Unknown /typeui command. Use /typeui help."


def _register_skills(ctx) -> None:
    if not hasattr(ctx, "register_skill"):
        return

    skills_dir = Path(__file__).parent / "skills"
    if not skills_dir.exists():
        return

    for child in sorted(skills_dir.iterdir()):
        skill_md = child / "SKILL.md"
        if child.is_dir() and skill_md.exists():
            ctx.register_skill(child.name, skill_md)


def register(ctx) -> None:
    """Register TypeUI tools, commands, and bundled skills with Hermes."""
    ctx.register_tool(
        name="typeui_install_mcp",
        toolset="typeui",
        schema=schemas.TYPEUI_INSTALL_MCP,
        handler=tools.install_mcp,
    )
    ctx.register_tool(
        name="typeui_mcp_status",
        toolset="typeui",
        schema=schemas.TYPEUI_MCP_STATUS,
        handler=tools.mcp_status,
    )

    if hasattr(ctx, "register_cli_command"):
        ctx.register_cli_command(
            name="typeui",
            help="Install and inspect TypeUI MCP for Hermes.",
            setup_fn=_setup_argparse,
            handler_fn=_cli_command,
        )

    if hasattr(ctx, "register_command"):
        ctx.register_command(
            "typeui",
            handler=_slash_command,
            description="Install and inspect TypeUI MCP.",
            args_hint="install-mcp|mcp-status",
        )

    _register_skills(ctx)
